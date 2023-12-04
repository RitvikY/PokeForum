import requests


class Movie(object):
    def __init__(self, omdb_json, detailed=False):
        if detailed:
            self.genres = omdb_json["Genre"]
            self.director = omdb_json["Director"]
            self.actors = omdb_json["Actors"]
            self.plot = omdb_json["Plot"]
            self.awards = omdb_json["Awards"]

        self.title = omdb_json["Title"]
        self.year = omdb_json["Year"]
        self.imdb_id = omdb_json["imdbID"]
        self.type = "Movie"
        self.poster_url = omdb_json["Poster"]

    def __repr__(self):
        return self.title


# class MovieClient(object):
#     def __init__(self, api_key):
#         self.sess = requests.Session()
#         self.base_url = f"http://www.omdbapi.com/?apikey={api_key}&r=json&type=movie&"

#     def search(self, search_string):
#         """
#         Searches the API for the supplied search_string, and returns
#         a list of Media objects if the search was successful, or the error response
#         if the search failed.

#         Only use this method if the user is using the search bar on the website.
#         """
#         search_string = "+".join(search_string.split())
#         page = 1

#         search_url = f"s={search_string}&page={page}"

#         resp = self.sess.get(self.base_url + search_url)

#         if resp.status_code != 200:
#             raise ValueError(
#                 "Search request failed; make sure your API key is correct and authorized"
#             )

#         data = resp.json()

#         if data["Response"] == "False":
#             raise ValueError(f'[ERROR]: Error retrieving results: \'{data["Error"]}\' ')

#         search_results_json = data["Search"]
#         remaining_results = int(data["totalResults"])

#         result = []

#         ## We may have more results than are first displayed
#         while remaining_results != 0:
#             for item_json in search_results_json:
#                 result.append(Movie(item_json))
#                 remaining_results -= len(search_results_json)
#             page += 1
#             search_url = f"s={search_string}&page={page}"
#             resp = self.sess.get(self.base_url + search_url)
#             if resp.status_code != 200 or resp.json()["Response"] == "False":
#                 break
#             search_results_json = resp.json()["Search"]

#         return result

#     def retrieve_movie_by_id(self, imdb_id):
#         """
#         Use to obtain a Movie object representing the movie identified by
#         the supplied imdb_id
#         """
#         movie_url = self.base_url + f"i={imdb_id}&plot=full"

#         resp = self.sess.get(movie_url)

#         if resp.status_code != 200:
#             raise ValueError(
#                 "Search request failed; make sure your API key is correct and authorized"
#             )

#         data = resp.json()

#         if data["Response"] == "False":
#             raise ValueError(f'[ERROR]: Error retrieving results: \'{data["Error"]}\' ')

#         movie = Movie(data, detailed=True)

#         return movie




class Pokemon:
    API_BASE_URL = "https://pokeapi.co/api/v2/"

    def __init__(self):
        # Initialization if needed
        pass

    def get_pokemon(self, name_or_id):
        """ Fetch a Pokémon by its name or ID. """
        response = requests.get(f"{self.API_BASE_URL}pokemon/{name_or_id}")
        if response.status_code == 200:
            return self.parse_pokemon_data(response.json())
        else:
            return None

    def parse_pokemon_data(self, data):
        """ Parse the Pokémon data into a structured format. """
        parsed_data = {
            "name": data.get("name", "Unknown"),
            "types": [t["type"]["name"] for t in data.get("types", [])],
            "abilities": [a["ability"]["name"] for a in data.get("abilities", [])],
            "height": data.get("height", 0),  # Height in decimeters
            "weight": data.get("weight", 0),  # Weight in hectograms
            "stats": [{"name": s["stat"]["name"], "base_stat": s["base_stat"]} for s in data.get("stats", [])],
            "sprites": data.get("sprites", {}).get("front_default", ""),
            "forms": [{"name": form["name"], "url": form["url"]} for form in data.get("forms", [])],


            # Add more fields as needed
        }
        return parsed_data

    # Additional methods as needed

    def get_pokemon_evolutions(self, species_name):
        """ Fetch a Pokémon's evolution chain. """
        response = requests.get(f"{self.API_BASE_URL}pokemon-species/{species_name}")
        if response.status_code == 200:
            species_data = response.json()
            evolution_chain_url = species_data['evolution_chain']['url']
            return self.get_evolution_chain(evolution_chain_url)
        else:
            return None

    def get_evolution_chain(self, evolution_chain_url):
        """ Fetch and parse the evolution chain. """
        response = requests.get(evolution_chain_url)
        if response.status_code == 200:
            evolution_data = response.json()
            return self.parse_evolution_chain(evolution_data['chain'])
        else:
            return None

    def parse_evolution_chain(self, chain):
        """ Parse the evolution chain data. """
        evolutions = []
        current_stage = chain

        while current_stage:
            species_name = current_stage['species']['name']
            evolutions.append(species_name)
            # Move to the next stage in the chain
            current_stage = current_stage['evolves_to'][0] if current_stage['evolves_to'] else None

        return evolutions

    def get_pokemon_by_type(self, type_name):
        """ Fetch Pokémon list by type. """
        response = requests.get(f"{self.API_BASE_URL}type/{type_name}")
        if response.status_code == 200:
            type_data = response.json()
            return [pokemon['pokemon']['name'] for pokemon in type_data['pokemon']]
        else:
            return []
        
    def get_pokemon_by_ability(self, ability_name):
        """ Fetch Pokémon list by ability. """
        response = requests.get(f"{self.API_BASE_URL}ability/{ability_name}")
        if response.status_code == 200:
            ability_data = response.json()
            return [pokemon['pokemon']['name'] for pokemon in ability_data['pokemon']]
        else:
            return []




## -- Example usage -- ###
if __name__ == "__main__":
    import os

    # client = MovieClient(os.environ.get("OMDB_API_KEY"))

    # movies = client.search("guardians")

    # for movie in movies:
    #     print(movie)

    # print(len(movies))


    # Testing Pokemon class
    poke_client = Pokemon()
    pikachu = poke_client.get_pokemon("pikachu")
    print(pikachu)