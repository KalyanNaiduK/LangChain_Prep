
import requests

def name_nationality_api(specified_name: str):
    """
    description: This function makes a GET request to the name nationality API "http://127.0.0.1:8000/items/{specified_name}" and returns the JSON response.

    Args:
        specified_name (str): The name to query for nationality information.

    Returns:
        dict: The JSON response from the API.
    """
    url = f"http://127.0.0.1:8000/items/{specified_name}"
    response = requests.get(url)
    return response.json()

print(name_nationality_api("smith"))