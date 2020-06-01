# -*- coding: utf-8 -*- 
from flask import Flask, render_template, request
from scrape import Scrap


app = Flask(__name__)
run = Scrap()

@app.route('/')
def index():

    keywords = run.get_keyword()

    return render_template("input.html",
                            keywords=keywords)
                            

@app.route('/post', methods=['POST'])
def post():
    value = request.form['keyword']

    run.search(value)
    run.extract()
    run.make_cloud()

    news_list = run.get_news_list()
    realtime_twitter_list = run.get_realtime_twitter_list()
    nvcafe_list = run.get_nvcafe_list()
    blog_list = run.get_blog_list()
    post_list = run.get_post_list()
    tags = run.get_tags()

    return render_template('result.html', 
                            news_list=news_list,
                            realtime_twitter_list=realtime_twitter_list,
                            nvcafe_list=nvcafe_list,
                            blog_list=blog_list,
                            post_list=post_list,
                            tags=tags,
                            img_src=value+'.png')


if __name__ == '__main__':
    app.run()
    