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


def test_professor_can_create_course(login_as_professor):
    page = login_as_professor

    new_course_name = "Economy for Dummies"
    page.goto("http://127.0.0.1:5000/courses")
    page.get_by_role("button", name="Create New Course").click()
    page.get_by_label("Name", exact=True).fill(new_course_name)
    page.get_by_text("Add", exact=True).click()

    new_course = page.get_by_test_id("course-card").filter(has=page.get_by_role("heading", name=new_course_name))
    expect(new_course).to_be_visible()


def test_professor_can_edit_course_name(login_as_professor):
    page = login_as_professor

    edited_course_name = "Economy for Intermediates"
    page.goto("http://127.0.0.1:5000/courses")
    page.locator("#open-edit-course-btn").nth(2).click()
    page.get_by_label("Course Name").fill(edited_course_name)
    page.get_by_text("Edit", exact=True).click()

    new_course = page.get_by_test_id("course-card").filter(has=page.get_by_role("heading", name=edited_course_name))
    expect(new_course).to_be_visible()


def test_professor_can_delete_course(login_as_professor):
    page = login_as_professor

    page.goto("http://127.0.0.1:5000/courses")
    page.locator("#open-edit-course-btn").nth(2).click()
    page.get_by_text("Delete").click()

    course_name = "Economy for Intermediates"
    deleted_course = page.get_by_test_id("course-card").filter(has=page.get_by_role("heading", name=course_name))
    expect(deleted_course).not_to_be_visible()


def test_attendance_page_table_shows_correct_data(login_as_professor):
    page = login_as_professor
    page.goto("http://127.0.0.1:5000/courses")
    softwareengineering_course_card = page.get_by_test_id("course-card").filter(
        has=page.get_by_role("heading", name="Softwareengineering"))

    softwareengineering_course_card.get_by_role("link", name="View Attendance").click()

    expect(page.get_by_role("heading", name="Softwareengineering")).to_be_visible()
    expected_lectures = ["01.01.25", "02.01.25", "03.01.25", "06.01.25"]
    absent = "Absent"
    attended = "Attended"
    expected_student_rows = {
        "ainz": [attended, absent, attended, attended],
        "alex": [absent, absent, absent, attended],
        "isagi": [absent, absent, attended, absent],
        "luffy": [attended, absent, attended, attended],
    }
    for lecture in expected_lectures:
        expect(page.get_by_role("columnheader", name=lecture)).to_be_visible()
    for student, attendance_history in expected_student_rows.items():
        student_row = page.get_by_test_id(f"student-row-{student}")
        expect(student_row).to_be_visible()
        all_attendances = student_row.get_by_role("cell")
        expect(all_attendances).to_have_count(4)
        for i in range(all_attendances.count()):
            expected_attendance = attendance_history[i]
            expect(all_attendances.nth(i).get_by_text(expected_attendance)).to_contain_text(expected_attendance)


def test_professor_can_mark_student_as_has_attended_or_absent(login_as_professor):
    page = login_as_professor
    page.goto("http://127.0.0.1:5000/courses/1")
    student_row = page.get_by_test_id("student-row-alex")
    toggle_attendance_btn = student_row.get_by_role("button").nth(1)
    expect(toggle_attendance_btn).to_contain_text("Absent")

    toggle_attendance_btn.click()

    toggle_attendance_btn = student_row.get_by_role("button").nth(1)
    expect(toggle_attendance_btn).to_contain_text("Attended")

    toggle_attendance_btn.click()
    toggle_attendance_btn = student_row.get_by_role("button").nth(1)
    expect(toggle_attendance_btn).to_contain_text("Absent")


def test_professor_can_create_lecture(login_as_professor):
    page = login_as_professor
    page.goto("http://127.0.0.1:5000/courses/1")
    create_lecture_btn = page.get_by_role("button", name="Add Lecture")
    create_lecture_btn.click()
    page.locator("#add-lecture-date").fill("2025-01-21")

    page.get_by_text("Submit Lecture").click()

    expect(page.get_by_role("columnheader", name="21.01.25")).to_be_visible()


def test_professor_can_edit_lecture(login_as_professor):
    page = login_as_professor
    page.goto("http://127.0.0.1:5000/courses/1")
    page.get_by_role("button", name="21.01.25").click()

    page.locator("#edit-lecture-date").fill("2025-01-22")
    page.get_by_text("Edit", exact=True).click()

    expect(page.get_by_role("columnheader", name="21.01.25")).not_to_be_visible()
    expect(page.get_by_role("columnheader", name="22.01.25")).to_be_visible()


def test_professor_can_delete_lecture(login_as_professor):
    page = login_as_professor
    page.goto("http://127.0.0.1:5000/courses/1")
    page.get_by_role("button", name="22.01.25").click()

    page.get_by_text("Delete").click()

    expect(page.get_by_role("columnheader", name="22.01.25")).not_to_be_visible()


def test_professor_can_set_password(login_as_professor):
    page = login_as_professor
    page.goto("http://127.0.0.1:5000/courses/1")
    page.get_by_role("button", name="Password").click()

    page.get_by_label("Password").fill("1234")
    page.get_by_label("Expiration Datetime").fill("2025-12-31T12:00")
    page.get_by_text("Submit", exact=True).click()

    expect(page.locator("#set-password")).not_to_be_visible()
