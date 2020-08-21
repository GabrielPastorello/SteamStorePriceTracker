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
    price = float(price_str[3:])
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

while(True):

# Remember to also add any new game here with the price of your choice

    price = steamPrice(univSandbox)
    if price < 14: # Maximum price for the bot to send the email
        sendEmail(price, univSandbox)

    price = steamPrice(grimFand)
    if price < 7: 
        sendEmail(price, grimFand)

    price = steamPrice(SRGat)
    if price < 5:
        sendEmail(price, SRGat)

    price = steamPrice(FC4)
    if price < 20:
        sendEmail(price, FC4)

    price = steamPrice(FCPrimal)
    if price < 20:
        sendEmail(price, FCPrimal)

    price = steamPrice(WD2)
    if price < 20:
        sendEmail(price, WD2)

    price = steamPrice(ACOrigins)
    if price < 40:
        sendEmail(price, ACOrigins)

    price = steamPrice(GTASA)
    if price < 6:
        sendEmail(price, GTASA)

    price = steamPrice(ShadowW2)
    if price < 20:
        sendEmail(price, ShadowW2)

    price = steamPrice(TCR6)
    if price < 8:
        sendEmail(price, TCR6)

    price = steamPrice(MCX)
    if price < 10:
        sendEmail(price, MCX)

    price = steamPrice(CODIW)
    if price < 4:
        sendEmail(price, CODIW)

    price = steamPrice(madMax)
    if price < 8:
        sendEmail(price, madMax)

    price = steamPrice(CODG)
    if price < 20:
        sendEmail(price, CODG)

    time.sleep(3600)
    
