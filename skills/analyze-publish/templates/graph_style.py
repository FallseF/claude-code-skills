"""
論文用グラフスタイル設定（Nature風）
このファイルをインポートして使用する
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter


def setup_nature_style():
    """Nature風のグラフスタイルを設定"""
    plt.rcParams.update({
        'font.family': 'Arial',
        'font.size': 8,
        'axes.labelsize': 9,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8,
        'axes.linewidth': 0.6,
        'xtick.major.width': 0.6,
        'ytick.major.width': 0.6,
        'xtick.major.size': 3.5,
        'ytick.major.size': 3.5,
        'figure.dpi': 300,
        'savefig.dpi': 600,
        'savefig.bbox': 'tight',
    })


def apply_axis_style(ax):
    """軸のスタイルを適用（上・右の軸非表示、数値フォーマット）"""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_major_formatter(FormatStrFormatter('%g'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%g'))


# 図サイズの定数
SINGLE_COLUMN = (3.3, 2.8)  # 89mm幅
DOUBLE_COLUMN = (7.0, 2.8)  # 183mm幅

# カラーパレット
COLORS = {
    'black': 'black',
    'red': '#c00000',
    'blue': '#1f77b4',
    'green': '#2ca02c',
    'orange': '#ff7f0e',
    'gray': '#888888',
    'light_gray': 'lightgray',
}

# マーカースタイル
MARKER_STYLE = {
    'markersize': 5.5,
    'markerfacecolor': 'white',
    'markeredgewidth': 0.8,
    'linewidth': 0.7,
}

# エラーバースタイル
ERRORBAR_STYLE = {
    'capsize': 2,
    'elinewidth': 0.7,
    'capthick': 0.6,
}
