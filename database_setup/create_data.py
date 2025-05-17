from faker import Faker
import mysql.connector
import random

def insert_fake_data():
    # 初始化 Faker
    fake = Faker()
    
    # 传感器类型列表
    SENSOR_TYPES = ['temperature', 'salinity', 'ph', 'oxygen', 'current']
    
    try:
        # 连接到数据库
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="596289",
            database="smart_ocean_ranch"
        )
        cursor = connection.cursor()

        # 1. 插入用户数据 (使用整合后的users表)
        print("正在生成用户数据...")
        
        # 插入10个普通用户
        for _ in range(10):
            username = fake.unique.user_name()
            password = fake.password(length=10)
            email = fake.unique.email()
            role = 'user'
            
            cursor.execute("""
                INSERT INTO users (username, password, email, role)
                VALUES (%s, %s, %s, %s)
            """, (username, password, email, role))

        # 插入2个管理员用户
        for _ in range(2):
            username = fake.unique.user_name()
            password = fake.password(length=12)
            email = fake.unique.email()
            role = 'admin'
            
            cursor.execute("""
                INSERT INTO users (username, password, email, role)
                VALUES (%s, %s, %s, %s)
            """, (username, password, email, role))

        print(f"成功插入12个用户(10普通用户+2管理员)")

        # 2. 插入传感器数据
        print("\n正在生成传感器数据...")
        
        # 插入15个传感器
        sensor_ids = []
        for i in range(1, 16):
            name = f"{random.choice(SENSOR_TYPES)}_sensor_{i}"
            sensor_type = random.choice(SENSOR_TYPES)
            location = f"Area_{chr(65 + random.randint(0, 3))}-{random.randint(1, 5)}"
            status = random.choice(['active', 'active', 'active', 'inactive', 'maintenance'])
            
            cursor.execute("""
                INSERT INTO sensors (name, type, location, status)
                VALUES (%s, %s, %s, %s)
            """, (name, sensor_type, location, status))
            
            # 获取最后插入的ID
            cursor.execute("SELECT LAST_INSERT_ID()")
            sensor_id = cursor.fetchone()[0]
            sensor_ids.append(sensor_id)
        
        print(f"成功插入15个传感器")

        # 3. 插入传感器读数数据
        print("\n正在生成传感器读数数据...")
        
        # 为每个传感器生成10-20条读数记录
        record_count = 0
        for sensor_id in sensor_ids:
            records = random.randint(10, 20)
            for _ in range(records):
                # 根据传感器类型生成合理的随机值
                sensor_type = None
                cursor.execute("SELECT type FROM sensors WHERE id = %s", (sensor_id,))
                sensor_type = cursor.fetchone()[0]
                
                if sensor_type == 'temperature':
                    value = round(random.uniform(10, 30), 2)  # 10-30°C
                elif sensor_type == 'salinity':
                    value = round(random.uniform(30, 40), 2)  # 30-40 ppt
                elif sensor_type == 'ph':
                    value = round(random.uniform(6.5, 8.5), 2)  # pH值
                elif sensor_type == 'oxygen':
                    value = round(random.uniform(2, 10), 2)  # mg/L
                else:  # current
                    value = round(random.uniform(0, 2.5), 2)  # m/s
                
                cursor.execute("""
                    INSERT INTO sensor_data (sensor_id, value)
                    VALUES (%s, %s)
                """, (sensor_id, value))
                record_count += 1
        
        print(f"成功插入{record_count}条传感器读数记录")

        # 提交所有更改
        connection.commit()
        print("\n所有数据已成功插入并提交!")

    except mysql.connector.Error as err:
        print(f"数据库操作失败: {err}")
        if connection.is_connected():
            connection.rollback()
    finally:
        # 关闭连接
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("数据库连接已关闭。")

if __name__ == "__main__":
    insert_fake_data()