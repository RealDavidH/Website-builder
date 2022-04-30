from flask_app import app, DATABASE , bcrypt
from flask import render_template, request, redirect, session, flash
from flask_app.models.model_calender import Calender
from flask_app.models.model_news import News
from flask_app.models.model_carousel import Carousel

@app.route('/')
def render_home():
    events = Calender.get_weekly_events()
    news = News.get_all()
    # carousel_imgs = Carousel.get_all() 
    print(events)
    return render_template('index.html', events = events, new = news)
