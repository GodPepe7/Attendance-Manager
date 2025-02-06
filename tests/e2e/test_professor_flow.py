import re
from datetime import datetime

import pytest
from dependency_injector import providers
from playwright.sync_api import expect
from tests.e2e_fixtures import storage, start_test_app, add_test_data, transactional_app, FixedClock

url = "127.0.0.1:5001"


@pytest.fixture
def login_as_professor(new_context, storage, transactional_app):
    flask_app = transactional_app
    if storage.exists():
        yield new_context(storage_state=storage).new_page(), flask_app
    else:
        context = new_context()
        page = context.new_page()
        page.clock.install()
        page.goto(url)
        page.get_by_label("Email").fill("prof@htw.de")
        page.get_by_label("Password").fill("test")
        page.get_by_role("button", name="Login").click()
        expect(page.get_by_role("heading", name="Your Courses")).to_be_visible()
        yield page, flask_app
        context.storage_state(path=storage)


@pytest.fixture
def go_to_softwareengineering(login_as_professor):
    page, flask_app = login_as_professor
    page.goto(url)
    softwareengineering_course_card = page.get_by_test_id("course-card").filter(
        has=page.get_by_role("heading", name="Softwareengineering"))
    softwareengineering_course_card.get_by_role("link", name="View Attendance").click()
    expect(page.get_by_text(re.compile("Student Count:"))).to_be_visible()
    return page, flask_app


def test_courses_page_has_2_courses(login_as_professor):
    page, _ = login_as_professor
    page.goto(f"{url}/courses")
    page.wait_for_load_state('networkidle')

    course_cards = page.get_by_test_id("course-card")
    course_cards_count = course_cards.count()
    assert course_cards_count == 2, "Only 2 course cards are expected"
    expected_course_titles = ["Softwareengineering", "Projectmanagement"]
    for i in range(course_cards_count):
        course_title = course_cards.nth(i).get_by_role("heading")
        assert course_title.count() == 1, "Card has no title"
        title_text = course_title.text_content()
        assert title_text in expected_course_titles, f"Unexpected course title '{title_text}' in card {i + 1}."


def test_professor_can_create_course(login_as_professor):
    page, _ = login_as_professor
    page.goto(f"{url}/courses")
    page.wait_for_load_state('networkidle')

    new_course_name = "Economy for Dummies"
    page.get_by_role("button", name="Create New Course").click()
    page.get_by_label("Name", exact=True).fill(new_course_name)
    page.get_by_text("Add", exact=True).click()

    page.wait_for_load_state('networkidle')
    new_course = page.get_by_test_id("course-card").filter(has=page.get_by_role("heading", name=new_course_name))
    expect(new_course).to_be_visible()
    expect(page.get_by_test_id("course-card")).to_have_count(3)


def test_professor_can_edit_course_name(login_as_professor):
    page, _ = login_as_professor
    page.goto(f"{url}/courses")
    page.wait_for_load_state('networkidle')

    to_be_edited_course_name = "Projectmanagement"
    updated_course_name = "Cowabunga"
    expect(page.get_by_role("heading", name=to_be_edited_course_name)).to_be_visible()
    page.locator("#open-edit-course-btn").nth(1).click()
    page.get_by_label("Course Name").fill(updated_course_name)
    page.get_by_text("Edit", exact=True).click()

    page.wait_for_load_state('networkidle')
    expect(page.get_by_role("heading", name=to_be_edited_course_name)).not_to_be_visible()
    expect(page.get_by_role("heading", name=updated_course_name)).to_be_visible()


def test_professor_can_delete_course(login_as_professor):
    page, _ = login_as_professor
    page.goto(f"{url}/courses")
    page.wait_for_load_state('networkidle')

    to_be_deleted_course_name = "Projectmanagement"
    expect(page.get_by_role("heading", name=to_be_deleted_course_name)).to_be_visible()
    page.locator("#open-edit-course-btn").nth(1).click()
    page.get_by_text("Delete").click()

    page.wait_for_load_state('networkidle')
    expect(page.get_by_role("heading", name=to_be_deleted_course_name)).not_to_be_visible()


