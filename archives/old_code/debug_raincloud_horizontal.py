"""
debug_raincloud_horizontal.py

u6c34u5e73u65b9u5411u306eRainCloudu30d7u30edu30c3u30c8u306eu30c7u30d0u30c3u30b0u3068u4feeu6b63u7528u30b9u30afu30eau30d7u30c8
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
from matplotlib.collections import PolyCollection
from scipy import stats
from shared.src.config.output_paths import get_debug_output_path

# u30c6u30b9u30c8u7528u306eu51fau529bu30c7u30a3u30ecu30afu30c8u30eau3092u4f5cu6210
np.random.seed(42)
data = pd.DataFrame({
    'group': np.repeat(['A', 'B', 'C'], 30),
    'value': np.concatenate([
        np.random.normal(0, 1, 30),
        np.random.normal(2, 1, 30),
        np.random.normal(4, 1, 30)
    ])
})

# u30c7u30d0u30c3u30b0u7528u306eu30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8u95a2u6570
def debug_half_violin(ax, data, position, width, orient, color, title):
    """
    u30c7u30d0u30c3u30b0u7528u306eu534au5206u30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8u95a2u6570
    """
    if len(data) < 2:
        return
    
    # KDEu306eu8a08u7b97
    kde = stats.gaussian_kde(data, bw_method=1)
    x_points = np.linspace(data.min(), data.max(), 100)
    y_points = kde(x_points)
    
    # u6700u5927u5bc6u5ea6u3092u53d6u5f97
    max_density = np.max(y_points)
    
    # u5bc6u5ea6u3092u6b63u898fu5316
    y_points = y_points / max_density * width / 2
    
    # u30c7u30d0u30c3u30b0u60c5u5831u3092u8868u793a
    print(f"\n{title}:")
    print(f"  Orient: {orient}, Position: {position}, Width: {width}")
    print(f"  Data range: {data.min():.2f} to {data.max():.2f}")
    print(f"  X points range: {x_points.min():.2f} to {x_points.max():.2f}")
    print(f"  Y points range: {y_points.min():.2f} to {y_points.max():.2f}")
    
    # u5411u304du306bu5fdcu3058u3066u5ea7u6a19u3092u8abfu6574
    if orient == 'v':
        # u5782u76f4u65b9u5411u306eu30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8
        vertices = np.vstack([
            np.column_stack([position - y_points, x_points]),
            np.column_stack([np.ones(len(y_points)) * position, x_points[::-1]])
        ])
        print(f"  Vertices X range: {vertices[:, 0].min():.2f} to {vertices[:, 0].max():.2f}")
        print(f"  Vertices Y range: {vertices[:, 1].min():.2f} to {vertices[:, 1].max():.2f}")
        
        # u660eu793au7684u306bu8ef8u306eu7bc4u56f2u3092u8a2du5b9a
        ax.set_xlim(position - width, position + width)
        ax.set_ylim(x_points.min() - 0.1 * (x_points.max() - x_points.min()), 
                   x_points.max() + 0.1 * (x_points.max() - x_points.min()))
    else:
        # u6c34u5e73u65b9u5411u306eu30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8
        vertices = np.vstack([
            np.column_stack([x_points, position - y_points]),
            np.column_stack([x_points[::-1], np.ones(len(y_points)) * position])
        ])
        print(f"  Vertices X range: {vertices[:, 0].min():.2f} to {vertices[:, 0].max():.2f}")
        print(f"  Vertices Y range: {vertices[:, 1].min():.2f} to {vertices[:, 1].max():.2f}")
        
        # u660eu793au7684u306bu8ef8u306eu7bc4u56f2u3092u8a2du5b9a
        ax.set_xlim(x_points.min() - 0.1 * (x_points.max() - x_points.min()), 
                   x_points.max() + 0.1 * (x_points.max() - x_points.min()))
        ax.set_ylim(position - width, position + width)
    
    # u30ddu30eau30b4u30f3u3092u4f5cu6210u3057u3066u63cfu753b
    poly = PolyCollection([vertices], facecolor=color, edgecolor='none')
    ax.add_collection(poly)
    
    # u30bfu30a4u30c8u30ebu3092u8a2du5b9a
    ax.set_title(title)

# u4feeu6b63u6848u306eu30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8u95a2u6570
def fixed_half_violin(ax, data, position, width, orient, color, title):
    """
    u4feeu6b63u6848u306eu534au5206u30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8u95a2u6570
    """
    if len(data) < 2:
        return
    
    # KDEu306eu8a08u7b97
    kde = stats.gaussian_kde(data, bw_method=1)
    x_points = np.linspace(data.min(), data.max(), 100)
    y_points = kde(x_points)
    
    # u6700u5927u5bc6u5ea6u3092u53d6u5f97
    max_density = np.max(y_points)
    
    # u5bc6u5ea6u3092u6b63u898fu5316
    y_points = y_points / max_density * width / 2
    
    # u30c7u30d0u30c3u30b0u60c5u5831u3092u8868u793a
    print(f"\n{title}:")
    print(f"  Orient: {orient}, Position: {position}, Width: {width}")
    print(f"  Data range: {data.min():.2f} to {data.max():.2f}")
    print(f"  X points range: {x_points.min():.2f} to {x_points.max():.2f}")
    print(f"  Y points range: {y_points.min():.2f} to {y_points.max():.2f}")
    
    # u5411u304du306bu5fdcu3058u3066u5ea7u6a19u3092u8abfu6574
    if orient == 'v':
        # u5782u76f4u65b9u5411u306eu30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8
        vertices = np.vstack([
            np.column_stack([position - y_points, x_points]),
            np.column_stack([np.ones(len(y_points)) * position, x_points[::-1]])
        ])
        print(f"  Vertices X range: {vertices[:, 0].min():.2f} to {vertices[:, 0].max():.2f}")
        print(f"  Vertices Y range: {vertices[:, 1].min():.2f} to {vertices[:, 1].max():.2f}")
    else:
        # u6c34u5e73u65b9u5411u306eu30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8
        # u4feeu6b63u6848: u5de6u534au5206u306eu30d0u30a4u30aau30eau30f3u3092u63cfu753bu3059u308bu3088u3046u306bu5909u66f4
        vertices = np.vstack([
            np.column_stack([x_points, position - y_points]),  # u4e0bu534au5206
            np.column_stack([x_points[::-1], np.ones(len(y_points)) * position])  # u4e2du592eu7dda
        ])
        print(f"  Vertices X range: {vertices[:, 0].min():.2f} to {vertices[:, 0].max():.2f}")
        print(f"  Vertices Y range: {vertices[:, 1].min():.2f} to {vertices[:, 1].max():.2f}")
    
    # u30ddu30eau30b4u30f3u3092u4f5cu6210u3057u3066u63cfu753b
    poly = PolyCollection([vertices], facecolor=color, edgecolor='none')
    ax.add_collection(poly)
    
    # u660eu793au7684u306bu8ef8u306eu7bc4u56f2u3092u8a2du5b9a
    if orient == 'v':
        ax.set_xlim(position - width, position + width)
        ax.set_ylim(x_points.min() - 0.1 * (x_points.max() - x_points.min()), 
                   x_points.max() + 0.1 * (x_points.max() - x_points.min()))
    else:
        ax.set_xlim(x_points.min() - 0.1 * (x_points.max() - x_points.min()), 
                   x_points.max() + 0.1 * (x_points.max() - x_points.min()))
        ax.set_ylim(position - width, position + width)
    
    # u30bfu30a4u30c8u30ebu3092u8a2du5b9a
    ax.set_title(title)

# u5b8cu5168u306au4feeu6b63u6848u306eu30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8u95a2u6570
def complete_fixed_half_violin(ax, data, position, width, orient, color, title):
    """
    u5b8cu5168u306au4feeu6b63u6848u306eu534au5206u30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8u95a2u6570
    """
    if len(data) < 2:
        return
    
    # KDEu306eu8a08u7b97
    kde = stats.gaussian_kde(data, bw_method=1)
    
    # u5411u304du306bu5fdcu3058u3066u5ea7u6a19u3092u8abfu6574
    if orient == 'v':
        # u5782u76f4u65b9u5411u306eu30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8
        x_points = np.linspace(data.min(), data.max(), 100)
        y_points = kde(x_points)
        
        # u6700u5927u5bc6u5ea6u3092u53d6u5f97
        max_density = np.max(y_points)
        
        # u5bc6u5ea6u3092u6b63u898fu5316
        y_points = y_points / max_density * width / 2
        
        # u5782u76f4u65b9u5411u306eu30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8
        vertices = np.vstack([
            np.column_stack([position - y_points, x_points]),
            np.column_stack([np.ones(len(y_points)) * position, x_points[::-1]])
        ])
        
        # u660eu793au7684u306bu8ef8u306eu7bc4u56f2u3092u8a2du5b9a
        ax.set_xlim(position - width, position + width)
        ax.set_ylim(x_points.min() - 0.1 * (x_points.max() - x_points.min()), 
                   x_points.max() + 0.1 * (x_points.max() - x_points.min()))
    else:
        # u6c34u5e73u65b9u5411u306eu30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8
        y_points = np.linspace(data.min(), data.max(), 100)
        x_points = kde(y_points)
        
        # u6700u5927u5bc6u5ea6u3092u53d6u5f97
        max_density = np.max(x_points)
        
        # u5bc6u5ea6u3092u6b63u898fu5316
        x_points = x_points / max_density * width / 2
        
        # u6c34u5e73u65b9u5411u306eu30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8
        vertices = np.vstack([
            np.column_stack([x_points, position - np.zeros(len(y_points))]),
            np.column_stack([np.zeros(len(y_points)), y_points + position])
        ])
        
        # u660eu793au7684u306bu8ef8u306eu7bc4u56f2u3092u8a2du5b9a
        ax.set_xlim(0, width)
        ax.set_ylim(position - 0.1, position + (y_points.max() - y_points.min()) + 0.1)
    
    # u30c7u30d0u30c3u30b0u60c5u5831u3092u8868u793a
    print(f"\n{title}:")
    print(f"  Orient: {orient}, Position: {position}, Width: {width}")
    print(f"  Data range: {data.min():.2f} to {data.max():.2f}")
    print(f"  Vertices X range: {vertices[:, 0].min():.2f} to {vertices[:, 0].max():.2f}")
    print(f"  Vertices Y range: {vertices[:, 1].min():.2f} to {vertices[:, 1].max():.2f}")
    
    # u30ddu30eau30b4u30f3u3092u4f5cu6210u3057u3066u63cfu753b
    poly = PolyCollection([vertices], facecolor=color, edgecolor='none')
    ax.add_collection(poly)
    
    # u30bfu30a4u30c8u30ebu3092u8a2du5b9a
    ax.set_title(title)

# u73feu5728u306eu5b9fu88c5u3068u4feeu6b63u6848u306eu6bd4u8f03u30d7u30edu30c3u30c8u3092u4f5cu6210
fig, axes = plt.subplots(3, 2, figsize=(15, 12))

# u5782u76f4u65b9u5411u306eu30d7u30edu30c3u30c8
# u73feu5728u306eu5b9fu88c5
debug_half_violin(axes[0, 0], data[data['group'] == 'A']['value'].values, position=0, width=0.8, 
                 orient='v', color='skyblue', title='Current Implementation (Vertical)')

# u4feeu6b63u6848
fixed_half_violin(axes[0, 1], data[data['group'] == 'A']['value'].values, position=0, width=0.8, 
                orient='v', color='skyblue', title='Fixed Implementation (Vertical)')

# u6c34u5e73u65b9u5411u306eu30d7u30edu30c3u30c8
# u73feu5728u306eu5b9fu88c5
debug_half_violin(axes[1, 0], data[data['group'] == 'A']['value'].values, position=0, width=0.8, 
                 orient='h', color='skyblue', title='Current Implementation (Horizontal)')

# u4feeu6b63u6848
fixed_half_violin(axes[1, 1], data[data['group'] == 'A']['value'].values, position=0, width=0.8, 
                orient='h', color='skyblue', title='Fixed Implementation (Horizontal)')

# u5b8cu5168u306au4feeu6b63u6848
complete_fixed_half_violin(axes[2, 0], data[data['group'] == 'A']['value'].values, position=0, width=0.8, 
                         orient='v', color='skyblue', title='Complete Fix (Vertical)')

complete_fixed_half_violin(axes[2, 1], data[data['group'] == 'A']['value'].values, position=0, width=0.8, 
                         orient='h', color='skyblue', title='Complete Fix (Horizontal)')

# u30d7u30edu30c3u30c8u3092u4fddu5b58
plt.tight_layout()
output_path = get_debug_output_path('horizontal_violin_comparison.png')
plt.savefig(output_path)
plt.close()

print(f"\nDebug plots saved to {output_path}")
