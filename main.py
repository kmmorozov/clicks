import requests
from dotenv import load_dotenv
import os
import urllib
import argparse

def get_cli_args():
    parser = argparse.ArgumentParser(
        description='Взаимодействие с сервисом "bitly.com"'
    )
    parser.add_argument("url")
    return parser.parse_args()

def shorten_link(long_link, headers):
    payload = {
        "long_url": long_link,
        "domain": "bit.ly"
    }
    response = requests.post(
        'https://api-ssl.bitly.com/v4/shorten',
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    short_url = response.json()['link']
    return short_url


def get_click_count(link, headers):
    url_template = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'
    url = url_template.format(link)
    response = requests.get(url,headers=headers)
    response.raise_for_status()
    click_count = response.json()['total_clicks']
    return click_count


def is_bitlink(link, headers):
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{link}',
        headers=headers
    )
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    cli_args = get_cli_args()
    user_link = cli_args.url
    url_components = urllib.parse.urlparse(user_link)
    link = '{}{}'.format(
        url_components.netloc,
        url_components.path
    )
    bitly_access_token = os.getenv("BITLY_TOKEN")
    headers = {
        'Authorization': 'Bearer {}'.format(bitly_access_token)
    }
    try:
        if is_bitlink(link, headers):
            click_count = get_click_count(link, headers)
            print('По Вашей ссылке {} переходов'.format(click_count))
        else:
            short_url = shorten_link(user_link, headers)
            print('Ваша короткая  ссылка: {}'.format(short_url))
    except (requests.HTTPError, requests.ConnectionError):
        print('Не удалось получить информацию')
