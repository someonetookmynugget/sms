
from asyncio.windows_events import NULL
from datetime import datetime
import datetime
from tabnanny import check
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
                    params["msg"] = "講師番号は数字6桁、パスワードは数字４桁に設定してください"
                    return render_template("register.html",params=params)
                elif re.compile('[0-9]+').fullmatch(request.form["teacher_name"]) == None and re.compile('[０-９]+').fullmatch(request.form["teacher_name"]) != None and re.compile('[ａ-ｚＡ-Ｚ]+').fullmatch(request.form["teacher_name"]) != None:
                    params["msg"] = "名前を正しく入力してください"
                    return render_template("register.html",params=params)
                elif re.compile('[\u3041-\u309F]+').fullmatch(request.form["name_sub"]) == None:
                    params["msg"] = "ふりがなを入力してください"
                    return render_template("register.html",params=params)
                elif len(str(request.form["ID"])) != 6:
                    params["msg"] = "講師番号は数字6桁にしてください"
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
                    id = int(request.form["ID"])
            except:
                    params["msg"] = "パスワードは数字４桁, 講師番号は数字6桁にしてください"
                    return render_template("register.html",params=params)
            values = [[request.form["ID"], request.form["password"], request.form["teacher_name"],request.form["name_sub"], int(request.form["age"]), request.form["gender"], 2 ,1]]

            with connection:
                with connection.cursor() as cursor:
                    sql = f'insert into teacher(teacher_id, password, name ,name_sub ,age, gender, subject_id, major_id ) values (%s, %s, %s, %s, %s, %s, %s, %s)'
                    try:
                        cursor.executemany(sql, values)
                    except psycopg2.errors.UniqueViolation:
                        params["msg"] = "この講師番号は既に存在しています。"
                        return render_template("register.html", params=params)
                    except psycopg2.errors.InvalidTextRepresentation:
                        params["msg"] = "講師番号に数字以外の文字が含まれています"
                        return render_template("register.html", params=params)
                    except psycopg2.errors.NumericValueOutOfRange:
                        params["msg"] = "講師番号が長すぎます,6文字にしてください"
                        return render_template("register.html", params=params)
                connection.commit()
            cursor.close()
        return render_template('register_complete.html')
    #  return redirect(url_for("login"))
@app.route("/")
def access():
    return redirect(url_for("login"))

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
                    # データベースから値を取得
                    #teacher_id と passwordを持ってkるう
                    cursor.execute("select * from teacher where teacher_id = %s and password = %s", (params["ID"], params["password"],))
                    rows = cursor.fetchall()
                    try:
                        print(rows)###### 消す
                        print(rows[0])###### 消す
                        id = rows[0][1]
                        password = rows[0][-1]
                        name = rows[0][2]
                        print(name)
                        print(password)
                        print(id)###### 消す
                        # IDとPASSWORDが一致した場合
                        # if id == params["ID"] and password == params["password"]:
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
                        if session["user_id"] == "000000":
                            print("A")
                            return render_template("home.html", params=params)
                        else:
                            print("ELSE")
                            subject_list = []
                            cursor.execute("SELECT SUBJECT_ID FROM teacher where teacher_id = %s",(session["user_id"],))
                            subject_ids = cursor.fetchall()
                            for subject_id in subject_ids:
                                if subject_id[0] != None:
                                    cursor.execute("SeLECT SUBJECT FROM SUBJECTS where id = %s", (subject_id[0],))
                                    subjects = cursor.fetchall()
                                    for subject in subjects:
                                        if subject[0] not in subject_list:
                                            subject_list.append(subject[0])
                            params["subject_list"] = subject_list
                            return render_template("subject_select.html", params=params)  
                            # ID, password が6文字と４文字以外の場合
                        # elif len(id) != 6 or len(password) != 4: 
                        #     params["msg"] = "IDかパスワードのどちらかが間違っていますaaaaaaaa"
                        #     return render_template("login.html", params=params)
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





subject = ""

@app.route("/logout")
def logout():
    # セッションの初期化
    session["loggedin"] = None
    session["user_id"] = None
    session["username"] = None
    params = {
        "msg":""
    }
    return render_template("login.html",params=params)
