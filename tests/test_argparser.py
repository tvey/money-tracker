import unittest
from unittest.mock import patch

from core.argparser import parse_args


class TestArgparser(unittest.TestCase):
    @patch('sys.argv', ['tracker', 'balance'])
    def test_balance_command(self):
        args = parse_args()
        self.assertEqual(args.command, 'balance')

    @patch('sys.argv', ['tracker', 'show', '-t', '2'])
    def test_show_command_with_tail(self):
        args = parse_args()
        self.assertEqual(args.command, 'show')
        self.assertEqual(args.tail, 2)

    @patch('sys.argv', ['tracker', 'list', '--tail', '5'])
    def test_list_command_with_tail(self):
        args = parse_args()
        self.assertEqual(args.command, 'list')
        self.assertEqual(args.tail, 5)

    @patch('sys.argv', ['tracker', 'add', '2024-05-08', '+', '200', 'etc etc'])
    def test_add_command(self):
        args = parse_args()
        self.assertEqual(args.command, 'add')
        self.assertEqual(args.date, '2024-05-08')
        self.assertEqual(args.category, '+')
        self.assertEqual(args.amount, 200)
        self.assertEqual(args.desc, ['etc etc'])

    @patch('sys.argv', ['tracker', 'edit', '1', '--amount', '500'])
    def test_edit_command(self):
        args = parse_args()
        self.assertEqual(args.command, 'edit')
        self.assertEqual(args.id, 1)
        self.assertEqual(args.amount, 500)

    @patch('sys.argv', ['tracker', 'search', '--category', 'Расход'])
    def test_search_command(self):
        args = parse_args()
        self.assertEqual(args.command, 'search')
        self.assertEqual(args.category, 'Расход')


if __name__ == '__main__':
    unittest.main()
