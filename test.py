import requests
from bs4 import BeautifulSoup

from konlpy.tag import Komoran 
from konlpy.utils import pprint
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class Scrap:
    news_list = []
    realtime_twitter_list = []
    realtime_nvcafe_list = []
    related_list = []
    blog_list = []
    merge_sentence = ""
    tags = []
    keyword = ""

    # def __init__(self):
    #     keywords = self.get_keyword()

    #     url_search = "https://search.naver.com/search.naver?where=nexearch&sm=tab_lve.ag20sgrpma0si0en0sp0&ie=utf8&query="
    #     query = input()

    #     search_request = requests.get(url_search+query)
    #     soup = BeautifulSoup(search_request.text, 'html.parser')

    #     # Get HTML
    #     imgs = soup.select("div.thumb > a > img")
    #     news = soup.select("a._sp_each_title")
    #     realtime_twitter = soup.select("span.cmmt")
    #     realtime_nvcafe = soup.select("a.txt_link")
    #     related = soup.select("ul._related_keyword_ul > li > a")
    #     blog = soup.select("a.sh_blog_title")

    #     # Get Text
    #     for i in news:
    #         self.news_list.append(i.text)
    #     for i in realtime_twitter:
    #         self.realtime_twitter_list.append(i.text)
    #     for i in realtime_nvcafe:
    #         self.realtime_nvcafe_list.append(i.text)
    #     for i in related:
    #         self.related_list.append(i.text)  
    #     for i in blog:
    #         self.blog_list.append(i.text)
            

    #     for sentence in self.news_list:
    #         self.merge_sentence += sentence
    #     for sentence in self.realtime_twitter_list:
    #         self.merge_sentence += sentence
    #     for sentence in self.realtime_nvcafe_list:
    #         self.merge_sentence += sentence
    #     # for sentence in self.related_list:
    #     #     self.merge_sentence += sentence
    #     # for sentence in self.blog_list:
    #     #     self.merge_sentence += sentence  


    def get_keyword(self):
        json = requests.get('https://www.naver.com/srchrank?frm=main&ag=20s&gr=0&ma=0&si=0&en=0&sp=0').json()
        ranks = json.get("data")
        keywords = []
        
        for r in ranks:
            rank = r.get("rank")
            keyword = r.get("keyword")
            keywords.append(keyword)
            # print(rank, keyword)

        print(keywords)
        return keywords

    def search(self, keyword):
        url_search = "https://search.naver.com/search.naver?query="
        query = keyword
        self.keyword = keyword

        search_request = requests.get(url_search+query)
        soup = BeautifulSoup(search_request.text, 'html.parser')

        # Get HTML
        imgs = soup.select("div.thumb > a > img")
        news = soup.select("a._sp_each_title")
        realtime_twitter = soup.select("span.cmmt")
        realtime_nvcafe = soup.select("a.txt_link")
        related = soup.select("ul._related_keyword_ul > li > a")
        blog = soup.select("a.sh_blog_title")

        # Get Text
        for i in news:
            self.news_list.append(i.text)
        for i in realtime_twitter:
            self.realtime_twitter_list.append(i.text)
        for i in realtime_nvcafe:
            self.realtime_nvcafe_list.append(i.text)
        for i in related:
            self.related_list.append(i.text)  
        for i in blog:
            self.blog_list.append(i.text)
            

        for sentence in self.news_list:
            self.merge_sentence += sentence
        for sentence in self.realtime_twitter_list:
            self.merge_sentence += sentence
        for sentence in self.realtime_nvcafe_list:
            self.merge_sentence += sentence
        # for sentence in self.related_list:
        #     self.merge_sentence += sentence
        # for sentence in self.blog_list:
        #     self.merge_sentence += sentence  

    
    def extract(self):
        kmr = Komoran()
        nouns = kmr.nouns(self.merge_sentence)
        processed = [n for n in nouns if len(n) >= 2]   # min length 2
        count = Counter(processed)

        self.tags = count.most_common(15)
        print(self.tags)


    def make_cloud(self):
        font_path = 'NanumGothic.ttf'
        word_cloud = WordCloud(
            font_path=font_path,
            width=800,
            height=800,
            background_color="white"
        )

        word_cloud = word_cloud.generate_from_frequencies(dict(self.tags))
        fig = plt.figure(figsize=(10,10))
        plt.imshow(word_cloud)
        plt.axis("off")
        fig.savefig('./static/' + self.keyword + '.png')


    def get_news_list(self):
        return self.news_list
    def get_realtime_twitter_list(self):
        return self.realtime_twitter_list
    def get_realtime_nvcafe_list(self):
        return self.realtime_nvcafe_list
    def get_related_list(self):
        return self.related_list
    def get_blog_list(self):
        return self.blog_list
    def get_tags(self):
        return self.tags