@app.route("/student_list", methods=["GET", "POST"])
def student_list():
    # if session["loggedin"] == True:
        # if request.method=="GET":
        #     print("stundet?list GET") 
        if request.method=="POST":
            print("POST stundet_list")
            test_names = {}
            msg = ""
            subject = request.form["subject"]
            students = []
            students_list = []

            with connection:
                with connection.cursor() as cursor:
            # 授業名と一致するSUBJECT_IDをとってくるSUBJECT_IDでSTUNDET_IDとNAMEを取得する
                    try:
                        cursor.execute(f"select test_name from test where subject = %s order by id asc",(subject,))
                        tests = cursor.fetchall()
                        aaa = []
                        for i in tests:
                            if i not in aaa:
                                aaa.append(i)
                        for i, test in enumerate(aaa):
                            test_names[f"test{i+1}"] = test[0]
                            
                        print("aaaaaa")
                        cursor.execute("select id from subjects where subject = %s",(request.form["subject"],))
                        print("id execute ")
                        subject_ids = cursor.fetchall()
                        print(subject_ids,"subject_id")
                        for id in subject_ids:
                            print(id[0],"id")
                                    #データベースから値を選択
                            cursor.execute("select student_id, name, note, rate FROM student where subject_id = %s", (id[0],))
                            student_db = cursor.fetchall()

                            for student in student_db:
                                students.append(student)


                            cursor.execute("SELECT test_name, test_score, student_id FROM test order by id asc")
                            test = cursor.fetchall()

                        for i, row in enumerate(students):
                            student_id = row[0]
                            student_name = row[1]
                            if row[2] == None:
                                student_note = ""
                            else:
                                student_note = row[2]
                            if row[3] == None:
                                student_rate = ""
                            else:
                                student_rate = row[3]
                            ### 複数要素あるものはAPPEND  students_list.append({"test":{},"something":{}})
                            students_list.append({"test":{}})
                            students_list[i]["name"] = student_name
                            students_list[i]["student_id"] = student_id
                            students_list[i]["note"] = student_note
                            students_list[i]["rate"] = student_rate

                            for j, row2 in enumerate(test):
                                test_name = row2[0]
                                # print(test_name,"test_naaaaaaaaaaaaaaaaame")
                                test_score = row2[1]
                                if row2[2] == students_list[i]["student_id"]:
                                    # count = len(students_list[i]["test"])
                                    students_list[i]["test"][f"{row2[0]}"] = test_score
                        

                            
                    except:
                        msg = "something went wrong in student_list"

            params = {
                "students": students_list,
                "test_names": test_names,
                "msg":msg,
                "subject_name":subject
            }
            return render_template("student_list.html", params=params)             

    #return redirect(url_for("login"))  

@app.route("/add_test", methods=["GET", "POST"])
def add_test():
    # if session["loggedin"] == True:
        if request.method == "POST":
            print("BBBBBBBBBBBBBBBBBBB POST ADD TEST")
            name = request.form["test_name"]
            print(name)
            values = [[name, ""]]
            students = []
            students_list = []
            test_names = {   
                        }
            subject = request.form["subject"]
            msg = ""
            with connection:
                with connection.cursor() as cursor:

                    cursor.execute("select id from subjects where subject = %s",(request.form["subject"],))

                    subject_ids = cursor.fetchall()

                    for id in subject_ids:

                                #データベースから値を選択
                        cursor.execute("select student_id, name FROM student where subject_id = %s", (id[0],))
                        student_db = cursor.fetchall()

                        for student in student_db:
                            students.append(student[0])


                    try:
                        cursor.execute(f"SELECT * from test where test_name = %s", (name, ))
                        a = cursor.fetchall()

                        if a == []:
                            for student in students:

                                cursor.execute(f'insert into test(test_name, test_score, student_id, subject) values (%s,%s,%s,%s);',(name, "",student, request.form["subject"]))

                        else:
                            msg = "同じテスト名は入力できません"
                    except:
                         msg = "something went wrong in add_test 1"
            #     connection.commit()
            # cursor.close()
                                                    

            # with connection:
            #     with connection.cursor() as cursor:
                    try:

                        #テスト一覧の取得と格納

                    
                        cursor.execute(f"select test_name from test where subject = %s order by id asc",(subject,))
                        tests = cursor.fetchall()
                        aaa = []
                        for i in tests:
                            if i not in aaa:
                                aaa.append(i)
                        for i, test in enumerate(aaa):
                            test_names[f"test{i+1}"] = test[0]
                        print(test_names)


                        # データベースから値を選択
                        cursor.execute("SELECT test_name, test_score, student_id FROM test order by id asc")
                        rows2 = cursor.fetchall()
                        cursor.execute("SELECT student_id, name from student")
                        rows = cursor.fetchall()
                        print(rows2)
                        try:
                            for i, row in enumerate(rows):
                                student_id = row[0]
                                student_name = row[1]
                                ### 複数要素あるものはAPPEND  students_list.append({"test":{},"something":{}})
                                students_list.append({"test":{}})
                                students_list[i]["name"] = student_name
                                students_list[i]["student_id"] = student_id
                                for j, row2 in enumerate(rows2):
                                    test_name = row2[0]
                                    print(test_name,"test_naaaaaaaaaaaaaaaaame")
                                    test_score = row2[1]
                                    if row2[2] == students_list[i]["student_id"]:
                    
                                        count = len(students_list[i]["test"])
                                        students_list[i]["test"][f"{row2[0]}"] = test_score

                            print(students_list)

                        except:
                            print("forbun")
                    except:
                        print("db")
            #     # パラメータの設定
                params = {
                    "students" : students_list,
                    "test_names": test_names,
                    "subject_name": subject,
                    "msg": msg
                }
            return render_template("student_list.html", params=params)
    # return redirect(url_for("login"))


