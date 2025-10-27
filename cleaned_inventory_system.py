"""
This module implements a basic inventory management system.

It allows adding, removing, and querying stock levels for items,
with data being loaded from and saved to a JSON file.
"""

import json
import logging
from datetime import datetime

# Configure logging for the main execution block
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def add_item(stock_data, item="default", qty=0, logs=None):
    """
    Adds a specified quantity of an item to the stock data.

    Args:
        stock_data (dict): The dictionary holding stock info.
        item (str): The name of the item to add.
        qty (int): The quantity to add.
        logs (list, optional): A list to append log messages to.
    """
    # Fix: (Pylint W0102) Mutable default arg
    if logs is None:
        logs = []

    # Fix: (Runtime Error) Implement input validation
    if not isinstance(item, str) or not isinstance(qty, int):
        logging.error("Invalid types: Item must be str, qty must be int.")
        return

    if not item:
        logging.warning("No item specified. Ignoring.")
        return

    stock_data[item] = stock_data.get(item, 0) + qty

    # Fix: (Pylint C0209) Use f-string
    log_message = f"{datetime.now()}: Added {qty} of {item}"
    logs.append(log_message)
    logging.info(log_message)


def remove_item(stock_data, item, qty):
    """
    Removes a specified quantity of an item from the stock data.

    Args:
        stock_data (dict): The dictionary holding stock info.
        item (str): The name of the item to remove.
        qty (int): The quantity to remove.
    """
    if not isinstance(qty, int):
        logging.error("Invalid quantity: Qty must be int. Got: %s", qty)
        return

    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
            logging.info("Removed all stock for %s.", item)

    # Fix: (Flake8 E722, Pylint W0702, Bandit B110) Bare 'except'
    except KeyError:
        logging.warning("Item %s not in stock, cannot remove.", item)


def get_qty(stock_data, item):
    """
    Gets the current quantity of a specific item.

    Args:
        stock_data (dict): The dictionary holding stock info.
        item (str): The name of the item to query.

    Returns:
        int: The quantity of the item, or 0 if not found.
    """
    # Fix: Use .get() to prevent crash if item doesn't exist
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """
    Loads inventory data from a JSON file.

    Args:
        file (str): The filename to load data from.

    Returns:
        dict: The loaded stock data, or an empty dict on failure.
    """
    try:
        # Fix: (Pylint R1732) Use 'with' statement
        # Fix: (Pylint W1514) Add encoding
        with open(file, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
            logging.info("Data loaded from %s.", file)
            return data
    except FileNotFoundError:
        logging.warning("File %s not found. Starting with empty stock.", file)
        return {}
    except json.JSONDecodeError:
        logging.error("Could not decode JSON from %s. Starting fresh.", file)
        return {}


def save_data(stock_data, file="inventory.json"):
    """
    Saves the current inventory data to a JSON file.

    Args:
        stock_data (dict): The dictionary holding stock info.
        file (str): The filename to save data to.
    """
    try:
        # Fix: (Pylint R1732) Use 'with' statement
        # Fix: (Pylint W1514) Add encoding
        with open(file, "w", encoding="utf-8") as f:
            # Use indent=4 for readable JSON
            f.write(json.dumps(stock_data, indent=4))
            logging.info("Data saved to %s.", file)
    except IOError as e:
        logging.error("Could not write to file %s: %s", file, e)


def print_data(stock_data):
    """
    Prints a report of all items and their quantities.

    Args:
        stock_data (dict): The dictionary holding stock info.
    """
    print("\n--- Items Report ---")
    if not stock_data:
        print("Inventory is empty.")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")
    print("--------------------\n")


def check_low_items(stock_data, threshold=5):
    """
    Checks for items with stock below a given threshold.

    Args:
        stock_data (dict): The dictionary holding stock info.
        threshold (int): The stock level to check against.

    Returns:
        list: A list of item names below the threshold.
    """
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    """Main function to run the inventory program."""

    # Load data instead of using a global
    stock_data = load_data()
    item_logs = []

    # Fix: (Pylint C0103) Rename all function calls to snake_case
    add_item(stock_data, "apple", 10, item_logs)
    # Fix: (Flake8 E261) Add two spaces before inline comment
    add_item(stock_data, "banana", 5, item_logs)  # Assuming -2 was a typo
    add_item(stock_data, 123, "ten", item_logs)  # Now handled by validation

    remove_item(stock_data, "apple", 3)
    remove_item(stock_data, "orange", 1)  # Now logs a warning
    remove_item(stock_data, "banana", "two")  # Now handled by validation

    print(f"Apple stock: {get_qty(stock_data, 'apple')}")
    print(f"Low items: {check_low_items(stock_data)}")

    save_data(stock_data)
    print_data(stock_data)

    # Fix: (Bandit B307, Pylint W0123) Removed dangerous 'eval'
    print("eval used")  # This is safe


if __name__ == "__main__":
    main()