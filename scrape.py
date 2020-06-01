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
    nvcafe_list = []
    blog_list = []
    post_list = []
    merge_sentence = ""
    tags = []
    keyword = ""


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
        url_list = ["https://search.naver.com/search.naver?where=new&query=",           # 뉴스
                    "https://search.naver.com/search.naver?where=realtime&section=6&query=",    # 트위터
                    "https://search.naver.com/search.naver?where=article&query=",       # 카페
                    "https://search.naver.com/search.naver?where=post&query=",          # 블로그
                    "https://post.naver.com/search/post.nhn?keyword="]                  # 포스트
        
        query = keyword
        self.keyword = keyword
        url_search = []
        search_request = []
        soup = []

        for index in range(5):
            url_search.append(url_list[index])
            search_request.append(requests.get(url_search[index]+query))  
            soup.append(BeautifulSoup(search_request[index].text, 'html.parser'))

        # Get HTML
        news = soup[0].select("a._sp_each_title")
        realtime_twitter = soup[1].select("span.cmmt")
        nvcafe = soup[2].select("a.txt_link")
        blog = soup[3].select("a.sh_blog_title")
        post = soup[4].select("strong.tit_feed ell")

        # Get Text
        for i in news:
            self.news_list.append(i.text)
        for i in realtime_twitter:
            self.realtime_twitter_list.append(i.text)
        for i in nvcafe:
            self.nvcafe_list.append(i.text)
        for i in blog:
            self.blog_list.append(i.text)
        for i in post:
            self.post_list.append(i.text)
            

        for sentence in self.news_list:
            self.merge_sentence += sentence
        for sentence in self.realtime_twitter_list:
            self.merge_sentence += sentence
        for sentence in self.nvcafe_list:
            self.merge_sentence += sentence
        for sentence in self.blog_list:
            self.merge_sentence += sentence   
        for sentence in self.post_list:
            self.merge_sentence += sentence  

    
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
    def get_nvcafe_list(self):
        return self.nvcafe_list
    def get_blog_list(self):
        return self.blog_list
    def get_post_list(self):
        return self.post_list
    def get_tags(self):
        return self.tags