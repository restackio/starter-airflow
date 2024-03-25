from airflow.decorators import dag, task
from pendulum import datetime 
import pandas as pd
import requests

MY_FAVORITE_POKEMON = "pikachu"
MY_OTHER_FAVORITE_POKEMON = "vulpix"

@dag(
    start_date=datetime(2022, 12, 20),
    schedule="@daily",
    catchup=False
)
def fetch_pokemon_data_dag():

    @task 
    def extract_data():
        """Extracts data from the Pokémon API. Returns a JSON serializeable dict."""

        r1 = requests.get(f"https://pokeapi.co/api/v2/pokemon/{MY_FAVORITE_POKEMON}")
        r2 = requests.get(f"https://pokeapi.co/api/v2/pokemon/{MY_OTHER_FAVORITE_POKEMON}")

        return {
            "pokemon": [f"{MY_FAVORITE_POKEMON}", f"{MY_OTHER_FAVORITE_POKEMON}"],
            "base_experience": [r1.json()["base_experience"], r2.json()["base_experience"]],
            "height" : [r1.json()["height"], r2.json()["height"]]
        }

    @task
    def calculate_xp_per_height(pokemon_data_dict):
        """Calculates base XP per height and returns a pandas DataFrame."""

        df = pd.DataFrame(pokemon_data_dict)

        df["xp_per_height"] = df["base_experience"] / df["height"]

        return df

    @task 
    def print_xp_per_height(pokemon_data_df):
        """Retrieves information from a pandas DataFrame in the custom XCom
        backend. Prints out Pokémon information."""

        for i in pokemon_data_df.index:
            pokemon = pokemon_data_df.loc[i, 'pokemon']
            xph = pokemon_data_df.loc[i, 'xp_per_height']
            print(f"{pokemon} has a base xp to height ratio of {xph}")

    print_xp_per_height(calculate_xp_per_height(extract_data()))

fetch_pokemon_data_dag()