@app.route("/delete_test", methods=["GET", "POST"])
def delete_test():
    # if session["loggedin"] == True:
        if request.method=="POST":
            students = []
            students_list = []
            test_names = {}
            msg=""
            subject = request.form["subject"]
            #############
            with connection:
                with connection.cursor() as cursor:




                    cursor.execute("select id from subjects where subject = %s",(subject,))
                    print("id execute ")
                    subject_ids = cursor.fetchall()
                    print(subject_ids)
                    for id in subject_ids:
                        print(id[0])
                        cursor.execute("select student_id, name FROM student where subject_id = %s", (id[0],))
                        student_db = cursor.fetchall()
                        print(student_db)
                        for student in student_db:
                            students.append(student[0])
                    print(students,"students")
                    try:
                        # DELETE 
                        for i in range(0, len(students)):
                            cursor.execute("delete from test where id=(select max(id) from test)")
                    except:
                        print("AAAASDASIDFUHAUFH UIW ")
            #     connection.commit()
            # cursor.close()
                                                    

            # with connection:
            #     with connection.cursor() as cursor:
                    try:
                        #テスト一覧の取得と格納
                        cursor.execute(f"select test_name from test where subject = %s order by id asc",(subject,))
                        tests = cursor.fetchall()
                        aaa = []
                        for i in tests:
                            if i not in aaa:
                                aaa.append(i)
                        for i, test in enumerate(aaa):
                            test_names[f"test{i+1}"] = test[0]
                        print(test_names)

                        # データベースから値を選択
                        cursor.execute("SELECT test_name, test_score, student_id FROM test order by id asc")
                        rows2 = cursor.fetchall()
                        cursor.execute("SELECT student_id, name from student")
                        rows = cursor.fetchall()

                        try:
                            for i, row in enumerate(rows):
                                student_id = row[0]
                                student_name = row[1]
                                ### 複数要素あるものはAPPEND  students_list.append({"test":{},"something":{}})
                                students_list.append({"test":{}})
                                students_list[i]["name"] = student_name
                                students_list[i]["student_id"] = student_id
                                for j, row2 in enumerate(rows2):
                                    test_name = row2[0]
                                    test_score = row2[1]
                                    if row2[2] == students_list[i]["student_id"]:
                    
                                        count = len(students_list[i]["test"])
                                        students_list[i]["test"][f"{row2[0]}"] = test_score
                            print(students_list)

                        except:
                            print("forbun")
                    except:
                        print("db")
                        print(test_names)
            # パラメータの設定
            params = {
                "students" : students_list,
                "test_names": test_names,
                "subject_name": subject,
                "msg": msg
            }
            return render_template("student_list.html", params=params)
    # return redirect(url_for("login"))


@app.route("/edit_info", methods=["GET", "POST"])
def edit_info():
    # if session["loggedin"] == True:
        if request.method=="POST":
            students_list = []
            test_names = {}
            msg = ""      
            subject = request.form["subject"]
            rate_list = request.form.getlist("rate")
            id_list = request.form.getlist("student_id")
            test_name_list = request.form.getlist("test_name")
            test_score_list = request.form.getlist("test_score")
            note_list = request.form.getlist("note")  

            for i, id in enumerate(id_list):
                with connection:         
                    with connection.cursor() as cursor:
                        
                        cursor.execute("select major_id from student where student_id = %s",(id,))
                        
                        major_id = cursor.fetchall()
                        cursor.execute("select id from subjects where subject = %s and major_id = %s", (subject,major_id[0][0]))
                        sub_id = cursor.fetchall()
                        
                        try:
                            if "点" in test_score_list[i]:
                        
                                if int(test_score_list[i][-1]) >= 101:
                                    raise
                        
                                cursor.execute(f"update test set test_score = %s where test_name = %s and student_id = %s and subject = %s",(int(test_score_list[i][:-1]), test_name_list[i], id, subject,))
                        
                            else:
                                if int(test_score_list[i]) >= 101:
                                    raise
                        
                                cursor.execute(f"update test set test_score = %s where test_name = %s and student_id = %s and subject = %s",(int(test_score_list[i]), test_name_list[i], id, subject,))
                        except:
                            msg="点数を数字で正しく入力してください"


                        for j, rate in enumerate(rate_list):
                            cursor.execute(f"update student set rate = %s, note = %s where student_id = %s and subject_id = %s",(rate, note_list[j],id_list[j], sub_id[0][0],))
                            
               
                    connection.commit()
                cursor.close()

            with connection:
                with connection.cursor() as cursor:
                    try:

                        #テスト一覧の取得と格納
                        cursor.execute(f"select test_name from test where subject = %s order by id asc",(subject,))
                        tests = cursor.fetchall()
                        aaa = []
                        for i in tests:
                            if i not in aaa:
                                aaa.append(i)
                        for i, test in enumerate(aaa):
                            test_names[f"test{i+1}"] = test[0]


                        # データベースから値を選択
                        cursor.execute("SELECT test_name, test_score, student_id FROM test order by id asc")
                        rows2 = cursor.fetchall()
                        print(rows2)
                        cursor.execute("SELECT student_id, name, rate, note from student")
                        rows = cursor.fetchall()

                        try:
                            for i, row in enumerate(rows):
                                student_id = row[0]
                                student_name = row[1]
                                student_rate = row[2]
                                student_note = row[3]
                                ### 複数要素あるものはAPPEND  students_list.append({"test":{},"something":{}})
                                students_list.append({"test":{}})
                                students_list[i]["name"] = student_name
                                students_list[i]["student_id"] = student_id
                                students_list[i]["rate"] = student_rate
                                students_list[i]["note"] = student_note
                                for j, row2 in enumerate(rows2):
                                    # print(test_names[f"test{i+1}"])
                                    # print(row2,"AAAAAAAAAAAAAAAA")
                                    test_name = row2[0]
                                    test_score = row2[1]

                                    if row2[2] == students_list[i]["student_id"]:

                                        # count = len(students_list[i]["test"])

                                        students_list[i]["test"][f"{test_name}"] = test_score

                        except:
                            print("forbun")
                    except:
                        print("db")

            print(students_list)
            #dbにinsert
            # パラメータの設定
            params = {
                "students": students_list,
                "test_names": test_names,
                "subject_name": subject,
                "msg": msg
            }             
        return render_template("student_list.html", params=params)        
    # return redirect(url_for("login"))

