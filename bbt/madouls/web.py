from playwright.async_api import async_playwright


class Web ():


    async def __init__(self):
        self.pl = await async_playwright().start()
        self.browser = await self.pl.chromium.launch(headless=False)
        self.contex = await self.browser.new_context()

    async def insert_text_of_person(self ,text ,selector ,tab):
                
                await tab.click(selector)
                await tab.keyboard.type(text) 


    async def main_page_desin(self ,data_of_train):
        tab = await self.contex.new_page()

        await tab.goto(f"https://www.alibaba.ir/train/{data_of_train['origin']}-{data_of_train['destination']}?adult=1&child=0&infant=0&ticketType={data_of_train['type']}&isExclusive=false&departing={data_of_train['date']}&sort=price_asc",wait_until='commit' , timeout=20000)
        await tab.wait_for_selector('[class="a-card available-card mb-3 md:mb-4 cards-flip-item last:mb-0"]')
        await tab.wait_for_timeout(5000)
        
        await tab.click('[class="btn is-md is-raw py-2 px-3 text-4 relative hover:bg-grays-100"]')
        await tab.click('[class="btn is-md is-link"]')
        await self.insert_text_of_person('9113677164','[inputmode="text"]', tab=tab)
        await self.insert_text_of_person('eNt?,GTDVS77','[type="password"]', tab=tab)
        await tab.click('[type="submit"]')


    