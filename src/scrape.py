from playwright.sync_api import sync_playwright

# Configurable items
# This is the string that gets entered into the search input field.
search_term = '2023 ACE Dialogue'

# Initialize playwright. See https://playwright.dev/python/docs/intro
playwright = sync_playwright().start()

# we specify headless=False to visualize what playwright is doing. In production code,
# it's probably faster to run this headless.
browser = playwright.chromium.launch(headless=False)
context = browser.new_context()
page = context.new_page()

# Go to the URL we want to target.
page.goto('https://unfccc.int/documents')

# Get the search input and fill it with the requested string. In this example, we use
# 2023 ACE Dialogue.
page.get_by_placeholder('Search here').fill(search_term)
page.keyboard.press('Enter')

# Get the load more button. If it's available, we will keep clicking on it
# until it is no longer visible (ie. when all results are loaded).
locator = page.locator('.pager__item > a.button')
has_more_content = locator.is_visible()
i = 0

while has_more_content:

    # Check if there are more items to load
    locator = page.locator('.pager__item > a.button')
    has_more_content = locator.is_visible()

    # break out of loop if there is no more content to load
    if not has_more_content:
        # when there is no more content to load, take a screenshot.
        page.screenshot(path='screenshot.png', full_page=True)
        continue

    # Click the button
    locator.click()

    # Wait for 10 seconds. There's probably a better way to do this, and the timeout
    # may need to be adjusted / randomized.
    page.wait_for_timeout(10000)
    page.screenshot(path=f'screenshot{i}.png', full_page=True)
    i += 1
