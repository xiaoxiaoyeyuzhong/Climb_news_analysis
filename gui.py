from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QStackedWidget
from chart_generator import plot_movie_ratings
from wordcloud_generator import scrape_news_titles_with_selenium, generate_wordcloud


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('新闻和电影数据展示')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()

        self.chart_button = QPushButton('绘制图表')
        self.wordcloud_button = QPushButton('生成词云')

        self.button_layout.addWidget(self.chart_button)
        self.button_layout.addWidget(self.wordcloud_button)

        self.layout.addLayout(self.button_layout)

        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        self.chart_widget = QWidget()
        self.wordcloud_widget = QWidget()

        self.init_chart_ui()
        self.init_wordcloud_ui()

        self.stacked_widget.addWidget(self.chart_widget)
        self.stacked_widget.addWidget(self.wordcloud_widget)

        self.setLayout(self.layout)

        self.chart_button.clicked.connect(self.show_chart)
        self.wordcloud_button.clicked.connect(self.show_wordcloud)

    def init_chart_ui(self):
        self.chart_layout = QVBoxLayout()
        self.chart_widget.setLayout(self.chart_layout)

    def init_wordcloud_ui(self):
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.generate_wordcloud_button = QPushButton('生成文章内容词云')
        self.generate_wordcloud_button.clicked.connect(self.generate_wordcloud_from_news)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.generate_wordcloud_button)
        self.wordcloud_widget.setLayout(layout)

    def show_chart(self):
        self.stacked_widget.setCurrentWidget(self.chart_widget)
        if not hasattr(self, 'chart_button_initialized'):
            self.chart_button = QPushButton('绘制豆瓣电影评分图表')
            self.chart_button.clicked.connect(plot_movie_ratings)
            self.chart_layout.addWidget(self.chart_button)
            self.chart_button_initialized = True

    def show_wordcloud(self):
        self.stacked_widget.setCurrentWidget(self.wordcloud_widget)
        self.display_news_titles()

    def display_news_titles(self):
        self.list_widget.clear()
        self.news_titles = scrape_news_titles_with_selenium('https://sports.huanqiu.com/')
        for title, news_id in self.news_titles:
            self.list_widget.addItem(title)

    def generate_wordcloud_from_news(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            selected_index = self.list_widget.currentRow()
            selected_news_id = self.news_titles[selected_index][1]
            selected_news_url = f'https://sports.huanqiu.com/article/{selected_news_id}'
            generate_wordcloud(selected_news_url)
