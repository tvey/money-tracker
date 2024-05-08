import argparse

from .utils import texts as txt


def parse_args() -> argparse.Namespace:
    """Create command line argument parser.
    
    Returns:
        A namespace object that contains parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Финансовый трекер',
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    subparsers.add_parser('balance', help=txt.balance_help)

    show = subparsers.add_parser('show', help=txt.show_help)
    list_ = subparsers.add_parser('list', help=txt.show_help)

    for subparser in [show, list_]:
        subparser.add_argument('-t', '--tail', type=int, help=txt.show_tail)

    add = subparsers.add_parser('add', help=txt.add_help)
    add.add_argument('date', help=txt.date_help)
    add.add_argument('category', help=txt.category_help)
    add.add_argument('amount', type=int, help=txt.amt_help)
    add.add_argument('desc', default='', help=txt.desc_help, nargs='+')

    edit = subparsers.add_parser('edit', help=txt.edit_help)
    edit.add_argument('id', type=int, help=txt.edit_id_help)
    edit.add_argument('--date', default=None, help='Новая дата')
    edit.add_argument('--category', default=None, help='Категория')
    edit.add_argument('--amount', default=None, type=int, help='Новая сумма')
    edit.add_argument('--desc', default='', help='Новое описание', nargs='+')

    search = subparsers.add_parser('search', help=txt.search_help)
    search.add_argument('--category', default=None, help=txt.category_help)
    search.add_argument('--date', default=None, help=txt.date_help)
    search.add_argument('--amount', default=None, type=int, help=txt.amt_help)
    search.add_argument('--desc', default='', help=txt.desc_help, nargs='+')

    return parser.parse_args()
