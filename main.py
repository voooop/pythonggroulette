import csv
import os
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime
import re
import time

def main():
    global page
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=250)
        page = browser.new_page()
        logging()
        while True:
            roulette()


def rouletteInformation():
    headers = ['numer gg', 'imię', 'wiek', 'płeć', 'miejscowość', 'opis', 'kiedy wylosowany', 'avatar', 'premium',
               'zweryfikowany']

    html = page.inner_html('div[class=roulette-data]')
    soup = BeautifulSoup(html, 'html.parser')
    description = soup.find('p', {'class': 'statusDescription'}).text
    additional = soup.find('p', {'class': 'aditionalInfo'}).get_text(separator='\n').splitlines()
    name = soup.find_all('p', {'class': 'info'})
    sex = re.findall('^\w+', additional[0])

    numergg = re.findall('[0-9]+', soup.find_all('a', href=True)[1]['href'])[0]
    nickname = "".join(re.findall('[^🏆✅]', name[2].text))
    desc = " ".join([descript.strip() for descript in description.splitlines()])
    age = "".join(re.findall('[0-9]+', additional[0]))
    date = str(datetime.now())
    avatar = soup.find_all('img')[0]['src']

    print('numer gg: ' + numergg)
    print('imie: ' + nickname)
    print('opis: ' + desc)
    print('wiek: ' + age)
    print('płeć: ' + sex[0])
    if len(additional) > 1:
        print('miejscowosc: ' + additional[1])
    else:
        print('miejscowosc: nie podano')
    print('kiedy: ' + date)
    print('avatar: ' + avatar)
    if '🏆' in name[2].text:
        premium = 'TAK'
        print('premium: ' + premium)
    else:
        premium = 'NIE'
        print('premium: ' + premium)
    if '✅' in name[2].text:
        verified = 'TAK'
        print('zweryfikowany: ' + verified)
    else:
        verified = 'NIE'
        print('zweryfikowany: ' + verified)

    print('\n')

    exists = os.path.exists("ggroulette.csv")
    with open("ggroulette.csv", mode="a+", encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

        if not exists:
            writer.writerow(headers)

        row = [numergg, nickname, age, sex[0], additional[1], desc, date, avatar, premium, verified]
        writer.writerow(row)


def logging():
    USERNAME = ""  # set username
    PASSWORD = ""  # set password

    print("Logging to site:")
    try:
        page.goto('https://www.gg.pl/')
        page.click('p[class=fc-button-label]')
        page.locator('a[id=loginModalId]').click()
        frame = page.frame(name='login-iframe')
        frame.fill('input#login_input.form-control', USERNAME)
        frame.fill('input#password.form-control', PASSWORD)
        page.keyboard.press("Enter")
        print("Logged!")
    except:
        print("Something went wrong, please restart the script!")

    page.click('a[class=roulette]')
    page.click('input[value="Opcje wyszukiwania"]')
    # page.click('img[src="/images/sr-avatar-blank-female-80.png"]')  # set females only
    # page.click('img[src="/images/sr-avatar-blank-male-80.png"]') # set males only
    page.locator('div[class=rc-slider-step]').click(position={'x': 18, 'y': 0})  # set range of ages to 18-120
    page.is_visible('input[value="Losuj rozmówcę"]')
    page.click('a[class="roulette active"]')
    page.locator('div[class="roulette-spinner-2 idle"]').wait_for(state='visible')
    page.locator('div[class="state-1 roulette-buttons"]').wait_for(state='visible')
    page.locator('#rouletteData input:has-text("Losuj rozmówcę")').click()


def roulette():
    time.sleep(2)   # TODO: Delete it somehow
    page.locator('div[class="state-2"]').wait_for(state='hidden', timeout=300000)

    if page.is_visible('div[class="state-3 interlocutor"]'):
        rouletteInformation()
        page.locator('input[value="Losuj dalej"]').click()
    elif page.is_visible('div[class="state-1 roulette-buttons"]'):
        page.locator('#rouletteData input:has-text("Losuj rozmówcę")').click()


if __name__ == "__main__":
    main()
