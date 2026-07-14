"""save_json(data, file_path): Saves data to a JSON file.
load_json(file_path): Loads data from a JSON file.
normalize_text(text): Performs general text normalization (e.g., lowercase, remove extra spaces).
handle_api_errors(func): A decorator for API calls to handle common errors (e.g., rate limits, connection issues).
time_it(func): A decorator to measure the execution time of a function.
is_valid_language_code(lang_code): Checks if a given string is a supported language code.
"""


def get_page_number(item) -> int:
    if hasattr(item, "prov") and item.prov:
        return item.prov[0].page_no
    return 1