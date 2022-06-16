import numpy as np
import csv
import tkinter as tk


file = open('tainan.csv', 'r', encoding="utf-8")
data = csv.reader(file)
temptdata = list(data)
dataset = np.array(temptdata)


def findbus(a, b):
    # delete the blank character by using strip()
    a = a.strip()
    b = b.strip()
    bus_num_list = []
    bus_num_list_2 = []
    a_index = np.where(dataset == a)
    b_index = np.where(dataset == b)
    a_tem = [int(a) for a in a_index[0]]
    b_tem = [int(b) for b in b_index[0]]

    a_tem = list(set(a_tem))
    b_tem = list(set(b_tem))

    for num_1 in (a_tem):
        bus_num = dataset[num_1][0]
        bus_num_list.append(bus_num)
    for num_2 in (b_tem):
        bus_num_2 = dataset[num_2][0]
        bus_num_list_2.append(bus_num_2)

    bus_num_list = list(set(bus_num_list))
    bus_num_list_2 = list(set(bus_num_list_2))

    return bus_num_list, bus_num_list_2


def findroute(a, b, c):
    bus_1, bus_2 = findbus(a, b)

    l1 = []
    l2 = []  # row of a
    l3 = []  # row of b
    l4 = []
    message = []
    for i in range(len(bus_1), ):
        if (bus_1[i] in bus_2):
            l1.append(bus_1[i])

    # find the row of the data in l1
    if (c == 0):

        for j in range(dataset.shape[0]):
            for k in range(len(l1)):
                if (l1[k] in dataset[j, :]) and (a in dataset[j, :]) and (int(dataset[j][3]) == 0):
                    l2.append(j)



                elif (l1[k] in dataset[j, :]) and (b in dataset[j, :]) and (int(dataset[j][3]) == 0):
                    l3.append(j)

    l2 = list(set(l2))
    l2.sort()

    if (c == 1):

        for j in range(dataset.shape[0]):
            for k in range(len(l1)):
                if (l1[k] in dataset[j, :]) and (a in dataset[j, :]) and (int(dataset[j][3]) == 1):
                    l2.append(j)


                elif (l1[k] in dataset[j, :]) and (b in dataset[j, :]) and (int(dataset[j][3]) == 1):
                    l3.append(j)

    l2 = list(set(l2))
    l2.sort()

    for i in range(len(l2)):
        if (l2[i] < l3[i]) and (c == 0):
            num = l3[i] - l2[i]
            message.append('可搭乘%s號公車，去程方向:%s到%s %s站\n' % (l1[i], dataset[l2[i]][1], dataset[l3[i]][1], num))
        elif (l2[i] > l3[i]) and (c == 0):
            num = l2[i] - l3[i]
            message.append('可搭乘%s號公車，去程方向:%s到%s %s站\n' % (l1[i], dataset[l3[i]][1], dataset[l2[i]][1], num))
        elif (l2[i] > l3[i]) and (c == 1):
            num = l2[i] - l3[i]
            message.append('可搭乘%s號公車，返程方向:%s到%s %s站\n' % (l1[i], dataset[l3[i]][1], dataset[l2[i]][1], num))
        elif (l2[i] < l3[i]) and (c == 1):
            num = l3[i] - l2[i]
            message.append('可搭乘%s號公車，返程方向:%s到%s %s站\n' % (l1[i], dataset[l2[i]][1], dataset[l3[i]][1], num))
    if len(message) == 0:
        message.append('目前沒有可搭乘班次')

    return message


def F(N, E, x, y):
    return ((x - N) ** 2 + (y - E) ** 2) ** (1 / 2)


