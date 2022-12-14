import sys
from HH_parse_class import JobScrapper
from pymongo import MongoClient
from pprint import pprint

_VACANCY = 'Developer'
_SALARY_MIN = 100000
_SALARY_CURRENCY = 'руб.'


def _show_vacancies(salary_min, collection):
    """Show on screen vacancies with minimal salary."""

    result = collection.find({
        'salary_currency': {'$eq': _SALARY_CURRENCY},
        '$or': [{'salary_min': {'$gte': salary_min}}, {'salary_max': {'$gt': salary_min}}]
    }
    )
    for item in result:
        pprint(item)


def _save_records(records, collection):
    """Insert new record in Mongo."""

    for record in records:
        collection.update(record, record, upsert=True)


def _main():
    """Entry point."""

    client = MongoClient('localhost', 27017)
    db = client['vacancies']
    vacancies = db.vacancies

    scrapper = JobScrapper(_VACANCY)

    _save_records(scrapper.storage, vacancies)

    _show_vacancies(_SALARY_MIN, vacancies)


if __name__ == '__main__':
    sys.exit(_main())


