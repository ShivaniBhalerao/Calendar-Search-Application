from flask import Flask
from elasticsearch import Elasticsearch
import GLOBAL
app = Flask(__name__)

#@app.route('/search',methods=['GET'])
def search(user):
   print('elastic_search_functions: search()')   
   es = Elasticsearch(cloud_id=GLOBAL.cloud_id_val,basic_auth=(GLOBAL.es_user,GLOBAL.es_password))
   query={
      "size":100,
        "query":{
            "wildcard":{
               "user":{
               "value":user
            }
         }
      }
   }

   response=es.search(index='index_username_date',body=query)
   
   return response['hits']['hits']

def search_festivals():
   print('elastic_search_functions: search_festivals()')
   es = Elasticsearch(cloud_id=GLOBAL.cloud_id_val,basic_auth=(GLOBAL.es_user,GLOBAL.es_password))
   query={
      "size":500
   }

   response=es.search(index='festivals_index',body=query)
   
   return response['hits']['hits']


def search_within_range(user,start_date,end_date):
   es = Elasticsearch(cloud_id=GLOBAL.cloud_id_val,basic_auth=(GLOBAL.es_user,GLOBAL.es_password))
   query={
      "size":100,
        "query": {
            "bool":{
               "must": [
               {
                  "match":{
                  "user":user
                  }
               },
               {
                  "range": {
                     "sasdate": {
                        "gte": start_date,
                        "lte": end_date
                     }
                  }
               }
            ]
         }
      }
   }

   response=es.search(index='index_username_date',body=query)
   
   return response['hits']['hits']
   


def festival_search_within_range(start_date,end_date):
   es = Elasticsearch(cloud_id=GLOBAL.cloud_id_val,basic_auth=(GLOBAL.es_user,GLOBAL.es_password))
   query={
      "size":100,
        "query": {
            "range": {
            "sasdate": {
              "gte": start_date,
              "lte": end_date
            }
          }
      }
   }

   response=es.search(index='festivals_index',body=query)
   
   return response['hits']['hits']
   
#@app.route('/add_event',methods=['GET'])
def add_event(query_data):
   print('elastic_search_functions: add_event()')
   es = Elasticsearch(cloud_id=GLOBAL.cloud_id_val,basic_auth=(GLOBAL.es_user,GLOBAL.es_password))
   id_str=query_data['user']+'_'+str(query_data['sasdate'])
   response=es.index(index='index_username_date',id=id_str,body=query_data)

   return response

"""
@app.route('/',methods=['GET'])
def show_index():
   es_user='elastic'
   es_password="FnkDbmxTmqG2vpkvdSuNfhi6"
   cloud_id_val="IR_deployment:dXMtd2VzdDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQ5YmE1ZmUxMTA1NGU0NzNhODRjMDdjZWM4ZWFlYjZlNiQ4NWQ5NmIyYzJlYzA0YTZiYTI3OWFkZDZmZTI0Y2YwMw=="
   es = Elasticsearch(cloud_id=cloud_id_val,basic_auth=(es_user,es_password))
   
   response=es.get(index='index_username_date',id='user_1_22497')
   print(response)
   return jsonify(response['_source'])
"""

if __name__ == '__main__':
   app.run('127.0.0.1',port=5000)
