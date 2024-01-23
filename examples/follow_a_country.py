import sys
sys.path.append('./../')

import WikipediaElection as WE

url_tail = "/wiki/2002_French_presidential_election"
while True :

    election = WE.fetch_election_data_from_web( url_tail )

    print('------------------------')

    for key in ['year','party', 'percentage']: #election.keys():#['candidate','percentage']: # 
        print( key, ':' , election[key])

    print('------------------------')

    url_tail = election['link_to_previous_election']

    if url_tail is None :
        print('Wikipedia time series stops here.')
        break