@app.route("/edit_test_name", methods=["POST"])
def edit_test_name():
    # if session["loggedin"] == True:
        if request.method=="POST":
            students_list = []
            test_names = {}
            msg = ""
            subject = request.form["subject"]
            current_test_name = request.form["current_test_name"]
            new_test_name = request.form["new_test_name"]
            
            with connection:            
                with connection.cursor() as cursor:
                    if current_test_name != new_test_name:
                        try:
                            cursor.execute(f"select test_name from test where test_name = %s",(new_test_name,))
                            test = cursor.fetchall()
                            print(test)
                            if test == []:
                                cursor.execute(f"update test set test_name = %s where test_name = %s and subject = %s",(new_test_name, current_test_name,subject,))
                            else:
                                raise
                        except:
                            msg="既に存在している名前です"
                        
            #     connection.commit()
            # cursor.close()

            # with connection:
            #     with connection.cursor() as cursor:
                    try:
                        #テスト一覧の取得と格納
                        cursor.execute(f"select test_name from test where subject = %s order by id asc",(subject,))
                        tests = cursor.fetchall()
                        aaa = []
                        for i in tests:
                            if i not in aaa:
                                aaa.append(i)
                        for i, test in enumerate(aaa):
                            test_names[f"test{i+1}"] = test[0]


                        # データベースから値を選択
                        cursor.execute("SELECT test_name, test_score, student_id FROM test order by id asc")
                        rows2 = cursor.fetchall()
                        cursor.execute("SELECT student_id, name from student")
                        rows = cursor.fetchall()

                        try:
                            for i, row in enumerate(rows):
                                student_id = row[0]
                                student_name = row[1]
                                ### 複数要素あるものはAPPEND  students_list.append({"test":{},"something":{}})
                                students_list.append({"test":{}})
                                students_list[i]["name"] = student_name
                                students_list[i]["student_id"] = student_id
                                for row2 in rows2:
                                    test_score = row2[1]
                                    if row2[2] == students_list[i]["student_id"]:
                                        students_list[i]["test"][f"{row2[0]}"] = test_score

                        except:
                            print("forbun")
                    except:
                        print("db")
                        print(test_names)
                connection.commit()
            cursor.close()
            print(students_list)
            #dbにinsert
            # パラメータの設定
            params = {
                "students": students_list,
                "test_names": test_names,
                "subject_name": subject,
                "msg": msg
        
            }                     
        return render_template("student_list.html", params=params)        
    # return redirect(url_for("login"))



