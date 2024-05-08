import unittest
from core import utils


class TestUtils(unittest.TestCase):
    def test_validate_date(self):
        self.assertTrue(utils.validate_date('2024-05-08'))
        self.assertTrue(utils.validate_date('2012-12-12'))
        self.assertFalse(utils.validate_date('08-05-2024'))
        self.assertFalse(utils.validate_date('2024-13-01'))
        self.assertFalse(utils.validate_date('2024-13-01'))
        self.assertFalse(utils.validate_date('12.12.12'))
        self.assertFalse(utils.validate_date('12-12-2012'))

    def test_validate_amount(self):
        self.assertTrue(utils.validate_amount('100'))
        self.assertTrue(utils.validate_amount('-50'))
        self.assertFalse(utils.validate_amount('1.5'))
        self.assertFalse(utils.validate_amount('abc'))

    def test_validate_category(self):
        self.assertTrue(utils.validate_category('e'))
        self.assertTrue(utils.validate_category('income'))
        self.assertTrue(utils.validate_category('+'))
        self.assertTrue(utils.validate_category('д'))
        self.assertTrue(utils.validate_category('-'))
        self.assertTrue(utils.validate_category('ДоХоД'.lower()))
        self.assertFalse(utils.validate_category('дхд'))
        self.assertFalse(utils.validate_category('расходы'))

    def test_normalize_category(self):
        self.assertEqual(utils.normalize_category('д'), 'Доход')
        self.assertEqual(utils.normalize_category('р'), 'Расход')
        self.assertEqual(utils.normalize_category('+'), 'Доход')
        self.assertEqual(utils.normalize_category('-'), 'Расход')
        self.assertEqual(utils.normalize_category('i'), 'Доход')
        self.assertEqual(utils.normalize_category('e'), 'Расход')

    def test_normalize_date(self):
        self.assertEqual(utils.normalize_date('2024-5-8'), '2024-05-08')
        self.assertEqual(utils.normalize_date('2024-5-08'), '2024-05-08')

    def test_get_today(self):
        today = utils.get_today()
        self.assertIsInstance(today, str)
        self.assertEqual(len(today), 10)
        self.assertTrue(today.startswith('202'))

    def test_process_args(self):
        self.assertEqual(
            utils.process_args('2024-05-08', 'income', '100', ['зп']),
            {
                'date': '2024-05-08',
                'category': 'Доход',
                'amount': 100,
                'desc': 'зп',
            },
        )
        self.assertIsNone(
            utils.process_args(
                '08-05-2024',
                'income',
                '100',
                ['Salary'],
            )
        )

        self.assertIsNone(
            utils.process_args(
                '2024-05-08',
                'investment',
                '100',
                ['Salary'],
            )
        )
        self.assertIsNone(
            utils.process_args(
                '2024-05-08',
                'income',
                'abc',
                ['Salary'],
            )
        )


if __name__ == '__main__':
    unittest.main()
