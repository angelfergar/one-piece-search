from webs.tcb_op import TcbOp

def test_find_chapter(navigate):
    driver = navigate("tcbop.html")
    page = TcbOp(driver)

    chapters = page.get_elementList(TcbOp._link_to_chapters_class, locator_type="class")
    first = page.get_element(TcbOp._title_list_class, locator_type="class", parent=chapters[0])
    chapter = page.get_text(element=first)

    assert page.get_chapter_images(chapter) is True

def test_chapter_not_found(navigate):
    driver = navigate("tcbop.html")
    page = TcbOp(driver)

    assert page.get_chapter_images("9999") is False