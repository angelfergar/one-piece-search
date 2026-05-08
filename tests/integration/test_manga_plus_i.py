from webs.manga_plus import MangaPlus
from datetime import datetime
def test_break_week(navigate):
    driver = navigate("manga_plus.html")
    page = MangaPlus(driver)
    result = page.find_break_week()

    assert result.startswith("W")
    assert result[1:].isdigit()
    assert 1 <= int(result[1:]) <= 53


def test_next_chapter(navigate):
    driver = navigate("manga_plus.html")
    page = MangaPlus(driver)
    result = page.find_chapter()

    assert isinstance(result, int)
    assert result > 0