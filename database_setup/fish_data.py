import mysql.connector
import os
import csv
from config import DB_CONFIG  # 从 config.py 导入数据库配置

# 数据库连接配置
db_config = DB_CONFIG
# 鱼类信息路径
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "Fish.csv")

def add_fish_data() :
    # 连接数据库
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # 插入语句
    insert_query = """
    INSERT INTO fish (species, weight, length1, length2, length3, height, width)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    # 读取CSV文件并插入数据
    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # 跳过标题行
        for row in csvreader:
            cursor.execute(insert_query, row)

    print('插入数据完毕')
    # 关闭连接
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    add_fish_data()