import datetime

expense_category_names: list = ['расход', '-', 'exp', 'expense']
income_category_names: list = ['доход', '+', 'inc', 'income']
file_call = 'python tracker.py'
texts = {
    'balance': f'Вывод баланса: {file_call} balance',
    'add': f'Добавить запись: {file_call} add <дата> <категория> <сумма> [описание]',
    'edit': f'Редактировать запись: {file_call} edit <номер строки> <дата> <категория> <сумма> [описание]',
    'search': f'Поиск: {file_call} search ...',
}


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
    """Normalize a valid date format to YYYY-MM-DD."""
    date_obj = datetime.datetime.strptime(value, '%Y-%m-%d')
    return date_obj.strftime('%Y-%m-%d')
