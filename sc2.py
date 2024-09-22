import asyncio
import csv

from playwright.async_api import async_playwright


# columns = [url,tagName,value,no_of_chars,fontSize,color,height,width,fontFamily,fontWeight,fontVariant,lineHeight,letterSpacing,wordSpacing,textAlign,textDecoration,textTransform,margin,padding,backgroundColor,backgroundImage,backgroundPosition,backgroundRepeat,backgroundSize]
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
            tagName = await element.evaluate('(element) => element.tagName')
            color = await element.evaluate('(element) => window.getComputedStyle(element).color')
            margin = await element.evaluate('(element) => element.style.margin ? element.style.margin : "none"')
            padding = await element.evaluate('(element) => element.style.padding ? element.style.padding : "none"')
            height = await element.evaluate('(element) => element.style.height ? element.style.height : "auto"')
            width = await element.evaluate('(element) => element.style.width ? element.style.width : "auto"')

            #-----------------------------Font styles--------------------------------------------------------
            fontSize = await element.evaluate('(element) => window.getComputedStyle(element).fontSize')
            fontFamily = await element.evaluate('(element) => window.getComputedStyle(element).fontFamily')
            fontWeight = await element.evaluate('(element) => window.getComputedStyle(element).fontWeight')
            fontVariant = await element.evaluate('(element) => window.getComputedStyle(element).fontVariant')
            lineHeight = await element.evaluate('(element) => window.getComputedStyle(element).lineHeight')
            letterSpacing = await element.evaluate('(element) => window.getComputedStyle(element).letterSpacing')
            wordSpacing = await element.evaluate('(element) => window.getComputedStyle(element).wordSpacing')
            textAlign = await element.evaluate('(element) => window.getComputedStyle(element).textAlign')
            textDecoration = await element.evaluate('(element) => window.getComputedStyle(element).textDecoration')
            textTransform = await element.evaluate('(element) => window.getComputedStyle(element).textTransform')

            # -----------------------------Background related styles--------------------------------------------------------
            backgroundColor = await element.evaluate('(element) => window.getComputedStyle(element).backgroundColor')
            backgroundImage = await element.evaluate('(element) => window.getComputedStyle(element).backgroundImage')
            backgroundPosition = await element.evaluate('(element) => window.getComputedStyle(element).backgroundPosition')
            backgroundRepeat = await element.evaluate('(element) => window.getComputedStyle(element).backgroundRepeat')
            backgroundSize = await element.evaluate('(element) => window.getComputedStyle(element).backgroundSize')

            text_content = await element.evaluate('(element) => element.textContent')
            no_of_chars = len(text_content)

            siz = float(fontSize.replace('px', ''))

            value = siz * siz * no_of_chars

            print('Element scrapped!')
            return (url,tagName,value,no_of_chars,fontSize,color,height,width,fontFamily,fontWeight,fontVariant,lineHeight,letterSpacing,wordSpacing,textAlign,textDecoration,textTransform,margin,padding,backgroundColor,backgroundImage,backgroundPosition,backgroundRepeat,backgroundSize)

        

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