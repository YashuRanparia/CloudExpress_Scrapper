import asyncio

import pandas as pd
from playwright.async_api import async_playwright

from sc2 import scrape_data


async def article_reading(article_site_url, csv_file):

    flag = True # flag is used to set whether to scrap whole data at one go

    #WARNING:   1 page = 15 webpages and there are such 23 pages : 23 * 15 = 345 webpages | 345*6 = 2070 datapoints

    async def pageData(rootele):
        container_div = await rootele.query_selector(".ct-archive-container")

        articles = await container_div.query_selector_all("article")

        article_links = []
        for article in articles:
            thumb_div = await article.query_selector(".ct-latest-thumb-archive")
            anchor_tag = await thumb_div.query_selector("a")
            href = await anchor_tag.evaluate("(element) => element.href")
            article_links.append(href)
        
        # print(article_links)

        final_urls = []
        done_url = ['https://tympanus.net/Development/3DPortalCard',
       'https://tympanus.net/Development/OnScrollShapeMorph',
       'https://tympanus.net/Development/PixelGooeyTooltip',
       'http://tympanus.net/Development/LayersAnimation',
       'http://tympanus.net/Development/MotionTrailAnimations/',
       'http://tympanus.net/Development/SlideshowAnimations/',
       'http://tympanus.net/Development/GridItemHoverEffect/',
       'http://tympanus.net/Development/ConnectedGrid/',
       'http://tympanus.net/Development/OnScrollColumnsRows/',
       'http://tympanus.net/Development/Scroll3DGrid/',
       'http://tympanus.net/Development/GridFlowEffect/',
       'http://tympanus.net/Development/ScrollBasedLayoutAnimations/',
       'http://tympanus.net/Development/TextBlockTransitions/',
       'http://tympanus.net/Development/OnScrollFilter/',
       'http://tympanus.net/Development/ImageTilesMenu/',
       'http://tympanus.net/Development/GridViewSwitch/',
       'http://tympanus.net/Development/PixelTransition/',
       'http://tympanus.net/Development/FullscreenClipEffect/',
       'http://tympanus.net/Development/DoubleImageHoverEffects/',
       'http://tympanus.net/Development/OnScrollTypographyAnimations/index2.html',
       'http://tympanus.net/Development/TypeShuffleAnimation/',
       'http://tympanus.net/Development/TwistedText/',
       'http://tympanus.net/Development/OnScrollTypographyAnimations/',
       'http://tympanus.net/Development/TooltipTransition/',
       'http://tympanus.net/Development/InlineLayoutSwitch/',
       'http://tympanus.net/Development/UnrevealEffects/',
       'http://tympanus.net/Development/ScrollPanels/',
       'http://tympanus.net/Development/MenuToGrid/',
       'http://tympanus.net/Development/GlitchPerspective/',
       'https://tympanus.net/Development/EmitterCursor/',
       'http://tympanus.net/Development/FullscreenScroll/',
       'http://tympanus.net/Development/ImageToContent/',
       'http://tympanus.net/Development/GridLayoutAnimation/',
       'http://tympanus.net/Development/MakeWayGridEffect/',
       'http://tympanus.net/Development/ScrollAnimationsGrid/',
       'http://tympanus.net/Development/ContentLayoutTransition/',
       'http://tympanus.net/Development/TextRepetitionEffect/',
       'http://tympanus.net/Development/LetterShuffleMenu/',
       'http://tympanus.net/Development/RepetitionHoverEffect/',
       'http://tympanus.net/Development/BackgroundShift/',
       'http://tympanus.net/Development/DistortedPixels/',
       'http://tympanus.net/Development/ColumnScroll/',
       'http://tympanus.net/Development/GridZoom/',
       'https://tympanus.net/Development/ParanoiaSlideshow/',
       'http://tympanus.net/Development/AutomaticImageMontage/',
       'http://tympanus.net/Development/ImageZoomTour/',
       'http://tympanus.net/Development/CircularContentCarousel/',
       'http://tympanus.net/Development/FullscreenGridPortfolioTemplate/']
        

        for article in article_links:
            page = await browser.new_page()
            await page.goto(article, timeout=120000)

            f1 = await page.query_selector(".ct-container")
            f2 = await f1.query_selector(".ct-content")
            f3 = await f2.query_selector(".ct-inner")
            f4 = await f3.query_selector(".ct-main-post")
            f5 = await f4.query_selector(".ct-post")
            art = await f5.query_selector("article")
            postcontent = await art.query_selector(".ct-post-content")
            postcontentimg = await postcontent.query_selector(".ct-post-featured-img")

            post_anchor_tag = await postcontentimg.query_selector("a")
            post_href = ''
            if(post_anchor_tag):
                post_href = await post_anchor_tag.evaluate("(element) => element.href")
            else:
                continue
            
            
            if(post_href in done_url):
                print("Already scrapped!")
                continue
            final_urls.append(post_href)

            # await asyncio.run(scrape_headings(post_href, f'articledata_{i}.txt'))
            try:
                await scrape_data(post_href, csv_file)
                print('Scrapped webpage.')
            except:
                print('Skipping this webpage due to timeout in scrap function!')
                pass
            pass
        pass

    async def allPageData(rootele, page):
        pagesdiv = await rootele.query_selector(".ct-postnav")
        pagedivin = await pagesdiv.query_selector("#wp_page_numbers")
        ul = await pagedivin.query_selector('ul')
        li = await ul.query_selector_all('li') # <<-- The anchor tage inside the li will consist the page-link


        page_urls = []
        #Manual check says page url is of form: https://tympanus.net/codrops/category/playground/page/2/
        for i in range(1,24):
            if i == 1:
                page_urls.append(article_site_url)
            else:
                page_urls.append("https://tympanus.net/codrops/category/playground/page/{i}/")
            pass

        for i, p in enumerate(page_urls):
            await page.goto(p, timeout= 90000)
            firstdiv = await page.query_selector(".ct-container")
            seconddiv = await firstdiv.query_selector(".ct-content")
            thirddiv = await seconddiv.query_selector(".ct-inner")
            fourthdiv = await thirddiv.query_selector(".ct-main-archive")
            fifthdiv = await fourthdiv.query_selector(".ct-archive")
            try:
                await pageData(fifthdiv)
            except:
                print("Skipping the page due to timeout!")
                pass
            
            print("All webpages on page {i} are scrapped.")
            pass
        pass
    

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(article_site_url, timeout= 120000)

        firstdiv = await page.query_selector(".ct-container")
        seconddiv = await firstdiv.query_selector(".ct-content")
        thirddiv = await seconddiv.query_selector(".ct-inner")
        fourthdiv = await thirddiv.query_selector(".ct-main-archive")
        rootele = await fourthdiv.query_selector(".ct-archive")

        if(flag):
            print("Scrapping the webpages on Page 1 !")
            try:
                await pageData(rootele)
            except:
                print("Skipping the webpage due to timeout!")
                pass
        else:
            print("Scrapping the webpages on all pages !")
            await allPageData(rootele,page)

    pass

async def getTop6(file):
    df = pd.read_csv(file)

    unique_urls = df['url'].unique()

    finaldf = pd.DataFrame(columns=df.columns)

    for url in unique_urls:
        toadd = df[df['url'] == url].sort_values('value',ascending = False)
        toadd = toadd.head(6)
        finaldf = pd.concat([finaldf, toadd], ignore_index=True)
        pass

    finaldf.to_csv('scrapped_data/final.csv',index=False)
    # finaldf.to_csv('scrapped_data/final.csv', index=False, mode='a')
    pass

if __name__ == "__main__":
    site_url = "https://tympanus.net/codrops/category/playground/page/19/"
    csv_file = 'scrapped_data/data.csv'

    # asyncio.run(scrape_headings('https://tympanus.net/Development/ImageTilesMenu/'))
    asyncio.run(article_reading(site_url, csv_file))
    # asyncio.run(getTop6(csv_file))
    pass