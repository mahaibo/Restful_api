#!/usr/bin/env python
import os
from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

# initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# extensions
db = SQLAlchemy(app)
auth = HTTPBasicAuth()


class Crawlebus(db.Model):
    __tablename__ = 'crawlebus'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), index=True)
    link = db.Column(db.String(255), index=True)
    desc = db.Column(db.String(255), index=True)


@app.route('/api/crawlebus', methods=['POST'])
def new_crawlebus():
    title = request.json.get('title')
    if title is None:
        abort(400)    # missing arguments
    link = request.json.get('link')
    if link is None:
        abort(400)    # missing arguments
    desc = request.json.get('desc')
    if desc is None:
        abort(400)    # missing arguments
    if Crawlebus.query.filter_by(title=title).first() is not None:
        abort(400)    # existing crawlebus
    
    save_crawlebus(title, link, desc)
    return (jsonify({'title': crawlebus.title, 'link': crawlebus.link, 
        'desc': crawlebus.desc}), 201,
            {'Location': url_for('get_crawlebus', id=crawlebus.id, _external=True)})

def save_crawlebus(title, link, desc):
    crawlebus = Crawlebus(title=title, link=link, desc=desc)
    db.session.add(crawlebus)
    db.session.commit()

@app.route('/api/crawlebus/<int:id>')
def get_crawlebus(id):
    crawlebus = Crawlebus.query.get(id)
    if not crawlebus:
        abort(400)
    return jsonify({'title': crawlebus.title, 
        'link': crawlebus.link, 
        'desc': crawlebus.desc})


if __name__ == '__main__':
    # if not os.path.exists('db.sqlite'):
    db.create_all()
    app.run(debug=True)