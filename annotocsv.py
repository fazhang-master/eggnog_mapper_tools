# 以下代码实现从eggNOG注释文件到COG分类图的完整流程
# 包含：数据解析、映射关联、统计绘图
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties

# ==================== 第一部分：数据预处理 ====================
# 读取eggNOG注释文件
annotations = pd.read_csv(
    "PA1.emapper.annotations",
    sep="\t",
    comment="#",
    header=None,
    usecols=[0, 6],  # 第0列是基因ID，第6列是COG分类代码
    names=["Gene_ID", "COG_code"]
)

# 清洗数据
valid_cogs = annotations["COG_code"].str.match(r"^[A-Z-]$")
cog_clean = annotations[valid_cogs].copy()

# ==================== 第二部分：加载映射表 ====================
# 读取映射表
cog_mapping = pd.read_csv("COG_mapping.csv")

# 合并数据：将COG代码映射到功能分类
merged = pd.merge(
    cog_clean,
    cog_mapping,
    on="COG_code",
    how="left"
).dropna(subset=["Function"])

# 统计各功能的基因数量
cog_counts = merged.groupby(
    ["Category", "Function", "COG_code"]
).size().reset_index(name="Count")
cog_counts.to_csv("cog_function_counts.csv", index=False, encoding='utf-8-sig')

print("文件已保存：cog_function_counts.csv")
