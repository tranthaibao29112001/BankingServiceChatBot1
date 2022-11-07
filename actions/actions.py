# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#
#
class ActionShowBalance(Action):

    def name(self) -> Text:
        return "action_show_balance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        card_id = tracker.get_slot("card_id")
        if not card_id:
            dispatcher.utter_message(text="I dont know your card id")
        else:
            dispatcher.utter_message(text="Your balance is: 1 000 000 VND")

        return []
class ActionGreetWithName(Action):

    def name(self) -> Text:
        return "action_greet_with_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_name = tracker.get_slot("user_name")
        if not user_name:
            dispatcher.utter_message(text="I dont know your name")
        else:
            dispatcher.utter_message(text=f"Hello {user_name}")

        return []
