import asyncio
import csv

from playwright.async_api import async_playwright


# columns = [url,tag_name,value,no_of_chars,size,color,height,width,font_family,font_weight,font_variant,line_height,letter_spacing,word_spacing,text_align,text_decoration,text_transform,margin,padding,background_color,background_image,background_position,background_repeat,background_size]
async def writeData(file_name, headings_data):
    with open(file_name, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # csv_writer.writerow(['site_url', 'Tag Name', 'Size', 'Font Family', 'Color', 'height', 'width', 'margin', 'padding'])
        for row in headings_data:
            # font_family_str = ', '.join(row[3])
            csv_writer.writerow(row)

async def scrape_data(url, file_name):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        scrapped_data = []


        async def get_element_styles(element):
            tag_name = await element.evaluate('(element) => element.tagName')
            size = await element.evaluate('(element) => window.getComputedStyle(element).fontSize')
            color = await element.evaluate('(element) => window.getComputedStyle(element).color')
            margin = await element.evaluate('(element) => element.style.margin ? element.style.margin : "none"')
            padding = await element.evaluate('(element) => element.style.padding ? element.style.padding : "none"')
            height = await element.evaluate('(element) => element.style.height ? element.style.height : "auto"')
            width = await element.evaluate('(element) => element.style.width ? element.style.width : "auto"')

            #-----------------------------Font styles--------------------------------------------------------
            font_family = await element.evaluate('(element) => window.getComputedStyle(element).fontFamily')
            font_weight = await element.evaluate('(element) => window.getComputedStyle(element).fontWeight')
            font_variant = await element.evaluate('(element) => window.getComputedStyle(element).fontVariant')
            line_height = await element.evaluate('(element) => window.getComputedStyle(element).lineHeight')
            letter_spacing = await element.evaluate('(element) => window.getComputedStyle(element).letterSpacing')
            word_spacing = await element.evaluate('(element) => window.getComputedStyle(element).wordSpacing')
            text_align = await element.evaluate('(element) => window.getComputedStyle(element).textAlign')
            text_decoration = await element.evaluate('(element) => window.getComputedStyle(element).textDecoration')
            text_transform = await element.evaluate('(element) => window.getComputedStyle(element).textTransform')

            # -----------------------------Background related styles--------------------------------------------------------
            background_color = await element.evaluate('(element) => window.getComputedStyle(element).backgroundColor')
            background_image = await element.evaluate('(element) => window.getComputedStyle(element).backgroundImage')
            background_position = await element.evaluate('(element) => window.getComputedStyle(element).backgroundPosition')
            background_repeat = await element.evaluate('(element) => window.getComputedStyle(element).backgroundRepeat')
            background_size = await element.evaluate('(element) => window.getComputedStyle(element).backgroundSize')

            text_content = await element.evaluate('(element) => element.textContent')
            no_of_chars = len(text_content)

            siz = float(size.replace('px', ''))

            value = siz * siz * no_of_chars

            print('Element scrapped!')
            return (url,tag_name,value,no_of_chars,size,color,height,width,font_family,font_weight,font_variant,line_height,letter_spacing,word_spacing,text_align,text_decoration,text_transform,margin,padding,background_color,background_image,background_position,background_repeat,background_size)

        

        stack = []
        stack.append(await page.query_selector('body'))

        selectors = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'p', 'a', 'button']
        
        while (len(stack) > 0):
            root = stack.pop(0)
            # elements = await root.query_selector_all('h1, h2 , h3, h4, h5, h6, div, p, a, button')
            elements = await root.query_selector_all('*')
            for e in elements:
                stack.append(e)
            elements = []
            
            data = await get_element_styles(root)
            scrapped_data.append(data)
            print('Element style extracted!',data)
            print('Current length of stack: ',len(stack))
            pass

        await browser.close()
        
        await writeData(file_name,scrapped_data)

        print('Scraping completed! Check data.txt for the results.')

# Run the scraping function
# asyncio.run(scrape_data('https://tympanus.net/Development/ImageTilesMenu/'))# Run the scraping function
# asyncio.run(scrape_data('https://tympanus.net/Development/PushGridItems/', 'scrapped_data/test.csv'))  #passed
# asyncio.run(scrape_data('https://tympanus.net/Development/IntroGridMotionTransition/', 'scrapped_data/test.csv'))