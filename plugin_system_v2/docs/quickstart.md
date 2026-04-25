# 快速开始指南

## 安装

### 1. 克隆项目

```bash
cd plugin_system_v2
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

## 运行系统

### 方式一：直接运行

```bash
python main.py
```

### 方式二：使用脚本

```bash
bash scripts/start.sh
```

### 方式三：使用 Docker

```bash
docker-compose up -d
```

## 验证安装

### 检查健康状态

```bash
curl http://localhost:8080/health
```

### 查看插件列表

```bash
curl http://localhost:8080/api/v1/plugins
```

## 基础使用

### 1. 执行单个插件

```bash
curl -X POST http://localhost:8080/api/v1/execute \
  -H "Content-Type: application/json" \
  -d '{
    "plugin": "echo_plugin",
    "data": {"message": "Hello World"}
  }'
```

### 2. 执行 sum 插件

```bash
curl -X POST http://localhost:8080/api/v1/execute \
  -H "Content-Type: application/json" \
  -d '{
    "plugin": "sum_plugin",
    "data": {"numbers": [1, 2, 3, 4, 5]}
  }'
```

### 3. 串行执行多个插件

```bash
curl -X POST http://localhost:8080/api/v1/execute/serial \
  -H "Content-Type: application/json" \
  -d '{
    "plugins": ["echo_plugin", "sum_plugin"],
    "data": {"message": "test", "numbers": [10, 20, 30]}
  }'
```

### 4. 并行执行多个插件

```bash
curl -X POST http://localhost:8080/api/v1/execute/parallel \
  -H "Content-Type: application/json" \
  -d '{
    "plugins": ["echo_plugin", "sum_plugin"],
    "data": {"message": "parallel", "numbers": [1, 2, 3]}
  }'
```

### 5. 查看统计信息

```bash
curl http://localhost:8080/api/v1/statistics
```

## 运行示例

```bash
python examples/basic_usage.py
```

## 运行测试

```bash
pytest tests/
```

## 下一步

- 阅读 [插件开发指南](docs/plugin_development.md)
- 查看 [API 参考](docs/api_reference.md)
- 了解 [架构设计](docs/architecture.md)
