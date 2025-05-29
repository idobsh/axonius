from pages.airbnb_home_page import AirbnbHomePage
from pages.asset_page import AssetPage
from pages.booking_page import BookingPage
from pages.results_page import ResultsPage
from helpers.utils import load_test_data, generate_random_dates
from tests.tests_data.Vacation import Vacation


class TestAirbnb:
    def test_airbnb_order(self, page):
        test_details = load_test_data()
        checkin, checkout = generate_random_dates()
        vacation = Vacation(
            test_details["destination"],
            checkin,
            checkout,
            test_details["adults"],
            test_details["children"],
        )
        airbnb_homepage = AirbnbHomePage(page, vacation, logger=self.logger)
        airbnb_results = ResultsPage(page, vacation, logger=self.logger)
        asset_page = AssetPage(page, logger=self.logger)
        booking_page = BookingPage(page, vacation, logger=self.logger)
        # checkin, checkout = airbnb_homepage.get_dates_for_vacation()
        airbnb_homepage.search_for_vacation()
        airbnb_results.verify_vacation_details()
        appartment, file_path = airbnb_results.search_asset_and_select()
        asset_page.reserve()
        booking_page.fill_phone_field(test_details["phone"])
        booking_page.verify_details(appartment)
