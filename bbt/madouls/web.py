from playwright.async_api import async_playwright


class Web ():
    """
    the browser functions 
    """


    def __init__(self):
        """the browser functions """
        pass


    async def start(self):
        self.pl = await async_playwright().start()
        self.browser = await self.pl.chromium.launch(headless=False)
        self.contex = await self.browser.new_context()



#._______________micro-functions_______________#       

    def time_to_num(self ,time):
            """input = 22:10. output=2210"""
    
            l_t = []
            for i in time:
                if i != ':' and i != ',':
                    l_t.append(i)
            
            return int(''.join(l_t))

    async def insert_text_of_person(self ,text ,selector ,tab):
                
        await tab.click(selector)
        await tab.keyboard.type(text) 

    async def list_of_locator(self ,tab ,selector):
        locator_element = tab.locator(selector)
        return(await locator_element.all())

#._______________micro-functions_______________#   


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

        return (tab)


#  ________________select ticket ________________ #



    async def list_ticket(self ,tab ,list_of_selectors:list):
        all_train_list = []
        list_of_list_selectors = []
        number_of_ticket = len(await self.list_of_locator(tab ,list_of_selectors[0]))

        for selector in list_of_selectors :list_of_list_selectors.append(await self.list_of_locator(tab ,selector)) 
        for number in range(number_of_ticket):
            train = {
                        'id':number,
                        'train':list_of_list_selectors[0][number],
                        'price':list_of_list_selectors[1][number],
                        'times_of_start':list_of_list_selectors[2][number*2],
                        'type_of_train':list_of_list_selectors[3][number],
                        'button':list_of_list_selectors[4][number]
                    }
            all_train_list.append(train)
        return (all_train_list)




    async def select_ticket(self ,tab ,all_train_list ,data_of_train):

        
                        
        for ticket in all_train_list :

            times_of_start_train = self.time_to_num(await ticket['times_of_start'].inner_text())
            price_of_train = self.time_to_num(await ticket['price'].inner_text())


            if data_of_train['the_max_time'] >= times_of_start_train >= data_of_train['the_min_time'] and data_of_train['the_max_price'] >= price_of_train :
                if data_of_train['buss'] :
                    await ticket['button'].click()
                    select = True
                    break
            
                else :
                    b_t_f = await ticket['type_of_train'].inner_text()
                    t_t_b = b_t_f.split()
            
                    if 'اتوبوسي' in t_t_b:
                        print(f'oh this buss')
                        select = False
            
                    else:
                        await ticket['button'].click()
                        select = True
                        break
                                        
            else:
                print(f'oh this ticket is bad price={price_of_train}. timeof start thise train = {times_of_start_train}')
                select = False

        return(select)




#  ________________select ticket ________________ #   





