# extract_COG_local_v2.1.3 使用文档

## 工具概述
本脚本用于自动化处理 ​**eggNOG-mapper** 生成的注释文件（`.emapper.annotations`），提取 ​**COG 功能分类**信息并生成统计报表。支持批量处理、进度可视化及健壮的错误检测。

---

## 主要功能
- ✅ ​**多文件批量处理**：支持通过 `-i` 参数指定多个输入文件
- ✅ ​**智能进度提示**：实时显示进度条和分步处理状态
- ✅ ​**错误自动捕获**：检测文件缺失、空文件、格式错误等异常
- ✅ ​**统计结果验证**：自动计算COG条目总数并校验数据完整性
- ✅ ​**跨平台兼容**：支持Linux/macOS系统（需Bash 4.0+）

---

## 系统要求
### 必需组件
- **Bash 4.0+** (检查命令: `bash --version`)
- 基础工具: `grep` `awk` `sort` `paste`

### 推荐环境
- 终端支持ANSI颜色代码（如VS Code终端、iTerm2）
- 屏幕宽度 ≥ 80字符

---

## 快速开始

### 1. 下载脚本
```bash
wget https://example.com/path/to/extract_COG_local_v2.1.sh
chmod +x extract_COG_local_v2.1.sh
```

### 2. 基本使用
```bash
# 处理单个文件
./extract_COG_local_v2.1.sh -i input.emapper.annotations

# 处理多个文件
./extract_COG_local_v2.1.sh -i file1.anno -i file2.anno
```

### 3. 查看结果
输出文件与输入文件同目录，命名格式：
`[输入文件名]-COG-final.csv`

## 参数说明
| 参数 | 必选 | 说明                       |
| ---- | ---- | -------------------------- |
| -i   | 是   | 输入文件路径（可多次使用） |
| -h   | 否   | 显示帮助信息               |

## 输出文件示例

| A    | 12   |
| ---- | ---- |
| B    | 8    |
| C    | 25   |
| ...  | ...  |
| sum  | 356  |

- 第1列: COG功能类别（A-Z字母）

- 第2列: 对应类别的基因数量
- 最后一行: 总基因数统计