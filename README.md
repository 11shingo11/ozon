# Ozon Parser

Краткое описание проекта:
Данный код представляет собой скрипт на языке Python для парсинга и извлечения информации о продуктах с веб-сайта и сохранения ее в файле формата Microsoft Excel. Скрипт использует библиотеку Selenium для автоматизации веб-браузинга и библиотеку openpyxl для работы с файлами Excel.

## Использование

- Запустите скрипт
- Введите URL(например вы ищите дрель,забейте в магазине Ozon в поиске дрель и скопируйте Url), который вы хотите спарсить, и нажмите Enter.
- Введите десятичное число (0-5) для фильтрации продуктов по рейтингу, и нажмите Enter.
- Введите минимальное количество комментариев, необходимое для включения продукта в таблицу Excel, и нажмите Enter.
- Введите желаемое имя для таблицы Excel, в которую будет сохранена информация, и нажмите Enter.
- Скрипт начнет парсинг веб-сайта, переходя на следующие страницы при необходимости, и извлекать соответствующую информацию о продуктах.
- По завершении парсинга данные будут сохранены в файле Excel с колонками для ID, рейтинга, названия продукта, цены, количества отзывов и URL продукта.

