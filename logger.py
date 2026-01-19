import logging
import os
import sys

class MyFormatter(logging.Formatter):
    """
    Formatter that ensures the 'Location' column starts at the same position,
    regardless of the log level length.
    
    Structure: Date | Level (Fixed Width) | Location (Variable) | Message
    """
    
    # --- Configuration ---
    # Width for the Level column to ensure Location starts at the same spot.
    # [CRITICAL] is the longest standard level (10 chars).
    LEVEL_WIDTH = 8 

    # ANSI escape codes
    GREY = "\x1b[38;20m"    # INFO/DEBUG
    GREEN = "\x1b[32;20m"   # Date
    YELLOW = "\x1b[33;20m"  # WARNING
    RED = "\x1b[31;20m"     # ERROR
    BLUE = "\x1b[34;20m"    # Location
    RESET = "\x1b[0m"

    def __init__(self, use_color=True):
        super().__init__()
        self.use_color = use_color
        self.datefmt = '%Y-%m-%d %H:%M:%S'

    def format(self, record):
        # 1. Format Time
        timestamp = self.formatTime(record, self.datefmt)
        
        # 2. Format Level (Fixed Width for alignment)
        # e.g., "[INFO]" -> "[INFO]    "
        level_raw = f"{record.levelname}"
        level_str = f"{level_raw:<{self.LEVEL_WIDTH}}"

        # 3. Format Location
        # e.g., "/absolute/path/to/file.py:Line"
        loc_str = f"{record.pathname}:{record.lineno}"

        # 4. Apply Colors
        if self.use_color:
            # Determine message/level color
            if record.levelno == logging.WARNING:
                main_color = self.YELLOW
            elif record.levelno >= logging.ERROR:
                main_color = self.RED
            else:
                main_color = self.GREY
            
            # Apply ANSI codes
            date_field = f"{self.GREEN}{timestamp}{self.RESET}"
            level_field = f"{main_color}{level_str}{self.RESET}"
            loc_field = f"{self.BLUE}{loc_str}{self.RESET}"
            msg_field = f"{main_color}{record.getMessage()}{self.RESET}"
        
        else:
            # Plain text for file
            date_field = timestamp
            level_field = level_str
            loc_field = loc_str
            msg_field = record.getMessage()

        # 5. Combine with Separators
        return f"{date_field} | {level_field} | {loc_field} | {msg_field}"

def setup_logger(log_folder="logs"):
    """
    Sets up the logger.
    """
    if not os.path.exists(log_folder):
        os.makedirs(log_folder, exist_ok=True)

    log_file_path = os.path.join(log_folder, "log.txt")
    
    logger = logging.getLogger("AppLogger")
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        return logger

    # --- Console Handler ---
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(MyFormatter(use_color=True))
    logger.addHandler(stream_handler)

    # --- File Handler ---
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(MyFormatter(use_color=False))
    logger.addHandler(file_handler)

    return logger

# --- Usage Example ---

if __name__ == "__main__":
    logger = setup_logger()

    logger.info("Process started.")
    
    # Even if the level text changes length, the location column starts at the same spot
    logger.warning("Configuration file not found.")
    
    try:
        x = 100 / 0
    except Exception as e:
        logger.error(f"Calculation failed: {e}")
        
    logger.info("Task finished.")
