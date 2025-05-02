from pathlib import Path

# Folders
ROOT = Path(__file__, "..", "..", "..").resolve()

FOLDER_CONFIGS = Path(ROOT, "config")
FOLDER_DATA = Path(ROOT, "data")
FOLDER_DATA_DEVICES_SMA = Path(FOLDER_DATA, "devices", "sma")
FOLDER_PNG_FILES = Path(FOLDER_DATA, "charts")
FILE_CONFIG_SECRETS = Path(FOLDER_CONFIGS, "openhab", "secrets.env")
