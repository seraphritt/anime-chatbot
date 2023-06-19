from jikanpy import Jikan
jikan = Jikan()
# available search queries
# characters / animes / manga (nomes sinônimos)


def query(command: str, arguments: list[str]) -> list[str]:
    result = jikan.search(command, *arguments)
    # se não houver resultado
    if command.lower() == "characters":
        if result["pagination"]["items"]["count"] == 0:
            return []
        else:
            return result["data"][0]['about']
    elif command.lower() == "anime":
        if result["pagination"]["items"]["count"] == 0:
            return []
        else:
            return result["data"][0]["synopsis"]
    elif command.lower() == "manga":
        if result["pagination"]["items"]["count"] == 0:
            return []
        else:
            res = []
            for each in range(len(result["data"][0]["titles"])):
                res.append(result["data"][0]["titles"][each]["title"])
            return res


# query para personagem:
# query("characters", ["naruto"])
# query para anime:
# query("anime", ["boruto"]))
# query para título similar de manga:
# query("manga", ["demon slayer"])
