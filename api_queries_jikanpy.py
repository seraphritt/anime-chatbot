from jikanpy import Jikan
jikan = Jikan()
# available search queries
# characters / animes / manga (episodes)
result = jikan.search("characters", "Naruto")
# se não houver resultado
if result["pagination"]["items"]["count"] == 0:
    print("No results found")
else:
    print(result["data"][0]['about'])
