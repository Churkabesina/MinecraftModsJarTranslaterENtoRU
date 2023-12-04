import zipfile
import json
from os import listdir
from os.path import isfile, join
from sys import argv


def IsExceptions(eng, rus):
    for i in str_exceptions:
        if i in eng or i in rus:
            return True


# //argv = [path_jars, path_tmx]//
if len(argv) == 1:
    path_jars = r'D:\JarsDatabase'
    path_tmx = r'D:\JarsDatabase\stringsdatabase.tmx'
else:
    path_jars = argv[1]
    path_tmx = argv[2]

str_exceptions = {'&', '<', '>'}
list_jars = [x for x in listdir(path_jars) if isfile(join(path_jars, x)) and x.endswith('.jar')]
count_strings = 0
print(f'Считано {len(list_jars)} названий модов')

with open(path_tmx, 'w', encoding='UTF-8') as f_out:
    f_out.write(f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                f'<tmx version="1.4">\n'
                f'    <header creationtool="ZubochistkaConverter" creationtoolversion="1.0" datatype="PlainText" '
                f'segtype="block" srclang="en" o-tmf="json" adminlang="ru"/>\n'
                f'    <body>\n')

with open('converter_log.txt', 'w', encoding='UTF-8'):
    pass
for mod_name in list_jars:
    with zipfile.ZipFile(join(path_jars, mod_name), 'r') as unzipped_mod:
        lang_files = sorted([file for file in unzipped_mod.namelist()
                             if 'ru_ru.json' in file or 'en_us.json' in file])
        if len(lang_files) == 0:
            with open('converter_log.txt', 'a', encoding='UTF-8') as f_out:
                f_out.write(f'{mod_name} - Не найдены файлы локализаций\n')
            continue
        if len(lang_files) == 1:
            with open('converter_log.txt', 'a', encoding='UTF-8') as f_out:
                f_out.write(f'{mod_name} - Найден только 1 из 2 нужных файлов локализации\n')
            continue
        try:
            with unzipped_mod.open(lang_files[0], 'r') as file_in:
                eng_strings: list[tuple[str, str]] = sorted(json.load(file_in).items())
            with unzipped_mod.open(lang_files[1], 'r') as file_in:
                ru_strings: list[tuple[str, str]] = sorted(json.load(file_in).items())
        except Exception or EOFError:
            with open('converter_log.txt', 'a', encoding='UTF-8') as f_out:
                f_out.write(f'{mod_name} - Не получилось считать json\n')
            continue
        if len(eng_strings) != len(ru_strings):
            with open('converter_log.txt', 'a', encoding='UTF-8') as f:
                f.write(f'{mod_name} - Ошибка записи в tmx, несовпадает кол-во записей в json файлах\n')
            continue
    with open(path_tmx, 'a', encoding='UTF-8') as f_out:
        for strings in zip(eng_strings, ru_strings, strict=True):
            if IsExceptions(strings[0][1], strings[1][1]):
                continue
            f_out.write(f'        <tu srclang="en">\n'
                        f'            <tuv xml:lang="en">\n'
                        f'                <seg>{strings[0][1]}</seg>\n'
                        f'            </tuv>\n'
                        f'            <tuv xml:lang="ru">\n'
                        f'                <seg>{strings[1][1]}</seg>\n'
                        f'            </tuv>\n'
                        f'        </tu>\n')
            count_strings += 1
        print(f'{mod_name} || количество строк: {len(eng_strings)}')
    with open('converter_log.txt', 'a', encoding='UTF-8') as f:
        f.write(f'{mod_name} - Успешно добавлен в базу\n')
with open(path_tmx, 'a', encoding='UTF-8') as f_out:
    f_out.write(f'    </body>\n'
                f'</tmx>')
print(f'Создание базы переводов завершено, было записано {count_strings} переводов')