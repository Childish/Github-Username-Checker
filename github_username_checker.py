"""
This is a github username checker of sorts. Needed to start using Github so here it is!

    TODO:
        - Add proxy support
        - Handle error messages such as "Whoa there!"
        - Maybe add a proxy scraper?
        - Better outputs
        - :^)
"""
from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import requests
import lxml.html

def read_username_file(file_path):
    """Read lines into a array."""
    with open(file_path, 'r') as loaded_file:
        return loaded_file.read().splitlines()

def check_username(username):
    """Check the username against Github."""
    start_time = time.time()
    session = requests.session()
    request = session.get('https://github.com/join').text
    source = lxml.html.fromstring(request)
    auth_token = source.xpath('//auto-check[@src="/signup_check/username"]/@csrf')[0]
    payload = {'authenticity_token': auth_token, 'value': username}
    result = session.post('https://github.com/signup_check/username', data=payload)
    end_time = int(round((time.time() - start_time) * 1000))
    print("{} has been checked in {} milliseconds".format(username, end_time))

    if b'is already taken' in result.content:
        return username + "\tUNAVAILABLE"
    return username + "\tAVAILABLE"

def main():
    '''Here we handle the loading of the usernames and the executor.'''

    url = 'C:/Users/Sparks/Documents/Python Scripts/Github-Username-Search/'
    usernames = read_username_file(url + "usernames.txt")
    print('Loaded {} usernames.'.format(len(usernames)))

    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(check_username, username) for username in usernames]
        results = []
        for future in as_completed(futures):
            results.append(future.result())

    with open(url + '/output.txt', "w") as file:
        file.write('\n'.join([str(i) for i in results if i is not None]))
    print("Processes finished!")

if __name__ == '__main__':
    main()
