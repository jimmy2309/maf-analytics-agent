import os
import logging
from datetime import datetime

class DailyFolderFileHandler(logging.FileHandler):
    """
    Custom FileHandler that dynamically writes logs to a folder based on the current date.
    e.g., logs/2026-07-04/tools.log
    """
    def __init__(self, base_log_dir: str, file_name: str, *args, **kwargs):
        self.base_log_dir = base_log_dir
        self.file_name = file_name
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Initialize with current date path
        log_path = self._get_current_log_path()
        super().__init__(log_path, *args, **kwargs)

    def _get_current_log_path(self) -> str:
        date_folder = os.path.join(self.base_log_dir, self.current_date)
        os.makedirs(date_folder, exist_ok=True)
        return os.path.join(date_folder, self.file_name)

    def emit(self, record):
        # Check if date has changed before writing
        new_date = datetime.now().strftime("%Y-%m-%d")
        if new_date != self.current_date:
            self.current_date = new_date
            self.close()
            self.baseFilename = os.path.abspath(self._get_current_log_path())
            self.stream = self._open()
        super().emit(record)

def setup_logger(name: str, log_file: str, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Base logs directory at project root
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
    
    handler = DailyFolderFileHandler(base_dir, log_file)
    handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate logs if instantiated multiple times
    if not logger.handlers:
        logger.addHandler(handler)
        
    return logger

# Pre-configured loggers for different categories
conversation_logger = setup_logger("conversation", "conversations.log")
tool_logger = setup_logger("tool", "tools.log")
system_logger = setup_logger("system", "system_errors.log", level=logging.ERROR)
