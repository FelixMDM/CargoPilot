import logging
from datetime import datetime
from pathlib import Path

class ServerLogger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServerLogger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance
    
    def _initialize_logger(self):
        # Setup log directory and file
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f"server-{datetime.now().strftime('%Y-%m-%d')}.log"
        
        # Configure logger
        self.logger = logging.getLogger("ServerLogger")
        self.logger.setLevel(logging.INFO)
        
        # Setup handlers with formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        for handler in [
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]:
            handler.setFormatter(formatter)
            handler.setLevel(logging.INFO)
            self.logger.addHandler(handler)
    
    def _format_message(self, message, kwargs):
        return f"{message} - {kwargs}" if kwargs else message
    
    def info(self, message, **kwargs):
        self.logger.info(self._format_message(message, kwargs))
    
    def error(self, message, **kwargs):
        self.logger.error(self._format_message(message, kwargs))
    
    def warning(self, message, **kwargs):
        self.logger.warning(self._format_message(message, kwargs))

# Create singleton instance
server_logger = ServerLogger()