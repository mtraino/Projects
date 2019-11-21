# imports
import csv
import json
import time
import requests

# url for virus total to call when using your api key and hashes to get a report
url = 'https://www.virustotal.com/vtapi/v2/file/report'

# path to the location of the hashs you want to run against virus total
path_to_hash = '$PATH_TO_HASHS.csv'
# your api key that will be sent with each hash request
apikey = '$API_KEY'
# output file to store all the json results from the hash report
outfile_name = 'output.json'
# declaring variables to store the hashes and the hash results in a list and dictionary format respectively
hash_results = {}

# reading in hashes from
with open(path_to_hash, 'r') as f:
    reader = csv.reader(f)
    hashes = list(reader)

# running the hashes through virus total using your api key and the hash
for i in range(len(hashes)):
    temp = hashes[i]
    params = {'apikey': apikey, 'resource': temp}  # setting parameters to pass to virus total
    response = requests.get(url, params=params)  # passing api key hash to the virus total site
    hash_results[i] = response.json()  # saving hash result into a table with the hash being linked to the output
    # print(response.json()) If you want to print out the results as they are returned
    time.sleep(15)

# saving the dictionary of hashes and results to a file with a json format
with open(outfile_name, 'w') as outfile:
    json.dump(hash_results, outfile)
