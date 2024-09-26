# from typing import Any, Text, Dict, List

# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher


# class ActionResponderCapital(Action):

#     def name(self) -> Text:
#         return "action_responder_capital"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         pais = tracker.get_slot("pais")

#         capitais = {
#             "brasil": "Brasília",
#             "portugal" : "Lisboa",
#             "argentina" : "Buenos Aires",
#             "japão" : "Tokio",
#             "alemanha" : "Berlim"
#         }

#         if pais:
#             pais_lower = pais.lower()
#             if pais_lower in capitais:
#                 capital = capitais[pais_lower]
#                 dispatcher.utter_message(text=f"A capital de {pais} é {capital}.")
#             else:
#                 dispatcher.utter_message(response="utter_capital_nao_sei")
#         else:
#             dispatcher.utter_message(text="Não entendi a pergunta, poderia repetir?")
        
#         return []