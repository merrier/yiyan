# yiyan (一言)

这是一个用于爬取“一句话”（名言、语录等）数据的爬虫项目，抓取的数据最终会以 JSON 格式保存。

## 项目结构

- `data/`：存放抓取下来的 JSON 数据文件。
- `src/`：爬虫核心源代码。
  - `config.py`：配置文件（URL、Headers、保存路径等）。
  - `scraper.py`：负责发送网络请求，获取网页/API数据。
  - `parser.py`：负责解析网页结构或 JSON 数据，提取所需的句子信息。
  - `storage.py`：负责将数据格式化并追加保存到 JSON 文件中。
- `main.py`：程序入口，串联抓取、解析、保存流程。
- `requirements.txt`：项目依赖（如 `requests`、`beautifulsoup4`）。

## 快速开始

1. 创建并激活虚拟环境（推荐）：
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # 或者 venv\Scripts\activate  # Windows
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 运行爬虫：
   ```bash
   python main.py
   ```

## 自定义开发
- 如果需要更改目标网站，请修改 `src/config.py` 中的 `TARGET_URL`。
- 如果目标网站返回的是 HTML，请修改 `src/parser.py` 并使用 BeautifulSoup 提取 DOM 中的文本内容。
