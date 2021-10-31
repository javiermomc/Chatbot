# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List

import arrow
import random
import dateparser
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

city_db = {
    'cancun': 'America/Cancun',
    'merida': 'America/Merida',
    'matamoros': 'America/Matamoros',
    'monterrey': 'America/Monterrey',
    'mexico': 'America/Mexico_City',
    'ojinaga': 'America/Ojinaga',
    'chihuahua': 'America/Chihuahua',
    'hermosillo': 'America/Hermosillo',
    'mazatlan': 'America/Mazatlan',
    'bahia banderas': 'America/Bahia_Banderas',
    'tijuana': 'America/Tijuana',
    'dakota': 'America/North_Dakota/Center',
    'beulah': 'America/North_Dakota/Beulah',
    'indianapolis': 'America/Indiana/Indianapolis',
    'marengo':'America/Indiana/Marengo',
    'vincennes': 'America/Indiana/Vincennes',
    'petersburg': 'America/Indiana/Petersburg',
    'vevay': 'America/Indiana/Vevay',
    'louisville': 'America/Kentucky/Louisville',
    'monticello': 'America/Kentucky/Monticello',
    'pangnirtung': 'America/Pangnirtung'
}

jokes = [
    "I failed math so many times at school, I can’t even count.",
    "I used to have a handle on life, but then it broke.",
    "I was wondering why the frisbee kept getting bigger and bigger, but then it hit me.",
    "Don’t you hate it when someone answers their own questions? I do."
]

class ActionTellTime(Action):

    def name(self) -> Text:
        return "action_tell_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_place = next(tracker.get_latest_entity_values("place"), None)
        utc = arrow.utcnow()
        
        if not current_place:
            msg = f"It's {utc.to(city_db['mexico']).format('HH:mm')} now, but it may change in a second."
            dispatcher.utter_message(text=msg)
            return []
        
        current_place = current_place.lower()        
        tz_string = city_db.get(current_place, None)
        if not tz_string:
            msg = f"My database don't contain {current_place}. Sorry for the inconviniences. :)"
            dispatcher.utter_message(text=msg)
            return []
        
        msg = f"It's {utc.to(city_db[current_place]).format('HH:mm')} in {current_place} now. It may be changed a second when you read this message!"
        dispatcher.utter_message(text=msg)
        
        return []

class ActionTellName(Action):

    def name(self) -> Text:
        return "action_tell_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = next(tracker.get_latest_entity_values("name"), None)
        utc = arrow.utcnow()
        
        if not name:
            msg = f"Sorry, I didn't get your name, please try again :("
            dispatcher.utter_message(text=msg)
            return []
        msg = f"Hello {name}! I think its better to call you human instead :)"
        dispatcher.utter_message(text=msg)
        
        return []

class ActionTellJoke(Action):

    def name(self) -> Text:
        return "action_tell_joke"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        msg = random.choice(jokes)
        dispatcher.utter_message(text=msg)
        return []
