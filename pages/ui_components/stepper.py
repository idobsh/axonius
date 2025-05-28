from playwright.sync_api import Page, expect
from typing import Optional


class Stepper:
    def __init__(
        self,
        page: Page,
        stepper_type: str,
        locator_pattern: dict,
        logger: Optional[object] = None,
    ):
        self.pw_page = page
        self.logger = logger
        self._type = stepper_type
        self._locator_pattern = locator_pattern

        self._plus_button = self.pw_page.get_by_test_id(
            locator_pattern["plus"].format(type=stepper_type)
        ).first

        self._minus_button = self.pw_page.get_by_test_id(
            locator_pattern["minus"].format(type=stepper_type)
        ).first

        self._value = self.pw_page.get_by_test_id(
            locator_pattern["value"].format(type=stepper_type)
        ).first

    @property
    def type(self):
        return self._type

    @property
    def plus_button(self):
        return self._plus_button

    @property
    def minus_button(self):
        return self._minus_button

    @property
    def value(self):
        return self._value

    def increase(self):
        self.plus_button.click()

    def decrease(self):
        self.minus_button.click()

    def get_value(self) -> int:
        text = self.value.text_content().strip()
        return int(text)

    def set_stepper_to(self, target: int):
        current = self.get_value()
        if self.logger:
            self.logger.info(f"Setting '{self._type}' stepper from {current} to {target}")

        if current < target:
            for i in range(target - current):
                self.increase()
                expect(self.value).to_have_text(str(current + i + 1))
        elif current > target:
            for i in range(current - target):
                self.decrease()
                expect(self.value).to_have_text(str(current - i - 1))