
from datetime import datetime
import datetime
from unittest.mock import patch#DBあったらいらないかも？
import psycopg2.extras
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib  # <--ここを追加
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg
import pandas as pd
import numpy as np
from flask import Flask,render_template, request, redirect, url_for ,make_response
import japanize_matplotlib
import re
#pip install flask

import psycopg2 #pip install psycopg2

# DBに日付を追加するときのため
t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)
d = now.strftime('%Y-%m-%d')

app = Flask(__name__)
connection = psycopg2.connect(host='localhost',
                             user='postgres',
                             password='apple2224',
                             database='testdb')

# ログイン認証
session = {"loggedin": None,
            "username": "",
            "user_id": ""
            }

@app.route('/register', methods=["GET", "POST"])
def register():
    # if session["loggedin"] == True:
        if request.method=="GET":
            # パラメータの設定
            params = {
                "msg": "",
                "ID": "",
                "name": "",
                "name_sub":"",
                "age":"",
                "password":"" ,
                "password2":"",
            }
            return render_template("register.html",params=params)
        elif request.method=="POST":
            # パラメータの設定
            params = {
                "msg": "",
                "ID": request.form["ID"],
                "name": request.form["teacher_name"],
                "name_sub": request.form["name_sub"],
                "age": request.form["age"],
                "password": request.form["password"],
                "password2": request.form["password2"]
            }
            try:
                if len(str(request.form["ID"])) != 6 and len(str(request.form["password"])) != 4:
                    params["msg"] = "IDは数字6桁、パスワードは数字４桁に設定してください"
                    return render_template("register.html",params=params)
                elif re.compile('[0-9]+').fullmatch(request.form["teacher_name"]) == None and re.compile('[０-９]+').fullmatch(request.form["teacher_name"]) != None and re.compile('[ａ-ｚＡ-Ｚ]+').fullmatch(request.form["teacher_name"]) != None:
                    params["msg"] = "名前を正しく入力してください"
                    return render_template("register.html",params=params)
                elif re.compile('[\u3041-\u309F]+').fullmatch(request.form["name_sub"]) == None:
                    params["msg"] = "ふりがなをひらがなで入力してください"
                    return render_template("register.html",params=params)
                elif len(str(request.form["ID"])) != 6:
                    params["msg"] = "ID数字6桁にしてください"
                    return render_template("register.html",params=params)
                elif len(str(request.form["password"])) != 4:
                    params["msg"] = "パスワードは数字４桁にしてください"
                    return render_template("register.html",params=params)
                elif request.form["password"] != request.form["password2"]:
                    params["msg"] = "パスワードが同じではありません"
                    return render_template("register.html",params=params)
                elif re.compile('[0-9]+').fullmatch(request.form["age"]) == None:
                    params["msg"] = "年齢に文字が含まれています"
                    return render_template("register.html", params=params)
                elif len(request.form["age"]) != 2:
                    params["msg"] = "年齢を正しく入力してください"
                    return render_template("register.html",params=params)
                else:
                    password = int(request.form["password"])
            except:
                    params["msg"] = "パスワードは数字４桁にしてください"
                    return render_template("register.html",params=params)
            values = [[request.form["ID"], request.form["password"], request.form["teacher_name"],request.form["name_sub"], int(request.form["age"]), request.form["gender"], 2 ,1]]

            with connection:
                with connection.cursor() as cursor:
                    sql = f'insert into teacher(teacher_id, password, name ,name_sub ,age, gender, subject_id, major_id ) values (%s, %s, %s, %s, %s, %s, %s, %s)'
                    try:
                        cursor.executemany(sql, values)
                    except psycopg2.errors.UniqueViolation:
                        params["msg"] = "このIDは既に存在しています。"
                        return render_template("register.html", params=params)
                    except psycopg2.errors.InvalidTextRepresentation:
                        params["msg"] = "IDに数字以外の文字が含まれています"
                        return render_template("register.html", params=params)
                    except psycopg2.errors.NumericValueOutOfRange:
                        params["msg"] = "IDが長すぎます,10文字以下にしてください"
                        return render_template("register.html", params=params)
                connection.commit()
            cursor.close()
        return render_template('register_complete.html')
    #  return redirect(url_for("login"))
