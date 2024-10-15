import Base
import logging
from bs4 import BeautifulSoup
import random
import asyncio

# Configure logging to display messages to the terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])


class Scroll(Base):
    """
        scroll through posts on a page
    """
    def __init__(self, page):
        self.page = page

    # beautiful soup to get each post link from a scroll
    async def post_hrefs(self, all_divs: list):
        all_hrefs = []
        for div in all_divs:
            anchor_tag = div.find('a')
            logging.info("Extracting link from anchor tag")
            if anchor_tag:
                href = anchor_tag.get('href')
                if href:
                    all_hrefs.append(href)
        return all_hrefs

    async def get_urls(self, all_links=None):
        post_urls = []
        if all_links is not None:
            links_len = len(all_links)
            for i in range(links_len):
                link = 'https://x.com' + all_links[i]
                logging.info(f"Link {i} {link}")
                post_urls.append(link)
            return post_urls

    async def execute(self):
        # get height of page
        last_height = await self.page.evaluate("document.body.scrollHeight")
        # counter for number of pages to scroll
        # logging.info(f"Home page random scroll for {home_scroll} times")

        # scroll each page to bottom
        await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight);")

        await self.page.wait_for_load_state()
        new_height = await self.page.evaluate("document.body.scrollHeight")
        last_height = new_height
        await asyncio.sleep(random.randint(2, 5))

        # Get the page content
        html_code = await self.page.content()

        # get all tweets or articles on each page scroll
        soup = BeautifulSoup(html_code, 'html.parser')

        # Find all divs with the specified class
        all_divs = soup.find_all('div', class_='css-175oi2r r-18u37iz r-1q142lx')
        logging.info(f"divs on scroll: {len(all_divs)}")

        # Extract href attributes from anchor tags within each div
        all_links = await self.post_hrefs(all_divs)
        # Print all extracted hrefs
        print(len(all_links))
        # visit each extracted link one after the other open and interact in new context
        each_post = await self.get_urls(all_links)
        each_post_len = len(each_post)
        return each_post

