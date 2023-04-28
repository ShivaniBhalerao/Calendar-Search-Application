## Calendar Search

### About
This project improves the search experience in calendar applications by developing an efficient calendar text search application using NLP techniques and a combination of synonym similarity score and Levenshtein distance, and utilizing Flask for frontend and Elasticsearch for backend and indexing.

### How to run this project?
You can run this project using the command 'python login.py' (make sure that the elastic search deployment is running.)

### How was this project built?
Step 1: Dataset to generate json files is downloaded from:
"https://data.world/cegomez22/dimdate/workspace/file?filename=calendar.csv" using the query "SELECT * FROM calendar where year>=2005;"

Step 2 (Project.ipynb): Used the above data structure and generated random events(given in the google collab notebook Project.ipynb) and stored json files with 100K users to a git repo:
https://github.com/ShivaniBhalerao/Calendar-Search-Data-Generator

Step 3 (Project V2.ipynb): Using these json files processed the generated events of calendar and created elastic search index deployed on https://cloud.elastic.co/deployments/
(For now only used user_event_1000.json, this could be scaled later)

emnlp_dict.txt used in this notebook is the dataset to normalize slang language(Eg: bday to birthday) downloaded from:
https://www.kaggle.com/datasets/841dab43e3e9047809fa046ad6fe0e3f97879c9eba46f44752829b01897ed93c?datasetId=525901&select=emnlp_dict.txt

Step 4:
Now comes the Flask project where I created calendar using a python library 'tkinter,tkcalendar' (referred: https://tkcalendar.readthedocs.io/en/stable/example.html), where you can view the events ('View Calendar' button) that are indexed previously, and add new events which will also be indexed.
You can also search for the events or events on specific dates using Query something button.


### Requirements:
Libraries:
1. flask
2. tkinter
3. tkcalendar
4. elasticsearch
5. nltk
6. sutime (setup and usage referred from https://github.com/FraBle/python-sutime) to extract date from the serach query
7. fuzzywuzzy (https://pypi.org/project/fuzzywuzzy/)


