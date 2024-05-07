"""Main module that initiates a tracker with a file and handles arguments."""

from core.tracker import Record, Tracker
from core.argparser import parse_args
from core.utils import process_args


def main():
    """Initiate tracker and handle CLI functionality."""
    tracker = Tracker('data.csv')
    args = parse_args()

    if args.command == 'add':
        record_data = process_args(
            args.date,
            args.category,
            args.amount,
            args.desc,
        )
        if record_data:
            new_record = Record(
                date=record_data['date'],
                category=record_data['category'],
                amount=record_data['amount'],
                desc=record_data['desc'],
            )
            tracker.add_record(new_record)

    elif args.command == 'edit':
        record_data = process_args(
            args.date,
            args.category,
            args.amount,
            args.desc,
        )
        if record_data:
            # remove empty values
            edit_data = {k: v for k, v in record_data.items() if v}
            tracker.edit_record(args.id, edit_data)

    elif args.command == 'search':
        tracker.search(
            category=args.category, date=args.date, amount=args.amount
        )

    elif args.command in ['list', 'show']:
        if args.tail:
            tracker.show_records(args.tail)
        else:
            tracker.show_records()

    elif args.command == 'balance':
        tracker.show_balance()


if __name__ == '__main__':
    main()
