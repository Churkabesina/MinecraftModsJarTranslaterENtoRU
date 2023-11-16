import requests
import json
import datetime
from config import o_auth


def get_actual_iam_token() -> None:

    o_auth_token = o_auth
    body = json.dumps({'yandexPassportOauthToken': f'{o_auth_token}'})

    with open('IAMtoken.json', 'r', encoding='UTF-8') as f_in:
        file = json.load(f_in)
        if (datetime.datetime.now() - datetime.datetime.strptime(file['expiresAt'], '%Y-%m-%d %H:%M:%S.%f'))\
                .total_seconds() / (60*60) > 3:
            i_am_token: dict = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', data=body).json()
            i_am_token['expiresAt'] = str(datetime.datetime.now())
            with open('IAMtoken.json', 'w', encoding='UTF-8') as f_out:
                json.dump(i_am_token, f_out, indent=4)
            print('iam токен обновлен')
        else:
            print('iam токен актуален')