from flask_app import app, DATABASE , bcrypt
from flask import render_template, jsonify, request, redirect, session, flash
from flask_app.models.model_calender import Calender

@app.route('/create/event')
def render_form():
    return render_template('create_event.html')

@app.route('/process/event', methods =['post'])
def create_event():
    print(request.form)
    id = Calender.addevents(request.form)
    print(id)
    return redirect('/')

@app.route('/render/eventlist')
def render_list():
    events = Calender.get_all_events()
    return render_template('delete_event.html', events = events)

@app.route('/delete/<id>')
def delete_event(id):
    Calender.delete_event(id)
    return redirect('/')