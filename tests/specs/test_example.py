# pytest-playwright fixtures are provided automatically
# No need to import 'page' - pytest-playwright does it for you

def test_visit_example(page):
    """Test: Verify that automatizando.vercel.app loads correctly and has the expected title"""
    page.goto("https://automatizando.vercel.app/")
    page.wait_for_load_state("load")
    # page.pause()  # This will open the inspector and pause execution here
    print("TITLE:", page.title())
    assert "automatizando" in page.title().lower()