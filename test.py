import datetime
t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)

d = now.strftime('%Y-%m-%d')
print(d)  # 2021-11-04

students = [
            {"id":"2004230011", "name":"西結都","test":{"test1": ""},"note":"", "date":{"2022-09-01":"attend","2022-09-02":"attend","2022-09-03":"attend","2022-09-04":"attend","2022-09-05":"absence"},"rate":""},
            {"id":"2222222222", "name":"古賀慶次郎","test":{"test1": ""},"note":"", "date":{"2022-09-01":"absence","2022-09-02":"attend","2022-09-03":"attend","2022-09-04":"attend","2022-09-05":"attend"},"rate":""},
            {"id":"3333333333", "name":"中村太一","test":{"test1": ""},"note":"", "date":{"2022-09-01":"absence","2022-09-02":"attend","2022-09-03":"absence","2022-09-04":"attend","2022-09-05":"absence"},"rate":""},
            ]

attend = 0
total = 0
for student in students:
    for key, value in student["date"].items():
        total += 1
        if value=="attend":
            attend += 1
    student["rate"] = str(round(attend / total * 100,1)) + "%"