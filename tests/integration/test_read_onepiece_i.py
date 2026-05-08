from webs.read_onepiece import ReadOnePiece

def test_find_chapter(navigate):
    driver = navigate("read_onepiece.html")
    page = ReadOnePiece(driver)

    chapters = page.get_elementList(ReadOnePiece._chapters_class, locator_type="class")
    first = page.get_element(ReadOnePiece._title_chapter_class, locator_type="class", parent=chapters[0])
    chapter = page.get_text(element=first)

    assert page.get_chapter_images(chapter) is True

def test_chapter_not_found(navigate):
    driver = navigate("read_onepiece.html")
    page = ReadOnePiece(driver)

    assert page.get_chapter_images("9999") is False