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
from raincloud_modern import RainCloud
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from shared.src.visualization.styles import configure_plots

# Configure plots with Nature style guidelines
configure_plots()

# Create sample data
np.random.seed(42)
data = pd.DataFrame({
    'group': np.repeat(['Group 1', 'Group 2', 'Group 3'], 30),
    'value': np.concatenate([
        np.random.normal(0, 1, 30),
        np.random.normal(1, 1, 30),
        np.random.normal(2, 1, 30)
    ]),
    'condition': np.repeat(['Condition 1', 'Condition 2'], 45)
})

# Create a simple RainCloud plot
fig, ax = plt.subplots(figsize=(6, 4))
RainCloud(x='group', y='value', data=data, ax=ax)
plt.title('Basic RainCloud Plot')
plt.tight_layout()
plt.savefig('basic_raincloud.png', dpi=300)
```

![Basic RainCloud Plot](/workspace/outputs/fixed/half_violin_fix.png)

### With Hue and Connected Means

```python
# Create a RainCloud plot with hue and connected means
fig, ax = plt.subplots(figsize=(8, 5))
RainCloud(x='group', y='value', hue='condition', data=data,
          alpha=0.6, point_size=4, pointplot=True, connect_means=True,
          ax=ax)
plt.title('RainCloud Plot with Hue and Connected Means')
plt.tight_layout()
plt.savefig('hue_raincloud.png', dpi=300)
```

![RainCloud Plot with Hue](/workspace/outputs/fixed/comprehensive_fixed.png)

### Adjusting Box Position

```python
# Create a RainCloud plot with adjusted box position
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Default box offset (0)
RainCloud(x='group', y='value', hue='condition', data=data,
          dodge=False, ax=ax1)
ax1.set_title('Dodge=False, Default Box Offset (0)')

# Custom box offset (0.2)
RainCloud(x='group', y='value', hue='condition', data=data,
          dodge=False, box_offset=0.2, ax=ax2)
ax2.set_title('Dodge=False, Box Offset=0.2')

plt.tight_layout()
plt.savefig('boxplot_position.png', dpi=300)
```

![Boxplot Position Adjustment](/workspace/outputs/fixed/boxplot_position_fix.png)

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

- `cloud_` for violin plot parameters
- `box_` for boxplot parameters
- `rain_` for stripplot parameters
- `point_` for pointplot parameters

Example:

```python
RainCloud(x='group', y='value', data=data,
          rain_color='blue', box_showfliers=False,
          cloud_linewidth=1, point_capsize=0.2)
```

## Style Configuration

For consistent styling across visualizations, use the `configure_plots()` function from the shared styles module:

```python
from shared.src.visualization.styles import configure_plots
configure_plots()
```

To apply Nature journal style guidelines to a specific plot:

```python
from raincloud_modern import apply_nature_style
apply_nature_style(fig, ax)
```

## Author

Yuki Sakai
