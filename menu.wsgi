import json
from pymongo import *
from bson.code import *
def application(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    received = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))
    
    #connect to the DB
    connection = Connection('localhost',27017)
    #get a DB instance
    db = connection['scrapy']
    
    
    #get a collection instance from the DB (collection =~ table in SQL) 
    collection = db['items']
    
    #get the ren languages for the received url
    langForUrl = collection.group(
        key = Code('function(doc){return {"url" : doc.url}}'),
        condition={"url" : received},
        initial={'lang': []},
        reduce=Code('function(doc, out){if (out.lang.indexOf(doc.lang) == -1) out.lang.push(doc.lang)}')
        )
    #langForUrl contains the url and the lan, we only pick the lan
    if (langForUrl):
        return json.dumps(langForUrl[0]['lang'])
    else:
        return ["None"]

    # for post in langForUrl:
    #     lang= post['lang']

    # f = open('/home/yelghali/Desktop/enseirb/stage/arvindkhadri-alipi-409655f/a11ypi_dict.json','r')
    # temp = f.read()

    # f.close()
    
    # temp_json = json.loads(temp, object_hook=dict)
    # myJSONObject = {}
    # for i in temp_json.keys():
    #     myJSONObject[i] = temp_json[i].keys()
    # #myJSONObject = {'http://a11y.in/a11ypi/idea/firesafety.html': ['lang.hi' ,'lang.kn']}
    # if myJSONObject.has_key(received):
    #     return [json.dumps(myJSONObject[received])]
   
