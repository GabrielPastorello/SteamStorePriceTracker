import bs4
import requests
import smtplib
import time

def steamPrice(productUrl):
    res = requests.get(productUrl, headers=headers, cookies=cookies)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elems = soup.select('#game_area_purchase > div.game_area_purchase_game_wrapper > div > div.game_purchase_action > div > div.game_purchase_price.price')
    if len(elems) == 0:
            elems = soup.select('#game_area_purchase > div:nth-child(1) > div > div.game_purchase_action > div > div.discount_block.game_purchase_discount > div.discount_prices > div.discount_final_price')
            if len(elems) == 0:
                elems = soup.select('#game_area_purchase > div.game_area_purchase_game_wrapper > div > div.game_purchase_action > div > div.discount_block.game_purchase_discount > div.discount_prices > div.discount_final_price')
    price_str = elems[0].text.strip()
    price_str = price_str.replace(',', '.')
    price = float(price_str[2:]) # Depending on your currency symbol you might have to change the interval here
    return price

def gameTitle(productUrl):
    res = requests.get(productUrl, headers=headers)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elems = soup.select('body > div.responsive_page_frame.with_header > div.responsive_page_content > div.responsive_page_template_content > div.game_page_background.game > div.page_content_ctn > div.page_title_area.game_title_area.page_content > div.apphub_HomeHeaderContent > div > div.apphub_AppName')
    if len(elems) == 0:
        elems = soup.select('body > div.responsive_page_frame.with_header > div.responsive_page_content > div.responsive_page_template_content > div.game_page_background.game > div.page_content_ctn > div.page_title_area.game_title_area.page_content > div.apphub_HomeHeaderContent > div > div.apphub_AppName')
    title = elems[0].text.strip()
    return title
    
def sendEmail(price, productUrl):
    title = gameTitle(productUrl)
    conn = smtplib.SMTP('smtp.gmail.com', 587) # If your email is from gmail
    conn.ehlo() 
    conn.starttls() 
    conn.login('ENTER YOUR EMAIL ADDRESS HERE', 'ENTER YOUR PASSWORD HERE') # Email and password
    from_ = 'ENTER YOUR EMAIL ADDRESS HERE'
    to_ = 'ENTER YOUR EMAIL ADDRESS HERE (AGAIN)'
    subject = '{} below the stipulated price!'.format(title)
    body = '{} is ${} at the moment.\nCheck it out in: {}\n\n-Steam Store Price Bot'.format(title, price, productUrl) # Remember to change the currency symbol if needed
    msg = 'Subject: {}\n\n{}'.format(subject, body)
    conn.sendmail(to_, from_, msg.encode('utf-8'))
    print('Email has been sent!')
    conn.quit()

def checkPrice(games):
    for game in games:
        if game['email'] != True:
            price = steamPrice(game['url'])
            if price < game['price']:
                sendEmail(price, game['url'])
                game['email'] = True

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}
cookies = {'birthtime': '568022401', 'mature_content': '1' }

# Games:
# Here you can add as many game URL's as you want, here are just some examples
univSandbox = 'https://store.steampowered.com/app/230290/Universe_Sandbox/'
grimFand = 'https://store.steampowered.com/app/316790/Grim_Fandango_Remastered/'
SRGat = 'https://store.steampowered.com/app/301910/Saints_Row_Gat_out_of_Hell/'
FC4 = 'https://store.steampowered.com/app/298110/Far_Cry_4/'
FCPrimal = 'https://store.steampowered.com/app/371660/Far_Cry_Primal/'
WD2 = 'https://store.steampowered.com/app/447040/Watch_Dogs_2/'
ACOrigins = 'https://store.steampowered.com/app/582160/Assassins_Creed_Origins/'
GTASA = 'https://store.steampowered.com/app/12120/Grand_Theft_Auto_San_Andreas/'
ShadowW2 = 'https://store.steampowered.com/app/324800/Shadow_Warrior_2/'
TCR6 = 'https://store.steampowered.com/app/359550/Tom_Clancys_Rainbow_Six_Siege/'
MCX = 'https://store.steampowered.com/app/307780/Mortal_Kombat_X/'
CODIW = 'https://store.steampowered.com/app/292730/Call_of_Duty_Infinite_Warfare/'
madMax = 'https://store.steampowered.com/app/234140/Mad_Max/'
CODG = 'https://store.steampowered.com/app/209160/Call_of_Duty_Ghosts/'


# Remember to also add any new game here with the price of your choice
games = [{'url': univSandbox, 'price': 14, 'email': False}, # 'price': maximum price for the bot to send the email
         {'url': grimFand, 'price': 7, 'email': False},
         {'url': SRGat, 'price': 5, 'email': False},
         {'url': FC4, 'price': 20, 'email': False},
         {'url': FCPrimal, 'price': 20, 'email': False},
         {'url': WD2, 'price': 20, 'email': False},
         {'url': ACOrigins, 'price': 40, 'email': False},
         {'url': GTASA, 'price': 6, 'email': False},
         {'url': ShadowW2, 'price': 20, 'email': False},
         {'url': TCR6, 'price': 8, 'email': False},
         {'url': MCX, 'price': 10, 'email': False},
         {'url': CODIW, 'price': 4, 'email': False},
         {'url': madMax, 'price': 8, 'email': False},
         {'url': legoB2, 'price': 7, 'email': False},
         {'url': CODG, 'price': 20, 'email': False}]

while(True):

    checkPrice(games)
    time.sleep(3600) # Here is the time between each run; right now is at 1 hour (3600s)
    
