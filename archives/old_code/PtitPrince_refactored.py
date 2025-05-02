"""
PtitPrince_refactored.py

seaborn 0.13.2に対応したPtitPrince.pyのリファクタリング版
Raincloudプロットを作成するためのユーティリティ関数を提供します。
"""

from __future__ import division

import warnings

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from functools import partial
from scipy import stats
from matplotlib.collections import PolyCollection
from matplotlib.path import Path

from seaborn_compatibility import translate_violinplot_params, translate_stripplot_params, PtitPrinceBase

__all__ = ["half_violinplot", "stripplot"]
__version__ = '0.2.6'  # リファクタリング版のバージョン


class _Half_ViolinPlotter(PtitPrinceBase):
    """
    seaborn 0.13.2のAPIを使用して片側バイオリンプロットを実装するクラス
    """
    
    def __init__(self, x=None, y=None, hue=None, data=None, order=None, hue_order=None,
                 bw="scott", cut=2, scale="area", scale_hue=True, gridsize=100,
                 width=.8, inner="box", split=False, dodge=True, orient=None,
                 linewidth=None, color=None, palette=None, saturation=.75, offset=.15):
        """
        パラメータを保存し、後でplot_half_violinメソッドで使用する
        """
        self.x = x
        self.y = y
        self.hue = hue
        self.data = data
        self.order = order
        self.hue_order = hue_order
        self.bw = bw
        self.cut = cut
        self.scale = scale
        self.scale_hue = scale_hue
        self.gridsize = gridsize
        self.width = width
        self.inner = inner
        self.split = split
        self.dodge = dodge
        self.orient = orient
        self.linewidth = linewidth
        self.color = color
        self.palette = palette
        self.saturation = saturation
        self.offset = offset
        
    def plot(self, ax, plot_kws=None):
        """
        片側バイオリンプロットを描画する
        """
        if plot_kws is None:
            plot_kws = {}
            
        # データフレームを準備
        data = self.data
        
        # 変数名を取得
        x = self.x
        y = self.y
        hue = self.hue
        
        # 向きを決定
        orient = self.orient
        if orient is None:
            if x is None:
                orient = "h"
            elif y is None:
                orient = "v"
            else:
                orient = "v" if data[x].nunique() < data[y].nunique() else "h"
        
        # データを整理
        if orient == "v":
            # 垂直方向のバイオリンプロット
            value_col = y
            group_col = x
        else:
            # 水平方向のバイオリンプロット
            value_col = x
            group_col = y
        
        # グループの順序を決定
        if self.order is not None:
            group_order = self.order
        else:
            group_order = data[group_col].unique()
        
        # hueの順序を決定
        if hue is not None:
            if self.hue_order is not None:
                hue_order = self.hue_order
            else:
                hue_order = data[hue].unique()
        else:
            hue_order = [None]
        
        # 色のパレットを設定
        if self.palette is not None:
            palette = self.palette
        elif self.color is not None:
            palette = [self.color] * len(hue_order)
        else:
            palette = sns.color_palette()
            
        # 線の幅を設定
        if self.linewidth is None:
            linewidth = 0.5
        else:
            linewidth = self.linewidth
        
        # 各グループごとにバイオリンプロットを描画
        for i, group in enumerate(group_order):
            group_data = data[data[group_col] == group]
            
            # hueごとに処理
            for j, hue_level in enumerate(hue_order):
                if hue is not None:
                    hue_data = group_data[group_data[hue] == hue_level]
                    color = palette[j % len(palette)]
                else:
                    hue_data = group_data
                    color = palette[i % len(palette)]
                
                if len(hue_data) < 2:
                    continue
                
                # 位置を調整
                if self.dodge and hue is not None:
                    dodge_width = self.width / len(hue_order)
                    position = i + (j - (len(hue_order) - 1) / 2) * dodge_width
                else:
                    position = i
                
                # KDEを計算
                values = hue_data[value_col].dropna().values
                if len(values) < 2:
                    continue
                
                kde = stats.gaussian_kde(values, bw_method=self.bw)
                
                # 密度のサポート範囲を計算
                cut = self.cut
                gridsize = self.gridsize
                support = np.linspace(
                    np.min(values) - cut * np.std(values),
                    np.max(values) + cut * np.std(values),
                    gridsize
                )
                density = kde(support)
                
                # 密度を正規化
                if self.scale == "area":
                    density = density / density.max()
                elif self.scale == "count":
                    density = density * len(values) / density.max()
                elif self.scale == "width":
                    density = density / density.max()
                
                # 幅を調整
                width = self.width
                if self.dodge and hue is not None:
                    width = width / len(hue_order)
                density = density * width / 2
                
                # 片側バイオリンプロットを描画
                if orient == "v":
                    # 垂直方向のバイオリンプロット
                    vertices = np.zeros((2 * len(support), 2))
                    vertices[:len(support), 0] = position
                    vertices[:len(support), 1] = support
                    vertices[len(support):, 0] = position + density
                    vertices[len(support):, 1] = support[::-1]
                else:
                    # 水平方向のバイオリンプロット - 完全に新しいアプローチ
                    # 水平方向の場合は、x軸が値、y軸がカテゴリになるため、座標を適切に設定
                    vertices = np.zeros((2 * len(support), 2))
                    # 最初の半分は下側の輪郭（値軸に沿った線）
                    vertices[:len(support), 0] = support
                    vertices[:len(support), 1] = position
                    # 後半は上側の輪郭（密度に基づいて上方向に伸びる）
                    vertices[len(support):, 0] = support[::-1]  # 逆順にして閉じた形状にする
                    vertices[len(support):, 1] = position + density  # 密度に基づいて上方向に伸びる
                
                # 明示的に軸の範囲を設定（水平方向の場合）
                if orient == "h":
                    # データの範囲に基づいて適切なマージンを追加
                    data_range = np.max(support) - np.min(support)
                    margin = data_range * 0.1
                    ax.set_xlim(np.min(support) - margin, np.max(support) + margin)
                    
                    # 密度の最大値に基づいてY軸の範囲を設定
                    density_max = np.max(density)
                    # より広いマージンを設定して、バイオリンプロットが確実に表示されるようにする
                    ax.set_ylim(position - density_max * 0.5, position + density_max * 2.0)
                
                # 色を設定
                if self.saturation < 1:
                    color = sns.utils.set_hls_values(
                        color, l=None, s=self.saturation
                    )
                
                # plot_kwsからseabornの特定のパラメータを除外（Polygonに渡せないパラメータ）
                polygon_kws = plot_kws.copy() if plot_kws else {}
                for key in ['density_norm', 'common_norm', 'bw_method', 'cut', 'scale', 'scale_hue']:
                    if key in polygon_kws:
                        polygon_kws.pop(key)
                
                # linecolorをplot_kwsから取得
                edgecolor = plot_kws.get('linecolor', 'white') if plot_kws else 'white'
                # alphaをplot_kwsから取得、デフォルトは1.0
                alpha = plot_kws.get('alpha', 1.0) if plot_kws else 1.0
                poly = plt.Polygon(vertices, facecolor=color, edgecolor=edgecolor,
                                linewidth=linewidth, alpha=alpha, **polygon_kws)
                ax.add_patch(poly)
                
                # 明示的に軸の範囲を更新（重要: 水平方向の場合に特に必要）
                ax.autoscale_view()
                
                # 内部マーカーを描画
                if self.inner is not None:
                    if self.inner == "box":
                        # 箱ひげ図のような内部マーカー
                        q25, q50, q75 = np.percentile(values, [25, 50, 75])
                        if orient == "v":
                            ax.plot([position, position + density.max() / 2], [q50, q50], color='w', linewidth=linewidth*2)
                            ax.plot([position, position + density.max() / 2], [q25, q25], color='w', linewidth=linewidth)
                            ax.plot([position, position + density.max() / 2], [q75, q75], color='w', linewidth=linewidth)
                        else:
                            ax.plot([q50, q50], [position, position + density.max() / 2], color='w', linewidth=linewidth*2)
                            ax.plot([q25, q25], [position, position + density.max() / 2], color='w', linewidth=linewidth)
                            ax.plot([q75, q75], [position, position + density.max() / 2], color='w', linewidth=linewidth)
                    elif self.inner == "point":
                        # 点を描画
                        if orient == "v":
                            ax.scatter([position + density.max() / 4] * len(values), values, color='w', s=10, alpha=0.5)
                        else:
                            ax.scatter(values, [position + density.max() / 4] * len(values), color='w', s=10, alpha=0.5)
                    elif self.inner == "stick":
                        # 線を描画
                        for value in values:
                            if orient == "v":
                                ax.plot([position, position + density.max() / 2], [value, value], color='w', linewidth=linewidth/2, alpha=0.5)
                            else:
                                ax.plot([value, value], [position, position + density.max() / 2], color='w', linewidth=linewidth/2, alpha=0.5)
                    elif self.inner == "quart":
                        # 四分位数を描画
                        quartiles = np.percentile(values, [25, 50, 75])
                        if orient == "v":
                            for q in quartiles:
                                ax.plot([position, position + density.max() / 2], [q, q], color='w', linewidth=linewidth, alpha=0.9)
                        else:
                            for q in quartiles:
                                ax.plot([q, q], [position, position + density.max() / 2], color='w', linewidth=linewidth, alpha=0.9)
        
        # 軸の設定
        if orient == "v":
            ax.set_xticks(range(len(group_order)))
            ax.set_xticklabels(group_order)
        else:
            ax.set_yticks(range(len(group_order)))
            ax.set_yticklabels(group_order)
        
        return ax


