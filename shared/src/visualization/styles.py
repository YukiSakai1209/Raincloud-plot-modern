# shared/src/plotting/styles.py の改善案
import matplotlib.pyplot as plt
from scienceplots import plt as sp_plt


def configure_plots(style="nature", font_size=5):
    """configuration of plot style and font size"""
    plt.style.use(
        [
            "science",
            style,
            "no-latex",
            "bright",
            {
                "font.size": font_size,
                "axes.labelsize": font_size,
                "xtick.labelsize": font_size,
                "ytick.labelsize": font_size,
                "legend.fontsize": font_size - 1,
                "legend.loc": "best",
                "legend.borderaxespad": 0,
            },
        ]
    )

    plt.rcParams.update(
        {
            "figure.figsize": (3.3, 2.5),
            "figure.dpi": 600,
            "savefig.bbox": "tight",
            "grid.linewidth": 0.0,
            "grid.linestyle": "-",
            "grid.color": "white",
            "grid.alpha": 0,
        }
    )
