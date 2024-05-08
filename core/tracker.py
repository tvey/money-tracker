"""This module provides the Tracker class to manage financial transactions
and the Record class to represent and validate individual records.

Example:
    tracker = Tracker("data.csv")
    record = Record(date="2024-05-01", category="+", amount=1000)
    tracker.add_record(record)
"""

import csv
from dataclasses import dataclass, fields


@dataclass
class Record:
    """Data class that represents a user's record of a transaction to track.

    Attributes:
        date: A date of a transaction in format YYYY-MM-DD.
        category: Type of a transaction (Expense/Income).
        amount: Monetary amount of a transaction, whole number.
        description: An optional description of a transaction.
    """

    date: str
    category: str
    amount: int
    desc: str = ''

    def update(self, **kwargs):
        for field in fields(self):
            if field.name in kwargs:
                setattr(self, field.name, kwargs[field.name])
        return self


class Tracker:
    """Class that manages financial records.

    Attributes:
        file: The path to the CSV file with records.
    """

    def __init__(self, file: str) -> None:
        """Initiate a tracker and specify a file which stores records.

        Args:
            file: The path to the CSV file.
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
            record: The Record object to convert to dict for CSV.
        """
        return {
            field: getattr(record, attr)
            for attr, field in self.field_map.items()
        }

    def _load_records(self) -> list[Record]:
        """Open the tracker file and load all rows as a list of Record objects.

        Returns:
            Rows from a file loaded as Record objects.
        """
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

    def show_records(
        self,
        records: list[Record] | None = None,
        n: int | None = None,
    ) -> None:
        """Print existing records from a file.

        Args:
            records: Records to show.
            n: Number of last records to show.
        """
        if not records:
            records = self._load_records()
        start = 1

        if records:
            if n and n < len(records):
                start = max(0, len(records) - n + 1)
                records = records[-n:]
                print('  ...')

            for i, rec in enumerate(records, start=start):
                print(
                    f'{i:3}.  {rec.date:12} {rec.category:6} '
                    f'{rec.amount:8}   {rec.desc}'
                )
        else:
            print('Записей нет')

    def show_balance(self) -> None:
        """Print info: current balance, total incomes, total expenses."""
        records = self._load_records()
        incomes: int = sum(r.amount for r in records if r.category == 'Доход')
        expenses: int = sum(r.amount for r in records if r.category == 'Расход')
        balance: int = incomes - expenses
        print(
            f'{"Текущий баланс:":<15} {balance:>10} ₽\n'
            f'{"Все доходы:":<15} {incomes:>10} ₽\n'
            f'{"Все расходы:":<15} {expenses:>10} ₽'
        )

    def search(
        self,
        category: str | None = None,
        date: str | None = None,
        amount: int | None = None,
        desc: str | None = None,
    ) -> None:
        """Search for records by category, date, amount, description.

        Args:
            category: The category to filter by.
            date: The date to filter by.
            amount: The amount to filter by.
            desc: The description to filter by.
        """
        records = self._load_records()
        filtered_records: list[Record] = [
            rec
            for rec in records
            if (category is None or rec.category == category)
            and (date is None or rec.date == date)
            and (amount is None or rec.amount == amount)
            and (desc is None or desc.lower() in rec.desc.lower())
        ]
        if filtered_records:
            self.show_records(records=filtered_records)
        else:
            print('Ничего не найдено.')

    def add_record(self, record: Record) -> None:
        """Append a new record row to a file based on user input.

        Args:
            record: The Record object to be saved to the file.
        """
        with open(self.file, 'a', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow(self._record_to_csv_dict(record))
            print('Запись сохранена.')

    def edit_record(self, record_id: int, edit_data: dict) -> bool:
        """Edit an existing record using its line number as ID.

        Args:
            record_id: A line number of a row to edit.
            edited_record: The Record object to replace existing row.
        """
        records = self._load_records()
        record_id -= 1  # using 1-based indexes in 'show'

        if 0 <= record_id < len(records):
            record = records[record_id]
            records[record_id] = record.update(**edit_data)
            with open(self.file, 'w', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
                for rec in records:
                    writer.writerow(self._record_to_csv_dict(rec))
            print('Запись обновлена.')
            return True

        print('Запись не найдена.')
        return False
