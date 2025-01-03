
class DataLogger:
    """
    The class to handle the data logging for altimeter
    """
    def __init__(self, file_name, mode='a'):
        """
        :param file_name: The name of the log file.
        :param mode: The mode to open the file in ('a' for append, 'w' for write).
        """
        self.file_name = file_name
        self.mode = mode
        self.file = None
        self.data = []

    def start(self):
        """
        Opens the file in the specified mode.
        """
        self.file = open(self.file_name, self.mode)

    def log(self, time_stamp, sensor_name, data):
        """
        saves the data internally to be written to the file.
        """
        self.data.append((time_stamp, sensor_name, data))

    def stop(self):
        """
        Write data to a log file and close it
        """
        for time_stamp, sensor_name, data in self.data:
            data = str(data)
            if self.file is not None:
                self.file.write(f"[{time_stamp}] {sensor_name} {data}\n")
                self.file.flush()
            else:
                 raise ValueError("File is not open. Please call start() first.")
        if self.file is not None:
            self.file.close()
            self.file = None
        else:
            raise ValueError("File is not open or already closed.")
