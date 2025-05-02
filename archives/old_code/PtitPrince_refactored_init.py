"""
PtitPrince_refactored_init.py

PtitPrince_refactored.pyとraincloud.pyからの関数をインポートして、
一つのモジュールとして提供するための初期化ファイル
"""

from PtitPrince_refactored import half_violinplot, stripplot, __version__
from raincloud import RainCloud

__all__ = ["half_violinplot", "stripplot", "RainCloud"]

if __name__ == "__main__":
    print(f"PtitPrince_refactored version {__version__}")
    print("half_violinplot, stripplot, RainCloud 関数が利用可能です。")
