import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from matplotlib.font_manager import FontProperties


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


def plot_movie_ratings():
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
