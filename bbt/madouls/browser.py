from playwright.async_api import async_playwright
import asyncio
from .capcha_hack import capcha_hack
from base64 import b64encode




async def main(data_of_train , the_max_price ,the_max_time ,the_min_time ,person_data ,favourite_food):

    def time_to_num(time):
        """input = 22:10. output=2210"""

        l_t = []
        for i in time:
            if i != ':' and i != ',':
                l_t.append(i)
        
        return int(''.join(l_t))

    async def insert_text_of_person(text , selector):
        

        await tab.click(selector)
        await tab.keyboard.type(text)
        
        
    ticket_is_buyed = False
    select = False
    


# ____________________start browser__________________________ #

    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    tab = await context.new_page()

# ____________________start browser__________________________ #


# ______________________main page____________________________ #

    await tab.goto(f'https://www.alibaba.ir/train/{origin}-{destination}?adult=1&child=0&infant=0&ticketType={type}&isExclusive=false&departing={date}&sort=price_asc',wait_until='commit' , timeout=20000)
    await tab.wait_for_selector('[class="a-card available-card mb-3 md:mb-4 cards-flip-item last:mb-0"]')
    await tab.wait_for_timeout(5000)

    await tab.click('[class="btn is-md is-raw py-2 px-3 text-4 relative hover:bg-grays-100"]')
    await tab.click('[class="btn is-md is-link"]')
    await insert_text_of_person('9113677164','[inputmode="text"]')
    await insert_text_of_person('eNt?,GTDVS77','[type="password"]')
    await tab.click('[type="submit"]')

# ______________________main page____________________________ #



# ___________________select the ticket_______________________ # 

    while not select:
        try:
            all_train_list = []

            trains =  tab.locator('[class="a-card available-card mb-3 md:mb-4 cards-flip-item last:mb-0"]')
            price_t = tab.locator('[class="text-secondary-400"]')
            times_of_start_t = tab.locator('[class="text-5 md:text-6 font-bold"]')
            type_of_train_t = tab.locator('[class="mr-3 text-3"]')
            button_t = tab.locator('[class="btn is-md is-solid-secondary font-medium my-1 text-3 leading-tight min-w-[9rem]"]')

            
            list_of_train = await trains.all()
            prices = await price_t.all()
            times_of_start = await times_of_start_t.all()
            type_of_train = await type_of_train_t.all()
            button = await button_t.all()

            for number in range(await trains.count()) :
                train = {
                    'id':number,
                    'train':list_of_train[number],
                    'price':prices[number],
                    'times_of_start':times_of_start[number*2],
                    'type_of_train':type_of_train[number],
                    'button':button[number]
                }
                all_train_list.append(train)

            for ticket in all_train_list :

                times_of_start_train = time_to_num(await ticket['times_of_start'].inner_text())
                price_of_train = time_to_num(await ticket['price'].inner_text())
                

                if the_max_time >= times_of_start_train >= the_min_time and the_max_price >= price_of_train :
                    if buss :
                        await ticket['button'].click()
                        select=True
                        break

                    else :
                        b_t_f = await ticket['type_of_train'].inner_text()
                        t_t_b = b_t_f.split()

                        if 'اتوبوسي' in t_t_b:
                            print(f'oh this ticket is bad price={price_of_train}. timeof start thise train = {times_of_start_train}')

                        else:
                            await ticket['button'].click()
                            select=True
                            break
                            
                else:
                    print(f'oh this ticket is bad price={price_of_train}. timeof start thise train = {times_of_start_train}')

            if not select:
                print('_____________')
                await asyncio.sleep(10)
                await tab.reload(wait_until='commit')
            else : 
                break

        except Exception as e:
            print(e)
            await asyncio.sleep(10)
            await tab.reload(wait_until='commit')

# ___________________select the ticket_______________________ # 
    




