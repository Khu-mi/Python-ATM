"""Activity logging for the ATM system."""

import csv  # Reads and writes CSV files safely
import os  # Lets us check if a file exists
from datetime import datetime  # Gives us timestamps


class ActivityLogger:
    """Records security events to a CSV log file."""

    HEADERS = ["timestamp", "phone_number", "event_type"]  # Columns

    def __init__(self, filename="log.txt"):
        """Set the log file name and create the file if missing."""
        self.filename = filename  # Remember which file to write to
        self._create_file_if_missing()  # Make sure the file exists

    def _create_file_if_missing(self):
        """Create the log file with a header row if it is missing."""
        if not os.path.exists(self.filename):  # File not there yet?
            with open(self.filename, "w", newline="") as file:  # Create
                writer = csv.writer(file)  # Tool that writes CSV rows
                writer.writerow(self.HEADERS)  # Write the header row

    def log_event(self, phone_number, event_type):
        """Append one timestamped event to the log file."""
        now = datetime.now()  # Current date and time
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")  # Format as text
        with open(self.filename, "a", newline="") as file:  # Append mode
            writer = csv.writer(file)  # Tool that writes CSV rows
            writer.writerow([timestamp, phone_number, event_type])  # Add row
