# -*- coding: UTF-8 -*- 
from flask import Flask, render_template, request
from scrape import Scrap

import os
import random


app = Flask(__name__)
run = Scrap()

@app.route('/')
def index():
    keywords = run.get_keyword()    # get keyword list
    return render_template("input.html",
                            keywords=keywords)
                            

@app.route('/result', methods=['POST'])
def result():
    value = request.form['keyword'] # input any keyword
    rand = random.randrange(0,9999) # 같은 파일이 있을경우 새로 파일을 생성해서 덮어 씌우더라도 이전의 파일을 전송하기에, 파일이름을 다르게 하기 위함
    path = './static/'

    file_list = os.listdir(path)
    png_file = [file for file in file_list if file.endswith(".png")]    # search *.png files

    if len(png_file) > 0:   # remove *.png files
        for f in png_file:
            os.remove(path + f)

    run.search(value)
    run.extract()
    run.make_cloud(rand)

    news_list = run.get_news_list()
    realtime_twitter_list = run.get_realtime_twitter_list()
    nvcafe_list = run.get_nvcafe_list()
    blog_list = run.get_blog_list()
    post_list = run.get_post_list()
    tags = run.get_tags()


    return render_template('result.html', 
                            keyword=value,
                            news_list=news_list,
                            realtime_twitter_list=realtime_twitter_list,
                            nvcafe_list=nvcafe_list,
                            blog_list=blog_list,
                            post_list=post_list,
                            tags=tags,
                            img_src=value+str(rand)+'.png')


if __name__ == '__main__':
    app.run(port=5000, threaded=True)
    