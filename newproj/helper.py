import datetime
from nltk.corpus import stopwords
from sutime import SUTime
import calendar

def set_loggedin_user(user):
    global loggedin_user
    loggedin_user=user
    return

def get_loggedin_user(user):
    return loggedin_user

def get_slang_dictionary():
    slang_dictionary=dict()
    with open("emnlp_dict.txt","r") as slang_file:
        for each_line in slang_file:
            each_line_split=each_line.strip().split("\t")
            slang_dictionary[each_line_split[0]]=each_line_split[1]

    #replace my, me I with the username
    slang_dictionary['my']=loggedin_user
    slang_dictionary['me']=loggedin_user
    slang_dictionary['i']=loggedin_user
    return slang_dictionary

def clean_string(raw_event):
    cleaned_event=""
    word=""
    slang_dict=get_slang_dictionary()
    index=0
    event_len=len(raw_event)
    
    for character in raw_event:
        if character.isalnum():
            cleaned_event=cleaned_event+character.lower()
            word=word+character.lower()
        if character==' ':
            if word in slang_dict:
                cleaned_event=cleaned_event.replace(word,slang_dict[word])
            word=""
            cleaned_event=cleaned_event+character
        if index==event_len-1:
            if word in slang_dict:
                cleaned_event=cleaned_event.replace(word,slang_dict[word])
            word=""
        index=index+1
    return cleaned_event

def convert_weekday_num(weekday_num):
    weekdays=['Mon','Tues','Wed','Thur','Fri','Sat','Sun']
    week_map={'Sun':1,'Mon':2,'Tues':3,'Wed':4,'Thur':5,'Fri':6,'Sat':7}
    return week_map[weekdays[weekday_num]]

def sasdate_to_date(sasdate):
    start_date = datetime.datetime.strptime('01/01/1960','%m/%d/%Y')
    return start_date+datetime.timedelta(days=sasdate)

def format_str_to_date(date_str):
    date_date=datetime.datetime.strptime(date_str,'%m/%d/%y')
    day=date_date.day
    month=date_date.month
    year=date_date.year
    weekday_num=convert_weekday_num(date_date.weekday())
    return day,month,year,weekday_num

def get_datekey(month,day,year):
    day_str=""
    if(day<10):
        day_str='0'+str(day)
    else:
        day_str=str(day)
    datekey_str=str(month)+day_str+str(year%100)
    return int(datekey_str)

def date_to_sasdate(date_str):
    date_date=datetime.datetime.strptime(date_str,'%m/%d/%y')
    start_date=datetime.datetime.strptime('1/1/1960','%m/%d/%Y')
    return abs((date_date-start_date).days)

def string_to_str_arr(str):
    str=str.split(' ')
    str_arr=[word for word in str if len(word)>0]
    return str_arr

def remove_stop_words(str):
    str_arr=string_to_str_arr(str)
    stopword_set=set(stopwords.words('english'))
    str_arr_no_stopword=[]
    for word in str_arr:
        if word not in stopword_set:
            str_arr_no_stopword.append(word)
    
    return str_arr_no_stopword

def get_weekday(weekday_num):
    weekdays=['Mon','Tues','Wed','Thur','Fri','Sat','Sun']
    return weekdays[int(weekday_num)-1]

def get_month_num(month):
    return False    

def format_sudate(date_str,flag):
    date_arr=date_str.split('-')
    for index in range(0,len(date_arr)):
        last_two_letters=date_arr[index][-2:]
        if last_two_letters.isnumeric() or last_two_letters=='XX': #month of jan
            date_arr[index]=last_two_letters
        else:
            first_four_letters=date_arr[index][0:4]
            if first_four_letters.isnumeric(): #year
                date_arr[index]=first_four_letters[-2:]
            else: #month
                date_arr[index]=first_four_letters[0:2]

    #only year
    if len(date_arr)==1:
        year_str=date_arr[0]
        if flag=='s':
            date_str='1/1/'+year_str
            print('date_str',date_str)
            return date_to_sasdate(date_str)
        else:
            date_str='12/31/'+year_str
            print('date_str',date_str)
            return date_to_sasdate(date_str)

    elif len(date_arr)==2:
        year_str=''
        if(date_arr[0]=='XX'):
            year_str='23' #for simplicity set to 2023 if year is unknown
        else:
            year_str=str(int(date_arr[0])%100)
        
        if flag=='s':
            date_str=date_arr[1]+'/1/'+year_str
            print('date_str',date_str)
            return date_to_sasdate(date_str)
        else:
            date_str=date_arr[1]+'/'+str(calendar.monthrange(int(year_str),int(date_arr[1]))[1])+'/'+year_str
            print('date_str',date_str)
            return date_to_sasdate(date_str)

    elif len(date_arr)==3:
        year_str=''
        if(date_arr[0]=='XX'):
            year_str='23' #for simplicity set to 2023 if year is unknown
        else:
            year_str=str(int(date_arr[0])%100)
        date_str=date_arr[1]+'/'+date_arr[2]+'/'+year_str
        print('date_str',date_str)
        return date_to_sasdate(date_str)
    
        

def get_date_range(date_arr):
    all_dates=[]
    for date_dict in date_arr:
        if date_dict['type']=='DATE':
            formatted_date_start=format_sudate(date_dict['value'],'s')
            formatted_date_end=format_sudate(date_dict['value'],'e')

            #if 'XXXX-12 to XXXX-02' was converted and XXXX was hardcoded to 2023
            if(formatted_date_start>formatted_date_end): 
                formatted_date_end=formatted_date_end+366
            print(formatted_date_start,formatted_date_end)
            all_dates.append([formatted_date_start,formatted_date_end])

        elif date_dict['type']=='DURATION':
            formatted_date_start=format_sudate(date_dict['value']['begin'],'s')
            formatted_date_end=format_sudate(date_dict['value']['end'],'e')
            #if 'XXXX-12 to XXXX-02' was converted and XXXX was hardcoded to 2023
            if(formatted_date_start>formatted_date_end): 
                formatted_date_end=formatted_date_end+366
            all_dates.append([formatted_date_start,formatted_date_end])
            print(formatted_date_start,formatted_date_end)    

    return all_dates    

def nlp_search_date_and_event(query_str):
    sutime = SUTime(mark_time_ranges=True, include_range=True)
    date_arr= sutime.parse(query_str)

    character_to_drop=set()
    for date_dict in date_arr:
        for index in range(date_dict['start'],date_dict['end']):
            character_to_drop.add(index)
    
    query_str_remove_date=""
    for index in range(0,len(query_str)):
        if index not in character_to_drop:
            query_str_remove_date=query_str_remove_date+query_str[index]
    query_set_no_stop_words=remove_stop_words(query_str_remove_date)
    
    remove_from_query=["events","event"]
    query_arr=[query_words for query_words in query_set_no_stop_words if query_words not in remove_from_query]
    final_event_query=' '.join(query_arr)
    print(date_arr)
    date_range=get_date_range(date_arr)
    print(str(date_range))

    return final_event_query,date_range