@translate_violinplot_params
def half_violinplot(x=None, y=None, hue=None, data=None, order=None, hue_order=None,
                   bw="scott", cut=2, scale="area", scale_hue=True, gridsize=100,
                   width=.8, inner="box", split=False, dodge=True, orient=None,
                   linewidth=None, color=None, palette=None, saturation=.75,
                   ax=None, offset=.15, **kwargs):
    """
    片側バイオリンプロットを描画する
    
    Parameters
    ----------
    x, y, hue : strings, optional
        データフレームの列名
    data : DataFrame, array, or list of arrays, optional
        プロットするデータ
    order, hue_order : lists of strings, optional
        カテゴリの順序
    bw : {'scott', 'silverman', float}, optional
        カーネル密度推定のバンド幅
    cut : float, optional
        カーネル密度推定の範囲
    scale : {"area", "count", "width"}, optional
        バイオリンプロットのスケーリング方法
    scale_hue : bool, optional
        異なるhueカテゴリ間でスケールを適用するかどうか
    gridsize : int, optional
        カーネル密度推定の解像度
    width : float, optional
        バイオリンプロットの幅
    inner : {"box", "quart", "stick", "point", None}, optional
        内部マーカーのスタイル
    split : bool, optional
        hueカテゴリごとに分割するかどうか
    dodge : bool, optional
        hueカテゴリごとに水平方向にずらすかどうか
    orient : {"v", "h"}, optional
        プロットの向き
    linewidth : float, optional
        線の幅
    color : matplotlib color, optional
        すべてのエレメントの色
    palette : palette name, list, or dict, optional
        hueカテゴリの色
    saturation : float, optional
        色の彩度
    ax : matplotlib Axes, optional
        プロットするAxesオブジェクト
    offset : float, optional
        バイオリンプロットのオフセット
    **kwargs : key, value mappings
        その他のキーワード引数はmatplotlibに渡される
    
    Returns
    -------
    ax : matplotlib Axes
        プロットが描画されたAxesオブジェクト
    """
    plotter = _Half_ViolinPlotter(x, y, hue, data, order, hue_order,
                              bw, cut, scale, scale_hue, gridsize,
                              width, inner, split, dodge, orient, linewidth,
                              color, palette, saturation, offset)
    
    if ax is None:
        ax = plt.gca()
    
    plotter.plot(ax, kwargs)
    return ax


