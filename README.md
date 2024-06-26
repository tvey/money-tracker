# Финансовый трекер

Консольное приложение для учёта личных расходов и доходов.

Используется только стандартная библиотека ради чистоты и спокойствия :)

Версия Python: **3.12**, стиль кода: [**Black**](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html), стиль docstring: [**Google**](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

Файл `data.csv` хранит записи и создаётся автоматически, если отсутствует. Формат `CSV` выбран, так как он имеет хорошую совместимость, подходит для простых данных без вложений, легко читается и не требует повторов заголовков.

## Использование

Забрать себе проект, перейти в папку и вызвать справку:

```bash
git clone https://github.com/tvey/money-tracker.git
cd money-tracker
python main.py -h
```
_Примечание_: в случае, если используется системный Python, команду запуска нужно заменить на `python3`. В примерах файл вызывается напрямую, но можно сделать его исполняемым и задать alias.

Список команд, доступных в трекере (для них также можно вызвать `-h`: `python main.py search -h`):

- **balance** — отобразить текущий баланс
  
    ```bash
    python main.py balance
    ```

- **show** или **list** — вывести список всех записей
  
    ```bash
    python main.py show
    python main.py list -t 5
    ```

  Опция `-t N` или `--tail N` позволяет показать N последних записей.

- **add** — добавить запись. Нужно передать четыре обязательных аргумента (дата, категория, сумма, описание)

    ```bash
    python main.py add <дата> <категория> <сумма> <описание>
    python main.py add 2024-05-05 расход 1000 продукты
    python main.py add t i 10000 зп
    python main.py add t - 20000 rent
    ```

    - дату нужно передать в формате ГГГГ-ММ-ДД, но _сегодня_ можно передать как `t`.
    - две категории: доход и расход, но можно передавать их в виде д/р, +/-, inc/exp и других вариантов;
    - сумма должна быть целым числом;
    - описание может состоять из нескольких слов.

- **edit** — отредактировать запись, для чего нужно знать ID записи (номер строки из команды `show`). Изменить можно любой атрибут, который нужно передать как опцию (`--date`, `--category`, `--amount`, `--desc`) с новым значением

    ```bash
    python main.py edit <id> [<опция>] [<значение>]
    python main.py edit 7 --amount 1200
    ```

- **search** — поиск по любому атрибуту записи, отображается список отфильтрованных записей

    ```bash
    python main.py [<опция>] [<значение>]
    python main.py search --date 2024-05-05
    python main.py search --desc еда
    ```