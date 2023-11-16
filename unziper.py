import zipfile
from os import listdir
from os.path import isfile, join
import shutil
import json
from translator import translate
from config import yandex_cloud_folder_id, mods_path, translated_mods_path


def get_list_jars(path: str = mods_path) -> tuple[list, str]:
    list_jars = [x for x in listdir(path) if isfile(join(path, x)) and x.endswith('.jar')]
    print(f'Считано {len(list_jars)} названий модов')
    return list_jars, path


def unzipping():

    list_jars, path = get_list_jars()
    translated_path = translated_mods_path
    translated_mod_count = 0
    yandex_cloud_folder = yandex_cloud_folder_id
    with open('IAMtoken.json', 'r', encoding='UTF-8') as r_token:
        token = json.load(r_token)['iamToken']
    open('log.txt', 'w').close()

    for mod_name in list_jars:
        with zipfile.ZipFile(join(path, mod_name), 'r') as unzipped_mod:
            file_names = [lang_file for lang_file in unzipped_mod.namelist()
                          if 'ru_ru.json' in lang_file or 'en_us.json' in lang_file]
            if len(file_names) == 0:
                with open('log.txt', 'a', encoding='UTF-8') as f_out:
                    f_out.write(f'{mod_name} - Не найдены файлы локализаций\n')
                continue
            if 'ru_ru.json' in str(file_names):
                with open('log.txt', 'a', encoding='UTF-8') as f_out:
                    f_out.write(f'{mod_name} - Уже имеет файл ru_ru.json, замена не производилась\n')
                continue
            else:
                with unzipped_mod.open(file_names[0], 'r') as editing_file:
                    strings_to_translate = json.load(editing_file)

        try:
            strings_to_translate = translate(strings_to_translate, token, yandex_cloud_folder)
        except Exception or EOFError:
            print(f'Ошибка во время перевода {mod_name}')
            with open('log.txt', 'a', encoding='UTF-8') as f_out:
                f_out.write(f'{mod_name} - ===Ошибка перевода===\n')
            continue

        strings_to_translate = json.dumps(strings_to_translate, indent=4, ensure_ascii=False).encode('UTF-8')
        shutil.copy(join(path, mod_name), translated_path)

        with zipfile.ZipFile(join(translated_path, mod_name), 'a') as translated_mod:
            file_names[0] = file_names[0].replace('en_us.json', 'ru_ru.json', 1)
            with translated_mod.open(file_names[0], 'w') as translation_file:
                translation_file.write(strings_to_translate)
        with open('log.txt', 'a', encoding='UTF-8') as f_out:
            f_out.write(f'{mod_name} - Успешно переведен\n')
            translated_mod_count += 1
    print(f'Переведено {translated_mod_count} модов')