# 🔍 SEO关键词研究与排名分析工具

[![Python 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ 功能特点

- 🔍 **关键词排名追踪**：自动检查您的网站在搜索引擎中的关键词排名
- 🌏 **多区域支持**：支持不同国家/地区的Google搜索（如google.com, google.com.hk）
- 📊 **竞争对手分析**：收集竞争对手的排名数据
- 📝 **详细报告**：生成Excel格式的详细分析报告
- ⚙️ **灵活配置**：支持命令行参数和配置文件两种方式设置

## 🚀 安装

### 前提条件

- Python 3.6+ 环境

### 依赖包安装

```bash
pip install requests beautifulsoup4 pandas openpyxl fake-useragent pyyaml
```

### 下载代码

```bash
git clone https://github.com/Gloridust/seo-research-tool.git
cd seo-research-tool
```

## 📖 使用方法

### 1️⃣ 通过命令行参数运行

```bash
python seo_research_tool.py --domain example.com --keywords "SEO优化,网站推广" --region com.hk
```

### 2️⃣ 通过配置文件运行

创建一个`config.yaml`文件，然后直接运行：

```bash
python seo_research_tool.py
```

## ⚙️ 配置选项

| 参数 | 命令行 | 配置文件 | 说明 | 默认值 |
|------|--------|----------|------|--------|
| 配置文件 | --config, -c | - | 配置文件路径 | config.yaml |
| 域名 | --domain, -d | domain | 要分析的目标域名 | - |
| 关键词 | --keywords, -k | keywords / keywords_list | 要分析的关键词列表 | - |
| 区域 | --region, -r | region | 搜索引擎的区域代码 | com |
| 搜索引擎 | --search-engine, -s | search_engine | 使用的搜索引擎 | google |
| 页数 | --pages, -p | pages | 要检查的搜索结果页数 | 3 |

## 🌟 使用示例

### 基本使用

```bash
# 使用默认配置文件
python seo_research_tool.py

# 香港地区搜索
python seo_research_tool.py --domain aircon88.innovisle.net --keywords "冷氣保養" --region com.hk

# 检查更多页数
python seo_research_tool.py --pages 10
```

## 📊 输出示例

工具将生成一个Excel文件，包含：
- **主要结果表**：所有关键词的排名概览
- **每个关键词的竞争对手表**：详细分析每个关键词的竞争情况

## ⚠️ 注意事项

- 🕒 请合理设置延迟时间，避免过度请求导致IP被暂时封锁
- 🔄 频繁运行脚本可能触发搜索引擎的反爬虫措施
- 🔍 搜索结果可能因地理位置、设备和个性化因素而异

---

💡 **提示**：此工具仅用于研究和分析目的，请遵守各搜索引擎的使用条款。