from playwright.sync_api import Page
from pages.base_page import BasePage
from helpers.utils import format_airbnb_checkout_date_range, clean_string, price_str_to_float
from pages.modals.guests_modal import GuestsModal
from tests.tests_data.Vacation import Vacation


class BookingPage(BasePage):
    PRICE_THRESHOLD = 1
    # LOCATORS
    TITLE = "#LISTING_CARD-title"
    PRICE = "price-item-total"
    DATES_SECTION = '[data-section-id="DATE_PICKER"]'
    GUESTS_EDIT_BTN = "checkout_platform.GUEST_PICKER.edit"
    PHONE_FIELD = "login-signup-phonenumber"

    def __init__(self, page: Page, vacation: Vacation, logger=None):
        super().__init__(page, logger=logger)
        self.pw_page = page
        self.logger = logger
        self._title = self.pw_page.locator(self.TITLE)
        self._price = self.pw_page.get_by_test_id(self.PRICE)
        self._dates = self.pw_page.locator(self.DATES_SECTION)
        self._guests_edit_btn = self.pw_page.get_by_test_id(self.GUESTS_EDIT_BTN)
        self._phone_field = self.pw_page.get_by_test_id(self.PHONE_FIELD)
        self.guests_modal = GuestsModal(page, context="checkout")
        self.vacation = vacation

    @property
    def guests_edit_btn(self):
        return self._guests_edit_btn

    @property
    def phone_field(self):
        return self._phone_field

    def get_dates(self) -> str:
        return self._dates.inner_text()

    def verify_dates(self) -> bool:
        expected_dates = format_airbnb_checkout_date_range(
            self.vacation.checkin, self.vacation.checkout
        )
        actual_dates = self.get_dates()
        assert (
            expected_dates in actual_dates
        ), f"Expected dates {expected_dates} not found in booking page. Found: {self.get_dates()}"

    def verify_appartment_name(self, appartment_name: str):
        actual_title = clean_string(self._title.inner_text())
        assert (
            appartment_name == actual_title
        ), f"Expected location {self.vacation.location} not found in booking page title. Found: {self._title.inner_text()}"

    def verify_details(self, appartment: dict):
        self.verify_appartment_name(appartment["name"])
        self.verify_dates()
        self.verify_guests()
        self.verify_price(appartment["price"])

    def open_guests_modal(self):
        self.guests_edit_btn.click()

    def fill_phone_field(self, phone_num: str):
        self.phone_field.fill(phone_num)

    @property
    def price(self):
        return price_str_to_float(self._price.inner_text())

    # I tried to do it as modular as can get so it finds this att in the guests modal
    def verify_guests_of_type(self, guest_type: str, count: int):
        stepper = getattr(self.guests_modal, f"{guest_type}_stepper", None)
        assert stepper is not None, f"No stepper found for guest type: {guest_type}"

        actual_value = int(stepper.get_value())
        assert (
            actual_value == count
        ), f"Expected {count} {guest_type}, but got {actual_value}"

    # TODO: Make it more robust, currently it only works for adults and children
    def verify_guests(self):
        self.open_guests_modal()
        adults_count = int(self.vacation.adults)
        children_count = int(self.vacation.children) if self.vacation.children else 0
        # infants_count = int(self.vacation.infants) if self.vacation.infants else 0
        # pets_count = int(self.vacation.pets) if self.vacation.pets else 0

        self.verify_guests_of_type("adults", adults_count)
        if children_count:
            self.verify_guests_of_type("children", children_count)
        # if infants_count:
        #     self.verify_guests_of_type("infants", infants_count)
        # if pets_count:
        #     self.verify_guests_of_type("pets", pets_count)

    def verify_price(self, price: int):
        assert self.price in range(
            price - self.PRICE_THRESHOLD, price + self.PRICE_THRESHOLD + 1
        )
