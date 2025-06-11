"""
raincloud_modern.py

A modern implementation of RainCloud plot compatible with seaborn 0.13.2
Created by Yuki Sakai
"""

from __future__ import division

import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.collections import PolyCollection
from scipy import stats


def RainCloud(
    x=None,
    y=None,
    hue=None,
    data=None,
    order=None,
    hue_order=None,
    palette=None,
    bw="scott",
    width_viol=0.8,
    width_box=0.15,
    figsize=None,
    orient="v",
    move=0,
    offset=None,
    ax=None,
    pointplot=False,
    connect_means=False,
    linecolor="black",
    point_size=5,
    jitter=True,
    dodge=True,
    scale="area",
    scale_hue=True,
    alpha=0.5,
    cut=2,
    linewidth=1,
    **kwargs,
):
    """
    RainCloud plots are a hybrid of violin, box, and strip plots.

    Parameters
    ----------
    x, y : names of variables in `data`
        Inputs for plotting long-form data.
    hue : name of variable in `data`
        Grouping variable that will produce points with different colors.
    data : DataFrame
        Long-form (tidy) dataset for plotting.
    order, hue_order : lists of strings
        Order to plot the categorical levels in.
    palette : list or dict of colors
        Colors to use for the different levels of the `hue` variable.
    bw : float or str
        Either the bandwidth or the method used to calculate it.
    width_viol : float
        Width of the violin plot elements.
    width_box : float
        Width of the box plot elements.
    figsize : tuple
        Size of the figure to create.
    orient : "v" or "h"
        Orientation of the plot (vertical or horizontal).
    move : float
        Adjustment for the position of the violin plots.
    offset : float
        Adjustment for the position of the box plots.
    ax : matplotlib axis
        Axis to plot on.
    pointplot : bool
        Whether to add a pointplot of the means.
    connect_means : bool
        Whether to connect the means across categories.
    linecolor : str
        Color for the line connecting the means.
    point_size : float
        Size of the points in the strip plot.
    jitter : bool or float
        Amount of jitter to add to the strip plot.
    dodge : bool
        Whether to dodge when hue is used.
    scale : "area" or "count" or "width"
        Scaling for the violins.
    scale_hue : bool
        Whether to scale the violins separately for each hue level.
    alpha : float
        Transparency of the plot elements.
    cut : float
        How far to extend the density past the extreme datapoints.
    linewidth : float
        Width of the lines.
    **kwargs : dict
        Other keyword arguments to pass to underlying functions.

    Returns
    -------
    ax : matplotlib axis
        Axis with the raincloud plot.
    """
    # Validate orientation
    if orient not in ["v"]:
        raise ValueError("Only vertical orientation 'v' is supported.")

    # Create axis if none is provided
    if ax is None:
        if figsize is None:
            figsize = (8, 6)
        fig, ax = plt.subplots(figsize=figsize)

    # Set default offset if not provided
    if offset is None:
        offset = max(width_box / 1.8, 0.15) + 0.05

    # Count plots for legend processing
    n_plots = 3

    # Separate keyword arguments for each component
    kwcloud = dict()
    kwbox = dict(saturation=1)  # Removed whiskerprops from default to avoid overriding
    kwrain = dict(zorder=0, edgecolor="white")
    kwpoint = dict()  # Simplified to avoid parameter issues

    for key, value in kwargs.items():
        if "cloud_" in key:
            kwcloud[key.replace("cloud_", "")] = value
        elif "box_" in key:
            kwbox[key.replace("box_", "")] = value
        elif "rain_" in key:
            kwrain[key.replace("rain_", "")] = value
        elif "point_" in key:
            kwpoint[key.replace("point_", "")] = value

    # Extract parameters for rain points
    rain_alpha = kwrain.pop("alpha", alpha)
    rain_offset = kwrain.pop("offset", 0.1)
    jitter_range = kwrain.pop("jitter_range", 0.05)

    # Extract parameters for box plots
    box_alpha = kwbox.pop("alpha", alpha)
    box_offset = kwbox.pop("offset", 0.1)

    # Extract parameters for cloud (violin) plots
    cloud_alpha = kwcloud.pop("alpha", alpha)
    cloud_offset = kwcloud.pop("offset", 0.0)

    # Extract parameters for point plots
    point_alpha = kwpoint.pop("alpha", alpha)
    point_offset = kwpoint.pop("offset", 0.0)

    # Category spacing
    category_spacing = kwargs.pop("category_spacing", 2.0)

    # Get data from the inputs
    if x is None and y is None:
        raise ValueError("Either `x` or `y` must be specified")
    elif x is None:
        # Vertical plot with `y` as the categorical
        categorical_var, value_var = y, x
    elif y is None:
        # Vertical plot with `x` as the categorical
        categorical_var, value_var = x, y
    else:
        # Both x and y are specified, assume x is categorical
        categorical_var, value_var = x, y

    # Extract the data
    categorical = data[categorical_var]
    values = data[value_var]

    # Get the categorical levels and value data
    if order is None:
        categories = categorical.unique()
    else:
        categories = order

    # Get the hue levels and colors
    if hue is None:
        hue_levels = [None]
        colors = ["C0"]
        legend = False
    else:
        hue_levels = data[hue].unique() if hue_order is None else hue_order
        n_colors = len(hue_levels)

        if palette is None:
            # Default color palette
            colors = [f"C{i}" for i in range(n_colors)]
        elif isinstance(palette, list):
            # List of colors
            colors = palette
        elif isinstance(palette, dict):
            # Dictionary mapping hue levels to colors
            colors = [palette[level] for level in hue_levels]
        else:
            # String name of a seaborn palette
            colors = sns.color_palette(palette, n_colors)

        legend = True

    # Store hue categories for legend ordering
    hue_categories = hue_levels

    # Calculate positions for each category
    positions = np.arange(len(categories)) * category_spacing

    # Clear any existing legend to avoid duplication
    if ax.get_legend() is not None:
        ax.get_legend().remove()

    # Create a dictionary to store legend handles and labels
    legend_handles = {}
    legend_labels = {}

    # Plot each category
    for i, category in enumerate(categories):
        # Get the position for this category
        pos = positions[i]

        # Filter data for this category
        cat_mask = categorical == category
        cat_vals = values[cat_mask]

        if hue is not None:
            hue_vals = data[hue][cat_mask]

            # Plot each hue level
            for j, level in enumerate(hue_levels):
                hue_mask = hue_vals == level
                hue_data = cat_vals[hue_mask]

                if len(hue_data) == 0:
                    continue

                # Get color for this hue level
                color = colors[j]

                # Calculate offset for this hue level if dodging
                if dodge and len(hue_levels) > 1:
                    # Calculate the width of each dodge
                    dodge_width = width_viol / len(hue_levels)
                    # Calculate the positions for each hue level
                    dodge_positions = np.linspace(
                        pos - width_viol / 2 + dodge_width / 2,
                        pos + width_viol / 2 - dodge_width / 2,
                        len(hue_levels),
                    )
                    # Get the position for this hue level
                    dodge_pos = dodge_positions[j]
                else:
                    dodge_pos = pos
                    dodge_width = width_viol

                # Draw half violin
                _draw_half_violin(
                    ax,
                    hue_data,
                    dodge_pos + cloud_offset,
                    dodge_width,
                    orient,
                    color,
                    cloud_alpha,
                    bw,
                    cut,
                    **kwcloud,
                )

                # Draw strip plot (rain)
                rain = _draw_strip(
                    ax,
                    hue_data,
                    dodge_pos + rain_offset,
                    jitter,
                    orient,
                    color,
                    point_size,
                    rain_alpha,
                    jitter_range=jitter_range,
                    **kwrain,
                )

                # Set the label for the rain points (only once per hue level)
                if level not in legend_handles:
                    rain.set_label(level)
                    legend_handles[level] = rain
                    legend_labels[level] = level

                # Draw box plot
                _draw_box(ax, hue_data, dodge_pos + box_offset, width_box, color, box_alpha, **kwbox)

                # Draw point plot if requested
                if pointplot:
                    # Calculate mean and confidence interval
                    mean = np.mean(hue_data)
                    # Draw the point
                    point = ax.scatter(
                        dodge_pos + point_offset, mean, color=color, alpha=point_alpha, zorder=30, **kwpoint
                    )
        else:
            # No hue, just plot the category
            color = colors[0]

            # Draw half violin
            _draw_half_violin(
                ax, cat_vals, pos + cloud_offset, width_viol, orient, color, cloud_alpha, bw, cut, **kwcloud
            )

            # Draw strip plot (rain)
            rain = _draw_strip(
                ax,
                cat_vals,
                pos + rain_offset,
                jitter,
                orient,
                color,
                point_size,
                rain_alpha,
                jitter_range=jitter_range,
                **kwrain,
            )

            # Draw box plot
            _draw_box(ax, cat_vals, pos + box_offset, width_box, color, box_alpha, **kwbox)

            # Draw point plot if requested
            if pointplot:
                # Calculate mean and confidence interval
                mean = np.mean(cat_vals)
                # Draw the point
                point = ax.scatter(
                    pos + point_offset, mean, color=color, alpha=point_alpha, zorder=30, **kwpoint
                )

    # Connect means if requested
    if connect_means and pointplot and hue is not None:
        # For each hue level
        for j, level in enumerate(hue_levels):
            # Get the means for this hue level
            means = []
            pos_means = []

            # For each category
            for i, category in enumerate(categories):
                # Get the position for this category
                pos = positions[i]

                # Filter data for this category and hue level
                cat_mask = categorical == category
                cat_vals = values[cat_mask]

                if hue is not None:
                    hue_vals = data[hue][cat_mask]
                    hue_mask = hue_vals == level
                    hue_data = cat_vals[hue_mask]

                    if len(hue_data) == 0:
                        continue

                    # Calculate dodge position if needed
                    if dodge and len(hue_levels) > 1:
                        # Calculate the width of each dodge
                        dodge_width = width_viol / len(hue_levels)
                        # Calculate the positions for each hue level
                        dodge_positions = np.linspace(
                            pos - width_viol / 2 + dodge_width / 2,
                            pos + width_viol / 2 - dodge_width / 2,
                            len(hue_levels),
                        )
                        # Get the position for this hue level
                        dodge_pos = dodge_positions[j]
                    else:
                        dodge_pos = pos

                    # Calculate mean
                    mean = np.mean(hue_data)
                    means.append(mean)
                    pos_means.append(dodge_pos + point_offset)

            # Connect the means
            if len(means) > 1:
                ax.plot(pos_means, means, color=linecolor, linewidth=linewidth, zorder=19)

    # Set the x-axis
    ax.set_xticks(positions)
    ax.set_xticklabels(categories)
    ax.set_xlim(min(positions) - 1, max(positions) + 1)

    # Add legend if needed
    if hue is not None and legend:
        # Create legend with unique entries in the original order
        if hue_categories is not None and len(hue_categories) > 0:
            # Use the original hue order
            unique_labels = []
            unique_handles = []

            for hue_val in hue_categories:
                if hue_val in legend_handles:
                    unique_labels.append(legend_labels[hue_val])
                    unique_handles.append(legend_handles[hue_val])

            # Create the legend
            if len(unique_handles) > 0:
                ax.legend(handles=unique_handles, labels=unique_labels)

    return ax