def test_attendance_page_table_shows_correct_data(go_to_softwareengineering):
    page, _ = go_to_softwareengineering

    expect(page.get_by_role("heading", name="Softwareengineering")).to_be_visible()
    expected_lectures = ["01.01.25", "02.01.25", "03.01.25", "23.01.25"]
    absent = "Absent"
    attended = "Attended"
    expected_student_rows = {
        "ainz": [attended, absent, attended, attended],
        "alex": [attended, absent, absent, absent],
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


def test_professor_can_mark_student_as_has_attended_or_absent(go_to_softwareengineering):
    page, _ = go_to_softwareengineering

    student_row = page.get_by_test_id("student-row-alex")
    toggle_attendance_btn = student_row.get_by_role("button").nth(1)
    expect(toggle_attendance_btn).to_contain_text("Absent")
    toggle_attendance_btn.click()

    page.wait_for_load_state('networkidle')
    toggle_attendance_btn = student_row.get_by_role("button").nth(1)
    expect(toggle_attendance_btn).to_contain_text("Attended")

    page.wait_for_load_state('networkidle')
    toggle_attendance_btn.click()
    toggle_attendance_btn = student_row.get_by_role("button").nth(1)
    expect(toggle_attendance_btn).to_contain_text("Absent")


def test_professor_can_create_lecture(go_to_softwareengineering):
    page, _ = go_to_softwareengineering

    page.get_by_role("button", name="Add Lecture").click()
    page.locator("#add-lecture-date").fill("2025-01-21")
    page.get_by_text("Submit Lecture").click()

    page.wait_for_load_state('networkidle')
    expect(page.get_by_role("columnheader", name="21.01.25")).to_be_visible()


def test_professor_can_edit_lecture(go_to_softwareengineering):
    page, _ = go_to_softwareengineering

    page.get_by_role("button", name="01.01.25").click()
    page.locator("#edit-lecture-date").fill("2025-01-22")
    page.get_by_text("Edit", exact=True).click()

    page.wait_for_load_state('networkidle')
    expect(page.get_by_role("columnheader", name="01.01.25")).not_to_be_visible()
    expect(page.get_by_role("columnheader", name="22.01.25")).to_be_visible()


def test_professor_can_delete_lecture(go_to_softwareengineering):
    page, _ = go_to_softwareengineering

    page.get_by_role("button", name="01.01.25").click()
    page.get_by_text("Delete").click()

    page.wait_for_load_state('networkidle')
    expect(page.get_by_role("columnheader", name="01.01.25")).not_to_be_visible()


def test_professor_can_set_new_password_and_student_can_use_it(go_to_softwareengineering, new_context):
    page, flask_app = go_to_softwareengineering
    date_of_second_lecture = datetime(2025, 1, 2, 10, 0, 0)
    fixed_clock = providers.Factory(
        FixedClock, fixed_datetime=date_of_second_lecture
    )
    flask_app.container.clock.override(fixed_clock)
    student_row = page.get_by_test_id("student-row-alex")
    toggle_attendance_btn = student_row.get_by_role("button").nth(1)
    expect(toggle_attendance_btn).to_contain_text("Absent")

    new_password = "safe password"
    page.get_by_role("button", name="Password").click()
    page.get_by_label("Password").fill(new_password)
    page.get_by_label("Expiration Datetime").fill("2025-01-02T12:00")
    page.get_by_text("Submit", exact=True).click()
    expect(page.locator("#set-password")).not_to_be_visible()

    context = new_context()
    new_page = context.new_page()
    new_page.goto(url)
    new_page.get_by_label("Email").fill("student@htw.de")
    new_page.get_by_label("Password").fill("test")
    new_page.get_by_role("button", name="Login").click()
    expect(new_page.get_by_role("heading", name="Log Attendance")).to_be_visible()
    new_page.get_by_label("Course").fill("Softwareengineering")
    new_page.get_by_text("Softwareengineering (chad)").click()
    new_page.get_by_label("password").fill(new_password)
    new_page.get_by_role("button", name="Submit").click()
    expect(new_page.get_by_text("Successfully logged attendance")).to_be_visible()

    page.reload()
    updated_student_row = page.get_by_test_id("student-row-alex")
    toggle_attendance_btn = updated_student_row.get_by_role("button").nth(1)
    expect(toggle_attendance_btn).to_contain_text("Attended")

def test_professor_can_create_qr_code_that_changes_after_30_seconds(go_to_softwareengineering):
    page, _ = go_to_softwareengineering

    page.get_by_role("button", name="QR Code").click()
    expect(page.locator("#qr-canvas")).not_to_be_visible()
    page.get_by_label("Select Lecture").select_option("1")

    expect(page.locator("#qr-canvas")).to_be_visible()
    first_qr_code = page.locator("#qr-code-string").text_content()
    with page.expect_response("**/attendance/qr**") as res:
        page.clock.fast_forward("00:29")

    assert res.value.ok
    second_qr_code = page.locator("#qr-code-string").text_content()
    assert first_qr_code != second_qr_code
