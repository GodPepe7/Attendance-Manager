import pytest
from playwright.sync_api import expect


@pytest.fixture(scope="session")
def storage(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("session")
    return tmp_path / "state.json"


@pytest.fixture
def login_as_professor(new_context, storage):
    if storage.exists():
        yield new_context(storage_state=storage).new_page()
    else:
        context = new_context()
        page = context.new_page()
        page.goto("127.0.0.1:5000")
        page.get_by_label("Email").fill("prof@htw.de")
        page.get_by_label("Password").fill("test")
        page.get_by_role("button", name="Login").click()

        expect(page.get_by_role("heading", name="Your Courses")).to_be_visible()
        yield page
        context.storage_state(path=storage)


def test_courses_page_has_2_courses(login_as_professor):
    page = login_as_professor

    page.goto("http://127.0.0.1:5000/courses")

    course_cards = page.get_by_test_id("course-card")
    course_cards_count = course_cards.count()
    assert course_cards_count == 2, "Only 2 course cards are expected"
    expected_course_titles = ["Softwareengineering", "Projektmanagement"]
    for i in range(course_cards_count):
        course_title = course_cards.nth(i).get_by_role("heading")
        assert course_title.count() == 1, "Card has no title"
        title_text = course_title.text_content()
        assert title_text in expected_course_titles, f"Unexpected course title '{title_text}' in card {i + 1}."


def test_attendance_page(login_as_professor):
    page = login_as_professor
    page.goto("http://127.0.0.1:5000/courses")
    softwareengineering_course_card = page.get_by_test_id("course-card").filter(
        has=page.get_by_role("heading", name="Softwareengineering"))

    softwareengineering_course_card.get_by_role("link", name="View Attendance").click()

    expect(page.get_by_role("heading", name="Softwareengineering")).to_be_visible()
    expected_lectures = ["04.12.24", "12.12.24", "18.12.24", "20.12.24", "25.12.24", "31.12.24"]
    for lecture in expected_lectures:
        expect(page.get_by_role("columnheader", name=lecture)).to_be_visible()
