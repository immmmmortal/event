from flask import Flask, render_template, request, url_for, Response
from flask_paginate import get_page_args, Pagination
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True)
    password = db.Column(db.String(24), index=True)


main_menu = [{"name": "Регистрация", "url": "registration"},
             {"name": "See user`s info", "url": "user_info"}]  # elements of top navigation
users = []  # array to store users info


@app.route('/')  # main page
def index():  # function that returns html page
    print(url_for('index'))
    return render_template("index.html", main_menu=main_menu)


@app.route('/registration', methods=["POST", "GET"])  # registration page
def registration():  # function that process data from html form to python
    if request.method == "POST":
        input_email = request.form['email']
        input_psw = request.form['psw']

        with open("user_info.txt", "w") as f:  # stores values per user
            f.write("{},{}".format(input_email, input_psw))
        temp_userdata = [input_email, input_psw]
        users.append(temp_userdata)  # adding all registered users to array

    fo = open("users.log", "w+")  # write all users to "users.log"
    for element in users:
        fo.write(str(element) + '\n')
    fo.close()

    return render_template("registration.html", main_menu=main_menu)


@app.route('/user_info', methods=["POST", "GET"])
def users_info():  # return read "users.log"
    input_per_page = request.form.get('per_page', False)

    def get_users(users_offset=0, users_per_page=3):
        return users[users_offset: users_offset + users_per_page]

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(users)
    pagination_users = get_users(users_offset=offset, users_per_page=int(input_per_page))
    pagination = Pagination(page=page, input_per_page=input_per_page, total=total, css_framework='bootstrap4')

    return render_template('user_info.html', page=page, per_page=50, pagination=pagination,
                           users=pagination_users, number=len(users), apps=users, aws_region='eu-west-1',
                           cloudwatch_log_stream='docker-swarm-lg')


if __name__ == "__main__":
    app.run(debug=True)  # runs application