class _StripPlotter(PtitPrinceBase):
    """
    seaborn 0.13.2のAPIを使用してstripplotを実装するクラス
    """
    
    def __init__(self, x=None, y=None, hue=None, data=None, order=None, hue_order=None,
                 jitter=True, dodge=False, orient=None, color=None, palette=None, width=.8, move=0):
        """
        パラメータを保存し、後でplot_stripsメソッドで使用する
        """
        self.x = x
        self.y = y
        self.hue = hue
        self.data = data
        self.order = order
        self.hue_order = hue_order
        self.jitter = jitter
        self.dodge = dodge
        self.orient = orient
        self.color = color
        self.palette = palette
        self.width = width
        self.move = move
        
    def plot(self, ax, plot_kws=None):
        """
        stripplotを描画する
        """
        if plot_kws is None:
            plot_kws = {}
            
        # seaborn 0.13.2のパラメータに変換
        kwargs = {
            'x': self.x,
            'y': self.y,
            'hue': self.hue,
            'data': self.data,
            'order': self.order,
            'hue_order': self.hue_order,
            'jitter': self.jitter,
            'dodge': self.dodge,
            'orient': self.orient,
            'color': self.color,
            'palette': self.palette,
            'ax': ax
        }
        
        # kwargsをplot_kwsで更新
        kwargs.update(plot_kws)
        
        # stripplotを描画
        sns.stripplot(**kwargs)
        
        # moveパラメータを適用（点を水平方向に移動）
        if self.move != 0:
            self._apply_move(ax, self.orient, self.move)
        
        return ax
    
    def _apply_move(self, ax, orient='v', move=0):
        """
        stripplotの点を水平方向に移動する
        
        Parameters
        ----------
        ax : matplotlib.axes.Axes
            stripplotが描画されているAxesオブジェクト
        orient : str, default 'v'
            プロットの向き ('v'または'h')
        move : float, default 0
            点の移動量
        """
        if move == 0:
            return ax
            
        # 散布図の点を探す
        for collection in ax.collections:
            offsets = collection.get_offsets()
            
            if len(offsets) > 0:
                # 向きに応じて座標を修正
                if orient == 'v' or orient is None:  # デフォルトは垂直方向
                    # 垂直方向のstripplot（x座標を移動）
                    offsets[:, 0] += move
                else:
                    # 水平方向のstripplot（y座標を移動）
                    offsets[:, 1] += move
                
                # オフセットを更新
                collection.set_offsets(offsets)
        
        return ax


