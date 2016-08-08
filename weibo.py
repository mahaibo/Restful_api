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


class Weibo(db.Model):
    __tablename__ = 'weibos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), index=True)

@app.route('/api/weibos', methods=['POST'])
def new_weibo():
    title = request.json.get('title')
    if title is None:
        abort(400)    # missing arguments
    if Weibo.query.filter_by(title=title).first() is not None:
        abort(400)    # existing weibo
    weibo = Weibo(title=title)
    db.session.add(weibo)
    db.session.commit()
    return (jsonify({'title': weibo.title}), 201,
            {'Location': url_for('get_weibo', id=weibo.id, _external=True)})

@app.route('/api/weibos/<int:id>')
def get_weibo(id):
    weibo = Weibo.query.get(id)
    if not weibo:
        abort(400)
    return jsonify({'title': weibo.title})


if __name__ == '__main__':
    # if not os.path.exists('db.sqlite'):
    db.create_all()
    app.run(debug=True)