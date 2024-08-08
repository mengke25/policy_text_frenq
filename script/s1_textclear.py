import os
from docx import Document
import pandas as pd
import numpy as np
import jieba
from func_citycode import citycode  # 导入 citycode 函数
from func_provcode import provcode  # 导入 provcode 函数


######################################################################################################

# 输入的关键词列表
keywords = ["数据跨境", "数据流动", "数据共享"]

######################################################################################################

# 定义文件路径
base_path = "……………………"
pool_path = os.path.join(base_path, "pool")
output_path = os.path.join(base_path, "output", "policy_list.xlsx")
stopword_path = os.path.join(base_path, "files", "stopword.txt")
custom_dict_path = os.path.join(base_path, "files", "custom.txt")

# 加载自定义词典和停用词
jieba.load_userdict(custom_dict_path)

with open(stopword_path, 'r', encoding='utf-8') as f:
    stopwords = set(f.read().strip().split())

def clean_text(text):
    # 移除无效字符
    return ''.join(char for char in text if char.isprintable() and char not in {'\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', '\x0b', '\x0c', '\x0e', '\x0f', '\x10', '\x11', '\x12', '\x13', '\x14', '\x15', '\x16', '\x17', '\x18', '\x19', '\x1a', '\x1b', '\x1c', '\x1d', '\x1e', '\x1f'})

def extract_year_from_text(text):
    for i in range(len(text) - 3):
        year = text[i:i+4]
        if year.isdigit() and 2010 <= int(year) <= 2025:
            return year
    return None

def extract_year_from_filename(filename):
    year = extract_year_from_text(filename)
    return year

# 步骤一：将txt文件转换为docx文件
txt_files = [f for f in os.listdir(pool_path) if f.endswith('.txt')]
for i, file_name in enumerate(txt_files, start=1):
    txt_path = os.path.join(pool_path, file_name)
    docx_path = txt_path.replace('.txt', '.docx')

    if not os.path.exists(docx_path):
        with open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 清理内容
        content = clean_text(content)

        doc = Document()
        doc.add_paragraph(content)
        doc.save(docx_path)
        print(f"正在转化txt文件 {i}/{len(txt_files)} 已完成 {i/len(txt_files)*100:.2f}%")
    else:
        print(f"跳过已存在的docx文件: {docx_path}")

# 打印输入的关键词信息
print(f"共输入{len(keywords)}个关键词，分别是{keywords}，开始提取")

# 步骤二：分析docx文件并生成Excel文件
data = []
docx_files = [f for f in os.listdir(pool_path) if f.endswith('.docx')]

for i, file_name in enumerate(docx_files, start=1):
    docx_path = os.path.join(pool_path, file_name)
    doc = Document(docx_path)
    content = "\n".join([para.text for para in doc.paragraphs])

    # 从文件名提取年份
    year = extract_year_from_filename(file_name)
    if not year:
        # 从内容中提取年份
        year = extract_year_from_text(content)

    # 计算总词数（排除停用词）
    words = jieba.lcut(content)
    words_filtered = [word for word in words if word not in stopwords]
    total_word_count = len(words_filtered)

    # 计算关键词出现频次
    keyword_counts = {kw: content.count(kw) for kw in keywords}

    # 添加到数据列表
    data.append([
        file_name,
        year,
        total_word_count,
        *keyword_counts.values()
    ])
    print(f"正在处理docx文件 {i}/{len(docx_files)} 已完成 {i/len(docx_files)*100:.2f}%")

# 创建DataFrame
columns = ["文件名", "年份", "总词数"] + keywords
df = pd.DataFrame(data, columns=columns)

# 初始化 citycode 和 provcode 列
df['citycode'] = 0
df['provcode'] = 0

# 备份 citycode 和 provcode 修改前的值
original_citycode = df['citycode'].copy()
original_provcode = df['provcode'].copy()

# 调用 citycode 函数
df = citycode(df, '文件名')

# 判断 citycode 是否发生变化
df['地级市层面'] = df.apply(lambda row: '地级市层面' if row['citycode'] != original_citycode[row.name] else '', axis=1)

# 调用 provcode 函数
df = provcode(df, '文件名')

# 判断 provcode 是否发生变化
df['省份层面'] = df.apply(lambda row: '省份层面' if row['provcode'] != original_provcode[row.name] else '', axis=1)

# 生成新的"政策级别"列
df['政策级别'] = df.apply(
    lambda row: '地级市层面' if row['地级市层面'] else ('省份层面' if row['省份层面'] else ''),
    axis=1
)

#df['citycode'].replace(0, np.nan, inplace=True)
#df['provcode'].replace(0, np.nan, inplace=True)
df['citycode'] = df['citycode'].replace(0, np.nan)
df['provcode'] = df['provcode'].replace(0, np.nan)


# 删除第{len(keywords)+6}列和第{len(keywords)+7}列
del df[df.columns[len(keywords) + 5]]
del df[df.columns[len(keywords) + 5]]

# Convert 'provcode' to string type to avoid dtype warnings
df['provcode'] = df['provcode'].astype(str)

# Iterate over rows and update 'provcode' based on 'citycode'
for index, row in df.iterrows():
    if pd.isna(row['provcode']) or row['provcode'] == 'nan':
        citycode_str = str(row['citycode'])
        if citycode_str and len(citycode_str) >= 2:
            df.at[index, 'provcode'] = citycode_str[:2] + '0000'


# 保存到Excel文件
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_excel(output_path, index=False)

print(f"分析结果已保存到 {output_path}")
