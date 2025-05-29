from time import sleep
from playwright.sync_api import Page, expect
from helpers.utils import generate_random_dates
from pages.base_page import BasePage
from pages.modals.date_picker_modal import DatePickerModal
from pages.modals.guests_modal import GuestsModal
import re

from tests.tests_data.Vacation import Vacation


class AirbnbHomePage(BasePage):
    PATH = "/"
    # LOCATORS
    WHERE_FIELD = "structured-search-input-field-query"
    CHECKIN_FIELD = "Check in"
    CHECKOUT_FIELD = "Check out"
    GUESTS_FIELD = r"^Who"
    SEARCH_BUTTON = "structured-search-input-search-button"

    def __init__(self, page: Page, vacation: Vacation, logger=None):
        super().__init__(page, path=self.PATH, logger=logger)
        self._url = self.url
        self.pw_page = page
        self.logger = logger
        self._destination_field = self.pw_page.get_by_test_id(self.WHERE_FIELD)
        self._checkin_field = self.pw_page.get_by_role(
            "button", name=self.CHECKIN_FIELD
        )
        self._checkout_field = self.pw_page.get_by_role(
            "button", name=self.CHECKOUT_FIELD
        )
        self._guests_field = self.pw_page.get_by_role(
            "button", name=re.compile(self.GUESTS_FIELD)
        )
        self._search_button = self.pw_page.get_by_test_id(self.SEARCH_BUTTON)
        self.date_picker_modal = DatePickerModal(page)
        self.guests_modal = GuestsModal(page, context="search")
        self.vacation = vacation

    @property
    def destination_field(self):
        return self._destination_field

    @property
    def checkin_field(self):
        return self._checkin_field

    @property
    def checkout_field(self):
        return self._checkout_field

    @property
    def guests_field(self):
        return self._guests_field

    @property
    def search_button(self):
        return self._search_button

    def navigate(self):
        self.pw_page.goto(self._url)

    def fill_destination(self):
        self.destination_field.click()
        self.destination_field.fill(self.vacation.location)
        self.destination_field.press("Enter")

    def open_date_picker(self):
        self.checkin_field.click()
        self.date_picker_modal.wait_to_be_visible()

    def select_dates(self):
        # TODO add an argument that state if it came after the dest or not
        # self.open_date_picker()
        self.pw_page.wait_for_load_state("load")
        self.date_picker_modal.wait_to_be_visible
        sleep(1)  # Sorry but I tried
        self.date_picker_modal.select_date(self.vacation.checkin)
        self.date_picker_modal.select_date(self.vacation.checkout)

    def get_dates_for_vacation(self):
        return generate_random_dates()

    def get_airbnb_date_display(self, date):
        return self.date_picker_modal.helper.format_to_airbnb_display(date)

    def open_guests_modal(self):
        self.guests_field.click()

    def set_num_of_guests(self):
        adults = int(self.vacation.adults)
        childrens = int(self.vacation.children)
        # infants = int(self.vacation.infants)
        # pets = int(self.vacation.pets)
        self.open_guests_modal()
        if adults:
            self.guests_modal.set_adults(adults)
        if childrens:
            self.guests_modal.set_childrens(childrens)
        # if infants:
        #     self.guests_modal.set_infants(infants)
        # if pets:
        #     self.guests_modal.set_pets(pets)

    def search(self):
        with self.pw_page.expect_navigation(wait_until="load"):
            self.search_button.click()

    def search_for_vacation(self):
        self.navigate()
        self.fill_destination()
        self.select_dates()
        self.set_num_of_guests()
        self.search()
