from tkinter import Tk,Entry,Label,Button
import calendar_display
from sutime import SUTime

def login():
    calendar_display.start(str(user_name.get()),root)

sutime=SUTime(mark_time_ranges=True, include_range=True)#added to load the sutime library at the start
root=Tk()

enter_username=Label(root,text='Enter your user name',fg='white',font=('Arial',12))
enter_username.place(x=40,y=40)

user_name=Entry(root,text='user name')
user_name.place(x=210,y=40)

submit=Button(root,text='Submit',command=login,fg='black',font=('Arial',12))
submit.place(x=140,y=100)

root.title('Login')
root.geometry('500x500')
root.mainloop()

