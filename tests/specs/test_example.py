def test_visit_example(page):
    page.goto("https://automatizando.vercel.app/")
    page.wait_for_load_state("load")
    page.pause()  # Esto abrirá el inspector y pausará la ejecución aquí
    print("TITLE:", page.title())
    assert "automatizando" in page.title().lower()