# @app.route("/")
# def access():
#     # return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="GET":
        # パラメータの設定
        params = {
            "msg": ""
        }
        return render_template("login.html", params=params)
    elif request.method=="POST":
        # パラメータの設定
        params = {
            "ID": request.form["ID"],
            "password": request.form["password"],
            "msg": "ログインが完了しました"
        }
        # データベースに接続
        with connection:
            with connection.cursor() as cursor:
                try:
                    # データベースから値を選択
                    cursor.execute("select * from teacher where teacher_id = %s and password = %s", (params["ID"], params["password"],))
                    rows = cursor.fetchall()

                    try:
                        print(rows)###### 消す
                        print(rows[0])###### 消す
                        id = rows[0][1]
                        password = rows[0][-1]
                        name = rows[0][2]
                        print(id)###### 消す
                        # IDとPASSWORDが一致した場合
                        if id == params["ID"] and password == params["password"]:
                            # ログイン認証
                            session["loggedin"] = True
                            session["username"] = name
                            session["user_id"] = id
                            print(session["user_id"])###### 消す
                            print(id)###### 消す
                            params = {
                                "ID": request.form["ID"],
                                "password": request.form["password"],
                                "msg": "ログインが完了しました",
                                "user": session["user_id"]
                            }
                            return render_template("home.html", params=params)  
                            # ID, password が6文字と４文字以外の場合
                        elif len(id) != 6 or len(password) != 4: 
                            params["msg"] = "IDかパスワードのどちらかが間違っていますaaaaaaaa"
                            return render_template("login.html", params=params)
                    except IndexError:
                        params["msg"] = "IDかパスワードのどちらかが間違っていますvbbbbbbbbbbb"
                        return render_template("login.html", params=params)
                except (psycopg2.errors.InvalidTextRepresentation, psycopg2.errors.NumericValueOutOfRange):
                    params["msg"] = "IDかパスワードのどちらかが間違っていますcccccccccccc"# 書き換え
                    return render_template("login.html", params=params)
                # except psycopg2.errors.NumericValueOutOfRange:
                #     params["msg"] = "IDかパスワードのどちらかが間違っています"
                #     return render_template("login.html", params=params)
                
    return render_template("home.html", params=params)



students = [
            {"id":"2004230011", "name":"西結都","test":{"test1": ""},"note":"", "date":{"2022-09-01":"attend","2022-09-02":"attend","2022-09-03":"absence","2022-09-04":"attend","2022-09-05":"attend"},"rate":"","rate_history":{"2022-09-01":100, "2022-09-02":100,"2022-09-03":66.7,"2022-09-04":75,}},
            {"id":"2222222222", "name":"古賀慶次郎","test":{},"note":"", "date":{"2022-09-01":"absence","2022-09-02":"attend","2022-09-03":"attend","2022-09-04":"absence","2022-09-05":"attend"},"rate":"","rate_history":{"2022-09-01":100, "2022-09-02":100,"2022-09-03":66.7,"2022-09-04":75,}},
            {"id":"3333333333", "name":"中村太一","test":{},"note":"", "date":{"2022-09-01":"absence","2022-09-02":"attend","2022-09-03":"absence","2022-09-04":"absence","2022-09-05":"absence"},"rate":"","rate_history":{"2022-09-01":0, "2022-09-02":50,"2022-09-03":66.7,"2022-09-04":75,}},
            ]
#### test
test_name = {
    "test1": "as"
}
for student in students:
    attend = 0
    total = len(student["date"])
    for key, value in student["date"].items():
        if value=="attend":
            attend += 1
        last_key_name = key
    student["rate"] = round(attend / total * 100, 1)
    student["rate_history"][f'{last_key_name}'] = student["rate"]
    



test_names = {
}

@app.route("/logout")
def logout():
    session["loggedin"] = None
    session["user_id"] = None
    session["username"] = None
    return render_template("login.html")

