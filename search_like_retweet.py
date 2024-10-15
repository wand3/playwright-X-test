from actions.base import Base
from actions.scroll import Scroll
import logging
import random
import asyncio
from bs4 import BeautifulSoup
# Configure logging to display messages to the terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])


class Search(Base):

    def __init__(self, new, search_keyword):
        self.new = new
        self.search_keyword = search_keyword

    async def search(self):
        search_word = self.search_keyword
        await asyncio.sleep(random.randint(1, 3))
        await self.new.get_by_label("Search and explore").click()
        logging.info('Search button click successful')
        await self.new.wait_for_load_state()
        await asyncio.sleep(random.randint(1, 3))

        await self.new.get_by_test_id("SearchBox_Search_Input").click()

        await self.new.get_by_test_id("SearchBox_Search_Input").fill(search_word)
        logging.info('Search box filled successfully!')
        await self.new.keyboard.press("Enter")

        await self.new.wait_for_load_state()
        await asyncio.sleep(random.randint(1, 4))

    async def reply(self):
        # reply
        await self.new.locator('[data-testid="tweet"]').nth(0).locator(
            '[data-testid="reply"]').click(delay=2000)
        # await new.on("dialog", handle_dialog)

        await self.new.wait_for_load_state()
        await asyncio.sleep(random.randint(1, 3))

        # get reply input box
        replyInput = self.new.get_by_test_id("tweetTextarea_0_label")
        await replyInput.click()
        logging.info('Text area click successful')

        logging.info('Text area hover successful')

        await self.new.mouse.up()
        comment = await self.get_random_comment()
        logging.info('Text area comment selected successful')

        await self.new.keyboard.type(comment, delay=100)
        await asyncio.sleep(random.randint(1, 3))

        # click tweet for reply
        # expect(await new.get_by_test_id("tweetButton")).to_be_visible()
        await self.new.get_by_test_id("tweetButton").click()
        await self.new.wait_for_load_state()
        logging.info("Post reply successful")
        await asyncio.sleep(random.randint(2, 5))

    # go back
    async def go_back(self):
        goBack = self.new.get_by_test_id('app-bar-back')
        goBackPos = await goBack.bounding_box()
        await self.new.mouse.move(goBackPos["x"] + goBackPos["width"] / 2, goBackPos["y"] + goBackPos["height"] / 2)
        await self.new.mouse.down()
        await self.new.mouse.up()
        logging.info("Back to home new")
        await asyncio.sleep(random.randint(4, 6))

    @staticmethod
    async def get_random_comment():
        with open('tch.txt', 'r') as file:
            notes = file.readlines()
            if notes:
                return random.choice(notes).strip()
            else:
                return "No notes found in the file."

    async def execute(self):
        await self.search()
        count = 0
        count_range = random.choice(range(4, 6))
        while count <= count_range:

            # get height of page
            last_height = await self.new.evaluate("document.body.scrollHeight")
            # counter for number of pages to scroll
            logging.info(f"Search page scroll for {count} times")

            # scroll each page to bottom
            await self.new.evaluate("window.scrollTo(0, document.body.scrollHeight);")

            await self.new.wait_for_load_state()
            new_height = await self.new.evaluate("document.body.scrollHeight")
            last_height = new_height
            logging.info(f"Sroll height of this page")

            await asyncio.sleep(random.randint(2, 5))

            # get all tweets or articles on each page scroll
            all_tweets = await self.new.query_selector_all('article')
            logging.info(f"articles on scroll: {len(all_tweets)}")

            for tweet in range(len(all_tweets)):
                all_text = await self.new.locator('[data-testid="tweet"]').nth(tweet).locator('[data-testid="tweetText"]').nth(0).is_visible()
                logging.info(f"Tweet {tweet} found")
                logging.info(all_text)

                if all_text:
                    text = await self.new.locator('[data-testid="tweet"]').nth(tweet).locator('[data-testid="tweetText"]').nth(0).inner_text()
                    logging.info(f'{tweet} - {text}')

                    if self.search_keyword in text:
                        logging.info(f"Tweet {tweet} Valid")

                        await self.new.locator('[data-testid="tweet"]').nth(tweet).locator('[data-testid="tweetText"]').nth(0).scroll_into_view_if_needed()
                        logging.info(f"Tweet {tweet} scroll into view")
                        await asyncio.sleep(random.randint(1, 3))

                        await self.new.locator('[data-testid="tweet"]').nth(tweet).locator('[data-testid="tweetText"]').nth(0).click()
                        logging.info(f"Tweet {tweet} Visited")
                        await self.new.wait_for_load_state()

                        try:
                            # check like at this indent of the raidPost
                            # all_tweets on page
                            logging.info(f'Len of all tweets {len(all_tweets)}')

                            check_like = await self.new.locator('[data-testid="tweet"]').nth(0).locator(
                                '[data-testid="like"]').is_visible()
                            if check_like:
                                await asyncio.sleep(random.randint(1, 3))

                                await self.new.locator('[data-testid="tweet"]').nth(0).locator('[data-testid="like"]').click()
                                logging.info('Shill liked')
                                await self.reply()
                                count += 1
                            logging.info(f'check like {check_like}')

                            check_unlike = await self.new.locator('[data-testid="tweet"]').nth(0).locator('[data-testid="unlike"]').is_visible()
                            if check_unlike:
                                logging.info("Post already liked")
                            logging.info(f'check unlike {check_unlike}')

                            check_retweet = await self.new.locator('[data-testid="tweet"]').nth(0).locator('[data-testid="retweet"]').is_visible()
                            if check_retweet:
                                await self.new.locator('[data-testid="tweet"]').nth(0).locator(
                                    '[data-testid="retweet"]').click(delay=2000)
                                await self.new.wait_for_load_state()
                                retweetConfirm = await self.new.get_by_test_id("retweetConfirm").click()

                                await asyncio.sleep(random.randint(1, 3))
                                # await new.get_by_test_id("sheetDialog").filter(has=new.get_by_test_id("retweetConfirm")).click()

                            logging.info(f'check retweet {check_retweet}')
                            #
                            check_unretweet = await self.new.locator('[data-testid="tweet"]').nth(0).locator(
                                '[data-testid="unretweet"]').is_visible()
                            if check_unretweet:
                                logging.info('Post already retweeted')
                            logging.info(f'check unretweet {check_unretweet}')

                        except Exception as e:
                            logging.error(e)
                            await self.new.evaluate('document.documentElement.click(0, 0)')

                        finally:
                            await asyncio.sleep(random.randint(1, 2))
                            check_like = await self.new.locator('[data-testid="tweet"]').nth(0).locator('[data-testid="like"]').is_visible()

                            if check_like:
                                await asyncio.sleep(random.randint(1, 3))

                                await self.new.locator('[data-testid="tweet"]').nth(0).locator('[data-testid="like"]').click()
                                logging.info('Shill liked')
                                await self.reply()
                                count += 1
                            logging.info(f'check like {check_like}')

                            check_unlike = await self.new.locator('[data-testid="tweet"]').nth(0).locator('[data-testid="unlike"]').is_visible()
                            if check_unlike:
                                logging.info("Post already liked")
                            logging.info(f'check unlike {check_unlike}')

                            check_retweet = await self.new.locator('[data-testid="tweet"]').nth(0).locator('[data-testid="retweet"]').is_visible()
                            if check_retweet:
                                await self.new.locator('[data-testid="tweet"]').nth(0).locator(
                                    '[data-testid="retweet"]').click(delay=2000)
                                await self.new.wait_for_load_state()
                                retweetConfirm = await self.new.get_by_test_id("retweetConfirm").click()

                                await asyncio.sleep(random.randint(1, 3))
                                # await new.get_by_test_id("sheetDialog").filter(has=new.get_by_test_id("retweetConfirm")).click()
                            logging.info(f'check retweet {check_retweet}')
                            logging.info(f'Count {count}')
                            await self.go_back()
                            await self.new.wait_for_load_state()
                else:
                    logging.info('No text')

            # Find all divs with the specified class
            # post_links = await Scroll.post_hrefs(all_divs: list)
