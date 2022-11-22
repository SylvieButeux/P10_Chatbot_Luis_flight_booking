 
import json
import pytest
from config import DefaultConfig

import http.client , urllib.request, urllib.parse, urllib.error, base64
print(http.client.__file__)


def test_key_azure_appinsight_Ok():
     assert DefaultConfig.APPINSIGHTS_INSTRUMENTATION_KEY == "f3001851-bd7c-4c79-b3f7-fa0cc1c30e55"
     #return DefaultConfig.APPINSIGHTS_INSTRUMENTATION_KEY == "f3001851-bd7c-4c79-b3f7-fa0cc1c30e55"

def test_key_azure_appinsight_NOk():
     assert DefaultConfig.APPINSIGHTS_INSTRUMENTATION_KEY != "" 
     #return DefaultConfig.APPINSIGHTS_INSTRUMENTATION_KEY == "" 

def test_key_app_luis_Ok():
     assert DefaultConfig.LUIS_API_KEY == "ad25e2608a7b496ca39d639f74a0dcd8"
     #return DefaultConfig.LUIS_API_KEY == "ad25e2608a7b496ca39d639f74a0dcd8"

def test_key_app_luis_NOk():
     assert DefaultConfig.LUIS_API_KEY != "" 
     #return DefaultConfig.LUIS_API_KEY != "" 



def test_luis_http():
#test avec naviguateur
# query="Hi I'd like to go to Caprica from Berlin, between Sunday August 21, 2016 and Wednesday August 31, 2016 with 1500$" 
# https://westeurope.api.cognitive.microsoft.com/luis/prediction/v3.0/apps/5a1ffd5c-f47a-49c7-8f17-2c91c3b53eab/slots/production/predict?query=Hi%20I%27d%20like%20to%20go%20to%20Caprica%20from%20Berlin,%20between%20Sunday%20August%2021,%202016%20and%20Wednesday%20August%2031,%202016%20with%201500$&subscription-key=ad25e2608a7b496ca39d639f74a0dcd8&show-all-intents=true&verbose=true

    conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
    conn.request("GET", "/luis/prediction/v3.0/apps/5a1ffd5c-f47a-49c7-8f17-2c91c3b53eab/slots/production/predict?query=Hi%20I%27d%20like%20to%20go%20to%20Caprica%20from%20Berlin,%20between%20Sunday%20August%2021,%202016%20and%20Wednesday%20August%2031,%202016%20with%201500$&subscription-key=ad25e2608a7b496ca39d639f74a0dcd8&show-all-intents=true&verbose=true")
    response = conn.getresponse()

    data = response.read()
   # print(data)
    obj_python = json.loads(data)
    print("Intent: ",     obj_python['prediction']['topIntent'])
    print("Origin: ",     obj_python['prediction']['entities']['or_city'])
    print("Destination: ",obj_python['prediction']['entities']['dst_city'])
    print("Budget: ",     obj_python['prediction']['entities']['budget'])
    print("Date debut: " ,obj_python['prediction']['entities']['datetimeV2'][0]['values'][0]['resolution'][0]['start'])
    print("Date fin: "   ,obj_python['prediction']['entities']['datetimeV2'][0]['values'][0]['resolution'][0]['end'])

    test_result=0
    if(obj_python['prediction']['topIntent']!= "book"): 
        test_result+=1
    if(str(obj_python['prediction']['entities']['or_city'])!="['Berlin']" ): 
        test_result+=10
    if(str(obj_python['prediction']['entities']['dst_city'])!="['Caprica']" ): 
         test_result+=100
    if(str(obj_python['prediction']['entities']['budget'])!="['1500$']" ): 
         test_result+=1000
    if(obj_python['prediction']['entities']['datetimeV2'][0]['values'][0]['resolution'][0]['start']!="2016-08-21" ): 
         test_result+=10000
    if(obj_python['prediction']['entities']['datetimeV2'][0]['values'][0]['resolution'][0]['end']!="2016-08-31" ): 
         test_result+=10000
    if(test_result==0):
         print("test luis resultat = OK ")
    else:
         print("test luis  = NOK err:",test_result)
    conn.close()

    assert test_result == 0
    #return test_result == 0

# verification de toutes les fonctions de test  

rslt1 = test_key_azure_appinsight_Ok()
rslt2 = test_key_azure_appinsight_NOk()
rslt3 = test_key_app_luis_Ok()
rslt4 = test_key_app_luis_NOk()
rslt5 = test_luis_http()
print("================")
cpt_err=0
if(rslt1==True):
     print("TEST1 OK")
else:
     cpt_err+=1
     print("TEST1 NOK")

if(rslt2==True):
     print("TEST2 OK")
else:
     cpt_err+=1
     print("TEST2 NOK")

if(rslt3==True):
     print("TEST3 OK")
else:
     cpt_err+=1
     print("TEST3 NOK")

if(rslt4==True):
     print("TEST4 OK")
else:
     cpt_err+=1
     print("TEST4 NOK")

if(rslt5==True):
     print("TEST5 OK")
else:
     cpt_err+=1
     print("TEST5 NOK")

print("================")
if(cpt_err==0):
     print("ALL TEST IS OK")
else:
     print("NUMBER OF TEST NOK :",cpt_err)
print("================")
 
