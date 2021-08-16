import os
from flask import Flask
from flask import render_template
from models import db
from flask import request # request 를 이용해서 요청정보를 확인 할 수있다.
from flask import redirect
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm

from models import Student
app = Flask(__name__)

# get 요청은 단순히 값을 보여주는것이고
# post 요청은 데이터를 가지고 오는 요청이다.
# 따라서, get과 post 인 경우를 구분해서 코드를 작성해야한다.
# 메서드가 기본적으로 get 만 되어있기 때문에,  methods=['GET', 'POST'] 로 post도 추가해준다.
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # form 안에서 validate_on_submit을 통해서 post 요청이 되었고, 유효성 검사가 잘 되었는지 한번에 확인 가능
    # 값이 정상적인지, 모든 값들을 확인하는 코드모두 필요없어짐
    if form.validate_on_submit():
        student_info = Student()
        student_info.studentid = form.data.get('studentid')
        student_info.studentname = form.data.get('studentname')
        student_info.password = form.data.get('password')

        db.session.add(student_info) # db에 넣겠다! 라는 의미
        db.session.commit()
        print('Success')

        return redirect('/')
    return render_template('register.html', form=form)

@app.route('/')
def hello():
    return render_template('hello.html')

# 파이썬 명령어로 실행할 수 있도록 아처럼 작성
if __name__ == '__main__':
    basedir = os.path.abspath(os.path.dirname(__file__))  # 현재 있는 파일의 dir
    dbfile = os.path.join(basedir, 'db.sqlite')

    # app관련 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '3fjwljflejflwjflejfef' # 원래는 복잡하게 해야함 지금은 임의적으로

    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app) # 다양한 app의 설정값들을 초기화 해줌
    db.app = app # app 을 명시적으로 넣어줄 수 있음.
    db.create_all() # 데이터 베이스 생성

    app.run(host='127.0.0.1', port=5000, debug=True)