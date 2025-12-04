"""
Car Inventory Tracker
Name: 
Student ID: 

"""


# ------------------------------
#Car class
# ------------------------------
class Car:
    def __init__(self, brand, received, sold):
        # Store raw values as plain attributes 
        self.brand = brand
        self.received = received
        self.sold = sold

    def available_units(self):
        """
        Calculate how many units are available for sale.
        If sold is greater than received (bad data), we will treat available as 0.
        """
        remaining = self.received - self.sold
        if remaining < 0:
            # keep it never negative
            remaining = 0
        return remaining


# ------------------------------
# Helper functions
# ------------------------------
def pause():
    """Wait for user so the output is readable."""
    input("\nPress Enter to continue...")


def get_default_or_input(prompt_text, default_value):
    """
    Ask user for a value. If the user presses Enter, use the default.
    This is used for the data file path.
    """
    print(prompt_text + f" [default: {default_value}]")
    answer = input().strip()
    if answer == "":
        return default_value
    else:
        return answer


def is_missing_token(text):
    """
    Treat common 'missing' tokens as missing.
    We will check this before trying to convert to int.
    """
    if text is None:
        return True
    t = text.strip().lower()
    if t == "" or t == "na" or t == "n/a" or t == "none" or t == "null" or t == "missing" or t == "missing data":
        return True
    return False


def try_parse_int(raw_text):
    """
    Try to convert raw_text to an integer.
    Returns (is_ok, value_or_message).
    If conversion fails or negative, return (False, "reason").
    """
    if is_missing_token(raw_text):
        return (False, "missing data")

    raw_text = raw_text.strip()
    # Try normal int conversion
    try:
        number = int(raw_text)
    except:
        # Conversion failed (like "nine")
        return (False, "not a number")

    if number < 0:
        return (False, "negative number not allowed")

    return (True, number)


def normalize_header_to_positions(header_line):
    """
    Convert the first line (header) into indexes for brand, received, sold.
    This lets the file have small header variations but still work.

    Returns a dictionary with keys 'brand', 'received', 'sold' and integer positions.
    """
    header_parts = header_line.strip().split(",")
    positions = {"brand": -1, "received": -1, "sold": -1}

    # We will search for column names by keyword to keep it simple.
    for i in range(len(header_parts)):
        name = header_parts[i].strip().lower()
        if "brand" in name:
            positions["brand"] = i
        elif "received" in name:
            positions["received"] = i
        elif "sold" in name:
            positions["sold"] = i

    return positions


def load_cars_from_file(filepath):
    """
    Reads the file line by line .
    Returns (cars_list, errors_list).
    - cars_list is a list of Car objects.
    - errors_list is a list of text messages describing any issues.
    """
    cars = []
    errors = []

    # Try to open the file first
    try:
        f = open(filepath, "r", encoding="utf-8")
    except FileNotFoundError:
        # File is not found, raise again to handle in main()
        raise
    except Exception as ex:
        # Unexpected read errors will be handled in main()
        raise

    # Read all lines
    lines = f.readlines()
    f.close()

    if len(lines) == 0:
        errors.append("The file is empty.")
        return (cars, errors)

    # The first line should be the header
    header = lines[0]
    positions = normalize_header_to_positions(header)

    # Check if we found the required columns
    if positions["brand"] == -1 or positions["received"] == -1 or positions["sold"] == -1:
        errors.append("Header does not contain required columns: carbrand, received, sold.")
        return (cars, errors)

    # Now go through each data line (starting from line index 1)
    line_number = 1  # we will show human-friendly numbers (1-based for header)
    while line_number < len(lines):
        line_number += 1  # so the first data row is line 2 for the user
        line_text = lines[line_number - 1].strip()

        # Skip completely empty lines
        if line_text == "":
            continue

        parts = line_text.split(",")

        # We must make sure there are enough columns
        # If not, skip but record an error
        if len(parts) <= max(positions["brand"], positions["received"], positions["sold"]):
            errors.append("Line " + str(line_number) + ": not enough columns.")
            continue

        raw_brand = parts[positions["brand"]].strip()
        raw_received = parts[positions["received"]].strip()
        raw_sold = parts[positions["sold"]].strip()

        # Brand must exist
        if raw_brand == "":
            errors.append("Line " + str(line_number) + ": missing car brand; row skipped.")
            continue

        # Parse received
        ok_r, val_r = try_parse_int(raw_received)
        if not ok_r:
            errors.append("Line " + str(line_number) + " (" + raw_brand + "): received -> " + val_r + ".")
            continue

        # Parse sold
        ok_s, val_s = try_parse_int(raw_sold)
        if not ok_s:
            errors.append("Line " + str(line_number) + " (" + raw_brand + "): sold -> " + val_s + ".")
            continue

        # If sold > received, we clamp sold to received and record a note
        if val_s > val_r:
            errors.append(
                "Line " + str(line_number) + " (" + raw_brand + "): sold (" + str(val_s) +
                ") exceeds received (" + str(val_r) + "); clamping sold to received."
            )
            val_s = val_r

        # Create a Car object and add to list
        car_obj = Car(raw_brand, val_r, val_s)
        cars.append(car_obj)

    return (cars, errors)


