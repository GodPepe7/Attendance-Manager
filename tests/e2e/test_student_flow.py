from datetime import datetime, timedelta

import pytest
from dependency_injector import providers
from playwright.sync_api import expect

from tests.fixtures import storage, start_test_app, add_test_data, FixedClock, transactional_app
from tests.test_data_e2e import course_expiration_datetime


@pytest.fixture
def login_as_student(new_context, storage, transactional_app):
    flask_app = transactional_app
    if storage.exists():
        yield new_context(storage_state=storage).new_page(), flask_app
    else:
        context = new_context()
        page = context.new_page()
        page.goto("127.0.0.1:5001")
        page.get_by_label("Email").fill("student@htw.de")
        page.get_by_label("Password").fill("test")
        page.get_by_role("button", name="Login").click()

        expect(page.get_by_role("heading", name="Log Attendance")).to_be_visible()
        yield page, flask_app
        context.storage_state(path=storage)


def test_student_can_choose_course_and_log_attendance(login_as_student):
    page, flask_app = login_as_student
    page.goto("127.0.0.1:5001/student")
    fixed_datetime = course_expiration_datetime - timedelta(hours=1)
    fixed_clock = providers.Factory(
        FixedClock, fixed_datetime=fixed_datetime
    )
    flask_app.container.clock.override(fixed_clock)

    page.get_by_label("Course").fill("sof")
    software_engineering_course = page.get_by_text("Softwareengineering (chad)")
    expect(software_engineering_course).to_be_visible()
    expect(page.get_by_text("Projectmanagement (chad)")).not_to_be_visible()
    expect(page.get_by_text("Rizz 101 (dude)")).not_to_be_visible()
    software_engineering_course.click()
    page.get_by_label("password").fill("password")
    page.get_by_role("button", name="Submit").click()

    expect(page.get_by_text("Successfully logged attendance")).to_be_visible()


def test_student_cannot_log_attendance_with_expired_password(login_as_student):
    page, flask_app = login_as_student
    page.goto("127.0.0.1:5001/student")
    password_expired_datetime = datetime(2024, 1, 23, 12, 1)
    flask_app.container.clock.override(providers.Factory(FixedClock, fixed_time=password_expired_datetime))

    page.get_by_label("Course").fill("sof")
    software_engineering_course = page.get_by_text("Softwareengineering (chad)")
    expect(software_engineering_course).to_be_visible()
    expect(page.get_by_text("Projectmanagement (chad)")).not_to_be_visible()
    expect(page.get_by_text("Rizz 101 (dude)")).not_to_be_visible()
    software_engineering_course.click()
    page.get_by_label("password").fill("password")
    page.get_by_role("button", name="Submit").click()

    expect(page.get_by_text("Successfully logged attendance")).not_to_be_visible()
