from flask import Flask, render_template
from markupsafe import escape
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

import click

from pathlib import Path


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(Path(app.root_path) / 'data.db')

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app, model_class=Base)

class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))

class Movie(db.Model):
    __tablename__ = 'movies'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(20))
    year: Mapped[int] = mapped_column(String(4))

@app.cli.command('init-db')
@click.option('--drop', is_flag=True, help='Create after drop.')
def init_datebase(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized the database.')

@app.context_processor
def inject_user():
    user = db.session.execute(select(User)).scalar()
    return dict(user=user)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/')
def index():
    movies = db.session.execute(select(Movie)).scalars().all()
    return render_template('index.html', movies=movies)

@app.cli.command()
def forge():
    '''
    Generate fake data
    '''
    db.drop_all()
    db.create_all()

    name = "lzj"
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    
    db.session.commit()
    click.echo('Done')

# 一个函数可以绑定多个路由
@app.route('/home')
def hello_home():
    return '<h1>HelloHome</h1>'

@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'

@app.route('/test')
def test_url_for():
    # 下面是一些调用示例（访问 http://localhost:5000/test 后在命令行窗口查看输出的 URL）：
    print(url_for('hello'))  # 生成 hello 视图函数对应的 URL，将会输出：/
    # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
    print(url_for('user_page', name='greyli'))  # 输出：/user/greyli
    print(url_for('user_page', name='peter'))  # 输出：/user/peter
    print(url_for('test_url_for'))  # 输出：/test
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'



if __name__ == '__main__':
    app.run(debug=True)