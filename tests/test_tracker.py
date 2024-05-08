import os
import unittest

from core.tracker import Record, Tracker


class TestRecord(unittest.TestCase):
    def test_create_record(self):
        record = Record('2024-05-01', '+', 1000, 'зп')
        self.assertEqual(record.date, '2024-05-01')
        self.assertEqual(record.category, '+')
        self.assertEqual(record.amount, 1000)
        self.assertEqual(record.desc, 'зп')

    def test_update_record(self):
        record = Record('2024-05-05', '+', 1000)
        record.update(date='2024-05-15', category='-', amount=500)
        self.assertEqual(record.date, '2024-05-15')
        self.assertEqual(record.category, '-')
        self.assertEqual(record.amount, 500)
        self.assertEqual(record.desc, '')


class TestTracker(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_data.csv'
        self.tracker = Tracker(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_record(self):
        record = Record('2024-05-01', 'exp', 1000, 'еда')
        self.tracker.add_record(record)

        records = self.tracker._load_records()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].date, '2024-05-01')
        self.assertEqual(records[0].category, 'exp')
        self.assertEqual(records[0].amount, 1000)
        self.assertEqual(records[0].desc, 'еда')

    def test_edit_record(self):
        record = Record('2024-05-01', '+', 1000, 'desc')
        self.tracker.add_record(record)
        success = self.tracker.edit_record(1, {'amount': 1200, 'desc': 'desc+'})
        self.assertTrue(success)
        records = self.tracker._load_records()
        self.assertEqual(records[0].amount, 1200)
        self.assertEqual(records[0].desc, 'desc+')

    def test_show_balance(self):
        self.tracker.add_record(Record('2024-05-01', '+', 1000, 'зп'))
        self.tracker.add_record(Record('2024-05-02', '-', 200, 'food'))

        import io
        import sys

        balance = io.StringIO()
        sys.stdout = balance  # capture balance output to memory
        self.tracker.show_balance()
        sys.stdout = sys.__stdout__
        output = balance.getvalue()
        self.assertIn('Текущий баланс:', output)
        self.assertIn('Все доходы:', output)
        self.assertIn('Все расходы:', output)


if __name__ == '__main__':
    unittest.main()
