from dotenv import load_dotenv

import os

load_dotenv()

def generate_url_conf_files(channel_file: str, url_file: str):
    """
    Generates a URL map from channel names and URLs.

    Args:
        channel_file: Path to the file containing channel names.
        url_file: Path to the file containing URLs.
    """
    with open(channel_file, 'r', encoding='utf-8') as cf, open(url_file, 'r', encoding='utf-8') as uf:
        channels = [line.strip().lower() for line in cf if line.strip()]
        urls = [line.strip() for line in uf if line.strip()]

    if len(channels) != len(urls):
        raise ValueError("The number of channels and URLs must match.")
    
    output_dir = '../.ott-configs'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, channel in enumerate(channels):
        output_file = f'{output_dir}/{channel}.conf'

        with open(output_file, 'w', encoding='utf-8') as of:
            of.write(f"URL={urls[i]}\n")


if __name__ == "__main__":
    channel_file = 'channel.txt'
    url_file = 'url.txt'

    generate_url_conf_files(channel_file, url_file)
