import requests
from bs4 import BeautifulSoup

from konlpy.tag import Komoran 
from konlpy.utils import pprint
from collections import Counter
import pytagcloud

class Scrap:
    news_list = []
    realtime_twitter_list = []
    realtime_nvcafe_list = []
    related_list = []
    blog_list = []
    merge_sentence = ""

    def get_keyword(self):
        json = requests.get('https://www.naver.com/srchrank?frm=main&ag=20s&gr=0&ma=0&si=0&en=0&sp=0').json()
        ranks = json.get("data")
        
        for r in ranks:
            rank = r.get("rank")
            keyword = r.get("keyword")
            print(rank, keyword)

        return ranks


    def __init__(self):
        keywords = self.get_keyword()

        url_search = "https://search.naver.com/search.naver?where=nexearch&sm=tab_lve.ag20sgrpma0si0en0sp0&ie=utf8&query="
        query = input()

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

        # print("뉴스 : ", news_list)
        # print("실시간 트위터 : ", realtime_twitter_list)
        # print("실시간 카페 : " , realtime_nvcafe_list)
        # print("연관검색어 : ", related_list)
        # print("블로그 : ", blog_list)

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

    
    def extract(self):
        kmr = Komoran()
        count = Counter(kmr.nouns(self.merge_sentence))

        tag2 = count.most_common(15)
        print(tag2)
        taglist = pytagcloud.make_tags(tag2, maxsize=80)
        pytagcloud.create_tag_image(taglist, 'wordcloud.jpg', size=(800, 600), fontname='Korean', rectangular=False)