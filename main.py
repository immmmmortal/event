from flask import Flask, render_template, request, url_for, Response

app = Flask(__name__)  # application

main_menu = [{"name": "Регистрация", "url": "registration"},
             {"name": "See user`s info", "url": "user_info"}]  # elements of top navigation
user_data = []  # array to store users info


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
            f.write(str(input_email) + ":" + str(input_psw) + "\n")
        user_data.append((input_email + ":" + input_psw))  # adding all registered users to array

    fo = open("users.log", "w+")  # write all users to "users.log"
    for element in user_data:
        fo.write(element + "\n")

    fo.close()

    return render_template("registration.html", main_menu=main_menu)


@app.route('/user_info')
def users_info():  # return read "users.log"
    with open("users.log", 'r') as f:
        content = f.read()
    return Response(content, mimetype='text/plain')


if __name__ == "__main__":
    app.run(debug=True)  # runs application
