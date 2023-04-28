import datetime
import elastic_search_functions
import helper
import nltk
from fuzzywuzzy import fuzz
from flask import Flask
nltk.download('wordnet')
from nltk.corpus import wordnet
nltk.download('omw-1.4')

def get_user_data(user):
    app=Flask(__name__)
    with app.app_context():
        search_obj=elastic_search_functions.search(user)
        festival_obj=elastic_search_functions.search_festivals()
        search_obj=search_obj+festival_obj
    return search_obj

def get_user_data_within_date_range(user,start_date,end_date):
    app=Flask(__name__)
    with app.app_context():
        search_obj=elastic_search_functions.search_within_range(user,start_date,end_date)
        festival_obj=elastic_search_functions.festival_search_within_range(start_date,end_date)
        search_obj=search_obj+festival_obj
    return search_obj

def start_search(raw_query,user):
    processed_query=helper.clean_string(raw_query)

    processed_query,search_dates=helper.nlp_search_date_and_event(processed_query)
    print(processed_query,str(search_dates))

    search_obj=[]
    if len(search_dates)!=0:
        for search_date in search_dates:
            search_obj_within_date_range=get_user_data_within_date_range(user,search_date[0],search_date[1])
            search_obj=search_obj+search_obj_within_date_range
    else:
        search_obj=get_user_data(user)

    event_list=[]
    for data in search_obj:
        data=data['_source']
        event_list.append(data['event'])

    #only date search
    if len(processed_query)==0 or processed_query.isspace():
        print('Searching on given dates only.....')
        search_data=[]
        for data in search_obj:
            data=data['_source']
            data['date']=helper.sasdate_to_date(data['sasdate'])
            search_data.append(data)
                
        ranked_search_data=sorted(search_data,key=lambda dictionary:(dictionary['date']),reverse=True)

        num_of_response=0
        ranked_retrieved_data=[]

        while(num_of_response<len(ranked_search_data)):
            ranked_retrieved_data.append([ranked_search_data[num_of_response]['date'],helper.get_weekday(ranked_search_data[num_of_response]['weekday_num']),ranked_search_data[num_of_response]['event']])
            num_of_response=num_of_response+1

        return ranked_retrieved_data

    #no results
    elif len(search_obj)==0:
        print('No results.....')
        return list()

    #event search
    #sort according to synonym match score and if same then according to fuzzywuzzy
    synonym_match_score=dict()

    query_arr=helper.string_to_str_arr(processed_query)
    query_synonym_set=set()

    for word in query_arr:
        for synonym in wordnet.synsets(word):
            #print('q',word,synonym)
            for lem in synonym.lemmas():
                query_synonym_set.add(lem.name())

    if(len(query_synonym_set)==0):
        query_synonym_set=set(query_arr)
    
    query_syn_len=len(query_synonym_set)
                
    for data in search_obj:
        data=data['_source']
        event=data['event']
        event_arr=helper.string_to_str_arr(event)
        event_synonym_set=set()
        
        for word in event_arr:
            for synonym in wordnet.synsets(word):
                #print(event,word,synonym)
                for lem in synonym.lemmas():
                    event_synonym_set.add(lem.name())
        
        if(len(event_synonym_set)==0):
            event_synonym_set=set(event_arr)

        intersection=query_synonym_set.intersection(event_synonym_set)
        intersection_len=len(intersection)
        synonym_match_score[event]=intersection_len/query_syn_len
        data['syn_score']=intersection_len/query_syn_len
        
    #print('synonym_match_score:',synonym_match_score)
    fuzzy_wuzzy_stop_word=dict()

    for data in search_obj:
        data=data['_source']
        event=data['event']
        val=fuzz.token_sort_ratio(event,processed_query)
        fuzzy_wuzzy_stop_word[event]=val/100
        data['fw_score']=val/100
        data['date']=helper.sasdate_to_date(data['sasdate'])

    fuzzy_wuzzy_stop_word=dict(sorted(fuzzy_wuzzy_stop_word.items(), key=lambda pair:pair[1]))

    search_data=[]
    for data in search_obj:
        search_data.append(data['_source'])

    ranked_search_data=sorted(search_data,key=lambda dictionary:(dictionary['syn_score'],dictionary['fw_score'],dictionary['date']),reverse=True)
    if(ranked_search_data[0]['syn_score']==0 and ranked_search_data[0]['fw_score']==0):
        print('Irrelevant results found.....')
        return list()
        
    #print(ranked_search_data)
    num_of_response=0
    ranked_retrieved_data=[]
    ##print(num_of_res<=min(5,len(ranked_search_data)),ranked_search_data[num_of_res]['syn_score']!=0,ranked_search_data[num_of_res]['fw_score']!=0)
    while(num_of_response<min(10,len(ranked_search_data)) and (ranked_search_data[num_of_response]['syn_score']>0 or ranked_search_data[num_of_response]['fw_score']>0.60)):
        print(ranked_search_data[num_of_response]['fw_score'])
        ranked_retrieved_data.append([ranked_search_data[num_of_response]['date'],helper.get_weekday(ranked_search_data[num_of_response]['weekday_num']),ranked_search_data[num_of_response]['event']])
        num_of_response=num_of_response+1

    print('Results found')
    return ranked_retrieved_data