@app.route("/view_profile/<student_id>",methods=["GET","POST"])
def view_profile(student_id):
    # if session["loggedin"] == True: 
        if request.method=="GET":
            print("AAAAAAAAAAAAAAAAAA")###### 消す
            test_names = []
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute("select student_id, name, department_id, major_id, age, class_id, gender from student where student_id = %s",(student_id,))
                    student_details = cursor.fetchall()
                    for detail in student_details:
                        student_id = detail[0]
                        student_name = detail[1]
                        department_id = detail[2]
                        major_id = detail[3]
                        age = detail[4]
                        class_id = detail[5]
                        gender = detail[6]

                        cursor.execute("select department from departments where id = %s",(department_id,))
                        department_name = cursor.fetchall()

                        department_name = department_name[0][0]

                        cursor.execute("select major from majors where id = %s",(major_id,))
                        major_name = cursor.fetchall()
                        major_name = major_name[0][0]

                        cursor.execute("select class from classes where id = %s",(class_id,))
                        class_name = cursor.fetchall()
                        class_name = class_name[0][0]


                    cursor.execute("select subject_id from student where student_id = %s",(student_id,))
                    subject_ids = cursor.fetchall()
                    print(subject_ids)
                    for subject_id in subject_ids:
                        print("A")
                        print("subject_id",subject_id)
                        cursor.execute("select subject from subjects where id = %s",(subject_id[0],))
                        print("b")
                        subject_name = cursor.fetchall()
                        subject_name = subject_name[0]
                        print(subject_name[0])
                        cursor.execute("select test_name from test where subject = %s",(subject_name[0],))
                        tests = cursor.fetchall()
                        print(tests)
                        for test in tests:
                            test_name = test[0]
                            print("a")
                            if test_name not in test_names:
                                test_names.append(test_name)

                    # 日付
                    # x = list(student["rate_history"].keys())
                    # # 出席率
                    # y = list(student["rate_history"].values())
                    # # 日付をDATE型に変更
                    # x_dt = pd.to_datetime(x, errors='coerce')
                    # # 出席率のグラフ作成表示
                    
                    # fig, ax = plt.subplots()
                    # plt.plot(x_dt, y, color="blue")
                    # ax.set_ylim(-4,105,5)
                    # plt.grid(c="black")
                    # plt.scatter(x, y, marker="o", color="blue", s=125)
                    # plt.xticks(rotation=30)
                    # plt.yticks(np.arange(-0, 110, step=10))
                    # #　出席率のグラフの保存
                    # path = f"static/graph_images/{student_id}.png"
                    # plt.savefig(path)  
# パラメータの       
                    print(test_names)
                    params = {
                        "student_id": student_id,
                        "student_name":student_name,
                        "department_name":department_name,
                        "major_name":major_name,
                        "age":age,
                        "class_name":class_name,
                        "gender":gender,
                        #  "student": student,
                        #  "image": path,
                         "test_names": test_names
                    }
                    return render_template("student_detail.html", params=params)
        return redirect(url_for("login"))   
@app.route("/view_profile/<student_id>/score_graph_<test_key>",methods=["GET","POST"])                      
def histogram(student_id, test_key):

    if request.method=="GET":
        name = []  
        name_label = []
        score = []
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("select subject_id from student where student_id = %s",(student_id,))
                subject_ids = cursor.fetchall()
                for subject_id in subject_ids:
                    cursor.execute("select subject from subjects where id = %s",(subject_id[0],))
                    subject_name = cursor.fetchall()
                    subject_name = subject_name[0]
                    cursor.execute("select test_name, test_score from test where test_name = %s",(subject_name,))
                    tests = cursor.fetchall()
                    for test in tests:
                        test_name = test[0]
                        test_score = test[1]
                        name.append(test_name)
                        name_label.append(test_name)
                        score.append(test_score)
                    
                plt.bar(name, score, tick_label = name_label, align="center")
                plt.title(f"{subject_name}")
                plt.xlabel("テスト名")
                plt.ylabel("点数")


        # x = []  
        # for student in students:
        #     x.append(student["test"][test_key])
        # sorted_x = sorted(list(set(x)),reverse=True)
        # print(sorted_x)###### 消す
        # fig, ax = plt.subplots()
        # y = range(1, len(sorted_x)+1) 
        # for student in students:
        #     #　自分の点数の色を変更する
        #     if student["id"] == student_id:
        #         color = ["red" if i == student["test"][test_key] else "blue" for i in sorted_x]

        # ax.bar(y, sorted_x, color=color)
        # plt.title(f"{test_names[test_key]}")
        # # そのテスト受講者の学生の人数分
        # plt.xlim(0.5,len(sorted_x)+0.5)
        # plt.xticks(np.arange(1, len(sorted_x)+1, step=1))
        # plt.ylabel("点数")
        # plt.grid(c="black")
        # plt.tick_params(labelsize = 10)


        path = f"static/graph_images/{student_id}_{test_key}.png"
        plt.savefig(path)
        # for student in students:
        #     if student["id"] == student_id:
        cursor.execute("select student_id, name, department_id, major_id, age, class_id, gender from student where student_id = %s",(student_id,))
        student_details = cursor.fetchall()
        for detail in student_details:
            student_id = detail[0]
            student_name = detail[1]
            department_id = detail[2]
            major_id = detail[3]
            age = detail[4]
            class_id = detail[5]
            gender = detail[6]
            cursor.execute("select department from departments where id = %s",(department_id,))
            department_name = cursor.fetchall()
            department_name = department_name[0][0]
            cursor.execute("select major from majors where id = %s",(major_id,))
            major_name = cursor.fetchall()
            major_name = major_name[0][0]
            cursor.execute("select class from classes where id = %s",(class_id,))
            class_name = cursor.fetchall()
            class_name = class_name[0][0]
        # パラメータの
        params = {
            "student_id": student_id,
            "student_name":student_name,
            "department_name":department_name,
            "major_name":major_name,
            "age":age,
            "class_name":class_name,
            "gender":gender,
            #  "student": student,
            #  "image": path,
            #  "test_names": test_names
        }         
        params["image"] = path
        print(name_label,"name_label")
        params["test_names"] = name_label
        # params = {
        #     "image": path,
        #     # "test_names": test_name,
        #     # "test_name_value": test_names[test_key] 
        #             }
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
    
    
@app.route("/teacher_classes_setting", methods=["POST", "GET"])
def teacher_classes_setting():
    # 講師、専攻、学年をプルダウンメニューで選択して、それに該当する授業をチェックボックス
        select_grade = "学年選択"
        select_teacher = "講師選択"
        select_major = "専攻選択"
        msg = ""
        teachers = []
        majors = []
        if request.method == "GET":
            checked_subjects = {}
            subjects = []
            print("teacher_classes_setting get")###### 消す
            with connection:
                with connection.cursor() as cursor:
                    try:
                        # データベースから値を選択

                        # 講師を取得
                        cursor.execute("select name from teacher order by id asc")
                        teachers_db = cursor.fetchall()
                        for teacher in teachers_db:
                            if teacher[0] not in teachers:
                                teachers.append(teacher[0])

                        # 選考の取得
                        cursor.execute("select major from majors order by id asc")
                        majors_db = cursor.fetchall()
                        for major in majors_db:
                            if major[0] not in majors:
                                majors.append(major[0])
                        # 授業一覧を取得
                        cursor.execute("select subject from subjects order by id asc")
                        subjects_db = cursor.fetchall()
                        for subject in subjects_db:
                            if subject[0] not in subjects:
                                subjects.append(subject[0])
