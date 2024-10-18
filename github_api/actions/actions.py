from typing import Any, Text, Dict, List
from rasa_sdk.events import AllSlotsReset
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import aiohttp
from collections import Counter
from functools import lru_cache
import json

class ActionGetGithubRepositoriesForm(Action):

    def name(self) -> Text:
        return "action_get_github_repositories"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        github_username = tracker.get_slot('github_username')
        linguagem = tracker.get_slot('linguagem')

        if not github_username:
            dispatcher.utter_message(
                text="Nome de usuário do GitHub inválido. Tente novamente.")
            return [AllSlotsReset()]
        else:
            github_repositories = await get_github_repositories(github_username, linguagem)
            dispatcher.utter_message(
                response='utter_github_response', repositories=github_repositories)
            return [AllSlotsReset()]
              

@lru_cache(maxsize=128)
async def get_github_repositories(github_username: Text, linguagem: Text =None) -> Text:
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.github.com/users/{github_username}/repos"
            async with session.get(url) as response:
                if response.status == 200:
                    github_repositories = await response.json()
                    if not github_repositories:
                        return f"Sem repositórios"

                    repo_messages = []
                    for github_repositorie in github_repositories:
                        repo_name = github_repositorie["name"]
                        languages_url = github_repositorie["languages_url"]
                        async with session.get(languages_url) as languages_response:
                            if languages_response.status == 200:
                                languages = await languages_response.json()
                                if languages:
                                    top_language = Counter(languages).most_common(1)[0][0]
                                    if linguagem is None or top_language.lower() == linguagem.lower():
                                        repo_messages.append(f"- {repo_name} ({top_language})")
                            else:
                                repo_messages.append(f"- {repo_name} (erro ao obter linguagem)")
                    
                    if repo_messages:
                        return f"Repositórios de {github_username} com a linguagem {linguagem}:\n\n" + "\n".join(repo_messages)
                    else:
                        return f"Não há repositórios de {github_username} com a linguagem {linguagem}."

                elif response.status == 403:
                    return f"Erro 403: Acesso à API do GitHub bloqueado. Tente novamente mais tarde. Pode ter atingido o limite de requisições."

                elif response.status == 404:
                    return f"Desculpe, não encontrei o usuário {github_username} no GitHub."

                else:
                    return f"Erro ao acessar a API do GitHub. Código de status: {response.status}"

    except aiohttp.ClientError as e:
        return f"Erro na requisição à API do GitHub: {e}"
    except json.JSONDecodeError as e:
        return f"Erro ao decodificar a resposta da API do GitHub: {e}"