@app.route("/student_list", methods=["GET", "POST"])
def student_list():

    # if session["loggedin"] == True:
        if request.method=="GET":
            msg = ""
            ##############
            subject = request.form["subject"]
            #subject がある学生でーたを持ってくる
            with connection:
                with connection.cursor() as cursor:
                    try:
                        # データベースから値を選択
                        cursor.execute("select student_id, name FROM student where subject = %s", (subject))
                        rows = cursor.fetchall()
                        print(rows)
                    except:
                        print("a")
            #f"select student_id, name, subject_id FROM student where subject = {subject}"
            # パラメータの設定
            params = {
                "students": students,#データベースからもってくる
                "test_names": test_names,
                "msg":msg
            }
            return render_template("student_list.html", params=params)  
        if request.method=="POST":
            msg = ""
            ##############
            subject = request.form["subject"]
            #subject がある学生でーたを持ってくる
            with connection:
                with connection.cursor() as cursor:
                    try:
                        # データベースから値を選択
                        cursor.execute("select student_id, name FROM student where subject = %s", (subject))
                        rows = cursor.fetchall()
                        print(rows)
                    except:
                        print("a")
            #f"select student_id, name, subject_id FROM student where subject = {subject}"
            # パラメータの設定
            params = {
                "students": students,#データベースからもってくる
                "test_names": test_names,
                "msg":msg
            }
            return render_template("student_list.html", params=params)             

    #return redirect(url_for("login"))  

@app.route("/add_test", methods=["GET", "POST"])
def add_test():
    # if session["loggedin"] == True:
        if request.method=="GET":
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAA")
        if request.method == "POST":
            name = request.form["test_name"]
            values = [[name, ""]]
            with connection:
                with connection.cursor() as cursor:
                    print(name)
                    sql = f'insert into test(test_name, test_score) values (%s, %s);'
                    try:
                        cursor.executemany(sql, values)
                    except:
                        pass
                connection.commit()
            cursor.close()

            students_list = {

            }
            with connection:
                with connection.cursor() as cursor:
                    try:
                        # データベースから値を選択
                        cursor.execute("SELECT test_name, test_score FROM test")
                        rows2 = cursor.fetchall()
                        cursor.execute("SELECT student_id, name from student")
                        rows = cursor.fetchall()
                        print(rows2,"row2")
                        print(rows,"row")
                        students_list = []
                        try:
                            for i, row in enumerate(rows):
                                student_id = row[0]
                                student_name = row[1]
                                ### 複数要素あるものはAPPEND  students_list.append({"test":{},"something":{}})
                                students_list.append({"test":{}})
                                students_list[i]["name"] = student_name
                                students_list[i]["student_id"] = student_id
                                for j, row in enumerate(rows2):
                                    test_name = row[0]
                                    test_score = row[1]
                                    students_list[i]["test"][test_name] = test_score
                                    print(students_list)
                            
                        except:
                            pass
                    except:
                        pass
                msg=""
            #     # パラメータの設定
                params = {
                    "students" : students_list,
                    # "test_names": test_names,
                    "msg": msg
                }
            return render_template("student_list.html", params=params)
    # return redirect(url_for("login"))


@app.route("/delete_test", methods=["GET", "POST"])
def delete_test():
    # if session["loggedin"] == True:
        if request.method=="GET":
            msg=""
            #############
            for student in students:
                try:
                    #　最後に追加されたテスト項目を削除
                    student["test"].popitem()
                except KeyError:
                    #　消せるテスト項目がなかった場合
                    msg = "消せるテスト項目がありません"
            try: 
                # テスト項目の名前も削除       
                test_names.popitem()
            except KeyError:
                pass
            # パラメータの設定
            params = {
                "students" : students,
                "test_names": test_names,
                "msg": msg
            }
            return render_template("student_list.html", params=params)
    # return redirect(url_for("login"))


