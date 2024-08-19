import asyncio

from playwright.async_api import async_playwright


async def scrape_headings(url, file_name):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        # Extract headings and their styles
        headings_data = []
        for i in range(1, 7):  # Heading levels from h1 to h6
            headings = await page.query_selector_all(f'h{i}')
            for heading in headings:
                # Extract the tag name
                tag_name = await heading.evaluate('(element) => element.tagName')
                size = await heading.evaluate('(element) => window.getComputedStyle(element).fontSize')
                color = await heading.evaluate('(element) => window.getComputedStyle(element).color')
                font_family = await heading.evaluate('(element) => window.getComputedStyle(element).fontFamily')
                margin = await heading.evaluate('(element) => element.style.margin ? element.style.margin : "none"')
                padding = await heading.evaluate('(element) => element.style.padding ? element.style.padding : "none"')
                height = await heading.evaluate('(element) => element.style.height ? element.style.height : "auto"')
                width = await heading.evaluate('(element) => element.style.width ? element.style.width : "auto"')

                headings_data.append((tag_name, size, font_family, color, height, width, margin, padding))

        for element in ['p', 'div']:
            all_eles = await page.query_selector_all(element)

            for e in all_eles:
                tag_name = await e.evaluate('(element) => element.tagName')
                size = await e.evaluate('(element) => window.getComputedStyle(element).fontSize')
                color = await e.evaluate('(element) => window.getComputedStyle(element).color')
                font_family = await e.evaluate('(element) => window.getComputedStyle(element).fontFamily')
                margin = await e.evaluate('(element) => element.style.margin ? element.style.margin : "none"')
                padding = await e.evaluate('(element) => element.style.padding ? element.style.padding : "none"')
                height = await e.evaluate('(element) => element.style.height ? element.style.height : "auto"')
                width = await e.evaluate('(element) => element.style.width ? element.style.width : "auto"')

                headings_data.append((tag_name, size, font_family, color, height, width, margin, padding))

        await browser.close()

        # Write data to a text file
        with open(file_name, 'w') as file:
            file.write(f"{'Tag Name':<10}{'Size':<20}{'Font Family':<30}{'Color':<20}{'height':<20}{'width':<20}{'margin':<20}{'padding':<20}\n")  # Column headers with fixed width
            for tag_name, size, font_family, color, height, width, margin, padding in headings_data:
                file.write(f"{tag_name:<10}{size:<20}{font_family:<30}{color:<20}{height:<20}{width:<20}{margin:<20}{padding:<20}\n")

        print('Scraping completed! Check headings_data.txt for the results.')

# Run the scraping function
# asyncio.run(scrape_headings('https://tympanus.net/Development/ImageTilesMenu/'))# Run the scraping function
# asyncio.run(scrape_headings('https://tympanus.net/Development/ImageTilesMenu/'))