import pandas as pd

# 读取 CSV 文件
file_path = "data/Fish.csv" 
data = pd.read_csv(file_path)

# 获取 Species 列的唯一值
unique_species = data['Species'].unique()

# 打印不同的值及其数量
print(f"Species 列中有 {len(unique_species)} 个不同的值：")
print(unique_species)