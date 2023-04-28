import tkinter as tk
from tkinter import Entry,Label,Button
from flask import Flask
import elastic_search_functions
import helper


def add_event_confirm():
    raw_event_str=str(raw_event.get()),
    event=helper.clean_string(raw_event_str[0])
    day,month,year,weekday_num=helper.format_str_to_date(obj['date'])
    datekey=helper.get_datekey(month,day,year)
    sasdate=helper.date_to_sasdate(obj['date'])
    input_obj={
        'user':obj['user'],
        'event':event,
        'datekey':datekey,
        'sasdate':sasdate,
        'day':day,
        'month':month,
        'year':year,
        'weekday_num':weekday_num
    }
    app=Flask(__name__)
    with app.app_context():
        search_obj=elastic_search_functions.add_event(input_obj)
    print(search_obj)
    
def add_event_func(date,user):
    top = tk.Toplevel()
    top.geometry('500x500')

    enter_event=Label(top,text='Enter event:',fg='white',font=('Arial',22))
    enter_event.place(x=40,y=40)

    global raw_event
    raw_event=Entry(top,text='event')
    raw_event.place(x=210,y=40)

    global obj
    obj={
        'date':date,
        'user':user
    }
    
    confirm=Button(top,text='Confirm',command=add_event_confirm,fg='black',font=('Arial',12))
    confirm.place(x=140,y=100)
    #app=Flask(__name__)
    #with app.app_context():
    #    search_obj=elastic_search_functions.add_event(user)
    

