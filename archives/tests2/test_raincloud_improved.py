#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RainCloudプロットの見た目の改善と機能整理をテストするスクリプト

以下の機能をテストします：
1. Half Violinの表示調整（左半分固定、透明度調整）
2. 凡例の重複問題の解決
3. Rain部分の調整（散布点サイズ、dodge機能）
4. 平均値接続機能の実装（pointplotで平均値を線で結ぶ機能）
5. Nature誌ガイドラインに準拠したスタイル適用
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 改良したRainCloud関数をインポート
from raincloud_modern import RainCloud, apply_nature_style
from shared.src.visualization.styles import configure_plots

# 出力ディレクトリの設定
OUTPUT_DIR = os.path.join(os.getcwd(), 'outputs', 'improved')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# テスト用のデータを生成
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

# hueパラメータ用のデータを生成
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

# 1. 基本的なRainCloudプロット（透明度調整）
def test_basic_raincloud():
    data = generate_test_data()
    
    fig, ax = plt.subplots(figsize=(5, 4))
    RainCloud(x='group', y='value', data=data, alpha=0.5, ax=ax)
    plt.title('Basic RainCloud Plot with Alpha=0.5')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'basic_raincloud.png'))
    plt.close()

# 2. 凡例の重複問題の解決
def test_legend_deduplication():
    data = generate_hue_data()
    
    fig, ax = plt.subplots(figsize=(6, 4))
    RainCloud(x='group', y='value', hue='condition', data=data, ax=ax)
    plt.title('RainCloud Plot with Deduplicated Legend')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'legend_deduplication.png'))
    plt.close()

# 3. Rain部分の調整（散布点サイズ、dodge機能）
def test_rain_customization():
    data = generate_hue_data()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # 散布点サイズの調整
    RainCloud(x='group', y='value', hue='condition', data=data, 
              point_size=3, ax=ax1)
    ax1.set_title('Small Point Size (3)')
    
    # dodge機能のオフ
    RainCloud(x='group', y='value', hue='condition', data=data, 
              dodge=False, ax=ax2)
    ax2.set_title('Dodge Disabled')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'rain_customization.png'))
    plt.close()

# 4. 平均値接続機能
def test_connect_means():
    data = generate_hue_data()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 垂直方向の平均値接続
    RainCloud(x='group', y='value', hue='condition', data=data, 
              pointplot=True, connect_means=True, ax=ax1)
    ax1.set_title('Vertical RainCloud with Connected Means')
    
    # 水平方向の平均値接続
    RainCloud(x='value', y='group', hue='condition', data=data, 
              orient='h', pointplot=True, connect_means=True, ax=ax2)
    ax2.set_title('Horizontal RainCloud with Connected Means')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'connect_means.png'))
    plt.close()

# 5. Nature誌ガイドラインに準拠したスタイル適用
def test_nature_style():
    data = generate_hue_data()
    
    # 共有スタイルを適用
    configure_plots()
    
    fig, ax = plt.subplots()
    RainCloud(x='group', y='value', hue='condition', data=data, 
              pointplot=True, connect_means=True, ax=ax)
    ax.set_title('Nature Style RainCloud Plot')
    
    # 追加のスタイル適用
    apply_nature_style(fig, ax)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'nature_style.png'))
    plt.close()

# 6. 水平・垂直方向の比較
def test_orientation_comparison():
    data = generate_test_data()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # 垂直方向
    RainCloud(x='group', y='value', data=data, ax=ax1)
    ax1.set_title('Vertical RainCloud')
    
    # 水平方向
    RainCloud(x='value', y='group', data=data, orient='h', ax=ax2)
    ax2.set_title('Horizontal RainCloud')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'orientation_comparison.png'))
    plt.close()

# 7. 総合テスト（すべての改善を組み合わせたもの）
def test_comprehensive():
    data = generate_hue_data()
    
    # 共有スタイルを適用
    configure_plots()
    
    fig, ax = plt.subplots(figsize=(5, 4))
    RainCloud(x='group', y='value', hue='condition', data=data,
              alpha=0.6, point_size=4, pointplot=True, connect_means=True,
              ax=ax)
    ax.set_title('Comprehensive Improved RainCloud')
    
    # 追加のスタイル適用
    apply_nature_style(fig, ax)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'comprehensive.png'))
    plt.close()

# メイン実行部分
if __name__ == "__main__":
    print("Testing improved RainCloud plots...")
    
    # すべてのテストを実行
    test_basic_raincloud()
    test_legend_deduplication()
    test_rain_customization()
    test_connect_means()
    test_nature_style()
    test_orientation_comparison()
    test_comprehensive()
    
    print(f"All tests completed. Output images saved to {OUTPUT_DIR}")
