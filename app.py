
from datetime import datetime
import datetime#DBあったらいらないかも？
import psycopg2.extras
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random
import numpy as np
from flask import Flask,render_template, request, redirect, url_for #pip install flask

import psycopg2 #pip install psycopg2

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)
d = now.strftime('%Y-%m-%d')

app = Flask(__name__)
connection = psycopg2.connect(host='localhost',
                             user='postgres',
                             password='apple2224',
                             database='testdb')
session = {"loggedin": None,
            "username": "",
            "user_id": ""
            }

@app.route('/register', methods=["GET", "POST"])
def register():
    # if session["loggedin"] == True:
        if request.method=="GET":
            params = {
                "msg": ""
            }
            return render_template("form.html",params=params)
        elif request.method=="POST":
            params = {
                "msg": ""
            }
            try:
                if len(request.form["ID"]) != 6 and len(request.form["password"]) != 4:
                    params["msg"] = "IDは数字6桁、パスワードは数字４桁に設定してください"
                    return render_template("form.html",params=params)
                elif len(request.form["ID"]) != 6:
                    params["msg"] = "ID数字6桁にしてください"
                    return render_template("form.html",params=params)
                elif len(request.form["password"]) != 4:
                    params["msg"] = "パスワードは数字４桁にしてください"
                    return render_template("form.html",params=params)
                else:
                    password = int(request.form["password"])
            except:
                    params["msg"] = "パスワードは数字４桁にしてください"
                    return render_template("form.html",params=params)
            values = [[request.form["ID"], request.form["password"]]]

            with connection:
                with connection.cursor() as cursor:
                    sql = f'insert into users(id, password) values (%s, %s)'
                    try:
                        cursor.executemany(sql, values)
                    except psycopg2.errors.UniqueViolation:
                        params["msg"] = "このIDは既に存在しています。"
                        return render_template("form.html", params=params)
                    except psycopg2.errors.InvalidTextRepresentation:
                        params["msg"] = "IDに数字以外の文字が含まれています"
                        return render_template("form.html", params=params)
                    except psycopg2.errors.NumericValueOutOfRange:
                        params["msg"] = "IDが長すぎます,10文字以下にしてください"
                        return render_template("form.html", params=params)
                connection.commit()
            cursor.close()
        return render_template('register_complete.html')
    # return redirect(url_for("login"))
@app.route("/")
def access():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="GET":
        params = {
            "msg": ""
        }
        return render_template("login.html", params=params)
    elif request.method=="POST":
        params = {
            "ID": request.form["ID"],
            "password": request.form["password"],
            "msg": "ログインが完了しました"
        }
        with connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute("select * from users where id = %s and password = %s", (params["ID"], params["password"],))
                    rows = cursor.fetchall()

                    try:
                        id = rows[0][0]
                        password = rows[0][1]
                        if id == int(params["ID"]) and password == params["password"]:
                            session["loggedin"] = True
                            session["username"] = "DBについかする"
                            session["user_id"] = id
                            return render_template("index.html", params=params)  
                        elif len(id) != 6 or len(password) != 4: 
                            params["msg"] = "IDかパスワードのどちらかが間違っています"
                            return render_template("login.html", params=params)
                    except IndexError:
                        params["msg"] = "IDかパスワードのどちらかが間違っています"
                        return render_template("login.html", params=params)
                except (psycopg2.errors.InvalidTextRepresentation, psycopg2.errors.NumericValueOutOfRange):
                    params["msg"] = "IDかパスワードのどちらかが間違っています"# 書き換え
                    return render_template("login.html", params=params)
                # except psycopg2.errors.NumericValueOutOfRange:
                #     params["msg"] = "IDかパスワードのどちらかが間違っています"
                #     return render_template("login.html", params=params)
                
    return render_template("index.html", params=params)



students = [
            {"id":"2004230011", "name":"西結都","test":{"test1": ""},"note":"", "date":{"2022-09-01":"attend","2022-09-02":"attend","2022-09-03":"attend","2022-09-04":"attend","2022-09-05":"absence"},"rate":"","rate_history":{"1":"100", "2":"100","3":"66.7","4":"75",}},
            {"id":"2222222222", "name":"古賀慶次郎","test":{"test1": ""},"note":"", "date":{"2022-09-01":"absence","2022-09-02":"attend","2022-09-03":"attend","2022-09-04":"absence","2022-09-05":"attend"},"rate":"","rate_history":{"1":"100", "2":"100","3":"66.7","4":"75",}},
            {"id":"3333333333", "name":"中村太一","test":{"test1": ""},"note":"", "date":{"2022-09-01":"absence","2022-09-02":"attend","2022-09-03":"absence","2022-09-04":"absence","2022-09-05":"absence"},"rate":"","rate_history":{"1":"0", "2":"50","3":"66.7","4":"75",}},
            ]