##########
                        #　パラメーターの設定
                        params={
                        "teachers": teachers, #dbから講師一覧
                        "majors":majors,
                        "select_teacher" : select_teacher,
                        "select_grade" : select_grade,
                        "select_major" : select_major,
                        "checked_subjects": checked_subjects,
                        "msg": msg,
                        "subjects":subjects
                        }
                    except:
                        print("something went wrong in teacher_classes_setting GET")

                    return render_template("teacher_list.html", params=params)
        if request.method == "POST":
            checked_subjects = {}
            subjects = []
            print("teacher_classes_setting PSOT")###### 消す
            major = request.form["major"]
            grade = request.form["grade"]
            teacher = request.form["teacher"]
            checked_subjects = {}
            with connection:
                with connection.cursor() as cursor:
                    if major != "0" and grade != "0"and teacher != "0":
                        print("dododododo")
                        select_grade = grade
                        select_major = major 
                        select_teacher = teacher

                        # 専攻のIDを取得
                        cursor.execute("select id from majors where grade = %s and major = %s order by id asc",(grade[0],major,))
                        major_id = cursor.fetchall()
                        # 専攻のIDがある授業を取得
                        cursor.execute("select subject from subjects where major_id = %s order by id asc",(major_id[0],))
                        subjects_db = cursor.fetchall()
                        for subject in subjects_db:
                            subjects.append(subject[0])
                        # 先生にすでに登録されている授業IDを取得
                        cursor.execute("select subject_id from teacher where name = %s and major_id = %s",(teacher, major_id[0],))
                        subject_ids = cursor.fetchall()
                        print(subject_ids,"sv")
                        print(subjects)
                        checked_subjects[f"{major}"] = []
                        for subject in subject_ids:
                            cursor.execute("select subject from subjects where id = %s", (subject[0],))
                            subjects_db = cursor.fetchall()
                            for subject2 in subjects_db:
                                # for sub_list in checked_subjects.values():
                                #     if subject2[0] not in sub_list:
                                #         for major_list in checked_subjects.keys():
                                # if major not in major_list:
                                if subject2[0] not in checked_subjects[f"{major}"]:
                                    checked_subjects[f"{major}"].append(subject2[0])
                        print(checked_subjects)

                    else:
                        msg = "選択されていない項目があります"
                    try:
                        # 講師を取得
                        cursor.execute("select name from teacher order by id asc")
                        teachers_db = cursor.fetchall()
                        for teacher_db in teachers_db:
                            if teacher_db[0] not in teachers:
                                teachers.append(teacher_db[0])

                        # 選考の取得
                        cursor.execute("select major from majors order by id asc")
                        majors_db = cursor.fetchall()
                        for m_d in majors_db:
                            if m_d[0] not in majors:
                                majors.append(m_d[0])

                    except:
                        print("something went wrong in teacher_classes_setting POST")
                    print(subjects)
                    print(checked_subjects)
                    params={
                        "teachers": teachers, #dbから講師一覧
                        "majors":majors,
                        "select_teacher" : select_teacher,
                        "select_grade" : select_grade,
                        "select_major" : select_major,
                        "msg": msg,
                        "subjects":subjects,
                        "checked_subjects" : checked_subjects
                        }
            return render_template("teacher_list.html", params=params)


