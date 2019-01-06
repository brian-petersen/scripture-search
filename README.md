# Scripture Search

Python and Elasticsearch project that creates indexing and searching the LDS
scriptures trivial.

Motivation for the project comes from
https://speeches.byu.edu/talks/david-a-bednar_reservoir-living-water/.
Elder David A. Bednar specifies a way of studying that includes identifying all
scriptures that include the form of a specific word. I found this time
consuming and this project is the result.

## Scripts

### `create_index.py`

Drops and creates an Elasticsearch index with all the standard work verses.

Verse text is analyzed before being indexed in such a way that only the roots
of words are indexed. The resulting benefit is searching for all forms of a
word becomes easier. (E.g. gathered, gathering, and like words are all indexed
as gather.)

To use, simply run `$ python create_index.py`.

### `search.py`

Uses the created index to search for verses by there text. It outputs the
results to the terminal in CSV format for easy pasting into Google
Spreadsheets.

The tool is self documenting, but is included here to reference:

    $ python .\search.py -h
    usage: search.py [-h] [--size SIZE] [--total] query

    Perform a search on the verses

    positional arguments:
    query        Query to search for in verse text

    optional arguments:
    -h, --help   show this help message and exit
    --size SIZE  Number of results to limit the search
    --total      Print total number of matches

The `query` argument must conform to [Query String Query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html)
as documented by Elasticsearch. As such, queries like `charity OR love` can
be performed. I found this useful for when the stemming algorithm described
earlier does not work as expected.

Examples:

    $ python search.py charity --size 2 --total
    Shown results: 5
    Total results: 53
    1 Corinthians 13:4,"Charity suffereth long, and is kind; charity envieth not; charity vaunteth not itself, is not puffed up,"
    1 Corinthians 13:13,"And now abideth faith, hope, charity, these three; but the greatest of these is charity."

    $ python search.py "marry OR marriage" --size 1 --total
    Shown results: 1
    Total results: 82
    Luke 20:34,"And Jesus answering said unto them, The children of this world marry, and are given in marriage:"

## Getting Setup

1. Install Python 3.7
2. Install project dependencies: `$ pip install -r requirements.txt`
3. Setup Elasticsearch endpoint: `$ cp .env.example .env && vim .env`
4. Create index: `$ python create_index.py`
5. Reap and prosper

## Recognitions

The JSON scriptures used to create the index are from the BCBooks project:
https://github.com/bcbooks/scriptures-json.
