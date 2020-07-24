from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sys
from flask import render_template
from flask import request, url_for, redirect, flash

WIN = sys.platform.startswith('win')

if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

db = SQLAlchemy(app)  # 初始化扩展，传入程序 app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页

    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)

# successfully get the right response of database
# PyDev console: starting.
# Python 3.7.4 (default, Aug 13 2019, 20:35:49)
# [GCC 7.3.0] on linux
# from db_demo import User, Movie
# user = User(name='Grey Li')
# m1 = Movie(title='Leon', year='1994')
# m2 = Movie(title='Mahjong', year='1996')
# db.session.add(user)
# Traceback (most recent call last):
#   File "<input>", line 1, in <module>
# NameError: name 'db' is not defined
# from db_demo import db
# db.session.add(user)
# db.session.add(m1)
# db.session.add(m2)
# db.session.commit()
# movie_detect = Movie.query.first()
# movie_detect.title
# 'Leon'
# movie_detect.year
# '1994'
# Movie.query.all()
# [<Movie 1>, <Movie 2>]
# Movie.query.count()
# 2
# Movie.query.get(1)
# <Movie 1>
# Movie.query.filter_by(title='Mahjong').first()
# <Movie 2>
# Movie.query.filter(Movie.title=='Mahjong').first()
# <Movie 2>
