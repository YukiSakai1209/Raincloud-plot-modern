#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RainCloudu30d7u30edu30c3u30c8u306eu4feeu6b63u3092u30c6u30b9u30c8u3059u308bu30b9u30afu30eau30d7u30c8

u4ee5u4e0bu306eu4feeu6b63u3092u30c6u30b9u30c8u3057u307eu3059uff1a
1. u6c34u5e73u65b9u5411u306eu30d7u30edu30c3u30c8u6a5fu80fdu306eu524au9664
2. u51e1u4f8bu8868u793au306eu4feeu6b63
3. Rainu90e8u5206uff08u6563u5e03u70b9uff09u304cViolinu30d7u30edu30c3u30c8u306bu91cdu306au3089u306au3044u3088u3046u8abfu6574
4. Dodgeu6a5fu80fdu3092u30aau30d5u306bu3057u305fu969bu306eBoxplotu4f4du7f6eu8abfu6574
5. u534au5206u306eu307fu8868u793au3055u308cu3066u3044u308bu554fu984cu306eu4feeu6b63
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# u4feeu6b63u3057u305fRainCloudu95a2u6570u3092u30a4u30f3u30ddu30fcu30c8
from raincloud_modern import RainCloud, apply_nature_style
from shared.src.visualization.styles import configure_plots

# u51fau529bu30c7u30a3u30ecu30afu30c8u30eau306eu8a2du5b9a
OUTPUT_DIR = os.path.join(os.getcwd(), 'outputs', 'fixed')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# u30c6u30b9u30c8u7528u306eu30c7u30fcu30bfu3092u751fu6210
def generate_test_data(n_samples=100, n_groups=3):
    np.random.seed(42)
    data = []
    
    for i in range(n_groups):
        group_data = np.random.normal(loc=i, scale=0.8, size=n_samples)
        data.append(pd.DataFrame({
            'group': f'Group {i+1}',
            'value': group_data
        }))
    
    return pd.concat(data, ignore_index=True)

# hueu30d1u30e9u30e1u30fcu30bfu7528u306eu30c7u30fcu30bfu3092u751fu6210
def generate_hue_data(n_samples=100, n_groups=3, n_conditions=2):
    np.random.seed(42)
    data = []
    
    for i in range(n_groups):
        for j in range(n_conditions):
            group_data = np.random.normal(loc=i + j*0.5, scale=0.6, size=n_samples)
            data.append(pd.DataFrame({
                'group': f'Group {i+1}',
                'condition': f'Condition {j+1}',
                'value': group_data
            }))
    
    return pd.concat(data, ignore_index=True)

# 1. u51e1u4f8bu8868u793au306eu4feeu6b63u3092u30c6u30b9u30c8
def test_legend_fix():
    data = generate_hue_data()
    
    fig, ax = plt.subplots(figsize=(6, 4))
    RainCloud(x='group', y='value', hue='condition', data=data, ax=ax)
    plt.title('Fixed Legend Display')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'legend_fix.png'))
    plt.close()

# 2. Rainu90e8u5206uff08u6563u5e03u70b9uff09u304cViolinu30d7u30edu30c3u30c8u306bu91cdu306au3089u306au3044u3088u3046u8abfu6574u3092u30c6u30b9u30c8
def test_rain_position_fix():
    data = generate_test_data()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # u30c7u30d5u30a9u30ebu30c8u306erain_offset
    RainCloud(x='group', y='value', data=data, ax=ax1)
    ax1.set_title('Default Rain Offset (0.1)')
    
    # u5927u304du3081u306erain_offset
    RainCloud(x='group', y='value', data=data, rain_offset=0.3, ax=ax2)
    ax2.set_title('Larger Rain Offset (0.3)')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'rain_position_fix.png'))
    plt.close()

# 3. Dodgeu6a5fu80fdu3092u30aau30d5u306bu3057u305fu969bu306eBoxplotu4f4du7f6eu8abfu6574u3092u30c6u30b9u30c8
def test_boxplot_position_fix():
    data = generate_hue_data()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # dodge=Falseu3067box_offset=0uff08u30c7u30d5u30a9u30ebu30c8uff09
    RainCloud(x='group', y='value', hue='condition', data=data, dodge=False, ax=ax1)
    ax1.set_title('Dodge=False, Default Box Offset (0)')
    
    # dodge=Falseu3067box_offset=0.2
    RainCloud(x='group', y='value', hue='condition', data=data, dodge=False, box_offset=0.2, ax=ax2)
    ax2.set_title('Dodge=False, Box Offset=0.2')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'boxplot_position_fix.png'))
    plt.close()

# 4. u534au5206u306eu307fu8868u793au3055u308cu3066u3044u308bu554fu984cu306eu4feeu6b63u3092u30c6u30b9u30c8
def test_half_violin_fix():
    data = generate_test_data()
    
    fig, ax = plt.subplots(figsize=(8, 5))
    RainCloud(x='group', y='value', data=data, ax=ax)
    plt.title('Fixed Half Violin Display')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'half_violin_fix.png'))
    plt.close()

# 5. u7dcfu5408u30c6u30b9u30c8uff08u3059u3079u3066u306eu4feeu6b63u3092u7d44u307fu5408u308fu305bu305fu3082u306euff09
def test_comprehensive():
    data = generate_hue_data()
    
    # u5171u6709u30b9u30bfu30a4u30ebu3092u9069u7528
    configure_plots()
    
    fig, ax = plt.subplots(figsize=(5, 4))
    RainCloud(x='group', y='value', hue='condition', data=data,
              alpha=0.6, point_size=4, pointplot=True, connect_means=True,
              rain_offset=0.2, box_offset=0.1, ax=ax)
    ax.set_title('Comprehensive Fixed RainCloud')
    
    # u8ffdu52a0u306eu30b9u30bfu30a4u30ebu9069u7528
    apply_nature_style(fig, ax)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'comprehensive_fixed.png'))
    plt.close()

# u30e1u30a4u30f3u5b9fu884cu90e8u5206
if __name__ == "__main__":
    print("Testing fixed RainCloud plots...")
    
    # u3059u3079u3066u306eu30c6u30b9u30c8u3092u5b9fu884c
    test_legend_fix()
    test_rain_position_fix()
    test_boxplot_position_fix()
    test_half_violin_fix()
    test_comprehensive()
    
    print(f"All tests completed. Output images saved to {OUTPUT_DIR}")
