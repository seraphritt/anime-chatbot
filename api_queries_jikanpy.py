from jikanpy import Jikan
import re
jikan = Jikan()
# available search queries
# characters / animes


def query_filter(query_result: str) -> str:
    resu = re.sub(r'\[.*\n', "", query_result)  # remove o [Written by...]
    resu = re.sub(r'\(.*\n', "", resu)  # remove o (Source ...)
    resu = re.sub(r'.*:.*\n', "", resu)  # remove as informações adicionais do personagem
    # informações adicionais como age, birthday...
    return resu


def query(command: str, arguments: list[str]) -> list[str]:
    result = jikan.search(command, *arguments)
    # se não houver resultado
    if command.lower() == "characters":
        if result["pagination"]["items"]["count"] == 0:
            return []
        else:
            return [result["data"][0]["about"]]
    elif command.lower() == "anime":
        if result["pagination"]["items"]["count"] == 0:
            return []
        else:
            return [result["data"][0]["synopsis"]]
    elif command.lower() == "manga":
        if result["pagination"]["items"]["count"] == 0:
            return []
        else:
            res = []
            for each in range(len(result["data"][0]["titles"])):
                res.append(result["data"][0]["titles"][each]["title"])
            return res


# a query é retornada em uma lista de strings

# query para personagem:
# query("characters", ["Tengen Uzui"])[0]
# query para anime:
# query("anime", ["Pokémon Pikachu"]))[0]

# passando a query pelo filtro

# query de anime

# resultado = query("anime", ["Boruto"])[0]
# resultado = query_filter(resultado)
# print(resultado)
# query de characters

# resultado = query("characters", ["Sasuke"])[0]
# resultado = query_filter(resultado)
# print(resultado)

