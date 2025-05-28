from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class AssetPage(BasePage):
    #LOCATORS
    TITLE =  "TITLE_DEFAULT"
    RESERVE_BTN = 'homes-pdp-cta-btn'
    BOOKING_SIDE_BAR = '[data-section-id="BOOK_IT_SIDEBAR"]'
    TRANSLATION_ANNOUNCE_DIALOG = "translation-announce-modal"
    TRANSLATION_ANNOUNCE_MODAL_CLOSE_BTN = "Close"

    def __init__(self, page: Page, logger=None):
        super().__init__(page, logger=logger)
        self.pw_page = page
        self.logger=logger
        self.booking_side_bar = self.pw_page.locator(self.BOOKING_SIDE_BAR)
        self._reserve_btn = self.booking_side_bar.get_by_test_id(self.RESERVE_BTN)
        

    @property
    def reserve_button(self):
        return self._reserve_btn
    
    def wait_for_page_loading(self):
        self.dismiss_translation_modal_if_visible()
        self.reserve_button.wait_for(state='visible')

    def reserve(self):
        self.wait_for_page_loading()
        with self.pw_page.expect_navigation(wait_until="load"):
            self.reserve_button.click()

    def dismiss_translation_modal_if_visible(self):
        translation_dialog = self.pw_page.get_by_role('dialog')
        try:
                expect(translation_dialog).to_be_visible
                self.logger.info("Translation modal appeared, dismissing it.")
                close_button_loactor = translation_dialog.get_by_label(self.TRANSLATION_ANNOUNCE_MODAL_CLOSE_BTN)
                close_button_loactor.wait_for()
                close_button_loactor.click()
        except:
            self.logger.info("Translation modal didnt appear, moving on.")