 
import json
from config import DefaultConfig
from flight_booking_recognizer import FlightBookingRecognizer
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    ConversationState,
    MemoryStorage,
    UserState,
    TelemetryLoggerMiddleware,
)

import http.client , urllib.request, urllib.parse, urllib.error, base64
print(http.client.__file__)

def test_bot_login():
        CONFIG=DefaultConfig()
        SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
        assertEqual(SETTINGS.app_id,"")
        
def test_bot_password(self):
        CONFIG=DefaultConfig()
        SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
        assertEqual(SETTINGS.app_password,"")
        
def test_flight_booking_isconfigured(self):
        CONFIG=DefaultConfig()
        RECOGNIZER = FlightBookingRecognizer(CONFIG)
        self.assertEqual(RECOGNIZER.is_configured,True)





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
#print(obj_python)
    print("Intent: ",     obj_python['prediction']['topIntent'])
    print("Origin: ",     obj_python['prediction']['entities']['or_city'])
    print("Destination: ",obj_python['prediction']['entities']['dst_city'])
    print("Budget: ",     str(obj_python['prediction']['entities']['budget']))
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
         print("resultat = OK ")
    else:
         print("resultat = NOK err:",test_result)
    conn.close()

    assert (test_result,0)




rslt = test_luis_http()

