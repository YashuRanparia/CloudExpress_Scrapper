import asyncio

import pandas as pd
from playwright.async_api import async_playwright

from sc2 import scrape_data
from scrapper import extract_and_save_style_data


async def article_reading(article_site_url, csv_file):
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page() 
        await page.goto(article_site_url, timeout= 90000)

        firstdiv = await page.query_selector(".ct-container")
        seconddiv = await firstdiv.query_selector(".ct-content")
        thirddiv = await seconddiv.query_selector(".ct-inner")
        fourthdiv = await thirddiv.query_selector(".ct-main-archive")
        fifthdiv = await fourthdiv.query_selector(".ct-archive")

        container_div = await fifthdiv.query_selector(".ct-archive-container")

        articles = await container_div.query_selector_all("article")

        article_links = []
        for article in articles:
            thumb_div = await article.query_selector(".ct-latest-thumb-archive")
            anchor_tag = await thumb_div.query_selector("a")
            href = await anchor_tag.evaluate("(element) => element.href")
            article_links.append(href)
        
        # print(article_links)

        final_urls = []

        for i, article in enumerate(article_links):
            page = await browser.new_page()
            await page.goto(article, timeout=60000)

            f1 = await page.query_selector(".ct-container")
            f2 = await f1.query_selector(".ct-content")
            f3 = await f2.query_selector(".ct-inner")
            f4 = await f3.query_selector(".ct-main-post")
            f5 = await f4.query_selector(".ct-post")
            art = await f5.query_selector("article")
            postcontent = await art.query_selector(".ct-post-content")
            postcontentimg = await postcontent.query_selector(".ct-post-featured-img")

            post_anchor_tag = await postcontentimg.query_selector("a")
            post_href = await post_anchor_tag.evaluate("(element) => element.href")
            final_urls.append(post_href)

            # await asyncio.run(scrape_headings(post_href, f'articledata_{i}.txt'))
            try:
                await scrape_data(post_href, csv_file)
            except:
                print('Skipping this article due to timeout!')
                pass
            pass

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
    pass

if __name__ == "__main__":
    site_url = "https://tympanus.net/codrops/category/playground/"
    csv_file = 'scrapped_data/data.csv'

    # asyncio.run(scrape_headings('https://tympanus.net/Development/ImageTilesMenu/'))
    asyncio.run(article_reading(site_url, csv_file))
    asyncio.run(getTop6(csv_file))
    pass