"""Make the functionalities of this package auto-discoverable by mara-app"""


def MARA_CONFIG_MODULES():
    from . import config
    return [config]


def MARA_CLICK_COMMANDS():
    from . import cli
    return [cli.download_data]
