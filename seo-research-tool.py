import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from urllib.parse import quote_plus
import argparse
import logging
import json
import yaml
import os
from fake_useragent import UserAgent
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import platform

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("seo_research.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SEOResearchTool:
    def __init__(self, target_domain, delay_min=0.5, delay_max=1.5, region='com', use_browser=False):
        """
        初始化SEO研究工具
        
        参数:
            target_domain (str): 需要跟踪排名的网站域名
            delay_min (int): 请求之间的最小延迟(秒)
            delay_max (int): 请求之间的最大延迟(秒)
            region (str): Google搜索的区域(例如: 'com', 'com.hk', 'co.jp')
            use_browser (bool): 是否使用浏览器模式
        """
        self.target_domain = target_domain
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.region = region
        self.ua = UserAgent()
        self.results = []
        self.use_browser = use_browser
        self.driver = None
        
        if self.use_browser:
            self._init_browser()
    
    def _init_browser(self):
        """初始化浏览器"""
        try:
            options = uc.ChromeOptions()
            options.add_argument('--lang=zh-CN,zh;q=0.9,en;q=0.8')
            options.add_argument(f'--user-agent={self.ua.random}')
            
            # 添加更多的浏览器参数
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-infobars')
            options.add_argument('--disable-browser-side-navigation')
            options.add_argument('--disable-features=IsolateOrigins,site-per-process')
            
            # 随机设置窗口大小
            viewports = ["1280x800", "1366x768", "1440x900", "1536x864", "1680x1050", "1920x1080"]
            viewport = random.choice(viewports)
            width, height = map(int, viewport.split('x'))
            options.add_argument(f'--window-size={width},{height}')
            
            # 设置代理（如果需要）
            # options.add_argument('--proxy-server=http://your-proxy-server')
            
            self.driver = uc.Chrome(options=options)
            
            # 执行反自动化检测的JavaScript代码
            self.driver.execute_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['zh-CN', 'zh', 'en-US', 'en']
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
            """)
            
            logger.info("浏览器初始化成功")
        except Exception as e:
            logger.error(f"浏览器初始化失败: {str(e)}")
            self.use_browser = False
    
    def get_random_headers(self):
        """生成随机请求头以模拟不同浏览器"""
        ua = self.ua.random
        # 随机生成 viewport 尺寸
        viewports = [
            "1280x800", "1366x768", "1440x900", "1536x864", "1680x1050", "1920x1080"
        ]
        viewport = random.choice(viewports)
        width, height = map(int, viewport.split('x'))
        
        # 随机选择平台
        platforms = ['Windows', 'Macintosh', 'X11']
        platform = random.choice(platforms)
        
        # 随机选择Chrome版本
        chrome_versions = ['112', '113', '114', '115', '116', '117']
        chrome_version = random.choice(chrome_versions)

        headers = {
            'User-Agent': ua,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,zh-HK;q=0.6,ja;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': f'"Google Chrome";v="{chrome_version}", "Chromium";v="{chrome_version}", "Not=A?Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': f'"{platform}"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Pragma': 'no-cache',
            'Priority': 'u=0, i',
            'DNT': '1',
            'Viewport-Width': str(width),
            'Device-Memory': f'{random.choice([4, 8, 16])}',
            'Referer': 'https://www.google.com/',
            'Cookie': f'1P_JAR=2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}-{random.randint(0,23):02d}; NID={random.randint(100000000,999999999)}; DV={"".join([str(random.randint(0,9)) for _ in range(20)])}',
        }
        
        # 随机添加额外的现代浏览器特征
        if random.random() > 0.5:
            headers.update({
                'Sec-Ch-Ua-Full-Version': f'"{chrome_version}.0.{random.randint(1000,9999)}.{random.randint(100,999)}"',
                'Sec-Ch-Ua-Arch': random.choice(['"x86"', '"arm"']),
                'Sec-Ch-Ua-Model': '""',
                'Sec-Ch-Ua-Bitness': random.choice(['"64"', '"32"']),
                'Sec-Ch-Ua-Full-Version-List': f'"Google Chrome";v="{chrome_version}.0.{random.randint(1000,9999)}.{random.randint(100,999)}", "Chromium";v="{chrome_version}.0.{random.randint(1000,9999)}.{random.randint(100,999)}", "Not=A?Brand";v="99.0.0.0"',
            })
        
        return headers
    
    def _get_page_with_browser(self, url):
        """使用浏览器获取页面内容"""
        try:
            self.driver.get(url)
            # 等待搜索结果加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class*="g"]'))
            )
            return self.driver.page_source
        except Exception as e:
            logger.error(f"浏览器获取页面失败: {str(e)}")
            return None

    def _simulate_user_browsing(self, url):
        """模拟用户浏览行为"""
        try:
            if not self.use_browser:
                logger.info("需要启用浏览器模式才能模拟用户浏览行为")
                return

            logger.info(f"模拟用户点击并浏览: {url}")
            
            # 保存当前窗口句柄
            original_window = self.driver.current_window_handle
            
            # 打开新标签页
            self.driver.execute_script(f"window.open('{url}', '_blank');")
            
            # 切换到新标签页
            self.driver.switch_to.window(self.driver.window_handles[-1])
            
            # 模拟用户浏览行为
            total_height = int(self.driver.execute_script("return document.body.scrollHeight"))
            for i in range(0, total_height, 100):
                self.driver.execute_script(f"window.scrollTo(0, {i});")
                time.sleep(random.uniform(0.1, 0.3))
            
            # 在页面停留随机时间（15-30秒）
            time.sleep(random.uniform(5, 10))
            
            # 关闭当前标签页并切回原标签页
            self.driver.close()
            self.driver.switch_to.window(original_window)
            
        except Exception as e:
            logger.error(f"模拟用户浏览时出错: {str(e)}")
            # 确保切回原始窗口
            try:
                self.driver.switch_to.window(original_window)
            except:
                pass

    def search_keyword(self, keyword, search_engine="google", num_pages=8):
        """
        搜索关键词并分析结果
        
        参数:
            keyword (str): 要搜索的关键词
            search_engine (str): 使用的搜索引擎 ("google", "bing")
            num_pages (int): 要分析的搜索结果页数
        
        返回:
            dict: 包含排名信息的字典
        """
        keyword_data = {
            'keyword': keyword,
            'found': False,
            'rank': None,
            'page': None,
            'url': None,
            'competitors': []
        }
        
        logger.info(f"搜索关键词: '{keyword}'")
        
        for page in range(1, num_pages + 1):
            # 根据搜索引擎构建URL
            if search_engine == "google":
                # 谷歌搜索的起始结果索引是(page-1)*10
                start_index = (page - 1) * 10
                search_url = f"https://www.google.{self.region}/search?q={quote_plus(keyword)}&start={start_index}&hl=zh-CN"
            elif search_engine == "bing":
                # 必应搜索的页码参数
                search_url = f"https://www.bing.com/search?q={quote_plus(keyword)}&first={(page-1)*10+1}"
            else:
                logger.error(f"不支持的搜索引擎: {search_engine}")
                return keyword_data
            
            try:
                logger.info(f"请求页面 {page}: {search_url}")
                
                if self.use_browser:
                    html_content = self._get_page_with_browser(search_url)
                    if not html_content:
                        continue
                else:
                    response = requests.get(search_url, headers=self.get_random_headers(), timeout=10)
                    if response.status_code != 200:
                        logger.warning(f"请求失败，状态码: {response.status_code}")
                        continue
                    html_content = response.text
                
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # 解析搜索结果
                if search_engine == "google":
                    # 更新选择器以适应Google的新HTML结构
                    search_results = soup.select('div[class*="g"]')
                    if not search_results:
                        # 备用选择器
                        search_results = soup.select('div[data-hveid]')
                        if not search_results:
                            # 第二备用选择器
                            search_results = soup.select('div.MjjYud')
                    
                    if not search_results:
                        logger.warning(f"页面 {page} 未找到搜索结果")
                        continue
                    
                    for index, result in enumerate(search_results):
                        # 提取链接和标题
                        link_element = result.select_one('a[href]')
                        if not link_element:
                            continue
                            
                        link = link_element.get('href', '')
                        
                        # 有时Google会在URL前添加/url?q=
                        if link.startswith('/url?q='):
                            link = link.split('/url?q=')[1].split('&')[0]
                        
                        # 提取标题
                        title_element = result.select_one('h3')
                        title = title_element.get_text() if title_element else "无标题"
                        
                        # 计算实际排名
                        rank = index + 1 + (page - 1) * 10
                        
                        # 检查是否是目标网站
                        if self.target_domain in link:
                            keyword_data['found'] = True
                            keyword_data['rank'] = rank
                            keyword_data['page'] = page
                            keyword_data['url'] = link
                            logger.info(f"在结果中找到目标网站: 排名 #{rank}, 页面 #{page}, URL: {link}")
                            
                            # 模拟用户点击和浏览行为
                            if self.use_browser:
                                self._simulate_user_browsing(link)
                        
                        # 收集竞争对手数据
                        if not self.target_domain in link:
                            keyword_data['competitors'].append({
                                'rank': rank,
                                'title': title,
                                'url': link
                            })
                elif search_engine == "bing":
                    # 必应搜索结果解析逻辑
                    search_results = soup.select('li.b_algo')
                    
                    for index, result in enumerate(search_results):
                        link_element = result.select_one('a')
                        if not link_element:
                            continue
                            
                        link = link_element.get('href', '')
                        
                        # 提取标题
                        title = link_element.get_text() if link_element else "无标题"
                        
                        # 计算实际排名
                        rank = index + 1 + (page - 1) * 10
                        
                        # 检查是否是目标网站
                        if self.target_domain in link:
                            keyword_data['found'] = True
                            keyword_data['rank'] = rank
                            keyword_data['page'] = page
                            keyword_data['url'] = link
                            logger.info(f"在必应结果中找到目标网站: 排名 #{rank}, 页面 #{page}, URL: {link}")
                        
                        # 收集竞争对手数据
                        if not self.target_domain in link:
                            keyword_data['competitors'].append({
                                'rank': rank,
                                'title': title,
                                'url': link
                            })
                
                # 如果已经找到目标网站，可以提前退出循环
                if keyword_data['found']:
                    break
                    
                # 随机延迟，避免被搜索引擎检测为自动脚本
                delay_time = random.uniform(self.delay_min, self.delay_max)
                logger.info(f"等待 {delay_time:.2f} 秒后继续...")
                time.sleep(delay_time)
                
            except Exception as e:
                logger.error(f"处理关键词 '{keyword}' 时出错: {str(e)}")
                # 遇到错误时的延迟时间也相应减少
                time.sleep(random.uniform(self.delay_min, self.delay_max * 1.5))
        
        return keyword_data
    
    def analyze_keywords(self, keywords_list, search_engine="google", num_pages=10):
        """
        分析多个关键词的排名
        
        参数:
            keywords_list (list): 要分析的关键词列表
            search_engine (str): 使用的搜索引擎
            num_pages (int): 要检查的页数
            
        返回:
            pandas.DataFrame: 包含所有关键词排名数据的DataFrame
        """
        self.results = []
        
        for keyword in keywords_list:
            result = self.search_keyword(keyword, search_engine, num_pages)
            self.results.append(result)
            
            # 减少延迟时间
            delay_time = random.uniform(self.delay_min, self.delay_max)
            logger.info(f"分析下一个关键词前等待 {delay_time:.2f} 秒...")
            time.sleep(delay_time)
        
        # 将结果转换为DataFrame
        df_results = pd.DataFrame([{
            'keyword': r['keyword'],
            'found': r['found'],
            'rank': r['rank'],
            'page': r['page'],
            'url': r['url'],
            'competitor_count': len(r['competitors']),
        } for r in self.results])
        
        return df_results
    
    def export_results(self, filename="seo_analysis_results.xlsx"):
        """
        将结果导出到Excel文件
        
        参数:
            filename (str): 输出文件名
        """
        if not self.results:
            logger.warning("没有可导出的结果")
            return
            
        # 创建一个Excel writer对象
        writer = pd.ExcelWriter(filename, engine='openpyxl')
        
        # 主结果表
        main_results = pd.DataFrame([{
            'keyword': r['keyword'],
            'found': r['found'],
            'rank': r['rank'],
            'page': r['page'],
            'url': r['url'],
            'competitor_count': len(r['competitors']),
        } for r in self.results])
        
        main_results.to_excel(writer, sheet_name='主要结果', index=False)
        
        # 为每个关键词创建单独的竞争对手表
        for result in self.results:
            keyword = result['keyword']
            sheet_name = f"{keyword[:28]}竞争对手" if len(keyword) > 28 else f"{keyword}竞争对手"
            
            if result['competitors']:
                competitors_df = pd.DataFrame(result['competitors'])
                competitors_df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # 保存文件
        writer.close()
        logger.info(f"结果已导出到 {filename}")
        
        return filename

    def __del__(self):
        """析构函数，确保浏览器正确关闭"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass

def load_config(config_file='config.yaml'):
    """
    从配置文件加载配置
    
    参数:
        config_file (str): 配置文件路径
        
    返回:
        dict: 包含配置的字典
    """
    if not os.path.exists(config_file):
        logger.warning(f"配置文件 {config_file} 不存在，将使用默认配置")
        return {}
        
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            if config_file.endswith('.yaml') or config_file.endswith('.yml'):
                config = yaml.safe_load(f)
            elif config_file.endswith('.json'):
                config = json.load(f)
            else:
                logger.error(f"不支持的配置文件格式: {config_file}")
                return {}
                
        logger.info(f"已从 {config_file} 加载配置")
        return config
    except Exception as e:
        logger.error(f"读取配置文件 {config_file} 时出错: {str(e)}")
        return {}

def main():
    """主函数，处理命令行参数并执行分析"""
    parser = argparse.ArgumentParser(description='SEO关键词研究与排名分析工具')
    
    parser.add_argument('--config', '-c', type=str, default='config.yaml',
                        help='配置文件路径 (默认: config.yaml)')
    
    parser.add_argument('--domain', '-d', type=str,
                        help='要分析的目标域名 (例如 example.com)')
    
    parser.add_argument('--keywords', '-k', type=str,
                        help='要分析的关键词，用逗号分隔 (例如 "SEO优化,网站推广,网络营销")')
    
    parser.add_argument('--region', '-r', type=str,
                        help='Google搜索的区域 (例如: com, com.hk, co.jp)')
    
    parser.add_argument('--search-engine', '-s', type=str,
                        choices=['google', 'bing'],
                        help='使用的搜索引擎')
    
    parser.add_argument('--pages', '-p', type=int,
                        help='要检查的搜索结果页数')
    
    parser.add_argument('--delay-min', type=float,
                        help='请求之间的最小延迟(秒)')
    
    parser.add_argument('--delay-max', type=float,
                        help='请求之间的最大延迟(秒)')
    
    parser.add_argument('--output', '-o', type=str,
                        help='输出文件名')
    
    parser.add_argument('--use-browser', '-b', action='store_true',
                        help='使用浏览器模式进行搜索 (默认: False)')
    
    args = parser.parse_args()
    
    # 从配置文件加载配置
    config = load_config(args.config)
    
    # 命令行参数优先于配置文件，配置文件优先于默认值
    domain = args.domain or config.get('domain')
    keywords_str = args.keywords or config.get('keywords')
    region = args.region or config.get('region', 'com')
    search_engine = args.search_engine or config.get('search_engine', 'google')
    pages = args.pages or config.get('pages', 3)
    delay_min = args.delay_min or config.get('delay_min', 0.5)
    delay_max = args.delay_max or config.get('delay_max', 1.5)
    output = args.output or config.get('output', 'seo_analysis_results.xlsx')
    use_browser = args.use_browser or config.get('use_browser', False)
    
    # 参数验证
    if not domain:
        logger.error("未提供目标域名，请通过命令行参数 --domain 或配置文件指定")
        return
        
    if not keywords_str and not (config.get('keywords_list') or config.get('keywords')):
        logger.error("未提供关键词，请通过命令行参数 --keywords 或配置文件指定")
        return
    
    # 处理关键词
    if keywords_str:
        # 从命令行参数获取关键词列表
        keywords_list = [k.strip() for k in keywords_str.split(',')]
    elif isinstance(config.get('keywords'), str):
        # 配置文件中的关键词是字符串
        keywords_list = [k.strip() for k in config['keywords'].split(',')]
    elif isinstance(config.get('keywords_list'), list):
        # 配置文件中的关键词是列表
        keywords_list = config['keywords_list']
    else:
        logger.error("无法解析关键词列表")
        return
    
    logger.info(f"开始分析域名 {domain} 的 {len(keywords_list)} 个关键词...")
    logger.info(f"使用搜索引擎: {search_engine}, 区域: {region}, 检查页数: {pages}")
    
    # 创建SEO研究工具实例
    tool = SEOResearchTool(domain, delay_min, delay_max, region, use_browser)
    
    # 分析关键词
    results_df = tool.analyze_keywords(keywords_list, search_engine, pages)
    
    # 导出结果
    output_file = tool.export_results(output)
    
    logger.info("分析完成!")
    logger.info(f"结果已保存到: {output_file}")
    
    # 打印摘要
    found_count = results_df['found'].sum()
    logger.info("\n关键词排名摘要:")
    logger.info(f"- 分析的关键词总数: {len(keywords_list)}")
    logger.info(f"- 在搜索结果中找到的关键词数: {found_count}")
    logger.info(f"- 未找到的关键词数: {len(keywords_list) - found_count}")
    
    if found_count > 0:
        avg_rank = results_df.loc[results_df['found'], 'rank'].mean()
        logger.info(f"- 平均排名位置: {avg_rank:.2f}")
        
        # 打印排名靠前的关键词
        top_keywords = results_df.loc[results_df['found']].sort_values('rank').head(5)
        if not top_keywords.empty:
            logger.info("\n排名最好的关键词:")
            for _, row in top_keywords.iterrows():
                logger.info(f"- '{row['keyword']}': #{row['rank']} (第{row['page']}页)")

if __name__ == "__main__":
    main()
