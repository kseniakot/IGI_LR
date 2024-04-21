class TimeLoggerMixin:
    from datetime import datetime

    def log_with_time(self, message):
        current_time = self.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[LOG {current_time}]: {message}')

