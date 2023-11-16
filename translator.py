import requests
import json


def translate(dict_to_translate: dict[str, str], token: str, folder_id: str) -> dict:
    target_language = 'ru'
    source_language = 'en'
    headers = {
        'Content-Type': 'application/json',
        "Authorization": f"Bearer {token}"
    }
    body = {
        "targetLanguageCode": target_language,
        "source_language_code": source_language,
        "texts": [],
        "folderId": folder_id,
    }
    try:
        for dict_key in dict_to_translate:
            string: list[str] = [dict_to_translate[dict_key]]
            body['texts'] = string
            response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                                     headers=headers,
                                     json=body
                                     )
            dict_to_translate[dict_key] = json.loads(response.text)['translations'][0]['text']

    except Exception or EOFError as error:
        print(f'Ошибка {error} во время перевода ключа {dict_key} и строки {string}\nОтвет yandex: {response}'
              f'\n{response.text}')
        raise Exception

    return dict_to_translate