def _draw_half_violin(ax, data, position, width, orient, color, alpha=None, bw_adjust=1, cut=2):
    """
    Draw a half violin plot (KDE plot)
    """
    if len(data) < 2:
        return None

    # Calculate KDE (direct calculation)
    kde = stats.gaussian_kde(data, bw_method=bw_adjust)

    # Calculate KDE over a slightly extended range of data
    data_min = data.min() - cut * data.std()
    data_max = data.max() + cut * data.std()
    x_points = np.linspace(data_min, data_max, 100)
    y_points = kde(x_points)

    # Get maximum density
    max_density = np.max(y_points)
    if max_density > 0:  # Avoid division by zero
        y_points = y_points / max_density * width / 2

    # Calculate coordinates to display only the left half
    vertices = np.vstack(
        [
            np.column_stack([position - y_points, x_points]),
            np.column_stack([np.ones(len(y_points)) * position, x_points[::-1]]),
        ]
    )

    # Create polygon and draw
    poly = PolyCollection([vertices], facecolor=color, edgecolor="none", alpha=alpha)
    ax.add_collection(poly)

    # Explicitly set axis range
    # Ensure sufficient padding to prevent plot clipping
    padding = (data_max - data_min) * 0.2  # Increased padding from 0.1 to 0.2
    ax.set_ylim(data_min - padding, data_max + padding)

    # Set x-axis range appropriately
    # Ensure sufficient padding on both sides for all plots to be visible
    current_xlim = ax.get_xlim()
    new_xlim = (
        min(current_xlim[0], position - width - padding),
        max(current_xlim[1], position + width + padding * 2),
    )
    ax.set_xlim(new_xlim)

    # Update axis range
    ax.autoscale_view()

    return poly


