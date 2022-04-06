import os


def get_environment_variable(key: str) -> str:
    try:
        value = os.environ[key]
        return value
    except KeyError:
        print(f'No value was found for key: {key}. Assign the key first.')
        exit()
