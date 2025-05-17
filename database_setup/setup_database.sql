-- 创建数据库
CREATE DATABASE IF NOT EXISTS smart_ocean_ranch 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE smart_ocean_ranch;

-- 创建用户表（整合普通用户和管理员）
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL COMMENT '存储明文密码（仅用于开发测试）',
    role ENUM('user', 'admin') NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建传感器表
CREATE TABLE IF NOT EXISTS sensors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL COMMENT '传感器类型',
    location VARCHAR(255) COMMENT '传感器位置描述',
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建传感器数据表
CREATE TABLE IF NOT EXISTS sensor_data (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    sensor_id INT NOT NULL,
    value DECIMAL(10,4) NOT NULL,
    recorded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE CASCADE,
    INDEX idx_sensor_id (sensor_id),
    INDEX idx_recorded_at (recorded_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建鱼类信息表
CREATE TABLE fish (
    id INT PRIMARY KEY AUTO_INCREMENT,              -- 主键
    species VARCHAR(50) NOT NULL,                   -- 种类
    weight FLOAT NOT NULL,                          -- 体重（g）
    length1 FLOAT NOT NULL,                         -- 体长-1（cm）
    length2 FLOAT NOT NULL,                         -- 体长-2（cm）
    length3 FLOAT NOT NULL,                         -- 体长-3（cm）
    height FLOAT NOT NULL,                          -- 高度（cm）
    width FLOAT NOT NULL,                           -- 宽度（cm）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_species (species)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建水质信息表
CREATE TABLE water_data (
    id INT PRIMARY KEY AUTO_INCREMENT,              -- 主键
    province VARCHAR(50) NOT NULL,                  -- 省份
    river_basin VARCHAR(50) NOT NULL,               -- 流域
    section_name VARCHAR(100) NOT NULL,             -- 断面名称
    monitoring_time DATETIME NOT NULL,              -- 监测时间
    water_quality_category VARCHAR(10) ,    -- 水质类别
    temperature FLOAT,                              -- 水温(℃)
    ph FLOAT,                                       -- pH(无量纲)
    dissolved_oxygen FLOAT,                         -- 溶解氧(mg/L)
    conductivity FLOAT,                             -- 电导率(μS/cm)
    turbidity FLOAT,                                -- 浊度(NTU)
    permanganate_index FLOAT,                       -- 高锰酸盐指数(mg/L)
    ammonia_nitrogen FLOAT,                         -- 氨氮(mg/L)
    total_phosphorus FLOAT,                         -- 总磷(mg/L)
    total_nitrogen FLOAT,                           -- 总氮(mg/L)
    chlorophyll_a FLOAT,                            -- 叶绿素α(mg/L)
    algae_density FLOAT,                            -- 藻密度(cells/L)
    station_status VARCHAR(50),                     -- 站点情况
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 创建时间
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新时间
    INDEX idx_province (province),                  -- 索引：省份
    INDEX idx_river_basin (river_basin),            -- 索引：流域
    INDEX idx_section_name (section_name)           -- 索引：断面名称
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 初始管理员账户（明文密码，仅用于开发）
INSERT INTO users (username, email, password, role) 
VALUES ('admin', 'admin@oceanranch.com', 'admin123', 'admin');

-- 初始普通用户账户
INSERT INTO users (username, email, password, role) 
VALUES ('user1', 'user1@oceanranch.com', 'user123', 'user');

-- 初始传感器数据
INSERT INTO sensors (name, type, location) VALUES
('温度传感器1', 'temperature', '东区养殖场A区'),
('盐度传感器1', 'salinity', '东区养殖场B区');

-- 初始传感器读数
INSERT INTO sensor_data (sensor_id, value) VALUES
(1, 25.5),
(1, 26.0),
(2, 33.2);