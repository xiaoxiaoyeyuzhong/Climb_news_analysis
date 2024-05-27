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
