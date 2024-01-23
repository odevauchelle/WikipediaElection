import sys
sys.path.append('./../')

import WikipediaElection as WE

url_tail = "/wiki/2002_French_presidential_election"

election_data = WE.fetch_election_data_from_web( url_tail )

for key, value in election_data.items():
    print(key, ':' , value)