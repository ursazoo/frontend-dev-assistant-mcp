-- MCP Analytics 数据库初始化脚本
-- 创建数据库表结构和索引

-- 设置时区
SET timezone = 'UTC';

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    uuid VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    department VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建使用日志表
CREATE TABLE IF NOT EXISTS usage_logs (
    id SERIAL PRIMARY KEY,
    user_uuid VARCHAR(36) NOT NULL,
    tool_name VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    arguments JSONB,
    FOREIGN KEY (user_uuid) REFERENCES users(uuid) ON DELETE CASCADE
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_department ON users(department);
CREATE INDEX IF NOT EXISTS idx_usage_logs_user_uuid ON usage_logs(user_uuid);
CREATE INDEX IF NOT EXISTS idx_usage_logs_timestamp ON usage_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_usage_logs_tool_name ON usage_logs(tool_name);
CREATE INDEX IF NOT EXISTS idx_usage_logs_user_tool ON usage_logs(user_uuid, tool_name);

-- 创建复合索引用于常见查询
CREATE INDEX IF NOT EXISTS idx_usage_logs_user_time ON usage_logs(user_uuid, timestamp DESC);

-- 插入一些示例数据（可选，用于测试）
INSERT INTO users (uuid, email, name, department) VALUES 
    ('test-uuid-1', 'test@example.com', 'Test User', 'Development')
ON CONFLICT (uuid) DO NOTHING;

-- 设置数据库配置
ALTER DATABASE mcp_analytics SET timezone TO 'UTC';

-- 打印初始化完成信息
DO $$
BEGIN
    RAISE NOTICE '✅ MCP Analytics 数据库初始化完成';
    RAISE NOTICE '📊 用户表: %', (SELECT COUNT(*) FROM users);
    RAISE NOTICE '📝 使用日志表结构已创建';
END $$;