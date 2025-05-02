#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RainCloudプロットの修正をテストするスクリプト

以下の修正をテストします：
1. 水平方向のプロット機能の削除
2. 凡例表示の修正
3. Rain部分（散布点）がViolinプロットに重ならないよう調整
4. Dodge機能をオフにした際のBoxplot位置調整
5. 半分のみ表示されている問題の修正
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 修正したRainCloud関数をインポート
from raincloud_modern import RainCloud, apply_nature_style
from shared.src.visualization.styles import configure_plots

# 出力ディレクトリの設定
OUTPUT_DIR = os.path.join(os.getcwd(), 'outputs', 'fixed')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# テスト用データを生成する関数
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

# hue変数を含むテスト用データを生成する関数
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

# 1. 凡例表示の修正をテスト
def test_legend_fix():
    data = generate_hue_data()
    
    fig, ax = plt.subplots(figsize=(6, 4))
    RainCloud(x='group', y='value', hue='condition', data=data, ax=ax)
    plt.title('Fixed Legend Display')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'legend_fix.png'))
    plt.close()

# 2. Rain部分（散布点）がViolinプロットに重ならないよう調整をテスト
def test_rain_position_fix():
    data = generate_test_data()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # デフォルトのrain_offset
    RainCloud(x='group', y='value', data=data, ax=ax1)
    ax1.set_title('Default Rain Offset (0.1)')
    
    # 大きいrain_offset
    RainCloud(x='group', y='value', data=data, rain_offset=0.3, ax=ax2)
    ax2.set_title('Larger Rain Offset (0.3)')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'rain_position_fix.png'))
    plt.close()

# 3. Dodge機能をオフにした際のBoxplot位置調整をテスト
def test_boxplot_position_fix():
    data = generate_hue_data()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # dodge=Falseでbox_offset=0（デフォルト）
    RainCloud(x='group', y='value', hue='condition', data=data, dodge=False, ax=ax1)
    ax1.set_title('Dodge=False, Default Box Offset (0)')
    
    # dodge=Falseでbox_offset=0.2
    RainCloud(x='group', y='value', hue='condition', data=data, dodge=False, box_offset=0.2, ax=ax2)
    ax2.set_title('Dodge=False, Box Offset=0.2')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'boxplot_position_fix.png'))
    plt.close()

# 4. 半分のみ表示されている問題の修正をテスト
def test_half_violin_fix():
    data = generate_test_data()
    
    fig, ax = plt.subplots(figsize=(8, 5))
    RainCloud(x='group', y='value', data=data, ax=ax)
    plt.title('Fixed Half Violin Display')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'half_violin_fix.png'))
    plt.close()

# 5. 総合的な修正をテスト
def test_comprehensive():
    data = generate_hue_data()
    
    # 共通スタイルを適用
    configure_plots()
    
    fig, ax = plt.subplots(figsize=(5, 4))
    RainCloud(x='group', y='value', hue='condition', data=data,
              alpha=0.6, point_size=4, pointplot=True, connect_means=True,
              rain_offset=0.2, box_offset=0.1, ax=ax)
    ax.set_title('Comprehensive Fixed RainCloud')
    
    # Natureスタイルを適用
    apply_nature_style(fig, ax)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'comprehensive_fixed.png'))
    plt.close()

# メイン関数
if __name__ == "__main__":
    print("Testing fixed RainCloud plots...")
    
    # 各テストを実行
    test_legend_fix()
    test_rain_position_fix()
    test_boxplot_position_fix()
    test_half_violin_fix()
    test_comprehensive()
    
    print(f"All tests completed. Output images saved to {OUTPUT_DIR}")