def print_summary(cars, errors):
    """
    Print a very simple, readable summary table and totals.
    Also print any data issues detected while loading.
    """
    print("=" * 60)
    print("CAR INVENTORY SUMMARY")
    print("=" * 60)

    # Print header row
    # Using manual alignment to keep it obvious
    print("{:<15}{:>12}{:>12}{:>14}".format("Brand", "Received", "Sold", "Available"))
    print("-" * 60)

    total_received = 0
    total_sold = 0
    total_available = 0

    # Sort by brand name to make it neat
    # (case-insensitive sort)
    cars_sorted = sorted(cars, key=lambda c: c.brand.lower())

    for c in cars_sorted:
        avail = c.available_units()
        print("{:<15}{:>12}{:>12}{:>14}".format(c.brand, c.received, c.sold, avail))
        total_received = total_received + c.received
        total_sold = total_sold + c.sold
        total_available = total_available + avail

    print("-" * 60)
    print("{:<15}{:>12}{:>12}{:>14}".format("TOTAL", total_received, total_sold, total_available))
    print("=" * 60)

    if len(errors) > 0:
        print("\nNotes / Data Issues Detected:")
        for e in errors:
            print("- " + e)


def search_by_brand(cars):
    """
    Ask the user for a brand and show its details.
    If not found, print 'Item not found'.
    """
    brand = input("Enter car brand to search: ").strip()
    if brand == "":
        print("Please enter a brand name.")
        return

    # Case-insensitive exact match
    found = None
    for c in cars:
        if c.brand.lower() == brand.lower():
            found = c
            break

    if found is None:
        print("Item not found")
    else:
        print("\nBrand:", found.brand)
        print("Received:", found.received)
        print("Sold:", found.sold)
        print("Available:", found.available_units())
        if found.available_units() > 0:
            print("Status: Available for sale")
        else:
            print("Status: Not available (no stock left)")


def list_all_available(cars):
    """
    Print all brands that have stock available (available > 0).
    """
    # Collect available cars
    available_list = []
    for c in cars:
        if c.available_units() > 0:
            available_list.append(c)

    if len(available_list) == 0:
        print("\nNo cars are currently available for sale.")
    else:
        print("\nCars available for sale:")
        # Print in alphabetical order
        available_list = sorted(available_list, key=lambda x: x.brand.lower())
        for c in available_list:
            print("- " + c.brand + " (Available: " + str(c.available_units()) + ")")


def print_menu():
    """
    Show the menu each time in a very simple way.
    """
    print("\nChoose an option:")
    print("1) Print summary report")
    print("2) Search car by brand name")
    print("3) List all cars available for sale")
    print("4) Exit")


def main():
    print("=== Car Inventory Tracker ===")
    # Ask for file path but allow Enter for default
    filepath = get_default_or_input("Enter data file path", "carinventory.txt")

    # Load data
    try:
        cars, errors = load_cars_from_file(filepath)
    except FileNotFoundError:
        print("Error: Could not find file '" + filepath + "'. Make sure it exists.")
        return
    except Exception as ex:
        print("Unexpected error while reading '" + filepath + "': " + str(ex))
        return

    # Simple loop for the menu
    while True:
        print_menu()
        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            print_summary(cars, errors)
            pause()
        elif choice == "2":
            search_by_brand(cars)
            pause()
        elif choice == "3":
            list_all_available(cars)
            pause()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-4.")

# Run the program
if __name__ == "__main__":
    main()
