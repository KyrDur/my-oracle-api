# My Oracle

一个以六爻与东方术数为灵感的个人实验项目：用户输入所在城市和“心中所求”，系统结合当前时间、真太阳时校准和 DeepSeek，生成一份中文的结构化解读。

项目希望把传统卦理中的“世爻、动爻、月破、旬空、六神”等概念，转译成更容易理解的“人生潮汐”语言，用作自我观察和思考的辅助工具。

> 本项目仅供学习、文化研究和娱乐使用，不构成医疗、法律、投资或其他现实决策建议。

## 在线体验

项目已经部署到服务器，可以直接访问：

<http://47.101.167.181:5000/>

网页和 API 使用同一个地址，前端通过同源接口 `/api/meihua` 发起问卦请求。

## 功能

- 极简网页界面：显示当前时间、日期和问卦输入框
- 城市真太阳时校准：根据城市经度计算太阳时偏移
- DeepSeek 中文解读：输出卦象构造、人生潮汐、节律分析和典籍赠言
- 独立六爻分析引擎：`六爻.py` 内置 64 卦、黄金策规则、六神意象和事业/求财/感情分类建议
- Flask API：提供问卦接口，并支持服务器部署

## 项目结构

```text
.
├── index.html     # 前端单页
├── app.py         # Flask API 与 DeepSeek 调用
├── 六爻.py        # 独立的六爻分析引擎
├── requirements.txt
├── .env.example    # 环境变量示例
├── .gitignore
└── README.md
```

## 工作流程

```text
用户输入城市与问题
        │
        ▼
    index.html
        │ POST /api/meihua
        ▼
      app.py
        │ 计算北京时间与真太阳时
        │ 调用 DeepSeek
        ▼
    中文解读结果
```

`六爻.py` 目前是独立的本地分析模块，并未被 Flask 路由直接调用。它可以单独运行，用于测试卦象数据库和规则输出。

## 本地运行

需要 Python 3.10 或更高版本。

```bash
git clone https://github.com/KyrDur/my-oracle-api.git
cd my-oracle-api

python -m venv .venv
```

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:DEEPSEEK_API_KEY = "你的 DeepSeek API Key"
python app.py
```

macOS / Linux：

```bash
source .venv/bin/activate
pip install -r requirements.txt
export DEEPSEEK_API_KEY="你的 DeepSeek API Key"
python app.py
```

启动后访问：<http://localhost:5000>

独立运行六爻分析引擎：

```bash
python 六爻.py
```

如需测试其他问题，修改 `六爻.py` 底部 `user_input` 中的本卦、变卦、技术标签和问题类别。

## API

### `GET /`

返回 Oracle 网页首页。

### `GET /health`

健康检查接口，正常时返回：

```text
oracle backend alive
```

### `POST /api/meihua`

请求体：

```json
{
  "city": "深圳",
  "goal": "最近是否适合换工作？"
}
```

成功响应：

```json
{
  "ok": true,
  "result": "中文解读内容……",
  "solar_time": "14:32"
}
```

当前支持的城市经度包括深圳、合肥、北京和上海；其他城市会使用默认经度 `120.0` 进行近似计算。

## 线上服务

当前线上服务地址：

- 首页：<http://47.101.167.181:5000/>
- 问卦接口：`POST http://47.101.167.181:5000/api/meihua`

服务器启动命令：

```bash
gunicorn app:app
```

`app.py` 会读取环境变量 `PORT`；未设置时默认使用 `5000`。

## 安全注意事项

API Key 通过 `DEEPSEEK_API_KEY` 环境变量读取，不会写入源码。公开仓库前仍建议立即轮换曾经出现在公开历史或日志中的旧 Key。

同时建议：

- 不要把 API Key 写入 Git、前端代码或截图
- 为 API 增加鉴权、频率限制和请求长度限制
- 生产环境中收紧 CORS 来源，不要长期使用通配符 `*`

## 当前限制

- 前端农历与干支展示目前使用固定示例文本，尚未根据当前日期动态计算
- 真太阳时只按有限城市经度表进行近似校准
- `/api/meihua` 当前主要调用大模型生成解读，并不会自动完成完整的传统起卦流程
- `六爻.py` 的 64 卦数据和规则适合实验演示，不能替代严谨的历法、排盘和传统术数校验

## License

当前仓库未单独声明开源许可证。如需公开复用，建议补充合适的 LICENSE 文件。