@app.route("/edit_score", methods=["GET", "POST"])
def edit_score():
    # if session["loggedin"] == True:
        msg = ""
        if request.method=="POST":
            ###########
            for student in students:
                # 選択した学生と一致した場合
                if student["id"] == request.form["id"]:
                    for i in range(1, len(student["test"])+1):
                        # 選択した学生のテストの点数を入れる
                        try:
                            pass
                            #db ni ireru 
                            # with connection:
                            #     with connection.cursor() as cursor:
                            #         try:
                            #             # データベースから値を選択
                            #             cursor.execute("insert into score(student_id, subject_id, score, test_day, test_name", (request.form["id"],"後で追加", int(request.form.get(f"test{i}"))))
                            #             rows = cursor.fetchall()
                            #         except:
                            #             pass
                        #    int(request.form.get(f"test{i}"))
                        except ValueError:
                            msg = "点数に文字は入れれません"
                            
                    # 備考追加
                    student["note"] = request.form["note"]    
                    break
            #dbにinsert
            # パラメータの設定
            params = {
                "students": students,
                "test_names": test_names,
                "msg": msg
            }             
        return render_template("student_list.html", params=params)        
    # return redirect(url_for("login"))

@app.route("/edit_test_name", methods=["POST"])
def edit_test_name():
    msg = ""
    # if session["loggedin"] == True:
    if request.method=="POST":
        #　テストテーブルの個数分回して新しいテストカラムをつくる
        for i in range(1, len(students[0]["test"])+1):
            # テスト名の文字数制限
            if len(request.form[f"test{i}_name"]) <= 20:
                # テスト名の変更
                test_names[f"test{i}"] = request.form[f"test{i}_name"]
            else:
                msg = "テストの名前は20文字以下に設定してください"
    
    #dbにinsert
    print(test_names["test1"])###### 消す
    # パラメータの設定
    params = {
        "students": students,
        "test_names": test_names,
        "msg": msg
    }             
    return render_template("student_list.html", params=params)        
    # return redirect(url_for("login"))



@app.route("/view_profile/<student_id>",methods=["GET","POST"])
def view_profile(student_id):
    # if session["loggedin"] == True: 
        if request.method=="GET":
            print("AAAAAAAAAAAAAAAAAA")###### 消す
            for student in students:
                if student["id"] == student_id:

                    # 日付
                    x = list(student["rate_history"].keys())
                    # 出席率
                    y = list(student["rate_history"].values())
                    # 日付をDATE型に変更
                    x_dt = pd.to_datetime(x, errors='coerce')
                    # 出席率のグラフ作成表示
                    
                    fig, ax = plt.subplots()
                    plt.plot(x_dt, y, color="blue")
                    ax.set_ylim(-4,105,5)
                    plt.grid(c="black")
                    plt.scatter(x, y, marker="o", color="blue", s=125)
                    plt.xticks(rotation=30)
                    plt.yticks(np.arange(-0, 110, step=10))
                    #　出席率のグラフの保存
                    path = f"static/graph_images/{student_id}.png"
                    plt.savefig(path)  
# パラメータの  
                    params = {
                         "student": student,
                         "image": path,
                         "test_names": test_names
                    }
                    return render_template("student_detail.html", params=params)
        return redirect(url_for("login"))   
@app.route("/view_profile/<student_id>/score_graph_<test_key>",methods=["GET","POST"])                      
def histogram(student_id, test_key):
    if request.method=="GET":  

        x = []  
        for student in students:
            x.append(student["test"][test_key])
        sorted_x = sorted(list(set(x)),reverse=True)
        print(sorted_x)###### 消す
        fig, ax = plt.subplots()
        y = range(1, len(sorted_x)+1) 
        for student in students:
            #　自分の点数の色を変更する
            if student["id"] == student_id:
                color = ["red" if i == student["test"][test_key] else "blue" for i in sorted_x]

        ax.bar(y, sorted_x, color=color)
        plt.title(f"{test_names[test_key]}")
        # そのテスト受講者の学生の人数分
        plt.xlim(0.5,len(sorted_x)+0.5)
        plt.xticks(np.arange(1, len(sorted_x)+1, step=1))
        plt.ylabel("点数")
        plt.grid(c="black")
        plt.tick_params(labelsize = 10)


        path = f"static/graph_images/{student_id}_{test_key}.png"
        plt.savefig(path)
        for student in students:
            if student["id"] == student_id:
                
                    params = {
                        "image": path,
                        "test_names": test_names,
                        "student": student,
                        "test_name_value": test_names[test_key] 
                                }
                    return render_template("student_detail.html", params=params)
        # return redirect(url_for("login"))

