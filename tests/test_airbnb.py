from pages.airbnb_home_page import AirbnbHomePage 
from playwright.sync_api import Page, expect

from pages.asset_page import AssetPage
from pages.booking_page import BookingPage
from pages.results_page import ResultsPage
from tests.data_for_tests.Vacation import Vacation


class TestAirbnb:
    def test_airbnb_order(self, page):
        adults = 2
        children = 1
        num_of_guests = adults+children
        destination = "Tel Aviv-Yafo"
        airbnb_homepage = AirbnbHomePage(page, logger=self.logger)
        airbnb_results = ResultsPage(page, logger=self.logger)
        asset_page = AssetPage(page, logger=self.logger)
        booking_page = BookingPage(page, logger=self.logger)
        checkin, checkout = airbnb_homepage.get_dates_for_vacation()
        airbnb_homepage.navigate()
        airbnb_homepage.fill_destination(destination)
        airbnb_homepage.select_dates(checkin, checkout)
        airbnb_homepage.set_num_of_guests(adults,children)
        airbnb_homepage.search()
        airbnb_results.details_verification(destination,checkin,checkout,adults,children)
        a = airbnb_results.check_cards_in_all_pages()
        airbnb_results.go_to_reservation_page(a.link)
        asset_page.reserve()
        booking_page.verify_dates(checkin, checkout)
        booking_page.fill_phone_field("546693187")
        booking_page.verify_guests(adults,children)
        booking_page.verify_price(a.price)
        
        