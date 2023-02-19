# -- STOCK TRADING BOT -- #
from requests import Session
import requests
import json
import webbrowser
import os
from twilio.rest import Client
import emoji
import math
from datetime import date


up = emoji.emojize(":red_triangle_pointed_up:")
down = emoji.emojize(":red_triangle_pointed_down:")


def get_market_data(api_key: str, slug: str, coin_id: str) -> json:
    """
    :param api_key: Get API Key here -> https://coinmarketcap.com/api/
    :param slug: Full name of a listed cryptocurrency, given as an ALL lowercase string. (EX: 'bitcoin', 'ethereum')
    :param coin_id: ID of given coin listed on API
    :return: Requested JSON data
    """

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

    parameters = {'slug': slug,
                  'convert': 'USD'}

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    print(data)
    parse_market_data(data, slug, coin_id)

    return data


def parse_market_data(json_data: json, slug, coin_id):
    data = json_data['data'][coin_id]
    symbol = data['symbol']
    time_of_update = data['last_updated']

    quote = data['quote']['USD']
    price = quote['price']
    change_24h = quote['percent_change_24h']

    get_news_data(change_24h, slug)


def get_news_data(change, slug):
    url = 'https://newsapi.org/v2/everything'

    parameters = {
        'q': slug,
        'from': date.today(),
        'sortBy': 'popularity',
        'apiKey': '438f31a7108d42898339a5d11fd208e8'
    }

    response = requests.get(url, params=parameters)
    response.raise_for_status()

    data = response.json()

    parse_news_data(data, change, slug)

    return data


def parse_news_data(json_data: json, change, slug):
    my_news = {}

    for count, article in enumerate(json_data['articles']):
        if count in range(0, 3):  # 1, 2, 3
            my_news[f'article-{count + 1}'] = list((json_data['articles'][count]['title'],
                                                    json_data['articles'][count]['description'],
                                                    json_data['articles'][count]['url']))
        else:
            break

    notify_user(change, slug, news=my_news)



def notify_user(change, slug, news):
    account_sid = 'ACece11a5e65aeb1139ec05a9e33e36f8c'
    auth_token = '5398fbb7b794008d0e2b28573656c162'
    client = Client(account_sid, auth_token)

    if math.floor(change) >= 0:
        sent_emoji = up
    else:
        sent_emoji = down

    coin = slug.upper()

    for i in range(0, 3):
        headline = f"Headline: {news[f'article-{i+1}'][0]}"
        description = f"Description: {news[f'article-{i+1}'][1]}"
        url = f"Read More Here! {news[f'article-{i+1}'][2]}"

        message = client.messages \
            .create(
            body=f"""\n\n\n{coin}{sent_emoji}{change:.2f}\n{headline}\n{description}""",
            from_='+18445950953',
            to='+19084193183'
        )

        print(message.sid)


get_market_data('c25d0b16-28d8-42da-aecb-6ae03f4ff20e', 'ethereum', '1027')



