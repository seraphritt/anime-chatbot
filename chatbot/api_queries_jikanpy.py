from jikanpy import Jikan
import random
import re
import requests
import json  
import time
jikan = Jikan()


def query_filter(query_result: list[str]) -> list[str]:
    output = []
    for each in query_result:
        resu = re.sub(r'\[.*', "", each)  # remove o [Written by...]
        resu = re.sub(r'\(.*\n', "", resu)  # remove o (Source ...)
        resu = re.sub(r'\(.*', "", resu)  # remove o (Source ...)
        resu = re.sub(r'.*:.*\n', "", resu)  # remove as informações adicionais do personagem
        # informações adicionais como age, birthday...
        output.append(resu)
    return output

def possible_query(result) -> bool:
    return result["pagination"]["items"]["count"] != 0

def query(command: str, arguments="") -> list[str]:
    # quem eh o personagem x ?
    if '*' in command:
        return ["Please don't use Regex Symbols on your question"]
    if command.lower() == "characters":
        result = jikan.search("characters", arguments)
        if not possible_query(result):
            return []
        else:
            return [result["data"][0]['about']]
    # sobre o que eh o anime x ?    
    elif command.lower() == "anime":
        result = jikan.search("anime", arguments)
        if not possible_query(result):
            return []
        else:
            return [result["data"][0]["synopsis"]]
    # quais os generos do anime x ?
    elif command.lower() == "genres":
        start = ["Sure thing: ", "Here you go: ", "Of course: "]
        result = jikan.search("anime", arguments)
        if not possible_query(result):
            return []
        else:
            ans = ""
            for genre in result["data"][0]['genres']:
                if ans != "": ans += ", "
                ans += genre['name']

            return random.choice(start) + ans + "."
    # recomendacao
    elif command.lower() == 'recommendations':
        result = jikan.recommendations(type='anime')
        rand = random.randint(0, len(result['data'])-1)
        ans = []
        for anime in result['data'][rand]['entry']:
            ans.append(anime['title'])
        ans.append(result['data'][rand]['content'])
        ans_string = f"Why don't you try watching '{ans[0]}' and '{ans[1]}'? {ans[2]}"
        return ans_string
    # anime da temporada
    elif command.lower() == 'season':
        start = ["A new anime is ", "Here you go: ", "A lastest anime sensation: "]
        result = jikan.seasons(extension='now')
        if not possible_query(result):
            return []
        else:
            rand = random.randint(0, len(result['data'])-1)
            return random.choice(start) + result['data'][rand]['title'] + "." 
    # anime top x ?
    elif command.lower() == 'top':
        start = ["The top one is: ", "Here you go: ", "The most epic anime ever: "]
        top = int(arguments)
        items = 0
        page = 1
        result = jikan.top(type='anime', page=page)
        while possible_query(result):
            items += result["pagination"]["items"]["count"]
            if top > items:
                page += 1
                top -= items
                result = jikan.top(type='anime', page=page)
            else:
                return random.choice(start) + result['data'][top-1]['title'] + "."
        return []
    # recomendacao de animes similares ao anime x
    elif command.lower() == 'similar':
        start = ["You should try ", "I recommend ", "A great choice is "]
        result = jikan.search('anime', arguments)
        if not possible_query(result):
            return []
        else:
            anime_id = result['data'][0]["mal_id"]
            time.sleep(0.5)
            res = requests.get(f'https://api.jikan.moe/v4/anime/{anime_id}/recommendations')
            result = json.loads(res.text)
            try:
                rand = random.randint(0, len(result['data'])-1)
                return random.choice(start) + result['data'][rand]['entry']['title'] + "."
            except (UnicodeDecodeError, ValueError):
                return ["Sorry, I can't recommend you a similar anime."]

    else:
        return ["I don't know the answer."]


## query (1) - quem é o personagem _ ?:
# resultado = query("characters", "luffy")
# resultado = query_filter(resultado)
# print(*resultado)

## query (2) - sobre o que é o anime _ ?
# resultado = query("anime", "one piece")
# print(resultado)
# resultado = query_filter(resultado)
# print(*resultado)

## query (3) - qual o gênero do anime _ ?
# print(*query("genres", "one piece"))

## query (4) - me recomende dois animes.
# print(query("recommendations"))

## query (5) - me fale um anime da temporada
# resultado = query("season")
# resultado = query_filter(resultado)
# print(resultado)

## query (6) - qual o anime top _ ?
# print(*query("top", "1"))

## query (7) - recomendacao de animes similares ao anime _ ?
# print(query("similar", "black cover"))