def Searchbus(N, E, D):
    place = []
    distance = 1000
    d = []
    n = 'no'
    p = 0
    list_1 = np.where(dataset == D)
    for i in list_1[0]:
        place.append(dataset[i][0])

    place = list(set(place))

    for i in place:
        list_2 = np.where(dataset == i)
        for j in list_2[0]:
            if (dataset[j][0] == i):
                X = float(dataset[j][5])
                Y = float(dataset[j][6])
                mix_distance = F(N, E, X, Y)
                d.append(mix_distance)
                if mix_distance <= distance:
                    p = i
                    n = dataset[j][1]
                    distance = mix_distance

    messages = '離你目前最近的公車站牌是%s號公車%s站,可搭這班車去%s' % (p, n, D)

    return messages


win = tk.Tk()
win.minsize(500, 300)
win.title('公車站點查詢系統')
win.geometry('500x500')
div_size = 500
lab_size = 50
# Using Frame to design the web page
frame1 = tk.Frame(win, width=div_size, height=lab_size)
frame2 = tk.Frame(win, width=div_size, height=lab_size)
frame3 = tk.Frame(win, width=div_size, height=lab_size)
frame4 = tk.Frame(win, width=div_size, height=lab_size)

frame1.grid(row=0, column=0, sticky=tk.W)
frame2.grid(row=1, column=0, sticky=tk.W)
frame3.grid(row=2, column=0, sticky=tk.W)
frame4.grid(row=3, column=0, sticky=tk.W)
var = tk.IntVar()


# When button is clicked, the function will be run
def button_event():
    message_1 = findroute(starting_entry.get(), ending_entry.get(), var.get())

    # Show the message
    message_label = tk.Label(frame2, text=(message_1))

    message_label.grid(row=4, column=0, ipadx=20, ipady=10, sticky=tk.W)
    # If place is not in dataset, the value of price is zero.They will not be show on the page


def button_event_2():
    message_2 = Searchbus(float(N_entry.get()), float(E_entry.get()), findbusstop_entry.get())

    # Show the message
    message_2_label = tk.Label(frame4, text=(message_2))

    message_2_label.grid(row=10, column=0, ipadx=20, ipady=10, sticky=tk.W)


starting_label = tk.Label(frame1, text='起點站:', font=('Arial', 12))
starting_entry = tk.Entry(frame1, font=('Arial', 12))
ending_label = tk.Label(frame1, text='終點站:', font=('Arial', 12))
ending_entry = tk.Entry(frame1, font=('Arial', 12))
radio_1 = tk.Radiobutton(frame1, text='去程', value=0, variable=var, font=('Arial', 12))
radio_2 = tk.Radiobutton(frame1, text='返程', value=1, variable=var, font=('Arial', 12))
check_button = tk.Button(frame2, text='尋找公車班次', fg='black', font=('Arial', 12), command=button_event)
findbusstop_label = tk.Label(frame3, text='目的地', font=('Arial', 12))
findbusstop_entry = tk.Entry(frame3, font=('Arial', 12))
N_label = tk.Label(frame3, text='目前所在緯度', font=('Arial', 12))
N_entry = tk.Entry(frame3)
E_label = tk.Label(frame3, text='目前所在經度', font=('Arial', 12))
E_entry = tk.Entry(frame3)
check_button_2 = tk.Button(frame4, text='尋找最近公車站牌', fg='black', font=('Arial', 12), command=button_event_2)

starting_label.grid(row=0, column=0)
starting_entry.grid(row=0, column=1, ipadx=20, ipady=10)
ending_label.grid(row=1, column=0)
ending_entry.grid(row=1, column=1, ipadx=20, ipady=10)
radio_1.grid(row=2, column=0, ipadx=20, ipady=10)
radio_2.grid(row=2, column=1, ipadx=20, ipady=10)
check_button.grid(row=3, column=0)
findbusstop_label.grid(row=6, column=0)
findbusstop_entry.grid(row=6, column=1, ipadx=20, ipady=10)
N_label.grid(row=7, column=0)
N_entry.grid(row=7, column=1)
E_label.grid(row=8, column=0)
E_entry.grid(row=8, column=1)
check_button_2.grid(row=9, column=0)

check_button['width'] = 37
check_button['height'] = 2
check_button_2['width'] = 37
check_button_2['height'] = 2

win.update()

win.mainloop()



