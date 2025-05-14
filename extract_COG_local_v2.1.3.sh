#!/bin/bash

# ==============================================
# eggnog COG分类统计工具 v2.1.3
# 支持多文件处理和健壮的错误检测
# ==============================================

# -------------------------------
# 颜色定义（ANSI转义码）
# -------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # 重置颜色

# -------------------------------
# 进度条显示函数
# 参数: 当前序号 总数量
# -------------------------------
progress_bar() {
    local current=$1
    local total=$2
    local width=30
    local percent=$(awk "BEGIN { pc=100*${current}/${total}; i=int(pc); print (pc-i<0.5)?i:i+1 }")
    local filled=$(awk "BEGIN { fl=(${width}*${current}/${total}); print int(fl) }")
    printf "\r["
    printf "%${filled}s" | tr ' ' '■'
    printf "%$((width-filled))s" | tr ' ' ' '
    printf "] ${CYAN}%3d%%${NC} (${MAGENTA}%d/${total}${NC})" "${percent}" "${current}"
}

# -------------------------------
# 显示帮助信息
# -------------------------------
show_help() {
    echo -e "${GREEN}用法: $0 [选项] -i 文件1 [ -i 文件2 ... ]${NC}"
    echo -e "选项:"
    echo -e "  -i  必选，输入文件路径（可多次使用）"
    echo -e "  -h  显示此帮助信息"
    echo -e "\n示例:"
    echo -e "  $0 -i file1.emapper.annotations"
    echo -e "  $0 -i data/file1.anno -i data/file2.anno"
    exit 0
}

# -------------------------------
# 解析命令行参数
# -------------------------------
declare -a input_files=()
while getopts ":i:h" opt; do
    case $opt in
        i)
            input_files+=("$OPTARG")
            ;;
        h)
            show_help
            ;;
        \?)
            echo -e "${RED}错误: 无效选项 -${OPTARG}${NC}" >&2
            exit 1
            ;;
        :)
            echo -e "${RED}错误: 选项 -${OPTARG} 需要参数${NC}" >&2
            exit 1
            ;;
    esac
done

# -------------------------------
# 验证输入参数
# -------------------------------
if [ ${#input_files[@]} -eq 0 ]; then
    echo -e "${RED}错误: 必须通过 -i 指定至少一个输入文件${NC}" >&2
    exit 1
fi

# ==============================================
# 主处理循环
# ==============================================
total_files=${#input_files[@]}
current_file=1
declare -a error_files=()
declare -a success_files=()

echo -e "\n${BLUE}=== 开始处理 ${total_files} 个文件 ===${NC}"

for input_file in "${input_files[@]}"; do
    # -------------------------------
    # 步骤0: 文件验证
    # -------------------------------
    echo -e "\n${YELLOW}【文件 ${current_file}/${total_files}】${NC} ${CYAN}${input_file}${NC}"
    progress_bar ${current_file} ${total_files}

    # 检查文件存在性
    if [ ! -f "${input_file}" ]; then
        echo -e "\n${RED}错误: 文件不存在 ${input_file}${NC}"
        error_files+=("${input_file} [文件不存在]")
        ((current_file++))
        continue
    fi

    # 检查文件是否为空
    if [ ! -s "${input_file}" ]; then
        echo -e "\n${RED}错误: 空文件 ${input_file}${NC}"
        error_files+=("${input_file} [空文件]")
        ((current_file++))
        continue
    fi

    # -------------------------------
    # 步骤1: 提取COG列
    # -------------------------------
    echo -e "\n${BLUE}[1/4] 提取COG分类列...${NC}"
    sorted_file="${input_file}-COG-sorted"
    if ! grep -v "^#" "${input_file}" | awk -F '\t' '{print $7}' | sort > "${sorted_file}" 2>/dev/null; then
        echo -e "${RED}错误: 无法提取第7列数据${NC}"
        error_files+=("${input_file} [列提取失败]")
        ((current_file++))
        continue
    fi

    # -------------------------------
    # 步骤2: 统计字母频率
    # -------------------------------
    echo -e "${BLUE}[2/4] 统计COG类别分布...${NC}"
    let_file="${input_file}-COG-let"
    num_file="${input_file}-COG-num"
    rm -f "${let_file}" "${num_file}"

    # 生成字母序列
    for letter in {A..Z}; do
        echo "${letter}" >> "${let_file}"
    done

    # 统计出现次数
    total_entries=0
    for letter in {A..Z}; do
        count=$(grep -wc "${letter}" "${sorted_file}")
        echo "${count}" >> "${num_file}"
        ((total_entries+=count))
    done

    # -------------------------------
    # 步骤3: 计算总和
    # -------------------------------
    echo -e "${BLUE}[3/4] 计算统计总和...${NC}"
    echo "${total_entries}" >> "${num_file}"
    echo "sum" >> "${let_file}"

    # -------------------------------
    # 步骤4: 生成CSV文件
    # -------------------------------
    echo -e "${BLUE}[4/4] 生成最终CSV...${NC}"
    final_file="${input_file%.*}-COG-final.csv"
    paste -d ',' "${let_file}" "${num_file}" > "${final_file}"

    # 验证输出文件
    if [ -s "${final_file}" ]; then
        echo -e "生成文件: ${GREEN}${final_file}${NC}"
        success_files+=("${input_file}")
    else
        echo -e "${RED}错误: CSV文件生成失败${NC}"
        error_files+=("${input_file} [CSV生成失败]")
    fi

    # -------------------------------
    # 清理临时文件
    # -------------------------------
    rm -f "${sorted_file}" "${let_file}" "${num_file}"

    ((current_file++))
done

# ==============================================
# 最终报告
# ==============================================
echo -e "\n\n${BLUE}=== 处理结果 ===${NC}"
echo -e "成功处理文件: ${GREEN}${#success_files[@]}${NC}/${total_files}"
if [ ${#error_files[@]} -gt 0 ]; then
    echo -e "${RED}错误详情:${NC}"
    printf "  %s\n" "${error_files[@]}"
fi

exit 0