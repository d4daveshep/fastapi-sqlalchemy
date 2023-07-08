import re

from playwright.sync_api import Page, expect


def test_delete_multiple_connection(loaded_test_data, my_base_url: str, page: Page):
    # search for some connections
    page.goto(my_base_url + "/connections/?name_like=e")
    orig_found_heading = page.get_by_role("heading", name=re.compile("Found [0-9]+ Connections"))
    expect(orig_found_heading).to_contain_text("17")

    # check 2 boxes in the left hand column box
    page.locator("#connection_id_3").check()
    page.locator("#connection_id_12").check()


    # refresh the page and the connection should not be there
    page.get_by_role("button", name="Delete Selected").click()

    # TODO continue here - get the page to do something

    expect(page).to_have_title("Connection Results")

    # check the connections found is one less than previously
    new_found_heading = page.get_by_role("heading", name=re.compile("Found [0-9]+ Connections"))
    expect(new_found_heading).to_contain_text("15")

    # check the connection we delete isn't there
    # no_row = page.get_by_role("row", name="Brian has title Practice Lead Delete")
    # expect(no_row).to_have_count(0)
