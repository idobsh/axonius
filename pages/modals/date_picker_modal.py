from playwright.sync_api import Page, expect
from helpers.date_picker_helper import DatePickerHelper
from typing import Literal


class DatePickerModal():
    DATE_PICKER_MODAL = "#tabs"

    def __init__(self, pw_page: Page, logger = None):
        self.pw_page = pw_page
        self._date_picker_modal = self.pw_page.locator(self.DATE_PICKER_MODAL).first
        self.helper = DatePickerHelper(logger)

    def wait_to_be_visible(self):
        self._date_picker_modal.wait_for(state="visible")
    
    def date_button(self, date: str):
        return self.pw_page.locator(f'[data-state--date-string="{date}"]').first
    
    def get_vacation_dates(self):
        return self.helper.generate_random_dates()
    
    def select_date(self, date: str):
        date_button = self.date_button(date)
        date_button.click()
        expect(date_button).to_be_focused()
        






    
    


