import pandas as pd

# Ищем 10 случайных строк из данных о птицах
api_url = "https://api.gbif.org/v1/species/search?rank=SPECIES&higherTaxonKey=212"  


headers = {"Content-Type": "application/json"}
response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    data = response.json()
    species = data.get("results", [])
    if species:
        df = pd.DataFrame(species)

    
        print(df[["key", "scientificName", "canonicalName", "kingdom", "phylum", "order", "family", "genus", "rank", "authorship"]].sample(10))
        df.to_csv("bird_species.csv", index=False)
    else:
        print("Список видов пуст.")
else:
    print("Ошибка запроса:", response.status_code)
