from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy  # 导入扩展类
import os
import sys
import click


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)

@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html' ,movies=movies)

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)


class User(db.Model):# 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)# 主键
    name = db.Column(db.String(20)) # 名字



class Movie(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()
    name = 'Sep'
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
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')





@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404




@app.cli.command() # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')