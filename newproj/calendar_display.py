#Referred from https://tkcalendar.readthedocs.io/en/stable/example.html
try:
    import tkinter as tk
    from tkinter import ttk,Button,Label,Entry
except ImportError:
    import Tkinter as tk
    import ttk

import datetime
from flask import Flask
from tkcalendar import Calendar
import search
import helper

#import app
import elastic_search_functions
import add_event

def add_event_on_date():
    add_event.add_event_func(cal.get_date(),user)

def search_func():
    response_arr=search.start_search(str(raw_query.get()),user)
    response_str=""
    if len(response_arr)==0:
        response_str='Oops! No such event!!!!'

    for item in response_arr:
        response_str=response_str+str(item[0])+'     '+item[1]+'     '+item[2]+'\n'
    response.config(text=response_str)

def view_events():
    top = tk.Toplevel()
    top.geometry('1000x1000')
    #print('user',user)
    app=Flask(__name__)
    with app.app_context():
        search_obj=elastic_search_functions.search(user)
        festival_obj=elastic_search_functions.search_festivals()
        #print('festival_obj',festival_obj)
        search_obj=search_obj+festival_obj
    
    #print(search_obj)
    global cal
    cal = Calendar(top, selectmode='day',font='Arial 40')
    for data in search_obj:
        data=data['_source']
        year=int(data['year'])
        month=int(data['month'])
        day=int(data['day'])
        date_str=str(month)+'/'+str(day)+'/'+str(year)
        date_date=datetime.datetime.strptime(date_str,'%m/%d/%Y')

        event=data['event']
        #print(date_str,data['weekday_num'],event)

        date = date_date
        cal.calevent_create(date, event, 'event')

    cal.tag_config('event', background='red', foreground='yellow')

    cal.pack(fill="both", expand=True)

    add_event_button=Button(top,text="Add Event",command=add_event_on_date,font='Arial 31').pack()
    #add_event_button.
    ttk.Label(top, text="Hover to view the events.",font='Arial 22').pack()

def search_query():
    top = tk.Toplevel()
    top.geometry('500x500')

    enter_query=Label(top,text='Any queries?',fg='white',font=('Arial',22))
    enter_query.place(x=40,y=40)
    global raw_query
    raw_query=Entry(top,text='query')
    raw_query.place(x=210,y=40)
    
    search=Button(top,text='Search',command=search_func,fg='black',font=('Arial',12))
    search.place(x=140,y=100)
    global response
    response=Label(top,text='',fg='white',font=('Arial',22),anchor="w")
    response.place(x=100,y=140)



def start(user_name,root):
    global user
    user=user_name
    helper.set_loggedin_user(user)
    root.title(user_name)
    top=tk.Toplevel(root)
    ttk.Button(top, text='View Calendar', command=view_events).pack(padx=10, pady=10)
    ttk.Button(top, text='Query something', command=search_query).pack(padx=10, pady=10)
