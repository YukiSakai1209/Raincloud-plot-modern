"""
seaborn_compatibility.py

このモジュールは、seaborn 0.13.2との互換性を確保するためのユーティリティ関数を提供します。
PtitPrince.pyのリファクタリングに使用されます。
"""

import warnings
import numpy as np
import seaborn as sns
from functools import wraps

def translate_violinplot_params(func):
    """
    seaborn 0.13.2のviolinplotパラメータ変更に対応するデコレータ
    
    以下のパラメータ変換を行います:
    - scale -> density_norm
    - scale_hue -> common_norm
    - bw -> bw_method
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # scale -> density_norm の変換
        if 'scale' in kwargs:
            scale = kwargs.pop('scale')
            if scale in ['area', 'count', 'width']:
                kwargs['density_norm'] = scale
            else:
                warnings.warn(
                    f"'scale' パラメータの値 '{scale}' は非推奨です。"
                    f"'density_norm' パラメータを使用してください。",
                    UserWarning
                )
        
        # scale_hue -> common_norm の変換
        if 'scale_hue' in kwargs:
            scale_hue = kwargs.pop('scale_hue')
            kwargs['common_norm'] = not scale_hue
            warnings.warn(
                "'scale_hue' パラメータは非推奨です。"
                "'common_norm' パラメータを使用してください。",
                UserWarning
            )
        
        # bw -> bw_method の変換
        if 'bw' in kwargs:
            bw = kwargs.pop('bw')
            kwargs['bw_method'] = bw
            warnings.warn(
                "'bw' パラメータは非推奨です。"
                "'bw_method' パラメータを使用してください。",
                UserWarning
            )
        
        return func(*args, **kwargs)
    
    return wrapper

def translate_stripplot_params(func):
    """
    seaborn 0.13.2のstripplotパラメータ変更に対応するデコレータ
    
    以下のパラメータ変換を行います:
    - split -> dodge (既にPtitPrince.pyで対応済みだが、念のため)
    - moveパラメータの処理 (PtitPrince.py特有のパラメータ)
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # split -> dodge の変換 (既にPtitPrince.pyで対応済みだが、念のため)
        if 'split' in kwargs:
            split = kwargs.pop('split')
            kwargs['dodge'] = split
            warnings.warn(
                "'split' パラメータは 'dodge' に名前が変更されました。",
                UserWarning
            )
        
        # moveパラメータの抽出（後で処理するため）
        move = kwargs.pop('move', 0)
        
        # 元の関数を呼び出し
        result = func(*args, **kwargs)
        
        # moveパラメータの処理（必要に応じて）
        if move != 0:
            # moveパラメータの処理は、refactored_stripplotの実装で行う
            pass
        
        return result
    
    return wrapper

class ViolinSplitter:
    """
    seaborn 0.13.2のviolinplotを拡張して、片側バイオリンプロットをサポートするクラス
    """
    
    @staticmethod
    def modify_violinplot_data(ax, orient='v', offset=0.15):
        """
        violinplotのデータを修正して片側バイオリンプロットを作成する
        
        Parameters
        ----------
        ax : matplotlib.axes.Axes
            バイオリンプロットが描画されているAxesオブジェクト
        orient : str, default 'v'
            プロットの向き ('v'または'h')
        offset : float, default 0.15
            バイオリンプロットのオフセット
        """
        # 現在のバイオリンプロットのコレクションを取得
        collections = [c for c in ax.collections if isinstance(c, plt.matplotlib.collections.PolyCollection)]
        
        for collection in collections:
            # パスのデータを取得
            paths = collection.get_paths()
            
            for path in paths:
                vertices = path.vertices
                
                # 向きに応じて座標を修正
                if orient == 'v':
                    # 垂直方向のバイオリンプロット
                    x_center = np.mean(vertices[:, 0])
                    mask = vertices[:, 0] > x_center
                    vertices[mask, 0] = x_center + offset
                else:
                    # 水平方向のバイオリンプロット
                    y_center = np.mean(vertices[:, 1])
                    mask = vertices[:, 1] > y_center
                    vertices[mask, 1] = y_center + offset
        
        return ax

# seaborn 0.13.2のAPIを使用して、PtitPrince.pyの関数を再実装するためのベースクラス
class PtitPrinceBase:
    """
    PtitPrince.pyの関数をseaborn 0.13.2のAPIを使用して再実装するためのベースクラス
    """
    
    @staticmethod
    def get_default_color(ax):
        """
        デフォルトの色を取得する
        """
        return sns.color_palette()[0]
    
    @staticmethod
    def get_gray_color():
        """
        グレーの色を取得する
        """
        return (0.5, 0.5, 0.5)

# テスト用のユーティリティ
def print_param_diff(original_params, current_params):
    """
    元のパラメータと現在のパラメータの違いを表示する
    
    Parameters
    ----------
    original_params : dict
        元のパラメータ
    current_params : dict
        現在のパラメータ
    """
    print("パラメータの違い:")
    print("-" * 40)
    
    # 元のパラメータにあって現在のパラメータにないもの
    for param in original_params:
        if param not in current_params:
            print(f"削除: {param}")
    
    # 現在のパラメータにあって元のパラメータにないもの
    for param in current_params:
        if param not in original_params:
            print(f"追加: {param}")
    
    # 両方にあるが値が異なるもの
    for param in original_params:
        if param in current_params and original_params[param] != current_params[param]:
            print(f"変更: {param} = {original_params[param]} -> {current_params[param]}")
    
    print("-" * 40)

# 互換性レイヤーのテスト
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    # violinplotパラメータの変換をテスト
    @translate_violinplot_params
    def test_violinplot_params(**kwargs):
        print("変換後のパラメータ:")
        for key, value in kwargs.items():
            print(f"{key}: {value}")
        return kwargs
    
    print("violinplotパラメータの変換テスト:")
    original_params = {
        'scale': 'area',
        'scale_hue': True,
        'bw': 0.5,
        'other_param': 'value'
    }
    
    converted_params = test_violinplot_params(**original_params)
    print_param_diff(original_params, converted_params)
    
    # stripplotパラメータの変換をテスト
    @translate_stripplot_params
    def test_stripplot_params(**kwargs):
        print("変換後のパラメータ:")
        for key, value in kwargs.items():
            print(f"{key}: {value}")
        return kwargs
    
    print("\nstripplotパラメータの変換テスト:")
    original_params = {
        'split': True,
        'move': 0.1,
        'other_param': 'value'
    }
    
    converted_params = test_stripplot_params(**original_params)
    print_param_diff(original_params, converted_params)
