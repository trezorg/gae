"""Utils."""

from typing import Iterable
import math
import csv
import io
import json
from itertools import islice

import requests


def is_prime(n: int):
    """Prime checking."""
    if n < 1:
        raise ValueError('Number cannot be less 1.')
    if n == 1:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    for x in range(3, int(math.sqrt(n)) + 1, 2):
        if not n % x:
            return False
    return True


def split_to_primes(n: int, split: int=3):
    """Split non prime to sum of primes respectively a split number."""
    results = set()
    for x in range(2, n):
        if not is_prime(x):
            continue
        if split == 2:
            if is_prime(n - x):
                yield x, n - x
        else:
            for value in split_to_primes(n - x, split=split - 1):
                res = tuple(sorted((x, *value)))
                if res not in results:
                    yield res
                results.add(res)


def get_prime_sum(n: int, number: int=2, split: int=3):
    """Result of sum of primes."""
    return tuple(islice(split_to_primes(n, split=split), number))


def prepare_row(n: int):
    """Prepare row."""
    sums_str = ('{}={}'.format('+'.join(map(str, sm)), n)
                for sm in get_prime_sum(n))
    return (n, 'FALSE', *sums_str)


def prepare_csv_output(rows: Iterable[tuple]):
    """Prepare file."""
    output = io.StringIO()
    writer = csv.writer(output, delimiter=',')
    writer.writerows(rows)
    return output.getvalue()


def read_csv_data(data: str) -> Iterable[int]:
    """Read input csv data."""
    inp = io.StringIO(data)
    reader = csv.reader(inp, delimiter=',')
    for row in reader:
        yield int(row[0])


def filter_input_data(data: str, x: int=20) -> Iterable[int]:
    """Read csv data and yield non prime that more then x."""
    for number in read_csv_data(data):
        if number > x and not is_prime(number):
            yield number


def process_input(data: str) -> str:
    """Process input data."""
    rows = []
    for number in filter_input_data(data):
        rows.append(prepare_row(number))
    return prepare_csv_output(rows)


def get_service_result(url, number):
    """Service request."""
    response = requests.post(url, data=json.dumps({'number': number}),
                             headers={'Content-Type': 'application/json'})
    return json.loads(response.text)['result']