@app.route("/home", methods=["GET", "POST"])    
def home():
    if request.method=="GET":
        params = {
          "user": session["user_id"]
        }
        return render_template("home.html", params=params)
    if request.method=="POST":
        return render_template("home.html", params=params)
    return redirect(url_for("login"))
     
@app.route("/selects", methods=["POST", "GET"])
def select_class():
    #データベースからその講師の担当授業一覧を持ってくる
    if request.method == "GET":
        return render_template("selects.html") #paramsの設定
    if request.method == "POST":
        return render_template("selects.html") #paramsの設定
    
    
@app.route("/teacher_classes_setting", methods=["POST", "GET"])
def teacher_classes_setting():
    # 講師、専攻、学年をプルダウンメニューで選択して、それに該当する授業をチェックボックス
        if request.method == "GET":
            print("aaaasdasdaa")###### 消す
            with connection:
                with connection.cursor() as cursor:
                    try:
                        # データベースから値を選択
                        cursor.execute("select name from teacher")
                        print("DBBBBBB") ###### 消す
                        rows = cursor.fetchall()
                        print(rows[1])###### 消す
                        teachers = []
                        for row in rows:
                            teachers.append(row[0])
                        params={
                        "teachers": teachers #dbから講師一覧
                        }
                    except:
                        pass
                    print("aaaaa")###### 消す

                    return render_template("teacher_list.html", params=params)
        if request.method == "POST":
            print("bbbbb")###### 消す
            return render_template("teacher_list.html", params=params)
@app.route("/attendance_check", methods=["POST", "GET"])       
def attendance_check():
    if request.method=="GET":
        return render_template("attendance_check.html")
    if request.method=="POST":
        return render_template("attendance_check.html")
                
@app.route("/subject_select", methods=["POST", "GET"])
def subject_select():
    if request.method=="GET":
        print("subject_select, POST")
        #DBからSUBJECTを持ってくる
        
        with connection:
                with connection.cursor() as cursor:
                    try:
                        print("AAAAAAAAAAAAAAAA")
                        # データベースから値を選択
                        if session["user_id"] == "000000":
                            print("BBBBBBBBBBBBBBBBBB")
                            cursor.execute("select subject from subjects")
                            print("IIIIIIIIIIIIIIIIIIIIII")
                            subjects = cursor.fetchall()
                            print("JJJJJJJJJJJJJJJJJJJJJJ")
                            print(subjects)
                        else:
                            print("CCCCCCCCCCC")
                            cursor.execute("SELECT SUBJECT_ID FROM teacher where teacher_id = %s",(session["user_id"]))
                            print("EEEEEEEEEEEEEE")
                            subject_ids = cursor.fetchall()
                            print("DDDDDDDDDDDDDD")
                            print(subject_ids)
                            print("FFFFFFFFFFFFFFFFFFF")
                            cursor.execute("SeLECT SUBJECT FROM SUBJECTS where subject_id = %s", (subject_ids))
                            print("GGGGGGGGGGGGGGGGGGGGGG")
                            subjects = cursor.fetchall()
                            print("HHHHHHHHHHHHHHHHHHHHHHHHHH")
                            print(subjects)
                    except:
                        print("EXCEPTTTTT FROM SUBEJCT SELECT")
                params = {
                    "subjects": subjects
                }
        return render_template("subject_select.html", params=params)
    if request.method=="POST":
        print("subject_select, POST")

if __name__ == "__main__":
    app.run(port=12345, debug=True) #12345でerrorがでたら8000にする
