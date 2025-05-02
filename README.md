# RainCloud Plot Modern

![Main Example](https://github.com/YukiSakai1209/Raincloud-plot-modern/raw/master/outputs/fixed/comprehensive_fixed.png)

A modern implementation of RainCloud plots with improved aesthetics and functionality, compatible with seaborn 0.13.2.

## Key Features

### 1. Enhanced Boxplot Styling

- Thinner whiskers and caps (linewidth=0.7)
- Adjusted marker sizes for outliers

![Boxplot Example](https://github.com/YukiSakai1209/Raincloud-plot-modern/raw/master/outputs/fixed/boxplot_position_fix.png)

### 2. Fixed Legend Handling

- Deduplicated legend entries
- Consistent color mapping

![Legend Example](https://github.com/YukiSakai1209/Raincloud-plot-modern/raw/master/outputs/fixed/legend_fix.png)

### 3. Rain (Points) Positioning

- Optimal jitter range (jitter_range=0.05)
- Offset from violin plots (rain_offset=0.05)

![Rain Points Example](https://github.com/YukiSakai1209/Raincloud-plot-modern/raw/master/outputs/fixed/rain_position_fix.png)

### 4. Nature Journal Style Compliance

- Uses styles from `shared/src/visualization/styles.py`
- Publication-ready formatting

## Installation

```bash
pip install git+https://github.com/YukiSakai1209/Raincloud-plot-modern.git
```

## Overview

RainCloud plots are a visualization technique that combines violin plots, boxplots, and raw data points (rain) to provide a comprehensive view of data distributions. This implementation offers a modern, customizable approach to creating RainCloud plots using matplotlib and seaborn.

## Usage

### Basic Usage

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from raincloud_modern import RainCloud

# Create sample data
np.random.seed(10)
data = pd.DataFrame({
    'value': np.concatenate([np.random.normal(0, 1, 100), np.random.normal(2, 1, 100)]),
    'group': np.repeat(['A', 'B'], 100)
})

# Create figure
fig, ax = plt.subplots(figsize=(8, 6))

# Create RainCloud plot
RainCloud(x='group', y='value', data=data, ax=ax)

plt.tight_layout()
plt.show()
```

### With Hue and Connected Means

```python
# Create sample data with hue
data_hue = pd.DataFrame({
    'value': np.concatenate([np.random.normal(0, 1, 100), np.random.normal(2, 1, 100), 
                           np.random.normal(0.5, 1, 100), np.random.normal(2.5, 1, 100)]),
    'group': np.repeat(['A', 'B'], 200),
    'hue': np.repeat(['X', 'Y'], 200)
})

fig, ax = plt.subplots(figsize=(10, 6))
RainCloud(x='group', y='value', hue='hue', data=data_hue, connect_means=True, ax=ax)
plt.tight_layout()
```

### Adjusting Box Position

```python
# Adjust box position when dodge is False
fig, ax = plt.subplots(figsize=(8, 6))
RainCloud(
    x='group', 
    y='value', 
    hue='hue', 
    data=data_hue, 
    dodge=False, 
    box_offset=0.15,  # Move boxplot to the right
    ax=ax
)
plt.tight_layout()
```

## Parameters

| Parameter     | Type      | Default | Description                                                |
| ------------- | --------- | ------- | ---------------------------------------------------------- |
| x             | str       | None    | Name of the categorical variable in the data frame         |
| y             | str       | None    | Name of the value variable in the data frame               |
| hue           | str       | None    | Name of the grouping variable for color encoding           |
| data          | DataFrame | None    | Pandas DataFrame containing the data                       |
| order         | list      | None    | Order of the categories                                    |
| hue_order     | list      | None    | Order of the hue categories                                |
| palette       | list/dict | None    | Color palette for the plot                                 |
| bw            | str/float | "scott" | Bandwidth for kernel density estimation                    |
| width_viol    | float     | 0.5     | Width of the violin plot                                   |
| width_box     | float     | 0.15    | Width of the boxplot                                       |
| figsize       | tuple     | None    | Figure size (width, height) in inches                      |
| move          | float     | 0       | Adjusts rain position along the x-axis                     |
| offset        | float     | None    | Adjusts cloud position along the x-axis                    |
| ax            | Axes      | None    | Matplotlib axes to draw the plot on                        |
| pointplot     | bool      | False   | Whether to add a pointplot showing mean and error          |
| connect_means | bool      | False   | Whether to connect means across categories                 |
| linecolor     | str       | "black" | Color of the line connecting means                         |
| point_size    | int       | 5       | Size of the rain points                                    |
| jitter        | bool      | True    | Whether to add jitter to the rain points                   |
| dodge         | bool      | True    | Whether to dodge the plots for different hue values        |
| scale         | str       | "area"  | Method for scaling the violin width                        |
| scale_hue     | bool      | True    | Whether to scale the violin width by hue                   |
| alpha         | float     | 0.5     | Transparency of the plot elements                          |
| cut           | float     | 2       | How far to extend the density past the extreme data points |
| linewidth     | float     | 1       | Width of the line connecting means                         |
| rain_offset   | float     | 0.05    | Offset for rain points to avoid overlap with violin        |
| box_offset    | float     | 0       | Offset for boxplot position when dodge is False            |

## Advanced Customization

You can pass additional parameters to specific plot elements by prepending the parameter name with:

- `point_` for rain points
- `box_` for boxplot elements
- `violin_` for violin plot elements
- `cloud_` for all elements

Example:

```python
RainCloud(x='group', y='value', data=data, 
          point_color='red', box_color='blue', violin_color='green',
          cloud_linewidth=1, point_capsize=0.2)
```

## Style Configuration

For consistent styling across visualizations, use the `configure_plots()` function from the shared styles module:

```python
from shared.src.visualization.styles import configure_plots, apply_nature_style

# Apply consistent styling
configure_plots()

# Create your plot
fig, ax = plt.subplots(figsize=(8, 6))
RainCloud(x='group', y='value', data=data, ax=ax)

# Apply Nature journal styling
apply_nature_style(fig, ax)
```

## Author

Yuki Sakai
