import sys
import jieba
import matplotlib.pyplot as plt
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget
from bs4 import BeautifulSoup
from wordcloud import WordCloud
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 使用Selenium爬取新闻标题和链接
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

    try:
        # 打开URL
        driver.get(url)

        # 等待页面加载完成，直到指定的元素出现
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'item-title'))
        )

        # 获取包含新闻标题和唯一标识符的元素
        news_titles = []
        news_ids = []
        title_elements = driver.find_elements(By.CLASS_NAME, 'item-title')
        id_elements = driver.find_elements(By.CLASS_NAME, 'item-aid')
        for title_element, id_element in zip(title_elements, id_elements):
            title = title_element.get_attribute('value')  # 获取标题内容
            news_id = id_element.get_attribute('value')  # 获取唯一标识符
            if title and news_id:
                news_titles.append((title, news_id))

    finally:
        driver.quit()

    return news_titles


# 爬取新闻内容并生成词云
def generate_wordcloud(news_url):
    response = requests.get(news_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ' '.join([p.get_text() for p in paragraphs])

    # 文本处理
    with open('merged_stopwords.txt', 'r', encoding='utf-8') as f:
        stopwords = set(f.read().split())
    words = jieba.cut(text)
    filtered_words = [word for word in words if word not in stopwords and len(word) > 1]
    cleaned_text = ' '.join(filtered_words)

    # 生成词云
    wordcloud = WordCloud(font_path='C:/Windows/Fonts/simhei.ttf',  # 指定中文字体路径
                          width=800,
                          height=400,
                          background_color='white').generate(cleaned_text)

    # 显示词云
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('新闻标题和词云展示')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # 爬取新闻标题
        self.news_titles = scrape_news_titles_with_selenium('https://sports.huanqiu.com/')

        # 调试信息，输出爬取到的新闻标题
        print("新闻标题:")
        for title, news_id in self.news_titles:
            print(f"{title} - {news_id}")

        # 新闻标题列表
        self.list_widget = QListWidget()
        for title, news_id in self.news_titles:
            self.list_widget.addItem(title)
        layout.addWidget(self.list_widget)

        # 绑定列表项点击事件
        self.list_widget.itemClicked.connect(self.show_details)

        self.setLayout(layout)

    def show_details(self, item):
        # 获取用户选择的新闻标题索引
        selected_index = self.list_widget.currentRow()
        selected_news_id = self.news_titles[selected_index][1]
        selected_news_url = f'https://sports.huanqiu.com/article/{selected_news_id}'

        # 生成词云并展示给用户
        generate_wordcloud(selected_news_url)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