@translate_stripplot_params
def stripplot(x=None, y=None, hue=None, data=None, order=None, hue_order=None,
              jitter=True, dodge=False, orient=None, color=None, palette=None, move=0,
              size=5, edgecolor="gray", linewidth=0, ax=None, width=.8, **kwargs):
    """
    カテゴリカルデータの散布図を描画する
    
    Parameters
    ----------
    x, y, hue : strings, optional
        データフレームの列名
    data : DataFrame, array, or list of arrays, optional
        プロットするデータ
    order, hue_order : lists of strings, optional
        カテゴリの順序
    jitter : float or bool, optional
        点をランダムにずらす量
    dodge : bool, optional
        hueカテゴリごとに水平方向にずらすかどうか
    orient : {"v", "h"}, optional
        プロットの向き
    color : matplotlib color, optional
        すべてのエレメントの色
    palette : palette name, list, or dict, optional
        hueカテゴリの色
    move : float, default 0
        点を水平方向に移動する量（PtitPrince特有のパラメータ）
    size : float, optional
        マーカーのサイズ
    edgecolor : matplotlib color, "gray" or None, optional
        マーカーの枠線の色
    linewidth : float, optional
        マーカーの枠線の幅
    ax : matplotlib Axes, optional
        プロットするAxesオブジェクト
    width : float, optional
        カテゴリの幅
    **kwargs : key, value mappings
        その他のキーワード引数はmatplotlibに渡される
    
    Returns
    -------
    ax : matplotlib Axes
        プロットが描画されたAxesオブジェクト
    """
    plotter = _StripPlotter(x, y, hue, data, order, hue_order,
                           jitter, dodge, orient, color, palette, width, move)
    
    if ax is None:
        ax = plt.gca()
    
    kwargs.setdefault("zorder", 3)
    size = kwargs.get("s", size)
    if linewidth is None:
        linewidth = size / 10
    if edgecolor == "gray":
        edgecolor = PtitPrinceBase.get_gray_color()
    kwargs.update(dict(s=size ** 2,
                       edgecolor=edgecolor,
                       linewidth=linewidth))
    
    plotter.plot(ax, kwargs)
    return ax


# RainCloud関数は次のタスクで実装します

if __name__ == "__main__":
    print(f"PtitPrince_refactored version {__version__}")
    print("half_violinplot と stripplot 関数が利用可能です。")
    print("RainCloud 関数は次のタスクで実装予定です。")