def _draw_box(ax, data, position, width, color, alpha=None, **kwargs):
    """
    Draw a boxplot
    """
    if len(data) < 1:
        return None

    # Remove parameters that can't be passed to boxplot
    kwargs.pop("saturation", None)

    # Set boxplot properties
    boxprops = kwargs.pop("boxprops", {"facecolor": "none", "edgecolor": "black"})
    boxprops["facecolor"] = color
    boxprops["alpha"] = alpha

    # Set flier (outlier) marker properties - reduce size by 1/2
    flierprops = kwargs.pop("flierprops", {})
    flierprops.setdefault("marker", "o")
    flierprops.setdefault("markerfacecolor", color)
    flierprops.setdefault("markeredgecolor", "black")
    flierprops.setdefault("markersize", 3)  # Reduced from default ~6 to 3 (1/2 size)
    flierprops.setdefault("alpha", alpha)

    # Set whisker properties - reduce cap size by 2/3 of current size
    whiskerprops = {}
    whiskerprops["linewidth"] = 0.7  # Further reduced from 1.0 to 0.7 (2/3 of current size)

    # Set cap properties - reduce width by 2/3 of current size
    capprops = {}
    capprops["linewidth"] = 0.7  # Further reduced from 1.0 to 0.7 (2/3 of current size)

    # Override any user-provided properties
    user_whiskerprops = kwargs.pop("whiskerprops", {})
    user_capprops = kwargs.pop("capprops", {})
    whiskerprops.update(user_whiskerprops)
    capprops.update(user_capprops)

    # Create the boxplot with our specific properties
    box = ax.boxplot(
        [data],
        positions=[position],
        widths=width,
        vert=True,
        patch_artist=True,
        boxprops=boxprops,
        flierprops=flierprops,
        whiskerprops=whiskerprops,
        capprops=capprops,
        **kwargs,
    )

    return box