@app.route("/form_check", methods=["POST"])
def form_check():
    select_grade = "学年選択"
    select_teacher = "講師選択"
    select_major = "専攻選択"
    if request.method=="POST":
        major = request.form["major"]
        grade = request.form["grade"]
        teacher = request.form["teacher"]
        check_list = request.form.getlist("check")
        print(check_list)
        checked_subjects = {}
        subjects = [] 
        teachers = []
        majors = [] 
        msg = ""
        with connection:
            with connection.cursor() as cursor:
                select_grade = grade
                select_major = major 
                select_teacher = teacher

                # インサート文
                for check in check_list:
                    
                    cursor.execute("select id from majors where major = %s and grade = %s", (major, grade[0],))
                    major_db = cursor.fetchall()  
                   
                    cursor.execute("select id from subjects where major_id = %s and subject = %s",(major_db[0][0], check))
                    subject_ids = cursor.fetchall()

                    cursor.execute("select exists (select * from teacher where subject_id = %s and major_id = %s)",(subject_ids[0][0],major_db[0][0],))
                    result = cursor.fetchone()

                    if result[0] == False:
                        cursor.execute("select teacher_id, name, name_sub, age, gender, password from teacher where name = %s", (teacher,))
                        teacher_info = cursor.fetchall()
                        cursor.execute("insert into teacher(teacher_id, name, name_sub, age, gender, password, subject_id, major_id) values(%s, %s, %s, %s, %s, %s, %s, %s)",(teacher_info[0][0], teacher_info[0][1],teacher_info[0][2],teacher_info[0][3],teacher_info[0][4],teacher_info[0][5], subject_ids[0][0], major_db[0][0]))


                # delete 文
                if check_list == []:
                    cursor.execute("select id from majors where major = %s and grade = %s", (major, grade[0],))
                    major_db = cursor.fetchall()  
                    cursor.execute("delete from teacher where major_id = %s",(major_db[0][0],))

                else:
                    for check in check_list:
                    # check sareta subject id 

                        cursor.execute("select id from majors where major = %s and grade = %s", (major, grade[0],))
                        major_db = cursor.fetchall()  
                    
                        cursor.execute("select subject_id from teacher where major_id = %s",(major_db[0][0],))
                        teacher_subject_ids = cursor.fetchall()

                        for teacher_subid in teacher_subject_ids:
                            cursor.execute("select subject from subjects where id = %s",(teacher_subid[0],))
                            teacher_subject_name = cursor.fetchall()

                            if teacher_subject_name[0][0] not in check_list:
                                cursor.execute("select id from subjects where subject = %s and major_id = %s",(teacher_subject_name[0][0], major_db[0][0],))
                                delete_sub_id = cursor.fetchall()
                                cursor.execute("delete from teacher where subject_id = %s",(delete_sub_id[0][0],))



                #　選択された学年と専攻名でIDを取得    
                cursor.execute("select id from majors where grade = %s and major = %s order by id asc",(grade[0],major,))
                major_id = cursor.fetchall()

                # 専攻のIDがある授業を取得
                cursor.execute("select subject from subjects where major_id = %s order by id asc",(major_id[0],))
                subjects_db = cursor.fetchall()
                for subject in subjects_db:
                    if subject[0] not in subjects:
                        subjects.append(subject[0])

                # 先生にすでに登録されている授業IDを取得
                cursor.execute("select subject_id from teacher where name = %s and major_id = %s",(teacher, major_id[0],))
                subject_ids = cursor.fetchall()
                checked_subjects[f"{major}"] = []

                for subject in subject_ids:
                    cursor.execute("select subject from subjects where id = %s", (subject[0],))
                    subjects_db = cursor.fetchall()
    
                    for subject2 in subjects_db:
                        if subject2[0] not in checked_subjects[f"{major}"]:
                            checked_subjects[f"{major}"].append(subject2[0])
                    

       
                # 講師を取得
                cursor.execute("select name from teacher order by id asc")
                teachers_db = cursor.fetchall()
                for teacher in teachers_db:
                    if teacher[0] not in teachers:
                        teachers.append(teacher[0])
                # 選考の取得
                cursor.execute("select major from majors order by id asc")
                majors_db = cursor.fetchall()
                for major in majors_db:
                    if major[0] not in majors:
                        majors.append(major[0])

                #　パラメーターの設定
                params={
                "teachers": teachers,
                "majors":majors,
                "select_teacher" : select_teacher,
                "select_grade" : select_grade,
                "select_major" : select_major,
                "msg": msg,
                "subjects":subjects,
                "checked_subjects" : checked_subjects
                }
        return render_template("teacher_list.html", params=params)


