import collections
import functools
from pathlib import Path
import re
import sys


def handle_file_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("File not found.")
            sys.exit(1)

    return wrapper


def handle_parse_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IOError as e:
            print(f"Error reading file: {e}")
            sys.exit(1)

    return wrapper


def handle_log_format_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError) as e:
            print(f"Error parsing data: {e}")
            sys.exit(1)

    return wrapper


@handle_file_errors
def load_logs(filename: str) -> list:
    script_path = Path(__file__).parent
    file_path = script_path / filename
    with open(file_path, "r", encoding="UTF-8") as f:
        data = f.read()
    data = data.split("\n")
    parsed_logs = []
    for row in data:
        line = parse_log_line(row)
        parsed_logs.append(line)

    return parsed_logs


@handle_log_format_errors
def parse_log_line(line: str) -> dict:
    pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.+)"
    match = re.match(pattern, line)
    if match:
        timestamp, message_type, description = match.groups()
        return {
            "timestamp": timestamp,
            "message_type": message_type,
            "description": description,
        }
    else:
        raise Exception("Invalid log format")


def filter_logs_by_level(logs: list, level: str, log_counts: dict) -> list:
    result = []
    if level.upper() in log_counts.keys():
        for log in logs:
            if log["message_type"] == level.upper():
                result.append(" ".join(list(log.values())))
    else:
        if level.strip():
            print(f"Invalid log level: {level}")

    return result


def count_logs_by_level(logs: list) -> dict:
    log_levels = []
    for log_record in logs:
        log_levels.append(log_record["message_type"])
    log_counts = collections.Counter(log_levels)
    result = dict(log_counts)

    return result


def display_log_counts(counts: dict):
    table_header_1 = "Рівень логування"
    table_header_2 = "Кількість"
    header_row = " | ".join([table_header_1, table_header_2])
    print("\n" + header_row)
    print("-" * len(header_row))
    data_values = counts["log_counts"]
    for key, value in data_values.items():
        formatted_key = str(key).ljust(max(len(table_header_1), len(key)))
        formatted_value = str(value).rjust(max(len(table_header_2), len(str(value))))
        formatted_row = f"{formatted_key} | {formatted_value}"
        print(formatted_row)

    if len(counts["level_logs"]) > 0:
        for index, row in enumerate(counts["level_logs"]):
            print(row)
            if index == len(counts["level_logs"]) - 1:
                print("-" * len(row) + "\n")
    else:
        print("-" * len(header_row) + "\n")


def main():
    while True:
        parsed_logs = []
        level_logs = []
        level = ""
        user_input = input("Enter a file name (and logs level): ")
        if user_input in ["close", "exit"]:
            print("Good bye!")
            break
        else:
            if len(user_input.split(" ")) == 2:
                file_name, level = user_input.split(" ")
            else:
                file_name = user_input

        parsed_logs = load_logs(file_name)
        log_counts = count_logs_by_level(parsed_logs)
        level_logs = filter_logs_by_level(parsed_logs, level, log_counts)
        counts = {}
        counts["level_logs"] = level_logs
        counts["log_counts"] = log_counts
        display_log_counts(counts)


if __name__ == "__main__":
    main()

# example_log.log