def _draw_strip(ax, data, position, jitter, orient, color, size, alpha=None, jitter_range=0.05, **kwargs):
    """
    Draw scatter points (rain part)
    """
    if len(data) < 1:
        return None

    # Jitter points if requested
    if jitter:
        # Add jitter with a uniform random distribution
        jitter_offsets = np.random.uniform(-jitter_range, jitter_range, size=len(data))
        positions = np.full(len(data), position) + jitter_offsets
    else:
        positions = np.full(len(data), position)

    # Draw the points
    points = ax.scatter(positions, data, color=color, s=size, alpha=alpha, **kwargs)

    return points


def _draw_point(ax, data, position, color, **kwargs):
    """
    Draw a point plot (mean and confidence interval)
    """
    if len(data) < 2:
        return None

    # Remove parameters that can't be passed to errorbar
    kwargs.pop("errwidth", None)
    kwargs.pop("capsize", None)

    # Calculate mean and standard error
    mean = np.mean(data)
    sem = np.std(data, ddof=1) / np.sqrt(len(data))

    # Draw point plot
    errorbar = ax.errorbar(position, mean, yerr=sem, fmt="o", color=color, **kwargs)

    return errorbar


# Function to explicitly set labels for plot elements
def _add_legend_data(ax, handle, label):
    """
    Function to explicitly set labels for plot elements

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axis to add legend to
    handle : object
        Handle to add to the legend
    label : str
        Label to display in the legend
    """
    # Simply set the label for the handle
    handle.set_label(label)

    # The legend will be created later with ax.legend()


# Function to apply Nature style guidelines
def apply_nature_style(fig=None, ax=None, font_size=8):
    """
    Apply Nature journal style guidelines to the plot

    Parameters
    ----------
    fig : matplotlib.figure.Figure, optional
        Figure to apply style to
    ax : matplotlib.axes.Axes, optional
        Axis to apply style to
    font_size : int, optional
        Font size to use (default: 8)
    """
    if fig is not None:
        # Set figure size to Nature guidelines
        fig.set_size_inches(3.5, 2.625)  # 89 mm x 66.7 mm

    if ax is not None:
        # Set font sizes
        ax.title.set_fontsize(font_size)
        ax.xaxis.label.set_fontsize(font_size)
        ax.yaxis.label.set_fontsize(font_size)

        # Set tick parameters
        ax.tick_params(axis="both", which="major", labelsize=font_size - 1)

        # Set spines
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)

        # Set legend
        if ax.get_legend() is not None:
            ax.legend(fontsize=font_size - 1, frameon=False)
