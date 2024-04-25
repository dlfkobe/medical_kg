from flask import Flask, request,jsonify,send_from_directory, render_template, request, redirect, url_for, flash,session
import requests
from chatbot_graph import ChatBotGraph
from flask_mysqldb import MySQL
import os
from functools import wraps
from flask_cors import CORS

# 问答处理器实例
handler = ChatBotGraph()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
CORS(app)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'medical_kg'
app.config['MYSQL_PORT'] = 3307

mysql = MySQL(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:  # 假设你将用户ID存储在session中
            return redirect(url_for('login'))  # 如果没有登录，则重定向到登录页面
        return f(*args, **kwargs)
    return decorated_function
@app.route('/api/tryChat', methods=['GET', 'POST'])
def tryChat():
    a = request.form.get('mydata')
    print(a)
    if a is None:
        return jsonify({'error': 'No input data provided.'}), 400
    
    # 使用你的问答处理器生成回答
    answer = handler.chat_main(a)
    print(answer)
    
    # return jsonify({'answer': answer})
    return answer

@app.route('/')
@login_required 
def search():
    return send_from_directory('templates', 'ChatBot.html')


# 确保在HTML模板中添加了相应的表单字段名，与这里的变量名匹配
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form.get('User')
        email = request.form.get('Email')
        password = request.form.get('Password')

        # 这里应添加数据验证和密码加密逻辑

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username FROM users WHERE username = %s", (user,))
        existing_user = cursor.fetchone()
        cursor.close()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('Login.html')

        # 假设用户不存在，继续注册逻辑
        try:
            # ... 省略的数据库插入和密码加密逻辑
            flash('You have successfully registered and can now log in', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print(e)
            return redirect(url_for('login'))
            # ... 省略的异常处理和回滚逻辑
    return render_template('Login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('User')
        password = request.form.get('Password')

        # 这里应添加密码验证逻辑

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (user, password))
        user = cursor.fetchone()
        print(user)
        cursor.close()
        
        if user:
            # 登录成功逻辑
            # flash('Login successful.', 'success')
            session['user_id'] = user
            print("成功！")
            return redirect('/')  # 重定向到主页路由
        else:
            flash('Login failed. Check your credentials', 'danger')

    return render_template('Login.html')

if __name__ == '__main__':
    app.run(debug=True)