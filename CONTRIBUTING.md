# Contributing to Plugin Execution System

感谢你对本项目的关注！我们欢迎任何形式的贡献。

## 📋 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [开发流程](#开发流程)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [测试要求](#测试要求)
- [文档贡献](#文档贡献)

## 行为准则

参与本项目即表示你同意遵守我们的行为准则：

- 尊重所有贡献者
- 接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表现出同理心

## 如何贡献

### 报告 Bug

如果你发现了 bug，请创建一个 Issue 并包含以下信息：

- **清晰的标题**：简要描述问题
- **复现步骤**：详细的复现步骤
- **期望行为**：你期望发生什么
- **实际行为**：实际发生了什么
- **环境信息**：
  - 操作系统
  - Python 版本
  - 项目版本
- **相关日志**：错误日志或堆栈跟踪
- **截图**（如适用）

### 提出新特性

如果你有新特性的想法：

1. 先检查 [Issues](https://github.com/yourusername/plugin-execution-system/issues) 是否已有类似建议
2. 创建一个 Feature Request Issue
3. 描述特性的用途和价值
4. 如果可能，提供实现思路

### 提交代码

1. **Fork 仓库**
2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```
3. **进行修改**
4. **编写测试**
5. **运行测试**
6. **提交代码**
7. **推送到你的 Fork**
8. **创建 Pull Request**

## 开发流程

### 1. 设置开发环境

```bash
# 克隆你的 fork
git clone https://github.com/your-username/plugin-execution-system.git
cd plugin-execution-system

# 添加上游仓库
git remote add upstream https://github.com/original-owner/plugin-execution-system.git

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
cd v2
pip install -r requirements.txt
```

### 2. 保持同步

```bash
# 获取上游更新
git fetch upstream
git checkout main
git merge upstream/main
```

### 3. 开发新特性

```bash
# 创建特性分支
git checkout -b feature/my-new-feature

# 进行开发
# ... 编写代码 ...

# 运行测试
pytest tests/

# 代码格式化
black .
flake8 .

# 提交更改
git add .
git commit -m "feat: add my new feature"

# 推送到你的 fork
git push origin feature/my-new-feature
```

### 4. 创建 Pull Request

- 在 GitHub 上创建 Pull Request
- 填写 PR 模板
- 等待代码审查
- 根据反馈进行修改

## 代码规范

### Python 代码风格

我们遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 规范：

- 使用 4 个空格缩进
- 行长度不超过 88 字符（Black 默认）
- 使用有意义的变量名
- 添加必要的注释和文档字符串

### 代码格式化工具

```bash
# 使用 Black 格式化代码
black .

# 使用 flake8 检查代码
flake8 .

# 使用 mypy 进行类型检查
mypy .
```

### 命名规范

- **类名**：使用 PascalCase（如 `PluginManager`）
- **函数/方法名**：使用 snake_case（如 `load_plugin`）
- **常量**：使用 UPPER_SNAKE_CASE（如 `MAX_RETRY_COUNT`）
- **私有成员**：使用前导下划线（如 `_internal_method`）

### 文档字符串

使用 Google 风格的文档字符串：

```python
def load_plugin(plugin_name: str, config: dict) -> Plugin:
    """加载指定的插件。

    Args:
        plugin_name: 插件名称
        config: 插件配置字典

    Returns:
        加载的插件实例

    Raises:
        PluginNotFoundError: 当插件不存在时
        PluginLoadError: 当插件加载失败时
    """
    pass
```

## 提交规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

### 提交消息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型

- `feat`: 新特性
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响代码运行）
- `refactor`: 重构（既不是新特性也不是 bug 修复）
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

### 示例

```bash
# 新特性
git commit -m "feat(plugin): add hot reload support"

# Bug 修复
git commit -m "fix(loader): resolve memory leak in plugin loading"

# 文档更新
git commit -m "docs(readme): update installation instructions"

# 重构
git commit -m "refactor(executor): simplify error handling logic"
```

## 测试要求

### 编写测试

- 所有新特性必须包含测试
- Bug 修复应包含回归测试
- 测试覆盖率应保持在 80% 以上

### 测试结构

```python
import pytest
from core.management.loader import PluginLoader

class TestPluginLoader:
    def setup_method(self):
        """每个测试方法前执行"""
        self.loader = PluginLoader()
    
    def test_load_valid_plugin(self):
        """测试加载有效插件"""
        plugin = self.loader.load("echo_plugin")
        assert plugin is not None
        assert plugin.metadata().name == "echo_plugin"
    
    def test_load_invalid_plugin(self):
        """测试加载无效插件"""
        with pytest.raises(PluginNotFoundError):
            self.loader.load("nonexistent_plugin")
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_loader.py

# 运行特定测试
pytest tests/test_loader.py::TestPluginLoader::test_load_valid_plugin

# 生成覆盖率报告
pytest --cov=core --cov-report=html
```

## 文档贡献

### 文档类型

- **代码文档**：函数/类的文档字符串
- **用户文档**：README、使用指南
- **开发文档**：架构设计、API 参考
- **示例代码**：演示如何使用

### 文档规范

- 使用清晰简洁的语言
- 提供代码示例
- 保持文档与代码同步
- 使用 Markdown 格式

### 文档结构

```
docs/
├── design/              # 设计文档
├── architecture.md      # 架构设计
├── plugin-development.md # 插件开发指南
├── api-reference.md    # API 参考
└── deployment.md       # 部署指南
```

## Pull Request 检查清单

提交 PR 前，请确保：

- [ ] 代码遵循项目的代码规范
- [ ] 所有测试通过
- [ ] 添加了必要的测试
- [ ] 更新了相关文档
- [ ] 提交消息符合规范
- [ ] 没有合并冲突
- [ ] PR 描述清晰完整

## PR 模板

```markdown
## 描述
简要描述这个 PR 的目的

## 变更类型
- [ ] Bug 修复
- [ ] 新特性
- [ ] 重构
- [ ] 文档更新
- [ ] 其他

## 相关 Issue
Closes #(issue number)

## 测试
描述你如何测试这些变更

## 截图（如适用）

## 检查清单
- [ ] 代码遵循项目规范
- [ ] 测试通过
- [ ] 文档已更新
```

## 代码审查

### 审查者指南

- 检查代码质量和规范
- 验证测试覆盖率
- 确认文档完整性
- 提供建设性反馈

### 被审查者指南

- 及时响应审查意见
- 虚心接受建议
- 解释设计决策
- 更新代码和文档

## 发布流程

1. 更新版本号（遵循语义化版本）
2. 更新 CHANGELOG.md
3. 创建 Git tag
4. 发布到 PyPI（如适用）
5. 创建 GitHub Release

## 获取帮助

如果你有任何问题：

- 查看 [文档](docs/)
- 搜索 [Issues](https://github.com/yourusername/plugin-execution-system/issues)
- 创建新的 Issue
- 发送邮件至 qiuqiuqiumao@qq.com

## 致谢

感谢所有贡献者的付出！

---

再次感谢你的贡献！🎉
