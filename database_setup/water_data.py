import mysql.connector
import os
import csv
from datetime import datetime
# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '596289',
    'database': 'smart_ocean_ranch'
}
# 水质信息路径
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "water", "water_quality_by_name", "黑龙江省","松花江流域","858九队","2021-04","858九队.csv")

def add_water_data() :
    # 连接数据库
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # 插入语句
    insert_query = """
        INSERT INTO water_data (
            province, river_basin, section_name, monitoring_time, water_quality_category,
            temperature, ph, dissolved_oxygen, conductivity, turbidity, permanganate_index,
            ammonia_nitrogen, total_phosphorus, total_nitrogen, chlorophyll_a, algae_density, station_status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

    # 读取CSV文件并插入数据
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # 跳过标题行
        for row in csvreader:
            # 替换空字符串或特殊值（如 *）为 None，以便在数据库中存储为 NULL
            row = [None if cell == '*' or cell == '' or cell == "--" else cell for cell in row]

            # 转换日期时间格式
            if row[3]:  # 假设日期时间在第4列（索引3）
                try:
                    # 将 '04-01 08:00' 转换为 '2023-04-01 08:00:00'
                    row[3] = datetime.strptime(row[3], '%m-%d %H:%M').replace(year=datetime.now().year).strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    print(f"日期时间格式错误: {row[3]}")
                    row[3] = None  # 如果格式不正确，设置为 None

            cursor.execute(insert_query, row)

    print('插入数据完毕')
    # 提交事务并关闭连接
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    add_water_data()