# 改良版RainCloudプロット

## 概要

RainCloudプロットは、データの分布を視覚化するための効果的な手法で、バイオリンプロット（KDE）、ボックスプロット、散布点プロットを組み合わせたものです。この改良版では、seaborn 0.13.2との互換性を維持しながら、見た目と機能の改善を行いました。

## 主な改良点

1. **Half Violinの表示調整**
   - 左半分固定の表示（垂直方向）または下半分固定の表示（水平方向）
   - 透明度の調整（デフォルトで0.5に設定）

2. **凡例の重複問題の解決**
   - 重複する凡例を自動的に削除し、1セットのみ表示

3. **Rain部分の調整**
   - 散布点サイズの調整機能の強化
   - dodge機能の改善（hueカテゴリごとに位置をずらす）

4. **平均値接続機能の実装**
   - pointplotで平均値を表示
   - カテゴリ間の平均値を線で結ぶ機能（`connect_means=True`）

5. **Nature誌ガイドラインに準拠したスタイル適用**
   - `apply_nature_style`関数の追加
   - 共有スタイル設定との連携（`shared.src.visualization.styles`）

## 使用方法

### 基本的な使用法

```python
from raincloud_modern import RainCloud
import matplotlib.pyplot as plt

# 基本的なRainCloudプロット
fig, ax = plt.subplots()
RainCloud(x='group', y='value', data=df, ax=ax)
plt.show()
```

### 平均値接続機能の使用

```python
# 平均値を表示し、カテゴリ間を線で接続
RainCloud(x='group', y='value', hue='condition', data=df,
          pointplot=True, connect_means=True, ax=ax)
```

### Nature誌スタイルの適用

```python
from raincloud_modern import RainCloud, apply_nature_style
from shared.src.visualization.styles import configure_plots

# 共有スタイルを適用
configure_plots()

fig, ax = plt.subplots()
RainCloud(x='group', y='value', data=df, ax=ax)

# 追加のNature誌スタイルを適用
apply_nature_style(fig, ax)
plt.show()
```

## 主要なパラメータ

| パラメータ | 説明 | デフォルト値 |
|------------|------|-------------|
| `x`, `y` | データフレーム内の変数名 | `None` |
| `hue` | 色分けに使用する変数名 | `None` |
| `data` | pandas DataFrame | `None` |
| `orient` | プロットの向き（'v'=垂直、'h'=水平） | `'v'` |
| `width_viol` | バイオリン（cloud）部分の幅 | `0.8` |
| `width_box` | ボックスプロットの幅 | `0.15` |
| `alpha` | 透明度 | `0.5` |
| `point_size` | 散布点のサイズ | `5` |
| `pointplot` | 平均値と信頼区間を表示するかどうか | `False` |
| `connect_means` | カテゴリ間の平均値を線で接続するかどうか | `False` |

## 実装の詳細

- **Half Violin**: KDEの計算に`scipy.stats.gaussian_kde`を使用し、片側のみを表示
- **Rain部分**: `matplotlib.pyplot.scatter`を使用して散布点をプロット
- **Box部分**: `matplotlib.pyplot.boxplot`を使用してボックスプロットを表示
- **Point部分**: `matplotlib.pyplot.errorbar`を使用して平均値と標準誤差を表示

## 注意点

- 水平方向のプロットでは、`x`と`y`の指定が垂直方向と逆になります（`orient='h'`を指定）
- `pointplot=True`の場合のみ`connect_means=True`が機能します
- Nature誌スタイルを適用する場合は、`configure_plots()`と`apply_nature_style()`の両方を使用することをお勧めします
