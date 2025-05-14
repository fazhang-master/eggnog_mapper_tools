#!/usr/bin/env python3
"""
eggnog-mapper注释文件转换工具 v2.1.3
将.anno文件转换为同目录下的.csv格式
"""

import argparse
import os
import sys
import pandas as pd

# 列定义（必须与eggnog-mapper输出严格匹配）
COLUMNS = [
    "query", "seed_ortholog", "evalue", "score", "eggNOG_OGs",
    "max_annot_lvl", "COG_category", "Description", "Preferred_name",
    "GOs", "EC", "KEGG_ko", "KEGG_Pathway", "KEGG_Module",
    "KEGG_Reaction", "KEGG_rclass", "BRITE", "KEGG_TC",
    "CAZy", "BiGG_Reaction", "PFAMs"
]

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="将eggnog-mapper的.anno注释文件转换为CSV格式",
        epilog="示例:\n  anno2csv_local_v2.1.3.py -i input.anno"
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="输入文件路径（eggnog-mapper的.annotations文件）"
    )
    return parser.parse_args()

def convert_anno_to_csv(input_path):
    """核心转换函数"""
    try:
        # 读取文件
        df = pd.read_csv(
            input_path,
            sep='\t',
            comment='#',
            header=None,
            names=COLUMNS,
            dtype=str
        )
        
        # 生成输出路径
        dir_name = os.path.dirname(input_path)
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(dir_name, f"{base_name}.csv")
        
        # 保存CSV
        df.to_csv(output_path, index=False)
        print(f"[SUCCESS] 转换完成 -> {output_path}")
        return 0
        
    except FileNotFoundError:
        print(f"[ERROR] 文件不存在: {input_path}")
        return 1
    except pd.errors.ParserError:
        print(f"[ERROR] 文件格式错误，请确认是eggnog-mapper输出文件")
        return 2
    except Exception as e:
        print(f"[ERROR] 未知错误: {str(e)}")
        return 3

def main():
    args = parse_arguments()
    sys.exit(convert_anno_to_csv(args.input))

if __name__ == "__main__":
    main()