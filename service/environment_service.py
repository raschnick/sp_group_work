import os


def get_environment_variable(key: str) -> str:
    """
    Loads a environment variable by a given key
    :param key: The environment variable key
    :return: The value for the key. If no key is found the program stops
    """
    try:
        value = os.environ[key]
        return value
    except KeyError:
        print(f'No value was found for key: {key}. Assign the key first.')
        exit()
