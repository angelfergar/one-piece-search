from webs.opscans import OpScans

def test_find_chapter(navigate):
    driver = navigate("opscans_found.html")
    page = OpScans(driver)

    assert page.get_chapter_images() is True

def test_chapter_not_found(navigate):
    driver = navigate("opscans_not_found.html")
    page = OpScans(driver)

    assert page.get_chapter_images() is False