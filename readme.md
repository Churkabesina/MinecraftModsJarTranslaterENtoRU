## Как пользоваться переводчиком:
1. Указать в config путь до папки с модами, которые нужно перевести
2. Указать путь, куда сохранятся переведенные версии модов(если указать ту же папку, то перезапишутся)
3. Переводчик работает на yandex translate API, поэтому понадобится ваш личный oAuth токен, указать также в cfg
4. Указать id папки в yandex cloud(можно от default)
5. Запуск через cmd -> <python.exe path> <main.py path>

### Использование утилиты конвертации хороших данных переводов в tmx для обучения собственной модели:
cmd -> <python.exe path> <JsonToTMXconverter.py path> <путь до папки хорошо переведенных модов> <куда сохранить tmx>