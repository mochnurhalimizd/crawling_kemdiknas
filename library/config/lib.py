import os
from configparser import ConfigParser


def get_config(files='config.conf'):
    """Get config file in workspace

    :param files : (String) name config file
    :return null"""

    try:
        config = ConfigParser()
        config.read(os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            files
        ))
        return config
    except Exception as e:
        raise Exception(e)
