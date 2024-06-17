import jieba
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
