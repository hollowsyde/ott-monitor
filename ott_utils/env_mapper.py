from dotenv import load_dotenv
import os
import json

load_dotenv()

def _load_url_map():
    """
    Private function to load and parse the URL_MAP from the environment.
    It handles potential errors like the variable not being set or being invalid JSON.
    """
    url_map_str = os.getenv("URL_MAP")

    if not url_map_str:
        # If the URL_MAP is not defined in the .env file at all
        raise ValueError("Environment variable 'URL_MAP' not found. Please define it in your .env file or via CLI.")

    try:
        # Convert the JSON string into a Python dictionary
        url_map_dict = json.loads(url_map_str)
        return url_map_dict
    except json.JSONDecodeError:
        # If the string in the .env file is not valid JSON
        raise ValueError("The 'URL_MAP' in your .env file is not valid JSON. Please check its format.")

# Load the map once when the module is imported.
URLS = _load_url_map()

def get_url(channel_name: str) -> str:
    """
    Retrieves a specific URL from the loaded URL_MAP based on the channel name.
    
    Args:
        channel_name: The key for the URL you want (e.g., 'sales', 'marketing').

    Returns:
        The corresponding URL as a string.
        
    Raises:
        KeyError: If the channel_name is not found in the map.
    """
    channel_name_lower = channel_name.lower()

    if channel_name_lower not in URLS:
        raise KeyError(f"Channel '{channel_name}' not found in the URL_MAP. Available channels are: {list(URLS.keys())}")
        
    return URLS[channel_name_lower]
