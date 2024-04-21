class TimeLoggerMixin:
    """A mixin class that provides a log_with_time method to print messages with the current time."""
    from datetime import datetime

    def log_with_time(self, message):
        """Prints a message with the current time"""
        current_time = self.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[LOG {current_time}]: {message}')

