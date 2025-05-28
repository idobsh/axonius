import json
from pathlib import Path
import tempfile
from playwright.sync_api import Locator, Page
import re


class AssetCard:
    PRICE = "price-availability-row"
    RATING = "5.0 out of 5"
    NAME = "listing-card-name"

    def __init__(self, page: Page, locator: Locator):
        self.pw_page = page
        self._asset_locator = locator
        self._price = self._extract_price()
        self._name = self._extract_name()
        self._link = self._extract_link()

    @property
    def price(self):
        return self._price

    @property
    def name(self):
        return self._name

    @property
    def link(self) -> str:
        return self._link

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "price": self.price,
        }

    def _extract_name(self):
        return self._asset_locator.get_by_test_id(self.NAME).inner_text()

    def _extract_price(self):
        price_content = self._asset_locator.get_by_test_id(self.PRICE).inner_text()
        match = re.search(r"₪([\d,]+)\s+total", price_content)
        if match:
            return int(match.group(1).replace(",", ""))
        print("Couldnt find price")
        return None

    def _extract_link(self):
        return self._asset_locator.locator("a").first.get_attribute("href")

    def is_valid(self):
        return self.RATING in self._asset_locator.inner_text()

    def save_card_to_temp(self):
        data = self.to_dict()  # assumes AssetCard has a .to_dict() method

        temp_dir = tempfile.gettempdir()
        file_path = Path(temp_dir) / "best_asset.json"

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

        return file_path
