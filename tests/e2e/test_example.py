import pytest
from playwright.sync_api import expect


@pytest.fixture(scope="session")
def storage(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("session")
    return tmp_path / "state.json"


@pytest.fixture
def authenticated_page(new_context, storage):
    if storage.exists():
        yield new_context(storage_state=storage).new_page()
    else:
        context = new_context()
        page = context.new_page()
        page.goto("127.0.0.1:5000")
        page.get_by_label("Email").fill("p@htw.de")
        page.get_by_label("Password").fill("test1234")
        page.get_by_role("button", name="Login").click()

        expect(page.get_by_role("heading", name="Your Courses")).to_be_visible()
        yield page
        context.storage_state(path=storage)


def test_example(authenticated_page):
    page = authenticated_page
    page.goto("http://127.0.0.1:5000/courses")
    expect(page.get_by_role("heading", name="Softwareengineering")).to_be_visible()
    page.get_by_role("link", name="View Attendance").click()
    expect(page.locator("body")).to_match_aria_snapshot(
        "- table:\n  - rowgroup:\n    - row /Name \\d+\\.\\d+\\.\\d+ \\d+\\.\\d+\\.\\d+ \\d+\\.\\d+\\.\\d+ \\d+\\.\\d+\\.\\d+ \\d+\\.\\d+\\.\\d+ \\d+\\.\\d+\\.\\d+ \\d+\\.\\d+\\.\\d+ \\d+\\.\\d+\\.\\d+ \\d+\\.\\d+\\.\\d+ \\d+\\.\\d+\\.\\d+/:\n      - cell \"Name\"\n      - cell /\\d+\\.\\d+\\.\\d+/:\n        - button /\\d+\\.\\d+\\.\\d+/\n      - cell /\\d+\\.\\d+\\.\\d+/:\n        - button /\\d+\\.\\d+\\.\\d+/\n      - cell /\\d+\\.\\d+\\.\\d+/:\n        - button /\\d+\\.\\d+\\.\\d+/\n      - cell /\\d+\\.\\d+\\.\\d+/:\n        - button /\\d+\\.\\d+\\.\\d+/\n      - cell /\\d+\\.\\d+\\.\\d+/:\n        - button /\\d+\\.\\d+\\.\\d+/\n      - cell /\\d+\\.\\d+\\.\\d+/:\n        - button /\\d+\\.\\d+\\.\\d+/\n      - cell /\\d+\\.\\d+\\.\\d+/:\n        - button /\\d+\\.\\d+\\.\\d+/\n      - cell /\\d+\\.\\d+\\.\\d+/:\n        - button /\\d+\\.\\d+\\.\\d+/\n      - cell /\\d+\\.\\d+\\.\\d+/:\n        - button /\\d+\\.\\d+\\.\\d+/\n      - cell /\\d+\\.\\d+\\.\\d+/:\n        - button /\\d+\\.\\d+\\.\\d+/\n  - rowgroup:\n    - row \"ainz Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance\":\n      - cell \"ainz\"\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n    - row \"alex Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance\":\n      - cell \"alex\"\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n    - row \"isagi Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance\":\n      - cell \"isagi\"\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n    - row \"luffy Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance Toggle attendance\":\n      - cell \"luffy\"\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img\n      - cell \"Toggle attendance\":\n        - button \"Toggle attendance\":\n          - img")
    page.locator("tr:nth-child(4) > td:nth-child(2) > .w-full").click()
    expect(page.locator("tbody")).to_match_aria_snapshot("- img")
    page.locator("tr:nth-child(4) > td:nth-child(2) > .w-full").click()
    expect(page.locator("tbody")).to_match_aria_snapshot("- img")
