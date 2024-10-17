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

        if not github_username:
            dispatcher.utter_message(
                text="Nome de usuário do GitHub inválido. Tente novamente.")
            return [AllSlotsReset()]
        else:
            github_repositories = await get_github_repositories(github_username)
            print("fodvt", github_repositories)
            dispatcher.utter_message(
                response='utter_github_response', repositories=github_repositories)
            return [AllSlotsReset()]
              

@lru_cache(maxsize=128)
async def get_github_repositories(github_username: Text) -> Text:
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.github.com/users/{github_username}/repos"
            async with session.get(url) as response:
                print(response.status)
                if response.status == 200:
                    github_repositories = await response.json()
                    print("dacuyd", github_repositories)
                    if not github_repositories:
                        return f"Sem repositórios"

                    repo_messages = []
                    for github_repositorie in github_repositories[:5]:
                        repo_name = github_repositorie["name"] 
                        languages_url = github_repositorie["languages_url"]
                        async with session.get(languages_url) as languages_response:
                            print("vauyfpdv", languages)
                            if languages_response.status == 200:
                                languages = await languages_response.json()
                                if languages:
                                    top_language = Counter(languages).most_common(1)[0][0]
                                    repo_messages.append(f"- {repo_name} ({top_language})")
                                else:
                                    repo_messages.append(f"- {repo_name} (linguagem não detectada)")
                            else:
                                repo_messages.append(f"- {repo_name} (erro ao obter linguagem)")
                    if len(github_repositories) > 5:
                        repo_messages.append("E mais outros repositórios")

                    return f"Alguns repositórios de {github_username}:\n\n" + "\n".join(repo_messages)
                elif response.status == 403:
                    return f"Erro 403: Acesso à API do GitHub bloqueado. Tente novamente mais tarde. Pode ter atingido o limite de requisições."
                elif response.status == 404:
                    return f"Desculpe, não encontrei o usuário {github_username} no GitHub."
                else:
                    return f"Erro ao acessar a API do GitHub."
    except aiohttp.ClientError as e:
        return f"Erro na requisição à API do GitHub: {e}"
    except json.JSONDecodeError as e:
        return f"Erro ao decodificar a resposta da API do GitHub: {e}"
