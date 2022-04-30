from distutils.command.config import config
import re
from threading import local
from flask_app import app, DATABASE , bcrypt, cloudinary
from flask import render_template, request, redirect, session, flash
from flask_app.models.model_news import News
from flask_app.models.model_img import Image
from cloudinary import uploader



@app.route('/create/news')
def render_template_news():
    return render_template('create_news.html')


@app.route('/process/news', methods=['post'])
def create_news():
    print(request.form)
    if not News.validate(request.form):
        return redirect('/create/news')

    id = News.create(request.form)
    urldict = uploader.upload(request.files['img'])
    print(urldict)
    url = urldict['url']
    public_id = urldict['public_id']
    imgdata ={
        'url': url,
        'public_id': public_id,
        'post_id': id
    }

    Image.create(imgdata)

    return redirect(f'/preview/news/{id}')

@app.route('/preview/news/<int:id>')
def render_preview(id):
    news = News.get_one({'id': id})
    print(news)
    return render_template('preview_news.html', news = news)


@app.route('/edit/news/<int:id>')
def render_edit(id):
    news = News.get_one({'id': id})
    return render_template('edit_news.html', news = news)


@app.route('/view/news/<int:id>')
def render_news_view(id):
    news = News.get_one({'id': id})
    return render_template('view_news.html', news = news)

@app.route('/news/list')
def render_news_list():
    news = News.get_all()
    return render_template('news_list.html', new = news)


@app.route('/process/update/<int:id>', methods = ['post'])
def update_news(id):
    News.update_one(request.form)
    if hasattr(request, 'files'):
        Image.delete({'post_id': id})
        urldict = uploader.upload(request.files['img'])
        print(urldict)
        url = urldict['url']
        public_id = urldict['public_id']
        imgdata ={
            'url': url,
            'public_id': public_id,
            'post_id': id
        }
        Image.create(imgdata)
        return redirect (f'/preview/news/{id}')
    
    return redirect (f'/preview/news/{id}')

@app.route('/delete/<int:id>')
def delete_news(id):
    Image.delete({'post_id': id})
    News.delete_one({'id': id})
    return redirect('/')

@app.route('/render/allnews') #placeholder route to delete news
def render_all():
    return render_template('delete_news.html', new = News.get_all())