import csv
import os
import sys
from dataclasses import dataclass
from typing import Optional

import utils


@dataclass
class Record:
    """Data class that represents a user's record of a transaction to track.

    Attributes:
        date (str): A date of a transaction in format YYYY-MM-DD.
        category (str): Type of a transaction (Расход/Доход).
        amount (int): An amount of a transaction.
        description (str): An optional description of a transaction.
    """

    date: str
    category: str
    amount: int
    desc: str = ''


class Tracker:
    """Class that manages financial records.

    Attributes:
        file (str): The path to the CSV file with records.
    """

    def __init__(self, file: str) -> None:
        """Initiate a tracker and specify a file which stores records.

        Args:
            file (str): The path to the CSV file.
        """
        self.file = file
        self.fieldnames = ['Дата', 'Категория', 'Сумма', 'Описание']
        self.field_map = {
            'date': 'Дата',
            'category': 'Категория',
            'amount': 'Сумма',
            'desc': 'Описание',
        }
        self._init_file()

    def _init_file(self):
        with open(self.file, 'a', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            if file.tell() == 0:
                writer.writeheader()

    def _record_to_csv_dict(self, record: Record) -> dict:
        """Convert a Record object to a CSV dict with required field names.

        Args:
            record (Record): The Record object to convert to dict for CSV.
        """
        return {
            field: getattr(record, attr)
            for attr, field in self.field_map.items()
        }

    def _load_records(self) -> list[Record]:
        with open(self.file, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [
                Record(
                    date=row['Дата'],
                    category=row['Категория'],
                    amount=int(row['Сумма']),
                    desc=row['Описание'],
                )
                for row in reader
            ]

    def show_records(self, records: Optional[list[Record]] = None) -> None:
        """Print existing records from a file.

        Args:
            records (list[Record], optional): Records to show, all by default.
        """
        if not records:
            records = self._load_records()



        for i, rec in enumerate(records, start=1):
            print(
                f'{i:4}. {rec.date:12} {rec.category:6} '
                f'{rec.amount:8} {rec.desc}'
            )

    def show_last_n_records(self, n: int) -> None:
        records = self._load_records()
        self.show_records(records[-n:])

    def show_balance(self) -> None:
        """Print info: current balance, total incomes, total expenses"""
        records = self._load_records()
        incomes = sum(r.amount for r in records if r.category == 'Доход')
        expenses = sum(r.amount for r in records if r.category == 'Расход')
        balance = incomes - expenses
        print(
            f'{"Текущий баланс:":<15} {balance:>10} ₽\n'
            f'{"Все доходы:":<15} {incomes:>10} ₽\n'
            f'{"Все расходы:":<15} {expenses:>10} ₽'
        )

    def search(
        self,
        category: Optional[str] = None,
        date: Optional[str] = None,
        amount: Optional[int] = None,
    ) -> None:
        """Searche for records by category, date, or amount.

        Args:
            category (Optional[str]): The category to filter by.
            date (Optional[str]): The date to filter by.
            amount (Optional[int]): The amount to filter by.
        """
        records = self._load_records()
        filtered_records = [
            rec
            for rec in records
            if (category is None or rec.category == category)
            and (date is None or rec.date == date)
            and (amount is None or rec.amount == amount)
        ]
        self.show_records(filtered_records)

    def add_record(self, record: Record):
        """Append a new record row to a file based on user input.

        Args:
            record (Record): The Record object to be saved to the file.
        """
        with open(self.file, 'a', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow(self._record_to_csv_dict(record))
            print('Запись сохранена.')

    def edit_record(self, record_id: int, edited_record: Record) -> bool:
        """Edit an existing record using its line number as the record ID.

        Args:
            record_id (int): A line number of a row to edit.
            edited_record (Record): The Record object to replace existing line.
        """
        records = self._load_records()
        record_id -= 1

        if 0 <= record_id < len(records):
            records[record_id] = edited_record
            with open(self.file, 'w', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
                for rec in records:
                    writer.writerow(self._record_to_csv_dict(rec))
            print('Запись обновлена.')
            return True

        return False


def handle_args():
    """Process the input arguments to handle add/show/balance functionality."""
    if len(sys.argv) < 2:
        print(
            'Финансовый трекер. Использование:\n'
            f'{utils.texts["balance"]}\n'
            f'{utils.texts["add"]}\n'
            f'{utils.texts["edit"]}\n'
            f'{utils.texts["search"]}'
        )
        return

    if sys.argv[1] == 'add':
        if len(sys.argv) < 5:
            print(utils.texts['add'])
            return

        date = sys.argv[2]
        category = sys.argv[3].lower()
        amount = sys.argv[4]
        description = ' '.join(sys.argv[5:]) if len(sys.argv) > 5 else ''

        if not utils.validate_date(date):
            print('Дата должна быть в формате ГГГГ-ММ-ДД.')
            return

        if not utils.validate_category(category):
            print('Ожидаемые категории: Расход/Доход, Exp/Inc или -/+.')
            return

        if not utils.validate_amount(amount):
            print('Сумма должна быть целым числом.')
            return

        new_record = Record(
            date=utils.normalize_date(date),
            category=utils.normalize_category(category),
            amount=int(amount),
            desc=description,
        )
        tracker.add_record(new_record)

    elif sys.argv[1] == 'show':
        tracker.show_records()
    elif sys.argv[1] == 'balance':
        tracker.show_balance()


if __name__ == '__main__':
    tracker = Tracker('data.csv')
    handle_args()
