import os
import pandas as pd
from matplotlib.font_manager import FontProperties
import requests
from bs4 import BeautifulSoup
import jieba
from wordcloud_generator import WordCloud
import matplotlib.pyplot as plt

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


def plot_movies(top_movies, font_prop):
    plt.figure(figsize=(10, 6))
    plt.bar(top_movies['电影标题'], top_movies['电影评分'].astype(float), color='skyblue')

    plt.xlabel('电影标题', fontproperties=font_prop)
    plt.ylabel('评分', fontproperties=font_prop)
    plt.title('豆瓣电影Top 20评分', fontproperties=font_prop)

    plt.xticks(range(len(top_movies['电影标题'])), top_movies['电影标题'], rotation=90, fontproperties=font_prop)
    plt.tight_layout()

    # 保存图表
    plt.savefig('douban_top20_movies_ratings.png', dpi=300, bbox_inches='tight')
    # 显示图表
    plt.show()


def fetch_news_messages():
    # Step 1: 爬取文章内容
    url = 'https://sports.huanqiu.com/article/4HiOewaGMhl'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # 提取所有 <p> 标签中的文字内容
    paragraphs = soup.find_all('p')
    text = ' '.join([p.get_text() for p in paragraphs])

    # Step 2: 文本处理
    with open('merged_stopwords.txt', 'r', encoding='utf-8') as f:
        stopwords = set(f.read().split())
    words = jieba.cut(text)
    filtered_words = [word for word in words if word not in stopwords and len(word) > 1]
    cleaned_text = ' '.join(filtered_words)

    # Step 3: 生成词云
    wordcloud = WordCloud(font_path='simhei.ttf',  # 指定中文字体路径
                          width=800,
                          height=400,
                          background_color='white').generate(cleaned_text)

    # Step 4: 显示词云
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    movie_titles, movie_ratings = fetch_movie_data()
    csv_file = 'douban_top250_movies.csv'
    if movie_titles and movie_ratings and not os.path.exists(csv_file):
        data = {
            "电影标题": movie_titles,
            "电影评分": movie_ratings
        }
        df = pd.DataFrame(data)
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print("电影标题和评分已成功保存到 douban_top250_movies.csv")
    
    if os.path.exists(csv_file):
        # 读取CSV文件
        df = pd.read_csv(csv_file, encoding='utf-8-sig')
    
        # 取前20个电影标题和评分
        top_movies = df.head(20)
    
        # 使用指定字体文件路径
        font_path = 'C:/Windows/Fonts/simhei.ttf'  # 确保路径正确
        font_prop = FontProperties(fname=font_path)
    
        # 绘制并显示图表
        plot_movies(top_movies, font_prop)

    # 爬取新闻网站新闻，生成词云
    # fetch_news_messages()
