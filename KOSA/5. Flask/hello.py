# _*_ coding : utf-8 _*_

from flask import Flask, request, session, render_template, redirect, url_for, abort, make_response

import member


app = Flask(__name__)


## http://127.0.0.1:5000/  < 기본! / 실행하면 아래 함수가 실행됨
@app.route('/')
def hello_world():
    print(member.get_emp(103))
    return render_template("hello.html",name=member.get_emp(103))
    #return render_template('hello.html',name="홍길동")  # {{name}}
    #return "hello world!"






# url에 값전달하는 변수 <> 를 pathvalue 라고 함. 실제 사용자 이름을 적음 이게 함수의 인수로 전달됨
# url 패턴과 POST method 를 정의하고 바단 하단의 함수에서 url 패턴 매칭되는 action 을 처리 int는 정로만 입력가능
@app.route('/user/<username>')
def showUserProfile(username):
    app.logger.debug("RETRIEVE DATA - USER ID : %s" % username) #app.logger 은 많아도 상관 없음. 이름을 가짐
    app.logger.debug("RETRIEVE DATA - Check Compelete")
    app.logger.warn("RETRIEVE DATA - Warning... User Not Found.")
    app.logger.error("RETRIEVE DATA - ERR! User unauthenification.") # 4개는 구동하는..아이..알필요 x
    return "USER : %s" % username # 이부분은 탬플릿을 이용해서 html을 가져올 수 있음


# 자바로 웹을 구연하고 파이썬으로 분석하는 모델을 구연하면
##  get url을 통해 가지고오고 post 방식은 insert 값을 요청받아서 쓰는것.
# URL 은 동일하나, methods 에 따라서 요청방식이 다름.
# put 은 업데이트 용도로 사용 . delect 는 삭제.


# 로그인 처리하기 로그인 하기위한 양식을 나에게 줘라! 라는 의미
@app.route('/account/login', methods= ["GET"])
def login_form():
    return render_template('login.html')


# post방식으로 요청이 일어날때, 이것이 실행됨을 의미함
# 내부에 methods 항목을 통해 받은 REST Action Type 을 지정 .
# 지정 이외의 Action Type을 사용하면 Flask가 405에러를 출력
# if 를 넣는 이유는 잘못된 접근을 알리기 위해서,
@app.route('/account/login', methods = ["POST"])
def login():
    if request.method == "POST": # request모둘에서post한 파라미터 값을 가져오기 / 요청방법을 알아냄을 의미 .
        userId = request.form['id'] # 로 사용시 id파라미터가 없으면 flask가 400에러 출력
        pw = request.form['pw'] # 원래는 데이터 베이스와 비교를 해야함. 조회할 행이 있으면 아이디 나 pw 가 있는 것.- 인증됨.
        # 인증된 정보가 있다면, session에 그 정보를 저장해야함.
        # session 아이디는 서버에 의해서 자동으로 만들어짐.

        if len(userId) == 0 or len(pw) == 0 :
            return render_template("error.html",msg = userId +', '+pw+ '로그인 정보를 제대로 입력하지 않았습니다.')  # 여기서는 db를 연결하지 않고 그냥 return했으나, 원래는 디비로 넘어가야함.
        session['logFlag'] = True # 이렇게 트루 해줌.
        session['userId'] = userId #session 을 사용해서, 저장을 해주는 것같음.
        #return session['userId']+' 님 환영합니다.'
        return render_template("login.html", id=userId) # login.html에서 사용할 ,id 를 명시해줌

    else:
        #return '잘못된 접근입니다.'
        return render_template("error.html", msg = "잘못된 접근업니다.")


# session 을 사용하려면 반.드.시. 넣어 줘야함.! 오른쪽 값은 내가 원하는 것을 넣어줘도 됨.
# 세션 키를 생성하며, 로그인과 같이 세션을 맺는 경우 필수적으로 넣어야한다.
# 세션 생성시, app.secret_key로 키를 생성하지 않으면 flask가 500 에러를 출력
app.secret_key = "sample_secreat_key"


@app.route('/user', methods = ["GET"])  # 로그인 정보 가져오기
# post 는 데이터를 주는 것을 의미. 다른것도 있긴함. 근데 get , post가 99%를 차지함.  # get 은 정보를 받는 것
def getUser():
    if session.get('logFlag') != True: # 트루가 아니면 , 로그인을 안한것.
        return '잘못된 접근입니다.' # 에러페이지 만들어놓고 error. html 연결
    userId = session['userId']
    return '[GET][USER] USER ID : {0}'.format(userId)

"""
@app.route('/user', methods = ['GET']) # 위에도 있는데?
def getUser():
    if 'userId' in session:
        return '[GET][USER] USER ID : {0}'.format(session['userId'])
    else:
        abort(400) # abort를 사용하면 특정 error를 발생시킬 수 있다. import해야함
"""


@app.route('/account/logout', methods =['POST','GET']) # 로그아웃
def logout():
    session['logFlag'] = False
    session.pop('userId', None) # 유저아이디를 삭제함을 의미. 유저아이디값을 반환.
    # 만약 값이 없을 때는 ,none이 바환됨.
    return redirect(url_for('login')) # 로그아웃하면 ,메인페이지로 다시 되돌아감.

# return redirect("/account/login")  함수를 이용하거나, url 이용해서 할수 있음.
# redirect는 내가 지정한 어떤 함수로 돌아가는 것을 의미.
# werkzeug.routing.BuildError : 경로가 지정되어있지 않다는 오류, 아직 main 함수 만들기 전.
# redirect()를 활용하면 사용자의 조회 위치를 변경할수 있다.
# url_for()는 route 주소로 이동하는 것이 아닌 정의된 함수!!를 호출한다.
#session.clear()를 사용하면 따로 설정 필요없이 session을 비울 수 있다.


@app.errorhandler(400) # 특정 에러를 catch및 처리 할수 있다.
def uncaughtError(error):
    return '잘못된 사용입니다.'





@app.errorhandler(404) # make_response()함수를 통해 반환되는 object를 만들고 이를 처리가능할수 있게 한다.
def not_found(error):
    res = make_response(render_template('error.html'))
    res.headers['X-Something'] = 'A value'
    return res


@app.route('/login', methods= ['POST','GET'])
def login_direct():
    # flask redirect처리 특정 url alias 등 redirect가 필요한데,
    # post 데이터를 같이 보내어서 redirect 를 하려면
    # url_for() 함수를 사용시, 상태 코드 값을 같이 보내어야 함.
    if request.method == "POST":
        return redirect(url_for('login'), code=307)
    else:
        return redirect(url_for('login'))





if __name__ == "__main__": # 항상 파이썬 코드의 아래에 있어야함
    # 파이썬은 전부다 함수이기 때문에, 함수가 정의가 되어있어야, 호출이 가능함.
    app.debug = True     # app.debug 는 개발의 편의를 위해서 존재
    # True 값의 경우 코드를 변경하면 자동으로 서버가 재 실행됨.
    # 웹상에서 파이썬 코드를 수행할 수 있게 되므로, 운영환경에서 사용을 유의해야함
    app.run()
    # 현재 접근은 개발 소스가 존재하는 로컬에서만 접근 가능 ,
    # 외부에서도 접근을 가능하게 하려면, app.run(host="0.0.0.0")로 서버 실행 부를 변경해야함.

