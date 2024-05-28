# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
#
# if __name__ == '__main__':
#     headers = {
#         'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
#     }
#     for start_num in range(0,250,25):
#         response = requests.get(f'https://movie.douban.com/top250?start={start_num}', headers=headers)
#         if response.ok:
#             html = response.text
#             soup = BeautifulSoup(html, 'html.parser')
#             all_titles = soup.findAll("span", attrs={"class": "title"})
#             # for title in all_titles:
#             #     title_string = title.string
#             #     if '/' not in title_string:
#             #         print(title_string)
#             data=[]
#             for title in all_titles:
#                 # 如果文字标题没有 ‘/’，则保存到 列表里
#                 if '/' not in title.string:
#                     data.append(title.string)
#             print(data)
#         else:
#             print("请求失败")
#             print(response.status_code)


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('新闻标题展示')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.list_widget.addItem("测试新闻标题1")
        self.list_widget.addItem("测试新闻标题2")
        layout.addWidget(self.list_widget)

        self.list_widget.itemClicked.connect(self.show_details)

        self.setLayout(layout)

    def show_details(self, item):
        print(f"点击了: {item.text()}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
