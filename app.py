from datetime import datetime

from flask import Flask, render_template_string, request
from faker import Faker
import random
import string
import gzip
import io
import logging

app = Flask(__name__)
fake = Faker('zh_CN')


# 生成随机路径
def generate_random_path():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


# 生成假文章
def generate_fake_article():
    title = fake.sentence(nb_words=6)
    content=''
    words=fake.paragraphs(nb=50)
    for _ in words:
        content+=f'<p><a href="/{generate_random_path()}.html">{_}</a></p>'
    return {
        'title': title,
        'content': content
    }


# 记录爬虫访问日志到 Redis


@app.route('/<path:path>')
def trap(path):
    article = generate_fake_article()
    next_path = generate_random_path()

    html = """
    <html>
    <head><meta charset="UTF-8"><title>{{ title }}</title></head>
    <body>
        <h1>{{ title }}</h1>
        <span>发布时间：{{pub_time}}</span>
        <div class="content">{{ content }}</div>
        <a href="/{{ next_path }}">下一页</a>
    </body>
    </html>
    """
    html=html.replace('{{ content }}', article['content'])
    print(html)
    return render_template_string(html, title=article['title'],pub_time=datetime.now(),next_path=next_path)
@app.route('/')
def traps():
    article = generate_fake_article()
    next_path = generate_random_path()

    html = """
    <html>
    <head><meta charset="UTF-8"><title>{{ title }}</title></head>
    <body>
        <h1>{{ title }}</h1>
        <span>发布时间：{{pub_time}}</span>
        <div class="content">{{ content }}</div>
        <a href="/{{ next_path }}">下一页</a>
    </body>
    </html>
    """
    html=html.replace('{{ content }}', article['content'])
    print(html)
    return render_template_string(html, title=article['title'],pub_time=datetime.now(),next_path=next_path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
