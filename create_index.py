import os
import json
from glob import glob

from search import Verse, setup_connection


def parse_verses(path):
    with open(path) as f:
        data = json.load(f)

    return data['verses']


if __name__ == '__main__':
    paths = list(
        map(lambda path: os.path.abspath(path), glob('./data/*.json'))
    )

    print(f"Importing verses from {', '.join(paths)}")

    books_verses = list(map(lambda path: parse_verses(path), paths))
    dict_verses = [verse
                   for book_verses in books_verses for verse in book_verses]
    verses = [Verse(reference=v['reference'], text=v['text'])
              for v in dict_verses]

    print(f'Importing {len(verses)} verses')

    setup_connection()

    Verse._index.delete()
    Verse.init()

    for verse in verses:
        verse.save()
