# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum
from typing import Dict
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import IntentScore, TopIntent, TurnContext

from booking_details import BookingDetails


class Intent(Enum):
    #BOOK_FLIGHT = "BookFlight"
    BOOK_FLIGHT = "book"   # NOTRE INTENT 
    CANCEL = "Cancel"
    NONE_INTENT = "NoneIntent"


def top_intent(intents: Dict[Intent, dict]) -> TopIntent:
    max_intent = Intent.NONE_INTENT
    max_value = 0.0

    for intent, value in intents:
        intent_score = IntentScore(value)
        if intent_score.score > max_value:
            max_intent, max_value = intent, intent_score.score

    return TopIntent(max_intent, max_value)

None
class LuisHelper:
    @staticmethod
    async def execute_luis_query(luis_recognizer: LuisRecognizer, turn_context: TurnContext    
    ) -> (Intent , object):
        #"""
        #Returns an object with preformatted LUIS results for the bot's dialogs to consume.
        #"""
        result = None
        intent = None
        
        #turn_context._activity.text= "Hi I'd like to go to Caprica from Busan, between Sunday August 21, 2016 and Wednesday August 31, 2016 with 1500$"

        try:
            recognizer_result = await luis_recognizer.recognize(turn_context)

            intent = (
                sorted(
                    recognizer_result.intents,
                    key=recognizer_result.intents.get,
                    reverse=True,
                )[:1][0]
                if recognizer_result.intents
                else None
            )

            if intent == Intent.BOOK_FLIGHT.value:
                result = BookingDetails()
                print("book found",intent)
                # We need to get the result from the LUIS JSON which at every level returns an array.

################### ORIGIN CITY
                origin_entities = recognizer_result.entities.get("$instance", {}).get(
                    "or_city", []
                )
                if len(origin_entities) > 0:
                    result.origin = origin_entities[0]["text"].capitalize()
                    print("result.origin              ok = ",result.origin)
                else:
                    result.origin = None
                    print("result.origin               not found  ")


################### DESTINATION CITY
                dest_entities = recognizer_result.entities.get("$instance", {}).get(
                    "dst_city", []
                )
                if len(dest_entities) > 0:
                    result.destination = dest_entities[0]["text"].capitalize()
                    print("result.destination         ok = ",result.destination)
                else:
                    result.destination =None
                    print("result.destination          not found  ")

################### START DATE TXT
                 
               

                start_date_entities = recognizer_result.entities.get("$instance", {}).get(
                    "str_date", []
                )
                if len(start_date_entities) > 0:
                    result.start_travel_date = start_date_entities[0]["text"].capitalize()
                    print("result.start_travel_date   ok = ",result.start_travel_date)
                else:
                    result.start_travel_date =None
                    print("result.start_travel_date   not found  ")

################### END DATE 

                end_date_entities = recognizer_result.entities.get("$instance", {}).get(
                    "end_date", []
                )
                if len(end_date_entities) > 0:
                    result.end_travel_date = end_date_entities[0]["text"].capitalize()
                    print("result.end_travel_date     ok = ", result.end_travel_date)
                else:
                    result.end_travel_date =None
                    print("result.end_travel_date     not found  ")  
 
###################  DATE START STOP

                tmp_start = None
                tmp_end = None

                date_entities = recognizer_result.entities.get("datetime", {})
                if date_entities:
                    if len(date_entities) > 0:
                        timex = date_entities[0]["timex"]
                        
                        # format range 
                        if date_entities[0]["type"] == "daterange":
                            print("timex =",timex[0])
                            datetime_value = timex[0].replace("(", "").replace(")", "").split(",")
                            tmp_start = datetime_value[0]
                            tmp_end = datetime_value[1]
                        
                        # format date unique
                        elif date_entities[0]["type"] == "date":
                            if(result.start_travel_date!=None):  # on verifie si le text orgine a ete detecte precedament
                                tmp_start = timex[0]
                            elif(result.end_travel_date!=None):
                                tmp_end   = timex[0]
                            else:                                # a default on remplit le start 
                                tmp_start = timex[0]

                result.start_travel_date=tmp_start
                result.end_travel_date=tmp_end



                
 ################### BUDGET 
                 
                budget_entities = recognizer_result.entities.get("$instance", {}).get(
                    "budget", []
                )
                if len(budget_entities) > 0:
                    result.budget = budget_entities[0]["text"].capitalize()
                    print("result.budget              ok = ", result.budget)
                else:
                    result.budget =None
                    print("result.budget               not found  ")                

        except Exception as exception:
            print(exception)

        return intent, result
