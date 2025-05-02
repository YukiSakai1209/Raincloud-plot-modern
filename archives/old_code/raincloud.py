"""
raincloud.py

seaborn 0.13.2に対応したRainCloud関数の実装
PtitPrince_refactored.pyから使用されます
"""

from __future__ import division

import warnings
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from seaborn_compatibility import translate_stripplot_params
from PtitPrince_refactored import half_violinplot, stripplot

def RainCloud(x=None, y=None, hue=None, data=None, order=None, hue_order=None,
              palette=None, bw="scott", width_viol=.8, width_box=.15,
              figsize=None, orient="v", move=0, offset=None, ax=None,
              pointplot=False, linecolor="black", point_size=5, jitter=True,
              dodge=True, scale="area", scale_hue=True, alpha=None,
              cut=2, linewidth=1, **kwargs):
    '''
    RainCloudプロットを作成する関数
    
    Parameters
    ----------
    x, y      : strings, names of variables in the data frame
    hue       : string, name of the variable for color encoding
    data      : pandas DataFrame
    order     : list, order of the categories
    hue_order : list, order of the hue
    orient    : string, vertical if "v" (default), horizontal if "h"
    width_viol: float, width of the cloud
    width_box : float, width of the boxplot
    move      : float, adjusts rain position to the x-axis (default value 0.)
    offset    : float, adjusts cloud position to the x-axis
    
    kwargs can be passed to the [cloud (default), boxplot, rain/stripplot, pointplot]
    by preponing [cloud_, box_, rain_ point_] to the argument name.
    '''
    
    # 水平方向の場合は、x,yを入れ替えるが、orientは'h'のままにする
    original_x, original_y = x, y
    if orient == 'h':  # swap x and y
        x, y = y, x
        
    if ax is None:
        ax = plt.gca()
    
    if offset is None:
        offset = max(width_box/1.8, .15) + .05
    n_plots = 3
    split = False
    boxcolor = "black"
    boxprops = {'facecolor': 'none', "zorder": 10}
    if hue is not None:
        split = True
        boxcolor = palette
        boxprops = {"zorder": 10}
    
    # キーワード引数を各コンポーネント用に分離
    kwcloud = dict()
    kwbox   = dict(saturation=1, whiskerprops={'linewidth': 2, "zorder": 10})
    kwrain  = dict(zorder=0, edgecolor="white")
    kwpoint = dict(capsize=0., errwidth=0., zorder=20)
    
    for key, value in kwargs.items():
        if "cloud_" in key:
            kwcloud[key.replace("cloud_", "")] = value
        elif "box_" in key:
            kwbox[key.replace("box_", "")] = value
        elif "rain_" in key:
            kwrain[key.replace("rain_", "")] = value
        elif "point_" in key:
            kwpoint[key.replace("point_", "")] = value
        else:
            kwcloud[key] = value

    # linewidthがkwcloudに含まれている場合は削除して、直接パラメータとして渡す
    cloud_linewidth = kwcloud.pop('linewidth', linewidth)

    # Draw cloud/half-violin - 元のパラメータ名を使用
    # 水平方向の場合は、入れ替えたx,yを使用するが、orientは'h'を明示的に渡す
    half_violinplot(x=x, y=y, hue=hue, data=data,
                    order=order, hue_order=hue_order,
                    orient=orient, width=width_viol,
                    inner=None, palette=palette, 
                    bw=bw,  # bw_methodではなくbwを使用
                    linewidth=cloud_linewidth,
                    cut=cut, 
                    scale=scale,  # density_normではなくscaleを使用
                    scale_hue=scale_hue,  # common_normではなくscale_hueを使用
                    split=split, offset=offset, ax=ax, **kwcloud)

    # Draw umbrella/boxplot
    # 水平方向の場合は、入れ替えたx,yを使用するが、orientは'h'を明示的に渡す
    sns.boxplot(x=x, y=y, hue=hue, data=data, orient=orient, width=width_box,
                order=order, hue_order=hue_order,
                color=boxcolor, showcaps=True, boxprops=boxprops,
                palette=palette, dodge=dodge, ax=ax, **kwbox)

    # Set alpha of the two
    if alpha is not None:
        plt.setp(ax.collections + ax.artists, alpha=alpha)

    # Draw rain/stripplot
    # 水平方向の場合は、入れ替えたx,yを使用するが、orientは'h'を明示的に渡す
    ax = stripplot(x=x, y=y, hue=hue, data=data, orient=orient,
                  order=order, hue_order=hue_order, palette=palette,
                  move=move, size=point_size, jitter=jitter, dodge=dodge,
                  width=width_box, ax=ax, **kwrain)

    # Add pointplot
    if pointplot:
        n_plots = 4
        if hue is not None:
            n_cat = len(np.unique(data[hue]))
            sns.pointplot(x=x, y=y, hue=hue, data=data,
                          orient=orient, order=order, hue_order=hue_order,
                          dodge=width_box * (1 - 1 / n_cat), palette=palette, ax=ax, **kwpoint)
        else:
            sns.pointplot(x=x, y=y, hue=hue, data=data, color=linecolor,
                         orient=orient, order=order, hue_order=hue_order,
                         dodge=width_box/2., ax=ax, **kwpoint)

    # Prune the legend, add legend title
    if hue is not None:
        handles, labels = ax.get_legend_handles_labels()
        if len(labels) > 0:  # レジェンドが存在する場合のみ処理
            plt.legend(handles[0:len(labels)//n_plots], labels[0:len(labels)//n_plots],
                      bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,
                      title=str(hue))

    # Adjust the ylim to fit (if needed)
    if orient == "h":
        ylim = list(ax.get_ylim())
        ylim[-1] -= (width_box + width_viol)/4.
        ax.set_ylim(ylim)
    elif orient == "v":
        xlim = list(ax.get_xlim())
        xlim[-1] -= (width_box + width_viol)/4.
        ax.set_xlim(xlim)

    return ax

if __name__ == "__main__":
    print("RainCloud function is available")
    print("This module provides the RainCloud function for PtitPrince_refactored.py")
