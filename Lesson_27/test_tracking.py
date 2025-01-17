"""Homework #27. Write a test that track parcel on the Nova Post website."""
# Create the necessary classes and functions to use Selenium
# on the website "https: // tracking.novaposhta.ua/  # /uk"
# to enter the invoice number(transmitted from the test)
# and receive the status of the parcel in tracking, e.g.
# Returns: Parcel received
# The test verify that the received status corresponds to the expected one.

import pytest

from POM_tracking import TrackingPage


class TestTracking:
    """Test suite to validate parcel tracking on the Nova Post website."""

    @pytest.mark.parametrize(
        'invoice, expected_statuses',
        [
            ('20400435833295', ['Отримана']),
            ('20400436336099', ['Отримана']),
            ('20400436340000', ['Прибула до відділення', 'Отримана']),
            ('59500000031324', ['Ми не знайшли посилку за таким номером.']),
        ],
    )
    def test_parcel_status(self, browser_driver, invoice, expected_statuses):
        """Test to verify the status of a parcel matches the expected value.

        Args:
            browser_driver: Selenium WebDriver instance.
            invoice(str): The parcel's invoice number.
            expected_statuses(list): The expected status text.

        Raises:
            ValueError: If the parcel status doesn't match the expected status.
        """
        tracking_page = TrackingPage(browser_driver)
        tracking_page.load()

        # Enter the invoice number and search
        tracking_page.set_invoice(invoice)
        tracking_page.click_search()

        # Retrieve and verify the status or error message
        status = tracking_page.get_status() or tracking_page.get_err_message()
        if not status or not any(
            expected_status in status for expected_status in expected_statuses
        ):
            raise ValueError(
                f'Expected one of the statuses: {expected_statuses}, '
                f'Got: {status}',
            )