@app.route("/student_register", methods=["POST", "GET"])
def student_register():
    params = {
        "msg":"",
        "student_id":"",
        "name":"",
        "name_sub":"",
        "age":"",
        "department":"",
        "major":"",
        "departments_list": [],
        "select_department":"学科選択",
        "majors_list": [],
        "select_major":"専攻選択"
    }
    if request.method == "GET":
        departments_list = []
        majors_list = []
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("select department from departments")
                departments_db = cursor.fetchall()
                for department_db in departments_db:
                
                    departments_list.append(department_db[0])
                params["departments_list"] = departments_list

                cursor.execute("select major from majors")
                majors_db = cursor.fetchall()
                for major_db in majors_db:
                    if major_db[0] not in majors_list:
                        majors_list.append(major_db[0])
                params["majors_list"] = majors_list

            connection.commit()
        cursor.close()
        return render_template("student_register.html",params=params)
    if request.method == "POST":
        params["student_id"] = request.form["student_id"]
        params["name"] = request.form["name"]
        params["name_sub"] = request.form["name_sub"]
        params["age"] = request.form["age"]
        params["department"] = request.form["department"]
        params["major"] = request.form["major"]

        try:
            if len(str(request.form["student_id"])) != 10:
                params["msg"] = "学籍番号は数字10桁に設定してください"
                return render_template("student_register.html",params=params)
            elif re.compile('[0-9]+').fullmatch(request.form["name"]) == None and re.compile('[０-９]+').fullmatch(request.form["name"]) != None and re.compile('[ａ-ｚＡ-Ｚ]+').fullmatch(request.form["name"]) != None:
                params["msg"] = "名前を正しく入力してください"
                return render_template("student_register.html",params=params)
            elif re.compile('[\u3041-\u309F]+').fullmatch(request.form["name_sub"]) == None:
                params["msg"] = "ふりがなを入力してください"
                return render_template("student_register.html",params=params)
            elif re.compile('[0-9]+').fullmatch(request.form["age"]) == None:
                params["msg"] = "年齢に文字が含まれています"
                return render_template("student_register.html", params=params)
            elif len(request.form["age"]) != 2:
                params["msg"] = "年齢を正しく入力してください"
                return render_template("student_register.html",params=params)
            
            
            vali = int(request.form["student_id"])
            
        except:
                params["msg"] = "except in student_register"
                return render_template("register.html",params=params)
        with connection:
            with connection.cursor() as cursor:
                # cursor.fetchall
                values = [[request.form["student_id"], request.form["name"],request.form["name_sub"], int(request.form["age"]), request.form["gender"],department_id,major_id]]
                sql = f'insert into student(student_id, name ,name_sub ,age, gender, department_id, major_id ) values (%s, %s, %s, %s, %s, %s, %s)'
                try:
                    cursor.executemany(sql, values)
                except psycopg2.errors.UniqueViolation:
                    params["msg"] = "この学籍番号は既に存在しています。"
                    return render_template("student_register.html", params=params)
                except psycopg2.errors.InvalidTextRepresentation:
                    params["msg"] = "学籍番号に数字以外の文字が含まれています"
                    return render_template("student_register.html", params=params)
                except psycopg2.errors.NumericValueOutOfRange:
                    params["msg"] = "学籍番号が長すぎます,10文字にしてください"
                    return render_template("student_register.html", params=params)
            connection.commit()
        cursor.close()
        return render_template("student_register.html",params=params)


@app.route("/attendance_check", methods=["POST", "GET"])       
def attendance_check():
    if request.method=="GET":
        return render_template("attendance_check.html")
    if request.method=="POST":
        return render_template("attendance_check.html")
                
@app.route("/subject_select", methods=["POST", "GET"])
def subject_select():
    if request.method=="GET":
        print("subject_select, GET")
        #DBからSUBJECTを持ってくる
        subject_list = []
        with connection:
            with connection.cursor() as cursor:
                try:

                    # データベースから値を選択
                    if session["user_id"] == "000000":

                        cursor.execute("select subject from subjects")

                        subjects = cursor.fetchall()

                        for subject in subjects:
                            subject_list.append(subject[0])
                        subject_list = list(set(subject_list))

                    else:
                        cursor.execute("SELECT SUBJECT_ID FROM teacher where teacher_id = %s",(session["user_id"],))
                        subject_ids = cursor.fetchall()

                        for subject_id in subject_ids:
                            if subject_id[0] != None:
                                cursor.execute("SeLECT SUBJECT FROM SUBJECTS where id = %s", (subject_id[0],))

                                subjects = cursor.fetchall()
                                for subject in subjects:
                                    if subject[0] not in subject_list:
                                        subject_list.append(subject[0])


                except:
                    print("EXCEPTTTTT FROM SUBEJCT SELECT")
        params = {
            "subject_list": subject_list
        }
        print(subject_list)
        return render_template("subject_select.html", params=params)

if __name__ == "__main__":
    app.run(port=12345, debug=True) # 12345でerrorがでたら8000にする
