from scrape import Scrap

run = Scrap()
keyword = run.get_keyword()
run.search(keyword[0])
print("뉴스 :", run.get_news_list())
print("트위터 :", run.get_realtime_twitter_list())
print("카페 :", run.get_realtime_nvcafe_list())
print("블로그 :", run.get_blog_list())
print("관련검색어 :", run.get_related_list())

run.extract()
run.make_cloud()