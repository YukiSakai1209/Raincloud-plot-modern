"""
debug_horizontal_kde.py

u6c34u5e73u65b9u5411u306eRainCloudu30d7u30edu30c3u30c8u3067KDEuff08u30d0u30a4u30aau30eau30f3uff09u90e8u5206u304cu8868u793au3055u308cu306au3044u554fu984cu3092u30c7u30d0u30c3u30b0u3059u308bu30b9u30afu30eau30d7u30c8
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from matplotlib.collections import PolyCollection
import os
from shared.src.config.output_paths import get_debug_output_path

# u30c7u30d0u30c3u30b0u7528u306eu51fau529bu30c7u30a3u30ecu30afu30c8u30eau3092u4f5cu6210
# u65b0u3057u3044u51fau529bu30d1u30b9u7ba1u7406u3092u4f7fu7528

# u30c7u30fcu30bfu306eu751fu6210
np.random.seed(42)
data = np.random.normal(0, 1, 100)

# KDEu306eu8a08u7b97
def calculate_kde(data, bw_adjust=1):
    kde = stats.gaussian_kde(data, bw_method=bw_adjust)
    x_points = np.linspace(data.min(), data.max(), 100)
    y_points = kde(x_points)
    return x_points, y_points

# u30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8u306eu63cfu753bu95a2u6570
def draw_half_violin(ax, data, position, width, orient, color, title):
    # KDEu306eu8a08u7b97
    x_points, y_points = calculate_kde(data)
    
    # u6700u5927u5bc6u5ea6u3092u53d6u5f97
    max_density = np.max(y_points)
    
    # u5bc6u5ea6u3092u6b63u898fu5316
    y_points = y_points / max_density * width / 2
    
    # u5411u304du306bu5fdcu3058u3066u5ea7u6a19u3092u8abfu6574
    if orient == 'v':
        # u5782u76f4u65b9u5411u306eu30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8
        # u5de6u534au5206u306eu307fu3092u63cfu753b
        vertices = np.vstack([
            np.column_stack([position - y_points, x_points]),
            np.column_stack([np.ones(len(y_points)) * position, x_points[::-1]])
        ])
    else:
        # u6c34u5e73u65b9u5411u306eu30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8
        # u4e0bu534au5206u306eu307fu3092u63cfu753b
        vertices = np.vstack([
            np.column_stack([x_points, position - y_points]),
            np.column_stack([x_points[::-1], np.ones(len(y_points)) * position])
        ])
    
    # u30ddu30eau30b4u30f3u3092u4f5cu6210u3057u3066u63cfu753b
    poly = PolyCollection([vertices], facecolor=color, edgecolor='none')
    ax.add_collection(poly)
    
    # u8ef8u306eu7bc4u56f2u3092u66f4u65b0
    ax.autoscale_view()
    
    # u30bfu30a4u30c8u30ebu3092u8a2du5b9a
    ax.set_title(title)
    
    # u30c7u30d0u30c3u30b0u60c5u5831u3092u8868u793a
    print(f"Orient: {orient}, Position: {position}, Width: {width}")
    print(f"X points range: {x_points.min():.2f} to {x_points.max():.2f}")
    print(f"Y points range: {y_points.min():.2f} to {y_points.max():.2f}")
    if orient == 'h':
        print(f"Vertices X range: {vertices[:, 0].min():.2f} to {vertices[:, 0].max():.2f}")
        print(f"Vertices Y range: {vertices[:, 1].min():.2f} to {vertices[:, 1].max():.2f}")
    else:
        print(f"Vertices X range: {vertices[:, 0].min():.2f} to {vertices[:, 0].max():.2f}")
        print(f"Vertices Y range: {vertices[:, 1].min():.2f} to {vertices[:, 1].max():.2f}")

# u30c7u30d0u30c3u30b0u7528u306eu30d7u30edu30c3u30c8u3092u4f5cu6210

# 1. u73feu5728u306eu5b9fu88c5
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# u5782u76f4u65b9u5411u306eu30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8
draw_half_violin(ax1, data, position=0, width=0.8, orient='v', color='skyblue', title='Vertical Violin Plot (Current)')

# u6c34u5e73u65b9u5411u306eu30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8
draw_half_violin(ax2, data, position=0, width=0.8, orient='h', color='skyblue', title='Horizontal Violin Plot (Current)')

# u8ef8u306eu30e9u30d9u30ebu3092u8a2du5b9a
ax1.set_xlabel('Position')
ax1.set_ylabel('Value')
ax2.set_xlabel('Value')
ax2.set_ylabel('Position')

# u30d7u30edu30c3u30c8u3092u4fddu5b58
plt.tight_layout()
output_path = get_debug_output_path('current_implementation.png')
plt.savefig(output_path)
plt.close()

# 2. u4feeu6b63u6848u306eu30c6u30b9u30c8
def draw_half_violin_fixed(ax, data, position, width, orient, color, title):
    # KDEu306eu8a08u7b97
    x_points, y_points = calculate_kde(data)
    
    # u6700u5927u5bc6u5ea6u3092u53d6u5f97
    max_density = np.max(y_points)
    
    # u5bc6u5ea6u3092u6b63u898fu5316
    y_points = y_points / max_density * width / 2
    
    # u5411u304du306bu5fdcu3058u3066u5ea7u6a19u3092u8abfu6574
    if orient == 'v':
        # u5782u76f4u65b9u5411u306eu30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8
        # u5de6u534au5206u306eu307fu3092u63cfu753b
        vertices = np.vstack([
            np.column_stack([position - y_points, x_points]),
            np.column_stack([np.ones(len(y_points)) * position, x_points[::-1]])
        ])
    else:
        # u6c34u5e73u65b9u5411u306eu30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8
        # u4e0bu534au5206u306eu307fu3092u63cfu753b
        # u4feeu6b63u6848: yu5ea7u6a19u306eu8a08u7b97u65b9u6cd5u3092u5909u66f4
        vertices = np.vstack([
            np.column_stack([x_points, position - y_points]),  # u4e0bu534au5206
            np.column_stack([x_points[::-1], np.ones(len(y_points)) * position])  # u4e2du592eu7dda
        ])
    
    # u30ddu30eau30b4u30f3u3092u4f5cu6210u3057u3066u63cfu753b
    poly = PolyCollection([vertices], facecolor=color, edgecolor='none')
    ax.add_collection(poly)
    
    # u8ef8u306eu7bc4u56f2u3092u660eu793au7684u306bu8a2du5b9a
    if orient == 'v':
        ax.set_xlim(position - width, position + width)
        ax.set_ylim(x_points.min() - 0.1, x_points.max() + 0.1)
    else:
        ax.set_xlim(x_points.min() - 0.1, x_points.max() + 0.1)
        ax.set_ylim(position - width, position + width)
    
    # u30bfu30a4u30c8u30ebu3092u8a2du5b9a
    ax.set_title(title)

# u4feeu6b63u6848u306eu30d7u30edu30c3u30c8u3092u4f5cu6210
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# u5782u76f4u65b9u5411u306eu30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8
draw_half_violin_fixed(ax1, data, position=0, width=0.8, orient='v', color='skyblue', title='Vertical Violin Plot (Fixed)')

# u6c34u5e73u65b9u5411u306eu30d0u30a4u30aau30eau30f3u30d7u30edu30c3u30c8
draw_half_violin_fixed(ax2, data, position=0, width=0.8, orient='h', color='skyblue', title='Horizontal Violin Plot (Fixed)')

# u8ef8u306eu30e9u30d9u30ebu3092u8a2du5b9a
ax1.set_xlabel('Position')
ax1.set_ylabel('Value')
ax2.set_xlabel('Value')
ax2.set_ylabel('Position')

# u30d7u30edu30c3u30c8u3092u4fddu5b58
plt.tight_layout()
output_path = get_debug_output_path('fixed_implementation.png')
plt.savefig(output_path)
plt.close()

print(f"Debug plots saved to {get_debug_output_path('')}")