# _______________________insert data of person___________________________ #
    
    await insert_text_of_person(person_data['name'],'[name="namePersian"]')
    await insert_text_of_person(person_data['lastNamePersian'],'[name="lastNamePersian"]')
    await insert_text_of_person(person_data["nationalCode"],'[name="nationalCode"]')

    await tab.wait_for_selector('[class="flex items-center self-stretch"]')
    await tab.wait_for_timeout(1200)
    tollbar_t = tab.locator('[class="flex items-center self-stretch"]')
    tollbar_l = await tollbar_t.all()
    

    list_of_selector = [f'[data-value="{type}"]' ,f'[data-value="{person_data['day']}"]' ,f'[data-value="{person_data['month']}"]' ,f'[data-value="{person_data['year']}"]' ,'[class="block px-4 py-3"]']


    for number in range(await tollbar_t.count()-1) :
        await tollbar_l[number].click()

        if number == 4 :
            fft = False
            await tab.wait_for_timeout(1200)
            food = tab.locator(list_of_selector[number])
            list_of_food = await food.all()

            for i in list_of_food:
                food_name = await i.inner_text()
                l_fn = food_name.split()
                if favourite_food in l_fn :
                    await i.click()
                    fft=True
                    break
            if not fft :
                await list_of_food[0].click()
            


        else:
            await tab.click(list_of_selector[number])


    await tab.click('[class="a-checkbox__bullet is-checkbox"]')
    await insert_text_of_person(f'{person_data['phonenumber']}','[name="contact-phone"]')

    await tab.click('[type="submit"]')

# _______________________insert data of person___________________________ #


# _______________________capcha onlock___________________________ #

    while not ticket_is_buyed :

        try :
            capcha_code = await capcha_hack(await tab.get_attribute('[alt="کد امنیتی"]' , name='src'),'thise code is 5 charakter(4 number and 1 lowercase letters)   ##Pay very close attention to the details##')
            print(capcha_code)
            await insert_text_of_person(capcha_code,'[placeholder="متن تصویر"]')
            await tab.click('[class="btn is-md is-solid-primary is-block !btn-secondary-lg-normal"]')

            await tab.wait_for_selector('[class="a-alert__content text-body-md"]',timeout=3000)
            await tab.click('[class="btn is-md is-solid-primary w-full !btn-secondary-lg-normal"]')
            ticket_is_buyed = True
            break

        except :
            continue

# _______________________capcha onlock___________________________ #



# _______________________pay page___________________________ #

    await insert_text_of_person('d','[title="شماره کارت"]')
    await insert_text_of_person('d','[name="Cvv2"]')
    await insert_text_of_person('d','[placeholder="ماه"]')
    await insert_text_of_person('d','[placeholder="سال"]')

    selector = await tab.query_selector('[id="imgc1"]')
    image_url = b64encode(await selector.screenshot(type='png')).decode('utf-8')
    capcha_code = await capcha_hack(f'data:image/png;base64,{image_url}','thise code is 5 charakter')
    await insert_text_of_person(capcha_code,'[id="Captcha"]')


    await tab.click('[class="request-dynamicPass"]') # رمز پویا
    await insert_text_of_person('s', '[class="effect-8 border-0 float-right inputbox keypad pin TS text-right p-0 col-md-12"]') # رمز پویا


    await tab.click('[type="checkbox"]')
    await tab.click('[type="submit"]')

# _______________________pay page___________________________ #

    await tab.wait_for_timeout(10000)
    await tab.screenshot(type='png',path='ticket.png')

        

    
        
    await asyncio.Future()
    
    
person_data = {'name':'محمد صدرا','lastNamePersian':'وزیری' ,"nationalCode":'0970469071' ,'year':'1390' ,'month':'11' ,'day':'4' , 'phonenumber':'09113677164'}


asyncio.run(main(origin='MHD' , destination='THR' ,type='male' ,date='1405-07-01' ,buss=False ,the_max_price=3000000 , the_max_time=2200 , the_min_time=0000 ,person_data=person_data ,favourite_food='چلوجوجه'))