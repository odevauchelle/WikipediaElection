# WikipediaElection

A few Python functions to download election data from Wikipedia.

## Quick example

Get data from Wikipedia:

```python
import WikipediaElection as WE

url_tail = "/wiki/2002_French_presidential_election"
election_data = WE.fetch_election_data_from_web( url_tail )
```
The output is a dictionnary:

```python
for key, value in election_data.items():
    print(key, ':' , value)
```
```
>>> Failed to find entry "Nominee"
Failed to find entry "Candidate"
Failed to find entry "Party"
Failed to find entry "Popular vote"
Failed to find entry "Percentage"
Failed to find entry "Candidate"
title : 2002 French presidential election - Wikipedia
link_to_previous_election : /wiki/1995_French_presidential_election
last_edition_time : 8 November 2023, at 23:11 (UTC)
href : https://en.wikipedia.org/wiki/2002_French_presidential_election
year : 2002
nominee : ['Jacques Chirac', 'Jean-Marie Le Pen']
party : ['RPR', 'FN']
popular_vote : [25537956, 5525032]
percentage : [82.21, 17.79]
```
## Track a country

Most election pages on Wikipedia feature a link to the previous election. We can recursively follow this link:

```python
while True :

    election = WE.fetch_election_data_from_web( url_tail )

    print('------------------------')
    for key in ['year','party', 'percentage']:
        print( key, ':' , election[key])
    print('------------------------')

    url_tail = election['link_to_previous_election']

    if url_tail is None :
        print('Wikipedia time series stops here.')
        break
```
```
>>> Failed to find entry "Nominee"
Failed to find entry "Candidate"
Failed to find entry "Party"
Failed to find entry "Popular vote"
Failed to find entry "Percentage"
Failed to find entry "Candidate"
------------------------
year : 2002
party : ['RPR', 'FN']
percentage : [82.21, 17.79]
------------------------
Failed to find entry "Nominee"
Failed to find entry "Candidate"
Failed to find entry "Party"
Failed to find entry "Popular vote"
Failed to find entry "Percentage"
Failed to find entry "Candidate"
------------------------
year : 1995
party : ['RPR', 'PS']
percentage : [52.64, 47.36]
------------------------

...

```

## Requirements

- [NumPy](https://numpy.org/)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [pandas](https://pandas.pydata.org/)
- [requests](https://pypi.org/project/requests/)
