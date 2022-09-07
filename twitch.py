from playwright.sync_api import sync_playwright
from datetime import datetime
import csv

with sync_playwright() as playwright:
    base_url = "https://www.twitch.tv"
    
    chromium = playwright.chromium
    # chromium = playwright.firefox
    browser = chromium.launch(headless = False)
    page = browser.new_page()
    page.goto(f'{base_url}/directory?sort=VIEWER_COUNT')
    categories = page.locator('a[data-a-target="tw-box-art-card-link"]')
    categories.last.wait_for()
    count_categories = categories.count()
    for c in range(count_categories):
        link = categories.nth(c).get_attribute('href')
        link = f'{base_url}{link}?sort=VIEWER_COUNT'
        page.goto(link)
        section = page.locator('div[data-target="directory-container"]')
        channels = section.locator('article')
        channels.last.wait_for()
        count_channels = channels.count()
        for i in range(count_channels):
            channel_info = channels.nth(i)
            channel_card = channel_info.locator('a[data-test-selector="TitleAndChannel"]')
            channel_link = channel_card.get_attribute('href')
            live_title = channel_card.locator('h3').text_content()
            channel_name = channel_card.locator('p').text_content()
            spectators = channel_info.locator('div[class*="ScMediaCardStatWrapper"]').text_content()
            
            with open('biTwitch.json', 'a+') as csvfile:
                headers = ['nomeCanal', 'tituloLive', 'linkCanal', 'qtdeEspectadores', 'categoria', 'dataCadastro']
                file_writer = csv.DictWriter(csvfile, delimiter=';')
                file_writer.writeheader()
                file_writer.writerow(
                    {
                        'nomeCanal': channel_name,
                        'tituloLive': live_title,
                        'linkCanal': channel_link,
                        'qtdeEspectadores': spectators,
                        'categoria': '',
                        'dataCadastro': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                    }
                )
                
            ...
        page.goto(f'{base_url}/directory?sort=VIEWER_COUNT')
        ...