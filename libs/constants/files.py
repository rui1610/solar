from pathlib import Path

# Folders
ROOT = Path(__file__, "..", "..", "..").resolve()

FOLDER_CONFIGS = Path(ROOT, "config")
FOLDER_DATA_DEVICES_SMA = Path(ROOT, "docs", "devices", "sma")
FILE_CONFIG_SECRETS = Path(FOLDER_CONFIGS, "openhab", "secrets.env")
