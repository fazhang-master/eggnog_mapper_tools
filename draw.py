import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

# --- 数据准备 ---
df = pd.read_csv("cog_function_counts.csv")
df = df[df["Function"] != "Function unknown"]

# --- 可视化配置 ---
rcParams['font.sans-serif'] = ['Arial']
rcParams['axes.unicode_minus'] = False

# 创建画布并设置高清尺寸
plt.figure(figsize=(15, 12), facecolor='white')  

# --- 颜色方案 ---
cog_palette = {
    "CELLULAR": "#F28E2B",
    "INFORMATION": "#4E79A7",
    "METABOLISM": "#E15759",
    "POORLY": "#59A14F"
}

# --- 绘制柱状图 ---
sns.set_style("white")  # 使用空白背景样式
ax = sns.barplot(
    x="Count",
    y="Function",
    hue="Category",
    data=df,
    palette=cog_palette,
    saturation=0.85,
    dodge=False,
    zorder=2  # 确保柱子显示在网格线上方
)

# --- 网格线配置 ---
# 设置x/y轴所有刻度线的网格线（形成格子效果）
ax.grid(
    True,
    which='both',
    axis='both',  # 同时控制x和y轴
    color='#ffffff', # 控制坐标线颜色
    linestyle='-',
    linewidth=0.8,
    zorder=1      # 网格线在柱子下方
)

# --- 坐标轴线配置 ---
# 设置x轴和y轴的刻度线颜色为白色
ax.tick_params(
    axis='both',
    which='both',
    length=4,          # 刻度线长度
    width=1.2          # 刻度线宽度
)

# 设置坐标轴边框颜色为白色
ax.spines['bottom'].set_color('#ffffff')
ax.spines['left'].set_color('#ffffff')
ax.spines['bottom'].set_linewidth(1.2)
ax.spines['left'].set_linewidth(1.2)

# 隐藏顶部和右侧边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# --- 标签优化 ---
max_count = df["Count"].max()
for p in ax.patches:
    width = p.get_width()
    ax.text(
        width + max_count * 0.03,
        p.get_y() + p.get_height()/2,
        f"{int(width)}",
        va="center",
        ha="left",
        fontsize=10,
        color='black',
        zorder=3  # 文本在最上层
    )

# --- 图表装饰 ---
plt.title("COG Functional Classification\n(TL1)", 
          fontsize=14, pad=20, fontweight="bold")
plt.xlabel("Number of Genes", fontsize=12, labelpad=10)
plt.ylabel("", fontsize=12, labelpad=10)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10, rotation=0)

# 调整布局
plt.subplots_adjust(left=0.35, right=0.85)

# 图例定制
ax.legend(
    bbox_to_anchor=(1.05, 0.9),
    frameon=False,
    title_fontsize=12,
    fontsize=10
)

# --- 导出高清图 ---
plt.savefig(
    "COG_Plot_Final.png",
    dpi=300,
    bbox_inches="tight",
    facecolor='white'
)
plt.close()