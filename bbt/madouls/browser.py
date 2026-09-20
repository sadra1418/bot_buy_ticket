from playwright.async_api import async_playwright
import asyncio
from capcha_hack import capcha_hack
from web import Web
from base64 import b64encode




async def main(data_of_train ,person_data ):

        
        
    ticket_is_buyed = False
    select = False
    


# ____________________start browser__________________________ #

    web_object = Web()
    await web_object.start()
# ____________________start browser__________________________ #


# ______________________main page____________________________ #

    tab = await web_object.main_page_desin(data_of_train)
    
# ______________________main page____________________________ #



# ___________________select the ticket_______________________ # 

    while not select:
        try:
            list_selectors = [
                '[class="a-card available-card mb-3 md:mb-4 cards-flip-item last:mb-0"]' ,
                '[class="text-secondary-400"]' ,
                '[class="text-5 md:text-6 font-bold"]',
                '[class="mr-3 text-3"]',
                '[class="btn is-md is-solid-secondary font-medium my-1 text-3 leading-tight min-w-[9rem]"]',
            ]

            all_train_list = await web_object.list_ticket(tab ,list_selectors)
            select = await web_object.select_ticket(tab ,all_train_list ,data_of_train)

        except Exception as e:
            print(e)
            await asyncio.sleep(10)
            await tab.reload(wait_until='commit')

# ___________________select the ticket_______________________ # 
    




# _______________________insert data of person___________________________ #
    
    await web_object.insert_text_of_person(person_data['name'],'[name="namePersian"]' ,tab)
    await web_object.insert_text_of_person(person_data['lastNamePersian'],'[name="lastNamePersian"]' ,tab)
    await web_object.insert_text_of_person(person_data["nationalCode"],'[name="nationalCode"]' ,tab)

    await tab.wait_for_selector('[class="flex items-center self-stretch"]')
    await tab.wait_for_timeout(1200)
    tollbar_l = await  web_object.list_of_locator(tab ,'[class="flex items-center self-stretch"]')
    
    

    list_of_selector = [f'[data-value="{person_data['type']}"]' ,f'[data-value="{person_data['day']}"]' ,f'[data-value="{person_data['month']}"]' ,f'[data-value="{person_data['year']}"]' ,'[class="block px-4 py-3"]']


    for number in range(len(tollbar_l) -1) :
        await tollbar_l[number].click()

        if number == 4 :
            fft = False
            await tab.wait_for_timeout(1200)
            food = tab.locator(list_of_selector[number])
            list_of_food = await food.all()

            for i in list_of_food:
                food_name = await i.inner_text()
                l_fn = food_name.split()
                if person_data['favourite_food'] in l_fn :
                    await i.click()
                    fft=True
                    break
            if not fft :
                await list_of_food[0].click()
            


        else:
            await tab.click(list_of_selector[number])


    await tab.click('[class="a-checkbox__bullet is-checkbox"]')
    await web_object.insert_text_of_person(f'{person_data['phonenumber']}','[name="contact-phone"]' ,tab)

    await tab.click('[type="submit"]')

# _______________________insert data of person___________________________ #


# _______________________capcha onlock___________________________ #

    while not ticket_is_buyed :

        try :
            capcha_code = await capcha_hack(await tab.get_attribute('[alt="کد امنیتی"]' , name='src'),'thise code is 5 charakter(4 number and 1 lowercase letters)   ##Pay very close attention to the details##')
            print(capcha_code)
            await web_object.insert_text_of_person(capcha_code,'[placeholder="متن تصویر"]' ,tab)
            await tab.click('[class="btn is-md is-solid-primary is-block !btn-secondary-lg-normal"]')

            await tab.wait_for_selector('[class="a-alert__content text-body-md"]',timeout=3000)
            await tab.click('[class="btn is-md is-solid-primary w-full !btn-secondary-lg-normal"]')
            ticket_is_buyed = True
            break

        except :
            continue

# _______________________capcha onlock___________________________ #



# _______________________pay page___________________________ #

    await web_object.insert_text_of_person('d','[title="شماره کارت"]' ,tab)
    await web_object.insert_text_of_person('d','[name="Cvv2"]' ,tab)
    await web_object.insert_text_of_person('d','[placeholder="ماه"]' ,tab)
    await web_object.insert_text_of_person('d','[placeholder="سال"]' ,tab)

    selector = await tab.query_selector('[id="imgc1"]')
    image_url = b64encode(await selector.screenshot(type='png')).decode('utf-8')
    capcha_code = await capcha_hack(f'data:image/png;base64,{image_url}','thise code is 5 charakter')
    await web_object.insert_text_of_person(capcha_code,'[id="Captcha"]' ,tab)


    await tab.click('[class="request-dynamicPass"]') # رمز پویا
    await web_object.insert_text_of_person('s', '[class="effect-8 border-0 float-right inputbox keypad pin TS text-right p-0 col-md-12"]' ,tab) # رمز پویا


    await tab.click('[type="checkbox"]')
    await tab.click('[type="submit"]')

# _______________________pay page___________________________ #

    await tab.wait_for_timeout(10000)
    await tab.screenshot(type='png',path='ticket.png')

        

    
        
    await asyncio.Future()
    
    
person_data = {'name':'محمد صدرا','lastNamePersian':'وزیری' ,"nationalCode":'0970469071' ,'year':'1390' ,'month':'11' ,'day':'4' , 'phonenumber':'09113677164' ,'type':'male' ,'favourite_food':'چلوجوجه'}
data_of_train = {'origin':'AZD' , 'destination':'THR' ,'type':'male' ,'date':'1405-07-01' ,'buss':True ,'the_max_price':3000000 , 'the_max_time':2200 , 'the_min_time':0000}

asyncio.run(main( data_of_train  ,person_data=person_data  ))





