from playwright.sync_api import Page, expect
from helpers.date_picker_helper import DatePickerHelper
from pages.base_page import BasePage
from pages.ui_components.asset_card import AssetCard

from tests.tests_data.Vacation import Vacation


class ResultsPage(BasePage):
    # LOCATORS
    NEXT_BTN = "Next"
    ASSETS = '[data-testid="card-container"]'
    LITTLE_SEARCH = "little-search-{field_type}"

    def __init__(self, page: Page, vacation: Vacation, logger=None):
        super().__init__(page, logger=logger)
        self.pw_page = page
        self.logger = logger
        self.vacation = vacation

    @property
    def next_button(self):
        return self.pw_page.get_by_role("link", name="Next")

    def get_asset_locators(self):
        return self.pw_page.locator(self.ASSETS)

    def get_little_search_field(self, field_type: str):
        return self.pw_page.get_by_test_id(
            self.LITTLE_SEARCH.format(field_type=field_type)
        )

    def verify_details_in_little_search_bar(self, field_type: str, value: str):
        field_locator = self.get_little_search_field(field_type)
        expect(
            field_locator,
            f"looking for value {value} in {field_type} field while it have {field_locator.inner_text()}",
        ).to_contain_text(value)

    def verify_vacation_details(self):
        dates = DatePickerHelper().format_airbnb_checkout_date_range(
            self.vacation.checkin, self.vacation.checkout
        )
        sum_of_guests = self.vacation.num_of_guests
        self.verify_details_in_little_search_bar("location", self.vacation.location)
        self.verify_details_in_little_search_bar("date", dates)
        self.verify_details_in_little_search_bar("guests", str(sum_of_guests))
        # self.details_in_url(self.url)

    def details_in_url(self):
        url = self.pw_page.url
        details = self.vacation.to_dict()
        for key, value in details.items():
            if key == "location":
                assert (
                    value in url
                ), f"Couldn't find {key} in the url. This is the url: {url}"
            if value:
                assert (
                    f"{key}={value}" in url
                ), f"Couldn't find {key}={value} in the url. This is the url: {url}"

    def next_page(self):
        expect(self.next_button).to_be_enabled(timeout=3000)
        self.next_button.click()
        self.pw_page.wait_for_load_state("load")

    def go_next(self):
        if self.next_button.is_enabled():
            self.next_page()
            return True
        return False

    def check_cards_in_page(self):
        chosen_card = None
        expect(self.get_asset_locators().nth(10)).to_be_visible(
            timeout=3000
        )  # Promise that all the assets loaded
        assets = self.get_asset_locators()
        self.logger.info(f"Found {assets.count()} asset cards on the page.")
        for i in range(assets.count()):
            card = AssetCard(self.pw_page, assets.nth(i))
            if card.is_valid():
                if (
                    chosen_card is None
                    or chosen_card._extract_price() > card._extract_price()
                ):
                    chosen_card = card
        self.logger.info(f"return chosen card: {chosen_card}")
        return chosen_card

    def check_cards_in_all_pages(self):
        best_card = None
        while True:
            if best_card is not None:
                self.logger.info(f"Best card is currently {best_card.price}")
            best_card_on_page = self.check_cards_in_page()
            if best_card_on_page is None:
                self.logger.info("Didn't find 5 stars on this page, moving on")
            else:
                self.logger.info(f"Best card on page is {best_card_on_page.price}")
                if best_card is None:
                    self.logger.info("Best card is None!")
                if (best_card is None) or (best_card.price > best_card_on_page.price):
                    self.logger.info(
                        f"Found better 5-star asset at price {best_card_on_page.price}"
                    )
                    best_card = best_card_on_page
            if not self.go_next():
                break

        return best_card

    def go_to_reservation_page(self, link: str):
        self.pw_page.goto(self.url + link)

    def search_asset_and_select(self):
        best_card = self.check_cards_in_all_pages()
        if best_card is None:
            raise Exception("No valid 5-star asset found")
        self.logger.info(
            f"Going to reserve {best_card.name} at price {best_card.price}"
        )
        best_asset_file_path = best_card.save_card_to_temp()
        self.go_to_reservation_page(best_card.link)
        return best_card.to_dict(), best_asset_file_path
