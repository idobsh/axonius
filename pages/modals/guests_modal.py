from playwright.sync_api import Page
from pages.ui_components.stepper import Stepper
from typing import Literal


class GuestsModal:
    ADULTS_STEPPER = "adults"
    CHILDREN_STEPPER = "children"
    INFANTS_STEPPER = "infants"
    PETS_STEPPER = "pets"

    def __init__(self, page: Page, context: Literal["search", "checkout"], logger=None):
        self.page = page
        self.logger = logger
        self._locators = self._get_locator_map(context)

        self.adults_stepper = Stepper(page, "adults", self._locators, logger)
        self.children_stepper = Stepper(page, "children", self._locators, logger)
        self.infants_stepper = Stepper(page, "infants", self._locators, logger)
        self.pets_stepper = Stepper(page, "pets", self._locators, logger)

    def _get_locator_map(self, context: str) -> dict:
        if context == "search":
            return {
                "plus": "stepper-{type}-increase-button",
                "minus": "stepper-{type}-decrease-button",
                "value": "stepper-{type}-value",
            }
        elif context == "checkout":
            return {
                "plus": "GUEST_PICKER-{type}-stepper-increase-button",
                "minus": "GUEST_PICKER-{type}-stepper-decrease-button",
                "value": "GUEST_PICKER-{type}-stepper-value",
            }
        else:
            raise ValueError(f"Unsupported modal context: {context}")

    def set_adults(self, count: int):
        self.adults_stepper.set_stepper_to(count)

    def set_childrens(self, count: int):
        self.children_stepper.set_stepper_to(count)

    def set_infants(self, count: int):
        self.infants_stepper.set_stepper_to(count)

    def set_pets(self, count: int):
        self.pets_stepper.set_stepper_to(count)
