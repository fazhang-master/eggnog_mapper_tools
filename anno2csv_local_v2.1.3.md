# eggnog-mapper注释文件转换工具

## 功能描述
将eggnog-mapper生成的`.annotations`文件转换为标准CSV格式，保留原始列结构

## 环境要求
- Python 3.6+
- 依赖库：`pandas`

```bash
pip install pandas
```

## 使用方法

### 基本命令
```bash
python anno2csv_local_v2.1.3.py -i input_file.annotations
```

### 参数说明
| 参数 | 必选 | 说明 |
|------|------|-----|
| `-i/--input` | 是 | 输入文件路径（.annotations文件）|

### 示例
```bash
# 转换当前目录文件
python anno2csv_local_v2.1.3.py -i sample.anno

# 转换子目录文件
python anno2csv_local_v2.1.3.py -i data/sample.anno
```

### 输出说明
- 生成文件位置：与输入文件同目录
- 输出文件名：`[输入文件名].csv`
- 文件格式：UTF-8编码的CSV文件

## 版本历史
- 添加路径自动处理功能
- 优化错误提示信息
- 增加文件格式校验

## 常见问题
Q：出现`文件格式错误`提示怎么办？  
A：请确认输入文件是eggnog-mapper直接生成的原始文件，且没有手动修改过列结构

Q：如何验证转换结果？  
A：检查输出CSV的列名是否包含以下字段：  
`COG_category, KEGG_ko, GOs` 等关键注释字段