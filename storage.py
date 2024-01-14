import json
from pathlib import Path


def read_data() -> dict:
    """Returns the address-name dictionary from the storage file."""
    ## If the file doesn't exist, make a new file with an empty dictionary.
    if not Path('storingfile.json').is_file():
        with open('storingfile.json', 'w') as file:
            json.dump({}, file)
    with open('storingfile.json', 'r') as file:
        address_dict = json.load(file)
    return address_dict


def add_data(address_dict: dict, new_name: str, new_address: str) -> dict:
    """Adds a new name-address pair to the address storage and store it in the file."""
    address_dict[new_name] = new_address
    with open('storingfile.json', 'w') as file:
        json.dump(address_dict, file, indent=4)
    return address_dict


def delete_data(address_dict: dict, name: str) -> dict:
    """Removes a name-address pair from the storage and file."""
    address_dict.pop(name)
    with open('storingfile.json', 'w') as file:
        json.dump(address_dict, file, indent=4)
    return address_dict
