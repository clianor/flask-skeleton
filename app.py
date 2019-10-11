import os
from flask import Flask
from flask import redirect
from flask import session
from flask import render_template
from werkzeug.security import generate_password_hash
from models import db
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm, LoginForm

from models import Fcuser

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():  # Post요청이 되었는지 그리고 값이 정상적인지 확인.
        fcuser = Fcuser()
        fcuser.userid = form.data.get('userid')
        fcuser.username = form.data.get('username')
        fcuser.password = generate_password_hash(form.data.get('password'))

        db.session.add(fcuser)
        db.session.commit()  # 설정에서 commit 하도록 해두었기에 제외해도 무방.
        print("Success")

        return redirect('/')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['userid'] = form.data.get('userid')

        return redirect('/')

    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid', None)
    return redirect('/')

@app.route('/')
def hello():
    userid = session.get('userid', None)
    return render_template('hello.html', userid=userid)

if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))  # 파일이 있는 위치를 기본 디렉토리로 설정.
    dbfile = os.path.join(basedir, 'db.sqlite')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile  # sqlite 파일 위치
    # teardown이란 사용자 요청의 끝을 의미
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # teardown이 발생할때 db commit을 발생
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 수정사항에 대한 추적을 하지않겠다.
    app.config["SECRET_KEY"] = '1234hjkhksdhakjfhlxv'

    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app)
    db.app = app
    db.create_all()

    app.run(host='127.0.0.1', port=5000, debug=True)
