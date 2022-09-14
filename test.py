import matplotlib.pyplot as plt
import numpy as np
students = [
            {"id":"2004230011", "name":"西結都","test":{"test1": ""},"note":"", "date":{"2022-09-01":"attend","2022-09-02":"attend","2022-09-03":"attend","2022-09-04":"attend","2022-09-05":"absence"},"rate":"","rate_history":{"1":100, "2":100,"3":66.7,"4":75,}},
            {"id":"2222222222", "name":"古賀慶次郎","test":{"test1": ""},"note":"", "date":{"2022-09-01":"absence","2022-09-02":"attend","2022-09-03":"attend","2022-09-04":"absence","2022-09-05":"attend"},"rate":"","rate_history":{"1":100, "2":100,"3":66.7,"4":75,}},
            {"id":"3333333333", "name":"中村太一","test":{"test1": ""},"note":"", "date":{"2022-09-01":"absence","2022-09-02":"attend","2022-09-03":"absence","2022-09-04":"absence","2022-09-05":"absence"},"rate":"","rate_history":{"1":0, "2":50,"3":66.7,"4":75,}},
            ]
#### test
for student in students:
    attend = 0
    total = len(student["date"])
    for key, value in student["date"].items():
        if value=="attend":
            attend += 1
    student["rate"] = round(attend / total * 100, 1)
    student["rate_history"][f'{len(student["date"])}'] = student["rate"]




x = np.arange(0, len(student["date"]), 2)

# y = np.arange(0, list(students[0]["rate_history"].values()), 1)
# print(y)
plt.plot(list(students[0]["rate_history"].values()),x)
plt.show()