from datetime import date, datetime, timedelta
import random


class DatePickerHelper:

    def __init__(self, logger=None):
        self._logger = logger

    def generate_random_dates(self) -> tuple[str, str]:
        today = date.today()
        start_range = today + timedelta(days=3)
        end_range = today + timedelta(days=30)

        check_in = start_range + timedelta(
            days=random.randint(0, (end_range - start_range).days)
        )
        stay_length = random.randint(2, 10)
        check_out = check_in + timedelta(days=stay_length)

        return check_in.strftime("%Y-%m-%d"), check_out.strftime("%Y-%m-%d")

    @staticmethod
    def format_to_airbnb_display(iso_date: str) -> str:
        """
        Converts an ISO date string (YYYY-MM-DD) to Airbnb-style format like 'Jul 8'.

        Args:
            iso_date (str): A date string in 'YYYY-MM-DD' format

        Returns:
            str: A formatted string like 'Jul 8'
        """
        dt = datetime.strptime(iso_date, "%Y-%m-%d")
        return dt.strftime("%b %-d")

    @staticmethod
    def format_airbnb_checkout_date_range(checkin: str, checkout: str) -> str:
        checkin_dt = datetime.strptime(checkin, "%Y-%m-%d")
        checkout_dt = datetime.strptime(checkout, "%Y-%m-%d")

        month_abbr = checkin_dt.strftime("%b")  # Jun
        day_start = checkin_dt.day  # 10
        day_end = checkout_dt.day  # 19

        return f"{month_abbr} {day_start} – {day_end}"

    # prices
    @staticmethod
    def price_str_to_float(price_str: str) -> int:
        cleaned = price_str.replace("₪", "").replace(",", "").split(".")[0]
        return int(cleaned)
