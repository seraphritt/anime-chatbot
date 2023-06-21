from jikanpy import Jikan
import random
jikan = Jikan()

def possible_query(result):
    return result["pagination"]["items"]["count"] != 0

def query(command, arguments="") -> list[str]:
    # quem eh o personagem x ?
    if command.lower() == "characters":
        result = jikan.search("characters", arguments)
        if not possible_query(result):
            return []
        else:
            return result["data"][0]['about']
    # sobre o que eh o anime x ?    
    elif command.lower() == "anime":
        result = jikan.search("anime", arguments)
        if not possible_query(result):
            return []
        else:
            return result["data"][0]["synopsis"]  
    # quais os generos do anime x ?
    elif command.lower() == "genres":
        result = jikan.search("anime", arguments)
        if not possible_query(result):
            return []
        else:
            ans = []
            for genre in result["data"][0]['genres']:
                ans.append(genre['name'])
            return ans
    # recomendacao
    elif command.lower() == 'recommendations':
        result = jikan.recommendations(type='anime')
        rand = random.randint(0, len(result['data'])-1)
        ans = []
        for anime in result['data'][rand]['entry']:
            ans.append(anime['title'])
        ans.append(result['data'][rand]['content'])
        return ans
    # anime da temporada
    elif command.lower() == 'season':
        result = jikan.seasons(extension='now')
        if not possible_query(result):
            return []
        else:
            rand = random.randint(0, len(result['data'])-1)
            return [result['data'][rand]['title'], result['data'][rand]['synopsis']]
    # anime top x ?
    elif command.lower() == 'top':
        top = int(arguments)
        items = 0
        page = 1
        result = jikan.top(type='anime', page=page)

        while(possible_query(result)):
            items += result["pagination"]["items"]["count"]
            if top > items:
                page += 1
                top -= items
                result = jikan.top(type='anime', page=page)
            else:
                return result['data'][top-1]['title']
        return []
    else:
        return "I don't know the answer."


## query (1) - quem é o personagem _ ?:
# print(query("characters", "luffy"))

## query (2) - sobre o que é o anime _ ?
# print(query("anime", "one piece"))

## query (3) - qual o gênero do anime _ ?
# print(query("genres", "one piece"))

## query (4) - me recomende um anime.
# print(query("recommendations"))

## query (5) - me fale um anime da temporada
# print(query("season"))

## query (6) - qual o anime top _ ?
# print(query("top", "1"))