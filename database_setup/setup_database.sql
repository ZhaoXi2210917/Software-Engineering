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