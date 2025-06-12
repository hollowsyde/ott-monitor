from datetime import datetime, timezone

import ffmpeg
import re
import subprocess
import sys

from ott_utils import env_mapper
from ott_utils.ott_logger import OTTLogger


def fetch_stream_logs(stream_url, channel_name, output_extension="txt"):

    # Initialize the OTTLogger with the channel name and output file extension
    logger = OTTLogger(channel_name, file_extension=f".{output_extension}")

    # Construct FFmpeg command for both black screen and freeze detection
    command = (
        ffmpeg.input(stream_url)
        .output("pipe:", format="null", vf="blackdetect=d=5:pix_th=0.01,freezedetect=n=0.01:d=5", loglevel="info")
        .compile()
    )

    # Run FFmpeg as a subprocess and read stderr in real-time
    process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True, bufsize=1)
    
    print("Fetching stream logs for " + channel_name + " ... \n")

    try:
        normal_flag = True
        freeze_entry = {}
        
        for line in process.stderr:
            line = line.strip()
            print(line)

            # Check for ts file reading
            if "frame=" in line:
                if normal_flag:
                    logger.normal_log(channel_name, datetime.now(timezone.utc).replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    normal_flag = True
            
            # Check for blank detection
            if "blackdetect" in line:
                black_matches = re.findall(r'(\w+):([\d.]+)', line)
                black_entry = {key: value for key, value in black_matches}
                black_duration = black_entry.get("black_duration", None)
                print(f"Blank screen detected for {black_duration} seconds on {channel_name}")
                
                logger.blank_log(
                    channel_name,
                    black_entry.get("black_duration", None),
                    datetime.now(timezone.utc).replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S')
                )

                normal_flag = False
            
            # Check for freeze detection
            if "freezedetect" in line:
                freeze_match = re.search(r'lavfi\.freezedetect\.(freeze_\w+):\s*([\d.]+)', line)
                if freeze_match:
                    key = freeze_match.group(1)
                    value = freeze_match.group(2)

                    freeze_entry[key] = value

                    if "freeze_start" in freeze_entry and "freeze_end" in freeze_entry and "freeze_duration" in freeze_entry:
                        freeze_duration = freeze_entry.get("freeze_duration", None)
                        print(f"Freeze screen detected for {freeze_duration} seconds on {channel_name}")

                        logger.freeze_log(
                            channel_name,
                            freeze_entry.get("freeze_duration", None),
                            datetime.now(timezone.utc).replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S')
                        )

                        freeze_entry = {}
                        normal_flag = False
    
    except Exception as e:
        print("\nStopping stream log monitoring for " + channel_name + " because of " + str(e) + "\n")
        process.terminate()

    # Wait for process to finish
    returncode = process.wait()

    if returncode != 0:
        print(f"Subprocess for {channel_name} exited with code {returncode}")
        # Exit with the same return code so systemd knows it failed
        sys.exit(returncode)

    # If normal, exit 0
    sys.exit(0)


if __name__ == "__main__":
    input_channel_name = sys.argv[1]
    mapped_stream_url = env_mapper.get_url(input_channel_name)
    fetch_stream_logs(mapped_stream_url, input_channel_name)
    