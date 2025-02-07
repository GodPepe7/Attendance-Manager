import pytest
from playwright.sync_api import expect
from tests.e2e_fixtures import storage, start_test_app, add_test_data, transactional_app

url = "127.0.0.1:5001"


@pytest.fixture
def login_as_admin(new_context, storage, transactional_app):
    if storage.exists():
        yield new_context(storage_state=storage).new_page()
    else:
        context = new_context()
        page = context.new_page()
        page.clock.install()
        page.goto(url)
        page.get_by_label("Email").fill("admin@htw.de")
        page.get_by_label("Password").fill("test")
        page.get_by_role("button", name="Login").click()
        expect(page.get_by_role("heading", name="Admin Dashboard")).to_be_visible()
        yield page
        context.storage_state(path=storage)


def test_edit_professor_email_and_name_then_professor_logs_in_with_new_email(login_as_admin, new_context):
    page = login_as_admin
    page.goto(url + "/admin")
    page.locator("#name-1").fill("Bob Der Baumeister")
    page.locator("#email-1").fill("bobderbaumeister@htw.de")
    row = page.get_by_role("row", name="Bob Der Baumeister bobderbaumeister@htw.de Edit Delete")
    page.once("dialog", lambda dialog: dialog.accept())
    row.get_by_role("button", name="Edit").click()

    context = new_context()
    new_page = context.new_page()
    new_page.goto(url)
    new_page.get_by_label("Email").fill("bobderbaumeister@htw.de")
    new_page.get_by_label("Password").fill("test")
    new_page.get_by_role("button", name="Login").click()
    expect(new_page.get_by_role("heading", name="Your Courses")).to_be_visible()


def test_delete_professor_and_then_professor_should_not_be_able_to_log_in(login_as_admin, new_context):
    page = login_as_admin
    page.goto(url + "/admin")
    row = page.get_by_role("row", name="dude prof2@htw.de Edit Delete")
    page.once("dialog", lambda dialog: dialog.accept())
    row.get_by_role("button", name="Delete").click()

    context = new_context()
    new_page = context.new_page()
    new_page.goto(url)
    new_page.get_by_label("Email").fill("prof2@htw.de")
    new_page.get_by_label("Password").fill("test")
    new_page.get_by_role("button", name="Login").click()
    expect(new_page.get_by_role("heading", name="Your Courses")).not_to_be_visible()
