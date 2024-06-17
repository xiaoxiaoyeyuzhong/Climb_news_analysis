import sys
import os
import jieba
import matplotlib.pyplot as plt
import pandas as pd
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton
from bs4 import BeautifulSoup
from wordcloud import WordCloud
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from matplotlib.font_manager import FontProperties


# 使用Selenium爬取新闻标题和链接
def scrape_news_titles_with_selenium(url):
    edge_options = EdgeOptions()
    edge_options.add_argument('--headless')
    edge_options.add_argument('--disable-gpu')
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-dev-shm-usage')

    service = EdgeService(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=edge_options)

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'item-title'))
        )

        news_titles = []
        news_ids = []
        title_elements = driver.find_elements(By.CLASS_NAME, 'item-title')
        id_elements = driver.find_elements(By.CLASS_NAME, 'item-aid')
        for title_element, id_element in zip(title_elements, id_elements):
            title = title_element.get_attribute('value')
            news_id = id_element.get_attribute('value')
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

    with open('merged_stopwords.txt', 'r', encoding='utf-8') as f:
        stopwords = set(f.read().split())
    words = jieba.cut(text)
    filtered_words = [word for word in words if word not in stopwords and len(word) > 1]
    cleaned_text = ' '.join(filtered_words)

    wordcloud = WordCloud(font_path='C:/Windows/Fonts/simhei.ttf',
                          width=800,
                          height=400,
                          background_color='white').generate(cleaned_text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()


# 爬取豆瓣电影数据
def fetch_movie_data():
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
    }
    all_titles = []
    all_ratings = []
    for start_num in range(0, 250, 25):
        response = requests.get(f'https://movie.douban.com/top250?start={start_num}', headers=headers)
        if response.ok:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            items = soup.findAll("div", class_="item")
            for item in items:
                title = item.find("span", class_="title")
                rating = item.find("span", class_="rating_num")
                if title and rating and '/' not in title.string:
                    all_titles.append(title.string)
                    all_ratings.append(rating.string)
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None, None

    return all_titles, all_ratings


# 绘制电影评分图表
def plot_movies(top_movies, font_prop):
    plt.figure(figsize=(10, 6))
    plt.bar(top_movies['电影标题'], top_movies['电影评分'].astype(float), color='skyblue')

    plt.xlabel('电影标题', fontproperties=font_prop)
    plt.ylabel('评分', fontproperties=font_prop)
    plt.title('豆瓣电影Top 20评分', fontproperties=font_prop)

    plt.xticks(range(len(top_movies['电影标题'])), top_movies['电影标题'], rotation=90, fontproperties=font_prop)
    plt.tight_layout()

    plt.savefig('douban_top20_movies_ratings.png', dpi=300, bbox_inches='tight')
    plt.show()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('新闻和电影数据展示')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # 新闻标题列表
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # 按钮
        self.news_button = QPushButton('显示新闻标题')
        self.chart_button = QPushButton('绘制电影评分图表')
        self.wordcloud_button = QPushButton('生成词云')

        button_layout.addWidget(self.news_button)
        button_layout.addWidget(self.chart_button)
        button_layout.addWidget(self.wordcloud_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # 绑定按钮点击事件
        self.news_button.clicked.connect(self.display_news_titles)
        self.chart_button.clicked.connect(self.plot_movie_ratings)
        self.wordcloud_button.clicked.connect(self.generate_wordcloud_from_news)

    def display_news_titles(self):
        self.list_widget.clear()
        self.news_titles = scrape_news_titles_with_selenium('https://sports.huanqiu.com/')
        for title, news_id in self.news_titles:
            self.list_widget.addItem(title)

    def plot_movie_ratings(self):
        movie_titles, movie_ratings = fetch_movie_data()
        csv_file = 'douban_top250_movies.csv'
        if movie_titles and movie_ratings and not os.path.exists(csv_file):
            data = {
                "电影标题": movie_titles,
                "电影评分": movie_ratings
            }
            df = pd.DataFrame(data)
            df.to_csv(csv_file, index=False, encoding='utf-8-sig')

        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file, encoding='utf-8-sig')
            top_movies = df.head(20)
            font_path = 'C:/Windows/Fonts/simhei.ttf'
            font_prop = FontProperties(fname=font_path)
            plot_movies(top_movies, font_prop)

    def generate_wordcloud_from_news(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            selected_index = self.list_widget.currentRow()
            selected_news_id = self.news_titles[selected_index][1]
            selected_news_url = f'https://sports.huanqiu.com/article/{selected_news_id}'
            generate_wordcloud(selected_news_url)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
