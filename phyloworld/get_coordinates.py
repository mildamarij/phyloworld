import pandas as pd
import requests

def get_country_coordinates(country):
    print(f"Getting coordinates for {country}")
    url = "{0}{1}{2}".format(
        "http://nominatim.openstreetmap.org/search?country=",
        country,
        "&format=json&polygon=0",
    )
    response = requests.get(url).json()[0]
    coordinates = [response.get(key) for key in ["lat", "lon"]]
    output = [float(i) for i in coordinates]
    return output

def merge_coordinates_with_metadata(metadata):
    coordinates = pd.DataFrame(columns=["Country", "Latitude", "Longitude"])
    countries = set(metadata["Country"])
    for country in countries:
        country_name = country.lower().replace(" ", "+")
        coordinates_list = get_country_coordinates(country_name)
        country_data = pd.DataFrame(
            [[country, coordinates_list[0], coordinates_list[1]]],
            columns=["Country", "Latitude", "Longitude"]
        )
        coordinates = pd.concat([coordinates, country_data], ignore_index=True)
    merged_metadata = metadata.merge(coordinates, on="Country")
    return merged_metadata