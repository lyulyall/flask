from flask import Flask, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


@app.route('/users')
def index():
    user = Users.query.all()
    return render_template("index.html", user=user)


@app.route('/user/<int:id>')
def user_n(id):
    user = Users.query.get(id)
    return render_template("user_n.html", user=user)


@app.route('/add-user', methods=['POST', 'GET'])
def add_user():
    user = Users.query.all()
    if request.method == "POST":
        new_user = Users(name=request.form['name'], surname=request.form['surname'], age=request.form['age'],
                         email=request.form['email'], password=generate_password_hash(request.form['password']))

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/users')
        except:
            return "При добавлении пользователя произошла ошибка"
    else:
        return render_template("add-user.html", user=user)


@app.route('/upd-user/<int:id>', methods=['POST', 'GET'])
def upd_user(id):
    user = Users.query.get(id)
    hash_password = generate_password_hash(request.form['password'])
    if request.method == "POST":
        user.name = request.form['name']
        user.surname = request.form['surname']
        user.age = request.form['age']
        user.email = request.form['email']
        user.password = hash_password

        try:
            db.session.commit()
            return redirect('/users')
        except:
            return "При редактировании пользователя произошла ошибка"
    else:
        return render_template("upd-user.html", user=user)


@app.route('/del-user/<int:id>')
def user_del(id):
    user = Users.query.get_or_404(id)

    try:
        db.session.delete(user)
        db.session.commit()
        return redirect('/users')
    except:
        return "При удалении пользователя произошла ошибка"


if __name__ == "__main__":
    app.run(debug=True)
