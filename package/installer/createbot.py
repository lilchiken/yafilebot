from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from createdb import create_connection, return_chromedriver, execute_query, return_bot_api, return_bot_hash, return_bot_name
import secrets
import string
from telethon import TelegramClient, events

def reg_tele_api():
    def unique_pass(length):
        letters_and_digits = string.ascii_letters + string.digits
        smthng = ''.join(secrets.choice(letters_and_digits) for i in range(length))
        return smthng

    path = '/Users/ilia/Documents/GitHub/yafilebot/package/chromedriver'
    # path = return_chromedriver(create_connection())[0] # - Перед деплоем убрать верхнюю строчку а эту раскомментить
    driver = webdriver.Chrome(executable_path=path)
    driver.get(url='https://my.telegram.org/apps')
    # Сделать login_phone в PyQT
    driver.find_element(by=By.ID, value='my_login_phone').send_keys(f'+79119886438')
    driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/div/div/div/div/div[2]/div/form[1]/div[2]/button').click()
    password = input('Введите TG-код ') # Сделать в PyQT
    driver.find_element(by=By.ID, value='my_password').send_keys(f'{password}')
    driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/div/div/div/div/div[2]/div/form[2]/div[4]/button').click()
    del password
    time.sleep(3)
    try:
        driver.find_element(by=By.NAME, value='app_url').send_keys(unique_pass(16))
        time.sleep(3)
        driver.find_element(by=By.ID, value='app_title').send_keys(unique_pass(32))
        time.sleep(3)
        driver.find_element(by=By.NAME, value='app_shortname').send_keys(unique_pass(32))
        time.sleep(3)
        driver.find_element(by=By.NAME, value='app_desc').send_keys('Создано при помощи YaFile. tg - @spbdqs . mail - andryuhin2@yandex.ru')
        time.sleep(3)
        driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/div/div/form/div[6]/div/button').click()
        time.sleep(3)
        api_id = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/div/div/form/div[1]/div[1]/span/strong').text
        print(api_id)
        time.sleep(3)
        api_hash = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/div/div/form/div[2]/div[1]/span').text
        print(api_hash)
    except:
        api_id = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/div/div/form/div[1]/div[1]/span/strong').text
        print(api_id)
        time.sleep(3)
        api_hash = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/div/div/form/div[2]/div[1]/span').text
        print(api_hash)

    execute_query(create_connection(), f"""
    INSERT INTO
      users_keys(name, value)
    VALUES
      ('phone', '{...}'),
      ('account_password', '{...}')
    """)

    execute_query(create_connection(), f"""
    INSERT INTO
      users_logs(name, value)
    VALUES
      ('api_id', '{api_id}'),
      ('api_hash', '{api_hash}'),
      ('bot_password', '{unique_pass(6)}'),
      ('bot_name', f'Yafile_{unique_pass(4)}')
    """)

    driver.close()

def create_bot():
    with TelegramClient('YaFile', return_bot_api(create_connection())[0], return_bot_hash(create_connection())[0]) as client:
        async def main():
            BF = '@BotFather'
            await client.send_message(BF, '/start')
            await client.send_message(BF, '/newbot')
            await client.send_message(BF, f'{return_bot_name(create_connection())[0]}')
            await client.send_message(BF, f'{return_bot_name(create_connection())[0]}_bot')
            time.sleep(3)
            b = await client.get_messages(BF, limit=1)
            b = f"""{b}"""
            bot_token = b.split('\n')[4]
            time.sleep(3)
            await client.send_message(BF, '/setdescription')
            await client.send_message(BF, f'{return_bot_name(create_connection())[0]}_bot')
            await client.send_message(BF, 'Создано при помощи YaFile . tg - @spbdqs . mail - andryuhin2@yandex.ru')
            execute_query(create_connection(), f"""
                        INSERT INTO
                          users_logs(name, value)
                        VALUES
                          ('bot_token', {bot_token})
                        """)

        client.loop.run_until_complete(main())

        client.run_until_disconnected()