from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

# client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost', 27017)
db = client.dbhomework

## HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('Fourth Week HW.html')

# @app.route('/')
# def homeworks():
#     return render_template('First Week HW.html')



# quantity
# 주문하기(POST) API
@app.route('/order', methods=['POST'])
def save_order():
    name_receive = request.form['name_give']
    quantity_receive = request.form['quantity_give']
    address_receive = request.form['address_give']
    fir_phone_receive = request.form['fir_phone_give']
    sec_phone_receive = request.form['sec_phone_give']

    doc = {
        'name': name_receive, 'quantity': quantity_receive,
        'address': address_receive,
        'phone': "010 - " + fir_phone_receive + " - " + sec_phone_receive
    }

    if quantity_receive == "NaN":
        return jsonify({'msg': "수량을 확인하세요."})

    elif fir_phone_receive == "NaN":
        return jsonify({'msg': "전화번호를 확인하세요."})

    elif sec_phone_receive == "NaN":
        return jsonify({'msg': "전화번호를 확인하세요."})

    else:
        # print(doc)
        db.orders.insert_one(doc)
        return jsonify({'msg': "주문 완료!"})


# 주문 목록보기(Read) API
@app.route('/order', methods=['GET'])
def view_orders():
    orders = list(db.orders.find({}, {'_id': False}))
    return jsonify({'all_orders': orders})

#회원등록 페이지
@app.route('/signuppage')
def signuppage():
    return render_template('sign up.html')

#회원등록
@app.route('/sign_up', methods=['POST'])
def sign_up():

    id_receive = request.form['id_give']
    password_receive = request.form['password_give']
    # human_receive = request.form['human_give']
    targetID = db.accounts.find_one({'ID': id_receive}, {'_id': False})
    print(targetID)

    if targetID == None:
        doc = {
            "ID": id_receive, "PassWord": password_receive
        }
        # db.accounts.insert_one(doc)
        print(doc)
        return jsonify({'msg': "등록 성공!"})
    else:
        return jsonify({'msg': "아이디가 이미 있습니다. 확인해 주십시오."})

#아이디 중복확인
@app.route('/duplicate', methods=['POST'])
def duplicate():
    id_receive = request.form['id_give']
    targetID = db.accounts.find_one({'ID': id_receive}, {'_id': False})
    print(targetID)
    if targetID == None:
        return jsonify({'msg': "사용 가능한 아이디입니다."})
    else:
        return jsonify({'msg': "이미 있는 아이디입니다."})

#로그인 페이지
@app.route('/loginpage')
def loginpage():
    return render_template('Log In Page.html')

#로그인 기능
@app.route('/login', methods=['POST'])
def login():
    id_receive = request.form['id_give']
    password_receive = request.form['password_give']
    targetID = db.accounts.find_one({'ID': id_receive}, {'_id': False})
    if targetID == None:
        return jsonify({'msg': "존재하지 않는 아이디입니다."})
    elif targetID['PassWord'] == password_receive:
        return jsonify({'msg': "로그인 확인"})
    else:
        return jsonify({'msg': "비밀번호가 틀립니다."})

# @app.route('/qhsowk')
# def qhsowk():
#     return render_template('qhsorl.html')
#
# @app.route('/qhsorl', methods=['post'])
# def qhsoa():
#     qhsoa_receive = request.form['name_give']
#     return render_template('qkerl.html', qhsoa_receive=qhsoa_receive)
#
# @app.route('/qkewk', methods=['get'])
# def qkewk():
#     return render_template('qkerl.html', qhsoa_receive=qhsoa_receive)


# 로그인 성공후 페이지
@app.route('/mainpageconnec',  methods=['POST'])
def mainpageconnec():
    if request.method == 'POST':
        ID_receive = request.form['id_give']
        # return render_template('Main Page.html', ID=ID_receive)
        return render_template('Main Page.html', ID=ID_receive)
    else:
        pass

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)