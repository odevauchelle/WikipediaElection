# from pylab import *
from numpy import array, nan
from bs4 import BeautifulSoup
from pandas import read_html
import re
import requests

default_entries = {
    'nominee': 'Nominee',
    'candidate': 'Candidate',
    'party': 'Party',
    'popular_vote': 'Popular vote',
    'percentage': 'Percentage',
}

def extract_lines_from_pandas_table( table, entries = None ) :

    if entries is None :
        entries = default_entries

    election_data = {}

    for entry_key, entry_value in entries.items() :
        try :
            line = array( table[ table[0] == entry_value ].iloc[[0]] )
            # print(line)
            line = line[ line == line ]
            election_data[ entry_key ] = list( line[1:] )
        except :
            print('Failed to find entry "' + entry_value + '"' )
            pass

    return election_data

def get_date_from_title( title ):

    year = None

    for word in title.split():
        try :
            year = int( word.split('–')[0] )
            break
        except :
            pass

    return year

def get_link_to_previous_election( webpage, left_arrow = None ) :

    if left_arrow is None :
        left_arrow = '←'

    try :
        return webpage.find( text = re.compile( left_arrow ) ).next_element.get('href')
    except :
        return None

def get_last_edition_time( webpage ) :
    try :
        return webpage.find('li', id="footer-info-lastmod" ).text.split(' This page was last edited on ')[-1].split('.')[0]
    except :
        return None

def get_canonical_link( webpage ) :

    try :
        return webpage.find('link', rel = 'canonical' ).get('href')
    except :
        return None


def convert_popular_vote( popular_vote_string ) :
    try :
        return int( popular_vote_string )
    except :
        try :
            return int(  popular_vote_string.split('[')[0].replace(',','').replace('.','') ) # if there is a footnote mark, like [1]
        except :
            return nan

def convert_percentage( percentage_string ):

    try :
        return float( percentage_string.replace('%','') )
    except :
        return nan

def get_info_from_summary_box( summary_box ) :

    election_data = {}

    for table in read_html( summary_box.prettify() ):

        new_data = extract_lines_from_pandas_table( table )

        if len(new_data) > 0 :
            election_data.update( new_data )
            break

    try :
        election_data['popular_vote'] = [ convert_popular_vote( popular_vote ) for popular_vote in election_data['popular_vote'] ]
    except :
        print('Could not convert popular vote to integer.')

    try :
        election_data['percentage'] = [ convert_percentage( percentage ) for percentage in election_data['percentage'] ]
    except :
        print('Could not convert percentage to float.')

    return election_data

def get_info_from_webpage( webpage ) :

    # for span_tag in webpage.findAll('span'):
    #     span_tag.replace_with('') # span tags somtimes mess with pandas read_html

    election_data = {
        'title' : webpage.title.string,
        'link_to_previous_election' : get_link_to_previous_election( webpage ),
        'last_edition_time' : get_last_edition_time( webpage ),
        'href' : get_canonical_link( webpage )
        }

    election_data.update( { 'year' : get_date_from_title( election_data['title'] ) } )


    for summary_box in webpage.find_all( "tbody" ) : # this should be the small upper right table. Not always the same one

        try :

            summary_box_data = get_info_from_summary_box( summary_box )

            if len( summary_box_data ) > 0 :
                    election_data.update( summary_box_data )
                    break

        except :
            print('Could not find a summary_box with useful data.')

    return election_data


def fetch_election_data_from_web( url_tail, url_base = None ) :

    if url_base is None :
        url_base = "https://en.wikipedia.org"

    request = requests.get( url_base + url_tail, allow_redirects = True )

    webpage = BeautifulSoup( request.content, 'html.parser' )

    election_data = get_info_from_webpage( webpage )

    return election_data



if __name__ == '__main__' :

    url_tail = "/wiki/2002_French_presidential_election"
    # url_tail = "/wiki/1992_Austrian_presidential_election"
    # url_tail = "/wiki/2020_Icelandic_presidential_election"

    # url_base = "https://en.wikipedia.org"
    # request = requests.get( url_base + url_tail, allow_redirects = True )
    # with open( 'webpage.html', 'w') as webpage_file :
    #     webpage_file.write( request.content.decode() )
    #
    # with open( 'webpage.html' ) as webpage_file :
    #     election_data = get_info_from_webpage( webpage_file )

    election_data = fetch_election_data_from_web( url_tail )

    for key, value in election_data.items():
        print(key, ':' , value)
