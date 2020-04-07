import attr
import yaml


@attr.s
class Config:
    SQUID_API_DSN = attr.ib(type=str)
    ZEEK_LOGS_DIRECTORY = attr.ib(type=str)
    MODELS_DIRECTORY = attr.ib(type=str)
    DISABLE_RULES = attr.ib(type=set, converter=set, default=set())


def read_config(config_file, **kwargs):
    with open(config_file, "r") as cfg:
        config_values = yaml.safe_load(cfg)
        config = Config(**config_values)
        if "DISABLE_RULES" in kwargs:
            config.DISABLE_RULES |= set(kwargs.pop("DISABLE_RULES"))
        return config
