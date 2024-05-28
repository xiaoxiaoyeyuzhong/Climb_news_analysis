# import requests
# from bs4 import BeautifulSoup
# import time
#
# def scrape_news_titles(url):
#     # 等待3秒
#     time.sleep(3)
#     headers = {
#         'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
#     }
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     news_titles = []
#     news_urls = []
#
#     # 找到所有包含新闻的div标签
#     feed_items = soup.find_all('div', class_='feed-item feed-item-a')
#     for item in feed_items:
#         # 在每个feed-item内找a标签
#         a_tag = item.find('a')
#         if a_tag:
#             # 在a标签内找h4标签
#             h4_tag = a_tag.find('h4')
#             if h4_tag:
#                 news_titles.append(h4_tag.get_text())
#                 news_urls.append('https://sports.huanqiu.com' + a_tag['href'])  # 拼接完整的URL
#
#     return news_titles, news_urls
#
#
# if __name__ == "__main__":
#     url = 'https://sports.huanqiu.com'
#     titles, urls = scrape_news_titles(url)
#
#     print("新闻标题:")
#     for title in titles:
#         print(title)
#
#     print("\n新闻链接:")
#     for url in urls:
#         print(url)


# import requests
# from bs4 import BeautifulSoup
# from lxml import etree
#
#
# def scrape_news_titles(url):
#     response = requests.get(url)
#     response.encoding = 'utf-8'  # 设置编码
#     soup = BeautifulSoup(response.content, 'html.parser')
#
#     # 使用lxml解析
#     tree = etree.HTML(str(soup))
#
#     # 使用XPath查找新闻标题和链接
#     titles_xpath = '/html/body/channel-container-template//div/div/div/div[2]/div[2]/div[1]/layout-block-template[2]//div/layout-bd-template//div/sketch-feed-template//div/div[1]/div[8]/a/h4/text()'
#     urls_xpath = '/html/body/channel-container-template//div/div/div/div[2]/div[2]/div[1]/layout-block-template[2]//div/layout-bd-template//div/sketch-feed-template//div/div[1]/div[8]/a/@href'
#
#     news_titles = tree.xpath(titles_xpath)
#     news_urls = tree.xpath(urls_xpath)
#
#     # 如果需要拼接完整URL，可以在这里处理
#     base_url = 'https://sports.huanqiu.com'
#     news_urls = [base_url + url for url in news_urls]
#
#     return news_titles, news_urls
#
#
# if __name__ == "__main__":
#     url = 'https://sports.huanqiu.com'
#     titles, urls = scrape_news_titles(url)
#
#     print("新闻标题:")
#     for title in titles:
#         print(title)
#
#     print("\n新闻链接:")
#     for url in urls:
#         print(url)


# import requests
# from bs4 import BeautifulSoup
# import time
#
# def scrape_news_titles(url):
#     # 等待3秒
#     time.sleep(3)
#
#     headers = {
#         'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
#     }
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     news_titles = []
#     news_urls = []
#
#     # 找到所有包含新闻标题的div标签
#     news_items = soup.find_all('div', class_='news_title')
#     for item in news_items:
#         # 在每个news_title内找h3标签
#         h3_tag = item.find('h3')
#         if h3_tag:
#             # 在h3标签内找a标签
#             a_tag = h3_tag.find('a')
#             if a_tag:
#                 news_titles.append(a_tag.get_text())
#                 news_urls.append(a_tag['href'])
#
#     return news_titles, news_urls
#
#
# if __name__ == "__main__":
#     url = 'https://news.163.com'
#     titles, urls = scrape_news_titles(url)
#
#     print("新闻标题:")
#     for title in titles:
#         print(title)
#
#     print("\n新闻链接:")
#     for url in urls:
#         print(url)


# 对于动态网页，直接用request和BeautifulSoup是行不通的
# import requests
# import time
#
#
# def scrape_full_page(url):
#     # 等待3秒
#     time.sleep(3)
#
#     headers = {
#         'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
#     }
#     response = requests.get(url, headers=headers)
#
#     # 打印响应状态码以确认请求成功
#     print(f"Response status code: {response.status_code}")
#
#     if response.status_code != 200:
#         print("Failed to retrieve the webpage.")
#         return None
#
#     return response.text
#
#
# def save_html_to_file(html_content, file_path):
#     with open(file_path, 'w', encoding='utf-8') as file:
#         file.write(html_content)
#     print(f"HTML content saved to {file_path}")
#
#
# if __name__ == "__main__":
#     url = 'https://sports.huanqiu.com'
#     full_page_content = scrape_full_page(url)
#
#     if full_page_content:
#         # 保存HTML内容到文本文件
#         save_html_to_file(full_page_content, 'page_content.html')


# from selenium import webdriver
# from selenium.webdriver.edge.service import Service as EdgeService
# from selenium.webdriver.edge.options import Options as EdgeOptions
# from webdriver_manager.microsoft import EdgeChromiumDriverManager
# import time
#
# def scrape_full_page_with_selenium(url):
#     # 设置Edge选项
#     edge_options = EdgeOptions()
#     edge_options.add_argument('--headless')  # 设置无头模式
#     edge_options.add_argument('--disable-gpu')
#     edge_options.add_argument('--no-sandbox')
#     edge_options.add_argument('--disable-dev-shm-usage')
#
#     # 启动Edge浏览器
#     service = EdgeService(EdgeChromiumDriverManager().install())
#     driver = webdriver.Edge(service=service, options=edge_options)
#
#     # 打开URL
#     driver.get(url)
#     time.sleep(3)  # 等待页面加载完成
#
#     # 获取页面内容
#     full_page_content = driver.page_source
#     driver.quit()
#
#     return full_page_content
#
# def save_html_to_file(html_content, file_path):
#     with open(file_path, 'w', encoding='utf-8') as file:
#         file.write(html_content)
#     print(f"HTML content saved to {file_path}")
#
# if __name__ == "__main__":
#     url = 'https://sports.huanqiu.com'
#     full_page_content = scrape_full_page_with_selenium(url)
#
#     if full_page_content:
#         # 保存HTML内容到文本文件
#         save_html_to_file(full_page_content, 'page_content.html')



from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
import time

def scrape_news_titles_with_selenium(url):
    # 设置Edge选项
    edge_options = EdgeOptions()
    edge_options.add_argument('--headless')  # 设置无头模式
    edge_options.add_argument('--disable-gpu')
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-dev-shm-usage')

    # 启动Edge浏览器
    service = EdgeService(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=edge_options)

    # 打开URL
    driver.get(url)
    time.sleep(3)  # 等待页面加载完成

    # 获取包含新闻标题的元素
    news_titles = []
    title_elements = driver.find_elements(By.CLASS_NAME, 'item-title')
    for element in title_elements:
        title = element.get_attribute('value')  # 获取标题内容
        if title:
            news_titles.append(title)

    driver.quit()

    return news_titles

if __name__ == "__main__":
    url = 'https://sports.huanqiu.com'
    titles = scrape_news_titles_with_selenium(url)

    print("新闻标题:")
    for title in titles:
        print(title)


