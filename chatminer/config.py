from platformdirs import PlatformDirs
from pathlib import Path
from configparser import ConfigParser
from functools import reduce
import operator
import shutil

from chatminer.common import log

DEFAULT_CONFIGS = {
    'database': {
        'admin': True,
        'host': 'localhost',
        'name': 'chatminer',
        'user': 'postgres',
        'password': ''
    }
}

configs = DEFAULT_CONFIGS


def read_configs(file_path: Path) -> None:
    config_parser = ConfigParser()
    config_parser.read(file_path)
    global configs
    configs = config_parser


def write_configs(file_path: Path, new_configs: dict) -> None:
    config_parser = ConfigParser()
    for key in new_configs:
        config_parser[key] = new_configs[key]
    with open(file_path, 'w') as file:
        config_parser.write(file)


dirs = PlatformDirs("chatminer")
config_dir = Path(dirs.user_config_dir)
config_file = config_dir / 'config.ini'
if config_dir.is_dir():
    if config_file.is_file():
        read_configs(config_file)
    else:
        write_configs(config_file, DEFAULT_CONFIGS)
else:
    config_dir.mkdir(exist_ok=True, parents=True)
    write_configs(config_file, DEFAULT_CONFIGS)


def set_config(name: str, value: str) -> None:
    keys = name.split(".")
    reduce(operator.getitem, keys[:-1], configs)[keys[-1]] = value
    write_configs(config_file, configs)
    log(f"Config item {name} set to {value}")


def reset_configs() -> None:
    write_configs(config_file, DEFAULT_CONFIGS)
    log(f"Configs reset to default")


def delete_configs() -> None:
    shutil.rmtree(config_dir)
    log("Config file deleted")
