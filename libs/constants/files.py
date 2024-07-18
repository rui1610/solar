from pathlib import Path

# Folders
ROOT = Path(__file__, "..", "..", "..").resolve()

FOLDER_CONFIGS = Path(ROOT, "config")
FILE_CONFIG_SECRETS = Path(FOLDER_CONFIGS, "openhab", "secrets.env")

FILE_CONFIG_OPENHAB_SMA_THINGS = Path(FOLDER_CONFIGS, "openhab", "sma_things.json")
FILE_CONFIG_SMA_METADATA = Path(
    ROOT, "resources", "sma_tripower", "modbus_params_sma_tripower_ALL.json"
)
