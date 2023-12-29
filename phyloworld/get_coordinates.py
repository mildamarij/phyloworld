import pandas as pd
import requests

def get_country_coordinates(country):
    """
    Retrieve latitude and longitude coordinates for a specified
    country using the Nominatim OpenStreetMap API.

    Parameters:
    - country (str): The name of the country for which
    coordinates are to be obtained.

    Returns:
    - output (list): A list containing the latitude and
    longitude coordinates for the specified country.
    """
    print(f"Getting coordinates for {country}")
    url = "{0}{1}{2}".format(
        "http://nominatim.openstreetmap.org/search?country=",
        country,
        "&format=json&polygon=0",
    )
    response = requests.get(url).json()[0]
    if not response or len(response) == 0:
        raise ValueError(f"Coordinates not found for {country}")
    coordinates = [response.get(key) for key in ["lat", "lon"]]
    output = [float(i) for i in coordinates]
    
    return output

def merge_coordinates_with_metadata(metadata):
    """
    Merge metata with latitude and longitude coordinates for each
    unique country present in the "Country" column.

    Parameters:
    - metadata (pd.DataFrame): A DataFrame containing metadata with a "Country" column.

    Returns:
    - merged_metadata (pd.DataFrame): The input metadata DataFrame with additional columns
    for latitude and longitude coordinates corresponding to each country.
    """
    country_data_list = []
    for country in set(metadata["Country"]):
        country_name = country.lower().replace(" ", "+")
        coordinates_list = get_country_coordinates(country_name)
        country_data_list.append([country, coordinates_list[0], coordinates_list[1]])
    country_data = pd.DataFrame(
        country_data_list, columns=["Country", "Latitude", "Longitude"]
    )
    merged_metadata = metadata.merge(country_data, on="Country")

    return merged_metadata
