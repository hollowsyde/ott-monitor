from dotenv import load_dotenv

import os
import json

load_dotenv()

def generate_url_map(channel_file: str, url_file: str, output_file: str):
    """
    Generates a URL map from channel names and URLs.

    Args:
        channel_file: Path to the file containing channel names.
        url_file: Path to the file containing URLs.
        output_file: Path to the output JSON file where the URL map will be saved.
    """
    with open(channel_file, 'r') as cf, open(url_file, 'r') as uf:
        channels = [line.strip().lower() for line in cf if line.strip()]
        urls = [line.strip() for line in uf if line.strip()]

    if len(channels) != len(urls):
        raise ValueError("The number of channels and URLs must match.")

    url_map = {channel: url for channel, url in zip(channels, urls)}

    with open(output_file, 'w') as of:
        json.dump(url_map, of, indent=4)

    print(f"URL map saved to {output_file}")

if __name__ == "__main__":
    channel_file = 'channel.txt'
    url_file = 'url.txt'
    output_file = 'url_map.json'

    generate_url_map(channel_file, url_file, output_file)
    
    # Load the generated URL map into the environment variable
    with open(output_file, 'r') as f:
        url_map = json.load(f)
        os.environ['URL_MAP'] = json.dumps(url_map)