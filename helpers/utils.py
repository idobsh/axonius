from datetime import date, timedelta
import os
import json
import random
import re


def load_test_data(filename="test_data.json"):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "..", "tests", "tests_data", filename)

    with open(os.path.abspath(file_path), "r") as f:
        return json.load(f)


def generate_random_dates() -> tuple[str, str]:
    today = date.today()
    start_range = today + timedelta(days=3)
    end_range = today + timedelta(days=30)

    check_in = start_range + timedelta(
        days=random.randint(0, (end_range - start_range).days)
    )
    stay_length = random.randint(2, 10)
    check_out = check_in + timedelta(days=stay_length)

    return check_in.strftime("%Y-%m-%d"), check_out.strftime("%Y-%m-%d")


def clean_string(string: str) -> str:
    cleaned = re.sub(r"\s+", " ", string).strip()
    return cleaned
