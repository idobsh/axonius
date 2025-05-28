from playwright.sync_api import Page, expect

class BasePage():
    DEFAULT_NAV_TIMEOUT = 10000000000
    BASE_URL = "https://www.airbnb.com"
    # DEFAULT_NAV_TIMEOUT = timeouts.pw.navigation.default_millis
    # SELECTORS

    def __init__(self, page: Page, path="", logger=None):
        self.pw_page = page
        self.url = self.BASE_URL+path
        self.logger = logger
    
    def navigate(self, wait_until="load", timeout=DEFAULT_NAV_TIMEOUT):
        self.pw_page.goto(url=self.url, wait_until=wait_until, timeout=timeout)
    
    def click(self, selector: str):
        self.pw_page.locator(selector).click()

    def fill(self, selector: str, text: str):
        self.pw_page.locator(selector).fill(text)

    def wait_for_element(self, selector: str):
        expect(self.pw_page.locator(selector)).to_be_visible()