import os

# 停用词文件所在的目录
directory = 'stopwords'

# 合并后的停用词文件
output_file = 'merged_stopwords.txt'

# 使用集合来存储停用词，以避免重复
stopwords_set = set()

# 遍历目录中的所有文件
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                # 去除前后空白字符，并添加到集合中
                stopword = line.strip()
                if stopword:
                    stopwords_set.add(stopword)

# 将集合中的停用词写入输出文件
with open(output_file, 'w', encoding='utf-8') as file:
    for stopword in sorted(stopwords_set):
        file.write(stopword + '\n')

print(f'停用词已合并到 {output_file}')
