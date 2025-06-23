import os

class OTTLogger:
    """
    A versatile logger class to create and append to log files with a standardized format.

    This class writes entries in the format:
    STATE,channel_name,duration,timestamp
    
    Attributes:
        filename (str): The full path to the log file.
        file_extension (str): The extension of the log file ('.log', '.txt', or '.csv').
        channel_name (str): The name of the channel or application being logged.
    """

    def __init__(self, channel_name, log_path=".", file_extension=".log"):
        """
        Initializes the Logger instance.

        Args:
            channel_name (str): A name for the log source (e.g., app name, process name).
                                This will be the main part of the filename.
            log_path (str): The directory path where the log file will be saved.
                            Defaults to the current directory (".").
            file_extension (str): The desired file extension.
                                  Accepted values are ".log", ".txt", ".csv".
                                  Defaults to ".log".

        Raises:
            ValueError: If the provided file_extension is not one of the
                        accepted values.
        """
        allowed_extensions = [".log", ".txt", ".csv"]
        if file_extension not in allowed_extensions:
            raise ValueError(f"Invalid file extension. Allowed extensions are: {', '.join(allowed_extensions)}")

        self.channel_name = channel_name
        self.file_extension = file_extension

        # Create the directory if it doesn't exist.
        os.makedirs(log_path, exist_ok=True)
        
        # Generate a static filename and join it with the provided path.
        base_filename = f"log_{self.channel_name}{self.file_extension}"
        self.filename = os.path.join(log_path, base_filename)
            
    def _write_log(self, state, channel_name, duration, timestamp):
        """A private helper method to write a consistently formatted log line."""
        try:
            # The format is the same regardless of file extension
            #csv_log_line = f"{state.upper()},{channel_name},{duration},{timestamp}\n"
            json_log_line = f'{{"state": "{state.upper()}", "channel_name": "{channel_name}", "duration": "{duration}", "timestamp": "{timestamp}"}}\n'
            # Open in append mode ('a') to add to the file if it exists, or create it if not.
            with open(self.filename, 'a') as f:
                f.write(json_log_line)
        except IOError as e:
            print(f"Error writing to log file: {e}")

    def normal_log(self, channel_name: str, timestamp: str):
        """
        Logs a NORMAL state event. Duration is set to "0.00".

        Args:
            channel_name (str): The channel where the event occurred.
            timestamp (str): The timestamp of the event.
        """
        self._write_log('NORMAL', channel_name, '0.00', timestamp)

    def blank_log(self, channel_name: str, duration: str, timestamp: str):
        """
        Logs a BLANK state with its duration.

        Args:
            channel_name (str): The name of the channel for the event.
            duration (str): The duration of the blank state.
            timestamp (str): The timestamp of the event.
        """
        self._write_log('BLANK', channel_name, duration, timestamp)

    def freeze_log(self, channel_name: str, duration: str, timestamp: str):
        """
        Logs a FREEZE state with its duration.

        Args:
            channel_name (str): The name of the channel for the event.
            duration (str): The duration of the frozen state.
            timestamp (str): The timestamp of the event.
        """
        self._write_log('FREEZE', channel_name, duration, timestamp)
