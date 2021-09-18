import requests
import string
import os
from bs4 import BeautifulSoup
from path import path
number_of_pages = int(input())
type_of_article = input()

for i in range(1, number_of_pages + 1):
    os.mkdir('Page_' + str(i))
    os.chdir(path + 'Page_' + str(i))
    url = 'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page=' + str(i)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for art in soup.find_all('article'):
        if type_of_article == art.find('span', {'class': 'c-meta__type'}).text:
            article = art.find('div', {'class': 'c-card__body'})
            name = article.find('a', {'class': 'c-card__link'}).text
            mapping = str.maketrans(string.punctuation + '’‘—', "#" * 35)
            name = name.translate(mapping).replace(' ', '_').replace('#', '')
            print(name)
            link = article.find('a', {'class': 'c-card__link'}).get('href')
            art_response = requests.get('https://www.nature.com' + link)
            art_soup = BeautifulSoup(art_response.content, 'html.parser')
            print('https://www.nature.com' + link)
            text = art_soup.find('div', {'class': 'c-article-body u-clearfix'}).text.replace('\n', '')
            with open(name + '.txt', 'w') as file:
                file.write(text)
    os.chdir(path)
