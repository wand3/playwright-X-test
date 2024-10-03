#!/usr/bin/env python3

import os
import typing
import asyncio
import json
import logging
import random
from playwright.async_api import Playwright, async_playwright, expect
import time
import re

# Configure logging to display messages to the terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])



async def save_cookies(context, file_path='/'):
    cookies = await context.cookies()
    with open(file_path, 'w') as f:
        json.dump(cookies, f)
    await save_cookies(context, 'cookie.json')


# handle and dismiss dialogs
async def handle_dialog(dialog):
    print(dialog.message)
    await dialog.dismiss()


async def login_save_cookies(page, context, email_or_username, password):
    """
    logs in with cookies stored in file
    :param username:
    :param email_or_username:
    :param context:
    :param page:
    :param password:
    :return:
    """

    # navigate to login page to check if user already logged in
    await page.goto('https://x.com/')
    # await page.wait_for_load_state()
    login_user = await page.get_by_test_id("loginButton").is_visible()

    if login_user:
        await page.get_by_test_id("loginButton").click()
        await page.locator("input[name='text']").click()
        await asyncio.sleep(random.randint(2, 5))
        await page.locator("input[name='text']").fill(email_or_username)

        await page.get_by_role("button", name="Next").click()
        await page.get_by_label("Password", exact=True).click()
        await page.get_by_label("Password", exact=True).fill(password)
        # close blocking for login
        await page.get_by_test_id("xMigrationBottomBar").click()

        await page.get_by_test_id("controlView").get_by_test_id("LoginForm_Login_Button").click()


        # Wait for login to complete
        await asyncio.sleep(10)
        # save cookies for the user
        await save_cookies(context, file_path)
        return True
    else:
        logging.error(f"Login FAILED for {email_or_username}")
        return False


async def login():
    async with async_playwright() as p:
        # browser configs
        browser = await p.firefox.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": int, "height": int}  # customizations for viewport size
        )

        page = await context.new_page()
        page.set_default_timeout(5000)

        email_or_username = input("Enter username or email: ")


        password = input("Enter password: ")

        # take count of number of cookies files in folder and user its len index to suffix cookies-(suffix).json
        if email_or_username and password and username:
            value = await login_save_cookies(page, context, email_or_username, password)
            if value is False:
                logging.error("Saving cookies failed")
            if value is True:
                logging.info('OPERATION SUCCESSFUL!')
                await asyncio.sleep(random.randint(2, 5))
        await context.close()

asyncio.run(login())
