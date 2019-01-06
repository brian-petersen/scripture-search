import argparse
import sys
import csv

from elasticsearch_dsl import connections, Document, Keyword, Text, analyzer

from settings import ELASTICSEARCH_URL


def setup_connection():
    connections.create_connection(hosts=[ELASTICSEARCH_URL])


class Verse(Document):
    reference = Keyword()
    text = Text(analyzer=analyzer(
        'verse',
        tokenizer='standard',
        filter=['standard', 'lowercase', 'porter_stem']
    ))

    class Index:
        name = 'verses'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Perform a search on the verses'
    )
    parser.add_argument('query', help='Query to search for in verse text')
    parser.add_argument(
        '--size',
        default=10,
        type=int,
        help='Number of results to limit the search'
    )
    parser.add_argument(
        '--total',
        help='Print total number of matches',
        action='store_true'
    )

    args = parser.parse_args()
    query = args.query
    size = args.size
    print_total = args.total

    setup_connection()

    search = Verse.search()
    search = search[0:size]
    search = search.query('query_string', default_field='text', query=query)

    response = search.execute()
    hits = [{'reference': h.reference, 'text': h.text} for h in response]

    if print_total:
        print(f'Shown results: {len(hits)}')
        print(f'Total results: {response.hits.total}')

    writer = csv.DictWriter(sys.stdout, fieldnames=['reference', 'text'])
    writer.writerows(hits)
