from turtle import color
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib  # <--ここを追加

from matplotlib.backends.backend_agg import FigureCanvasAgg
# students = [
#             {"id":"2004230011", "name":"西結都","test":{"test1": ""},"note":"", "date":{"2022-09-01":"attend","2022-09-02":"attend","2022-09-03":"attend","2022-09-04":"attend","2022-09-05":"absence"},"rate":"","rate_history":{"2022-09-01":100, "2022-09-02":100,"2022-09-03":66.7,"2022-09-04":75,}},
#             {"id":"2222222222", "name":"古賀慶次郎","test":{"test1": ""},"note":"", "date":{"2022-09-01":"absence","2022-09-02":"attend","2022-09-03":"attend","2022-09-04":"absence","2022-09-05":"attend"},"rate":"","rate_history":{"2022-09-01":100, "2022-09-02":100,"2022-09-03":66.7,"2022-09-04":75,}},
#             {"id":"3333333333", "name":"中村太一","test":{"test1": ""},"note":"", "date":{"2022-09-01":"absence","2022-09-02":"attend","2022-09-03":"absence","2022-09-04":"absence","2022-09-05":"absence"},"rate":"","rate_history":{"2022-09-01":0, "2022-09-02":50,"2022-09-03":66.7,"2022-09-04":75,}},
#             ]
# #### test
# for student in students:
#     attend = 0
#     total = len(student["date"])
#     for key, value in student["date"].items():
#         if value=="attend":
#             attend += 1
#         last_key_name = key
#     student["rate"] = round(attend / total * 100, 1)
#     student["rate_history"][f'{last_key_name}'] = student["rate"]

# print(students[0]["rate_history"])

# id = "2004230011"
# for student in students:
#     if student["id"] == id:

#         x = list(student["rate_history"].keys())
#         y = list(student["rate_history"].values())
#         x_dt = pd.to_datetime(x)
#         fig = plt.figure(figsize=(12, 8))
#         ax = fig.add_subplot(111)
#         ax.plot(x_dt, y, color="blue")
#         ax.set_ylim(-4,105,5)
#         plt.grid(True)
#         plt.scatter(x, y , marker="o", color="blue", s=125)
#         plt.xticks(rotation=30)
#         plt.yticks(np.arange(-0, 110, step=10))
#         plt.show()

# fig, ax = plt.subplots()
# num_list=[30,30,30,40,50,70,85,90,94,100]
# n, bins, patches = plt.hist(num_list)
# patches[5].set_facecolor('red')
# plt.xlim(-5,105, 5)
# plt.grid(c="black")
# plt.tick_params(labelsize = 10)
# plt.minorticks_on()
# plt.xticks(np.arange(-0, 110, step=10))
# plt.show()

# print(np.arange(90,101,1))

fig, ax = plt.subplots()

x = [100, 80, 50, 20]
y = range(0, len(x))


color = ["red" if i == 20 else "blue" for i in x]
ax.bar(y,x,color=color)
plt.show()