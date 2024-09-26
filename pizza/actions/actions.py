from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionColetarInformacoesPedido(Action):
    def name(self) -> Text:
        return "action_coletar_informacoes_pedido"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tamanho = tracker.get_slot("tamanho")
        sabor = tracker.get_slot("sabor")

        if tamanho and sabor:
            dispatcher.utter_message(text=f"Seu pedido é uma pizza {tamanho} de {sabor}. Confirma?")
        else:
            dispatcher.utter_message(text="Para finalizar o pedido, por favor, informe o tamanho e o sabor da pizza.")

        return []