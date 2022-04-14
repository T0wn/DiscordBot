import json

GUILD_CONFIG_FILE = "/app/data/guild_config.json"


def read_config():
    with open(GUILD_CONFIG_FILE, "r") as config_file:
        return json.load(config_file)


def write_config(config):
    with open(GUILD_CONFIG_FILE, "w") as config_file:
        json.dump(config, config_file, indent=2)


def set_guild_config(guild_id: int, new_config):
    config = read_config()
    config["guilds"][guild_id] = new_config
    write_config(config)


def load_guild_config(guild_id: int):
    config = read_config()
    print(config)
    return config.get(str(guild_id))
