#!/usr/bin/env python3
import os
import typing
import asyncio
import json
import logging
import random
from playwright.async_api import Playwright, async_playwright, expect
import re

# Configure logging to display messages to the terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])


# load cookies if it exists
async def load_cookies(context, file_path):
    with open(file_path, 'r') as f:
        cookies = json.load(f)
        await context.add_cookies(cookies)


async def like():
    async with async_playwright() as p:
        # browser configs
        browser = await p.firefox.launch(headless=False)
        context = await browser.new_context( )

        await load_cookies(context, "cookies.json")
        logging.info("Session cookies loaded succesfully")

        page = await context.new_page()
        page.set_default_timeout(55000)
        await page.goto('tweetlink') #any X post link of choice
        logging.info("Session continued")
        await page.wait_for_load_state()
        await asyncio.sleep(random.randint(5, 8))

        likeTweet = await page.query_selector_all('button[data-testid="like"]')
        unlikeTweet = await page.query_selector_all('button[data-testid="unlike"]')
        # unretweet = await page.query_selector_all('button[data-testid="unretweet"]')

        try:
            if unlikeTweet:
                # click to go back if post already liked
                goBack = page.get_by_test_id('app-bar-back')
                goBackPos = await goBack.bounding_box()
                await page.mouse.move(goBackPos["x"] + goBackPos["width"] / 2, goBackPos["y"] + goBackPos["height"] / 2)
                await page.mouse.down()
                await page.mouse.up()
                logging.info("Back to home page")
                await asyncio.sleep(random.randint(4, 6))
                # await page.wait_for_load_state()

            elif likeTweet:
                # like
                await likeTweet[0].click()
                logging.info("Liking post successful")
                await asyncio.sleep(random.randint(4, 6))

                page.on("dialog", lambda dialog: dialog.accept())

        except Exception as e:
            logging.error("Post already Liked check logs")
            logging.error(f"Failed reason {e}")


    await context.close()

asyncio.run(like())
