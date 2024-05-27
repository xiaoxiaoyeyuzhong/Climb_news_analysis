import sys

import jieba
import matplotlib.pyplot as plt
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton
from bs4 import BeautifulSoup
from wordcloud import WordCloud


# 爬取新闻标题
def scrape_news_titles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # 新闻标题在 <a> 标签下的 <h4> 标签中,跳过a标签下没有h4标签的情况
    titles = soup.find_all('a')
    news_titles = []
    for title in titles:
        h4_tag = title.find('h4')
        if h4_tag:
            news_titles.append(h4_tag.get_text())
    return news_titles



# 爬取新闻内容并生成词云
def generate_wordcloud(news_url):
    response = requests.get(news_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # 提取所有 <p> 标签中的文字内容
    paragraphs = soup.find_all('p')
    text = ' '.join([p.get_text() for p in paragraphs])

    # 文本处理
    with open('merged_stopwords.txt', 'r', encoding='utf-8') as f:
        stopwords = set(f.read().split())
    words = jieba.cut(text)
    filtered_words = [word for word in words if word not in stopwords and len(word) > 1]
    cleaned_text = ' '.join(filtered_words)

    # 生成词云
    wordcloud = WordCloud(font_path='simhei.ttf',  # 指定中文字体路径
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
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # 爬取新闻标题
        self.news_titles = scrape_news_titles('https://example.com/news')

        # 新闻标题列表
        self.list_widget = QListWidget()
        for title in self.news_titles:
            self.list_widget.addItem(title)
        layout.addWidget(self.list_widget)

        # 显示新闻详情按钮
        self.show_details_button = QPushButton('显示新闻详情')
        self.show_details_button.clicked.connect(self.show_details)
        layout.addWidget(self.show_details_button)

        self.setLayout(layout)

    def show_details(self):
        # 获取用户选择的新闻标题
        selected_index = self.list_widget.currentRow()
        selected_news_url = f'https://sports.huanqiu.com/{selected_index}'

        # 生成词云并展示给用户
        generate_wordcloud(selected_news_url)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
