import sys
import jieba
import matplotlib.pyplot as plt
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget
from bs4 import BeautifulSoup
from wordcloud import WordCloud


# 爬取新闻标题和链接
def scrape_news_titles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    news_titles = []
    news_urls = []

    # 找到所有包含新闻的div标签
    feed_items = soup.find_all('div', class_='feed-item feed-item-a')
    for item in feed_items:
        # 在每个feed-item内找a标签
        a_tag = item.find('a')
        if a_tag:
            # 在a标签内找h4标签
            h4_tag = a_tag.find('h4')
            if h4_tag:
                news_titles.append(h4_tag.get_text())
                news_urls.append('https://sports.huanqiu.com' + a_tag['href'])  # 拼接完整的URL
    return news_titles, news_urls


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
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # 爬取新闻标题
        self.news_titles, self.news_urls = scrape_news_titles('https://sports.huanqiu.com')

        # 调试信息，输出爬取到的新闻标题
        print("新闻标题:")
        for title in self.news_titles:
            print(title)

        # 新闻标题列表
        self.list_widget = QListWidget()
        for title in self.news_titles:
            self.list_widget.addItem(title)
        layout.addWidget(self.list_widget)

        # 绑定列表项点击事件
        self.list_widget.itemClicked.connect(self.show_details)

        self.setLayout(layout)

    def show_details(self, item):
        # 获取用户选择的新闻标题索引
        selected_index = self.list_widget.currentRow()
        selected_news_url = self.news_urls[selected_index]

        # 生成词云并展示给用户
        generate_wordcloud(selected_news_url)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