#### test
for student in students:
    attend = 0
    total = len(student["date"])
    for key, value in student["date"].items():
        if value=="attend":
            attend += 1
    student["rate"] = str(round(attend / total * 100, 1))
    student["rate_history"][f'{len(student["date"])}'] = student["rate"]
    



test_names = {
    "test1": "test1"
}

@app.route("/logout")
def logout():
    session["loggedin"] = None
    session["user_id"] = None
    session["username"] = None
    return redirect(url_for('login'))

@app.route("/student_list", methods=["GET", "POST"])
def student_list():

    if session["loggedin"] == True:
        if request.method=="GET":
            msg = ""
            ##############
            params = {
                "students": students,#データベースからもってくる
                "test_names": test_names,
                "msg":msg
            }
            return render_template("student_list.html", params=params)          
    return redirect(url_for("login"))  

@app.route("/add_test", methods=["GET", "POST"])
def add_test():
    if session["loggedin"] == True:
        if request.method=="GET":
            #############
            for student in students:
                student["test"][f"test{len(student['test'])+1}"] = ""
                test_names[f"test{len(student['test'])}"] = "test"+str(len(student["test"]))
                print(test_names)
                msg=""
                params = {
                    "students" : students,
                    "test_names": test_names,
                    "msg": msg
                }
            return render_template("student_list.html", params=params)
    return redirect(url_for("login"))


@app.route("/delete_test", methods=["GET", "POST"])
def delete_test():
    if session["loggedin"] == True:
        if request.method=="GET":
            msg=""
            #############
            for student in students:
                try:
                    student["test"].popitem()
                except KeyError:
                    msg = "消せるテスト項目がありません"
            try:        
                test_names.popitem()
            except KeyError:
                pass
            params = {
                "students" : students,
                "test_names": test_names,
                "msg": msg
            }
            return render_template("student_list.html", params=params)
    return redirect(url_for("login"))


@app.route("/edit_score", methods=["GET", "POST"])
def edit_score():
    if session["loggedin"] == True:
        msg = ""
        if request.method=="POST":
            ###########
            for student in students:
                if student["id"] == request.form["id"]:
                    for i in range(1, len(student["test"])+1):
                        print(request.form.get(f"test{i}"))
                        student["test"][f"test{i}"] = request.form.get(f"test{i}")
                    student["note"] = request.form["note"]    
                    break
            #dbにinsert
            params = {
                "students": students,
                "test_names": test_names,
                "msg": msg
            }             
        return render_template("student_list.html", params=params)        
    return redirect(url_for("login"))

@app.route("/edit_test_name", methods=["POST"])
def edit_test_name():
    msg = ""
    if session["loggedin"] == True:
        if request.method=="POST":
            ########
            for i in range(1, len(students[0]["test"])+1):
                if len(request.form[f"test{i}_name"]) <= 20:
                    test_names[f"test{i}"] = request.form[f"test{i}_name"]

                else:
                    msg = "テストの名前は20文字以下に設定してください"
       
        #dbにinsert
        print(test_names["test1"])
        params = {
            "students": students,
            "test_names": test_names,
            "msg": msg
        }             
        return render_template("student_list.html", params=params)        
    return redirect(url_for("login"))


    #### test
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
x = np.arange(0, len(student["date"]), 0.1)
y = x**2

@app.route("/view_profile/<student_id>",methods=["GET","POST"])
def view_profile(student_id):
    if session["loggedin"] == True: 
        if request.method=="GET":
            plt.cla()
            fig.suptitle("title", fontsize="24")

            ax1.set_title("test")
            ax1.grid()
            ax1.set_xlabel('x',fontsize=16)
            ax1.set_ylabel('y1',fontsize=16)
            ax1.plot(x, y)
            
            canvas = FigureCanvasAgg(fig)
            png_output = BytesIO()
            canvas.print_png(png_output)
            data = png_output.getvalue()
            for student in students:
                if student["id"] == student_id:
                    print("a")
                    params = {
                         "student": student,
                         "image": data
                    }
                    return render_template("student_detail.html", params=params)
        if request.method=="POST":    
            print("B")
    return redirect(url_for("login"))
    
    
if __name__ == "__main__":
    app.run(port=12345, debug=True) #12345でerrorがでたら8000にする


