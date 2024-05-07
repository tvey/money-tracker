"""Validation, normalization functions, texts for unloading other modules."""
import datetime
from types import SimpleNamespace
from typing import Iterable

expense_category_names: list = ['расход', 'р', '-', 'e', 'ex', 'exp', 'expense']
income_category_names: list = ['доход', 'д', '+', 'i', 'in', 'inc', 'income']

texts = SimpleNamespace(
    balance_help='Показать текущий баланс, доходы и расходы',
    date_help='Дата дохода/расхода, ГГГГ-ММ-ДД',
    category_help='Категория (Доход/Расход)',
    amt_help='Сумма (целое число)',
    desc_help='Описание (может быть несколько слов)',
    show_help='Показать все записи или последние записи',
    show_tail='Показать последние N записей',
    search_help='Найти записи по дате/категории/сумме/описанию',
    add_help='Добавить новую запись',
    edit_help='Отредактировать запись',
    edit_id_help='Номер строки записи (можно узнать с помощью show или list)',
    date_validation='Дата должна быть в формате ГГГГ-ММ-ДД.',
    category_validation='Ожидаемые категории: Расход/Доход, Exp/Inc или -/+.',
    amount_validation='Сумма должна быть целым числом.',
)


def validate_date(value: str) -> bool:
    """Check if a user input is a valid date in the required format."""
    try:
        datetime.datetime.strptime(value, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_amount(value: str) -> bool:
    """Ensure that the amount string is a valid integer."""
    try:
        int(value)
        return True
    except ValueError:
        return False


def validate_category(value: str) -> bool:
    """Ensure the category is one of the allowed values."""
    return value in (expense_category_names + income_category_names)


def normalize_category(value: str) -> str:
    """Unify category format for saving."""
    if value in income_category_names:
        return 'Доход'
    else:
        return 'Расход'


def normalize_date(value: str) -> str:
    """Normalize a valid date string to YYYY-MM-DD format."""
    date_obj = datetime.datetime.strptime(value, '%Y-%m-%d')
    return date_obj.strftime('%Y-%m-%d')


def get_today() -> str:
    """Get a string value of today's date in YYYY-MM-DD format."""
    return datetime.datetime.now().date().strftime('%Y-%m-%d')


def process_args(
    date: str | None,
    category: str | None,
    amount: str | None,
    desc: Iterable[str] | None,
) -> dict | None:
    """Validate and normalize values from args.

    Args:
        date: A string representing the record date.
        category: A string of a category.
        amount: The financial amount (rubles), must be an integer.
        desc: A list of strings representing the description of the record.

    Returns:
        A dictionary containing normalized data or None if any validation fails.
    """
    if date is not None and not validate_date(date) and not date == 't':
        print(texts.date_validation)
        return

    if category is not None and not validate_category(category.lower()):
        print(texts.category_validation)
        return

    if amount is not None and not validate_amount(amount):
        print(texts.amount_validation)
        return

    if date == 't':
        date = get_today()
    elif date is not None:
        date = normalize_date(date)

    return {
        'date': date if date else None,
        'category': normalize_category(category) if category else None,
        'amount': int(amount) if amount is not None else None,
        'desc': ' '.join(desc),
    }
