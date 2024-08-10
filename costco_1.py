import asyncio
from pyppeteer import launch
from datetime import datetime

async def scrape_costco(model_number):
    model_url = f"https://www.costco.com/CatalogSearch?dept=All&keyword={model_number}"
    print(model_url)

    browser = await launch(headless=True)
    page = await browser.newPage()

    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    try:
        await page.goto(model_url, {'waitUntil': 'networkidle0'})
        
        # Get the page content
        content = await page.content()

        # Save the content to a file
        with open('costco_source.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Page source saved to costco_source.html")

        return content

    except Exception as e:
        print(f"Error fetching the page: {e}")
        return None

    finally:
        await browser.close()

async def main():
    model_number = "GTW485ASWWB"
    source = await scrape_costco(model_number)
    if not source:
        print("Failed to fetch the page source.")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())