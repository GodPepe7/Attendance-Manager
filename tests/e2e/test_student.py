import pytest
from playwright.sync_api import expect


@pytest.fixture(scope="session")
def storage(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("session")
    return tmp_path / "state.json"


@pytest.fixture
def login_as_student(new_context, storage):
    if storage.exists():
        yield new_context(storage_state=storage).new_page()
    else:
        context = new_context()
        page = context.new_page()
        page.goto("127.0.0.1:5000")
        page.get_by_label("Email").fill("student@htw.de")
        page.get_by_label("Password").fill("test")
        page.get_by_role("button", name="Login").click()

        expect(page.get_by_role("heading", name="Log Attendance")).to_be_visible()
        yield page
        context.storage_state(path=storage)


def test_course_searching_shows_course_list(login_as_student):
    page = login_as_student

    page.get_by_placeholder("Business English").fill("soft")

    expect(page.get_by_text("Softwareengineering (chad)")).to_be_visible()
    expect(page.get_by_text("Projektmanagement (chad)")).not_to_be_visible()
