#################################
##### Name: Maia O'Meara
##### Uniqname: maiao
#################################

from bs4 import BeautifulSoup
import requests
import json
import secrets # file that contains your API key

CACHE_FILENAME = "nps_cache.json"

def open_cache():
    ''' opens the cache file if it exists and loads the JSON into
    a dictionary, which it then returns.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()

NPS_CACHE = open_cache()

class NationalSite:
    '''a national site

    Instance Attributes
    -------------------
    category: string
        the category of a national site (e.g. 'National Park', '')
        some sites have blank category.

    name: string
        the name of a national site (e.g. 'Isle Royale')

    address: string
        the city and state of a national site (e.g. 'Houghton, MI')

    zipcode: string
        the zip-code of a national site (e.g. '49931', '82190-0168')

    phone: string
        the phone of a national site (e.g. '(616) 319-7906', '307-344-7381')
    '''
    def __init__(self, category, name, address, zipcode, phone):
        self.category = category
        self.name = name
        self.address = address
        self.zipcode = zipcode
        self.phone = phone

    def info(self):
        return self.name + ' (' + self.category + '): ' + self.address + ' ' + self.zipcode


def build_state_url_dict():
    ''' Make a dictionary that maps state name to state page url from "https://www.nps.gov"

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is a state name and value is the url
        e.g. {'michigan':'https://www.nps.gov/state/mi/index.htm', ...}
    '''
    # Setting up objects for dictionary
    endpoint = "https://www.nps.gov"
    state_name = []
    state_url = []
    state_url_dict = {}
    url = 'https://www.nps.gov/index.htm'

    # Accessing NPS site for relevant data
    if url in NPS_CACHE:
        print('Using Cache')
    else:
        print('Fetching')
        response = requests.get(url)
        NPS_CACHE[url] = response.text
        save_cache(NPS_CACHE)

    nps_index_text = BeautifulSoup(NPS_CACHE[url], 'html.parser')

    all_list_items = nps_index_text.find('ul', {'class': 'dropdown-menu SearchBar-keywordSearch'}).find_all('a')

    for item in all_list_items:
        state_url.append(item.get('href'))
        state_name.append(item.text.strip().lower())

    # Creating dictionary
    for i in range(len(state_name)):
        state_url_dict[state_name[i]] = endpoint + state_url[i]

    return state_url_dict


def get_site_instance(site_url):
    '''Make an instances from a national site URL.

    Parameters
    ----------
    site_url: string
        The URL for a national site page in nps.gov

    Returns
    -------
    instance
        a national site instance
    '''
    url = site_url

    if url in NPS_CACHE:
        print('Using Cache')
    else:
        print('Fetching')
        response = requests.get(url)
        NPS_CACHE[url] = response.text
        save_cache(NPS_CACHE)

    nps_site_text = BeautifulSoup(NPS_CACHE[url], 'html.parser')

    # Accessing relevant data for NationalSites class, 'if' statements confirm data exist and create a blank field if not
    if nps_site_text.find('div', {'class': 'Hero-titleContainer clearfix'}).find('a'):
        name = nps_site_text.find('div', {'class': 'Hero-titleContainer clearfix'}).find('a').text.strip()
    else:
        name = ' '

    if nps_site_text.find('span', {'class': 'Hero-designation'}):
        category = nps_site_text.find('span', {'class': 'Hero-designation'}).text.strip()
    else:
        category = ' '

    if nps_site_text.find('span', {'class': 'Hero-location'}):
        state = nps_site_text.find('span', {'class': 'Hero-location'}).text.strip()
    else:
        state = ' '
    if nps_site_text.find('span', {'itemprop': 'addressLocality'}):
        city = nps_site_text.find('span', {'itemprop': 'addressLocality'}).text.strip()
    else:
        city = ' '
    if nps_site_text.find('span', {'itemprop': 'addressRegion'}):
        state_abrv = nps_site_text.find('span', {'itemprop': 'addressRegion'}).text.strip()
    else:
        state_abrv = ' '

    address = city + ', ' + state_abrv

    if nps_site_text.find('span', {'itemprop': 'postalCode'}):
        zipcode = nps_site_text.find('span', {'itemprop': 'postalCode'}).text.strip()
    else:
        zipcode = ' '

    if nps_site_text.find('span', {'itemprop': 'telephone'}):
        phone = nps_site_text.find('span', {'itemprop': 'telephone'}).text.strip()
    else:
        phone = ' '

    # Creating a full site
    site = NationalSite(category=category, name=name, address=address, zipcode=zipcode, phone=phone)

    return site


def get_sites_for_state(state_url):
    '''Make a list of national site instances from a state URL.

    Parameters
    ----------
    state_url: string
        The URL for a state page in nps.gov

    Returns
    -------
    list
        a list of national site instances
    '''
    site_urls = []
    site_list = []

    if state_url in NPS_CACHE:
        print('Using Cache')
    else:
        print('Fetching')
        response = requests.get(state_url)
        NPS_CACHE[state_url] = response.text
        save_cache(NPS_CACHE)

    nps_state_text = BeautifulSoup(NPS_CACHE[state_url], 'html.parser')
    site_keys = nps_state_text.find('ul', {'id': 'list_parks'}).find_all('h3')
    for key in site_keys:
        site_url = 'https://www.nps.gov' + key.find('a').get('href') + 'index.htm'
        site_urls.append(site_url)
    for url in site_urls:
        site_list.append(get_site_instance(url))

    return site_list


def get_nearby_places(site_object):
    '''Obtain API data from MapQuest API.

    Parameters
    ----------
    site_object: object
        an instance of a national site

    Returns
    -------
    dict
        a converted API return from MapQuest API
    '''
    #Constructing request URL
    baseurl = 'http://www.mapquestapi.com/search/v2/radius'
    params = {
        'key': secrets.API_KEY,
        'origin': site_object.zipcode,
        'radius': 10,
        'maxMatches': 10,
        'ambiguities': 'ignore',
        'outFormat': 'json'
    }
    param_strings = []
    connector = '_'
    for key in params.keys():
        param_strings.append(f'{key}_{params[key]}')
    param_strings.sort()
    site_key = baseurl + connector + connector.join(param_strings)

    # Using the cache

    if site_key in NPS_CACHE.keys():
        print("Using cache", site_key)
    else:
        print("Fetching", site_key)
        NPS_CACHE[site_key] = requests.get(baseurl, params=params).json()
        save_cache(NPS_CACHE)

    results = NPS_CACHE[site_key]['searchResults']
    print('-------------------------------------')
    print('Places near', site_object.name)
    print('-------------------------------------')
    mapquest_results = {}
    for result in results:
        result_dict = {}
        if result['fields']['name'] == '':
            result_dict['name'] = 'no name'
        else:
            result_dict['name'] = result['fields']['name']
        if result['fields']['group_sic_code_name'] == '':
            result_dict['category'] = 'no category'
        else:
            result_dict['category'] = result['fields']['group_sic_code_name']
        if result['fields']['address'] == '':
            result_dict['address'] = 'no address'
        else:
            result_dict['address'] = result['fields']['address']
        if result['fields']['city'] == '':
            result_dict['city'] = 'no city'
        else:
            result_dict['city'] = result['fields']['city']
        mapquest_results[result['fields']['name']] = result_dict
        print('- '+ result_dict['name'] +' (' + result_dict['category'] + '): ' + result_dict['address'] + ', ' + result_dict['city'])

    return mapquest_results


if __name__ == "__main__":
    state_url_dict = build_state_url_dict()
    # Step 1 & Step 2
    state_input = input("Enter a state name or 'Exit': ")

    while True:
        if state_input.lower() == 'exit':
            quit()
        elif state_input.lower() in state_url_dict.keys():
            state_sites = get_sites_for_state(state_url_dict[state_input.lower()])
            print('-------------------------------------')
            print('List of National Sites in', state_input.title())
            print('-------------------------------------')
            for site in state_sites:
                index = state_sites.index(site)+1
                print('[' + str(index) + '] ' + site.info())
            while True:
                site_num = input("Enter a number for detailed search or 'Exit' or 'Back':  ")
                if site_num.lower() == 'back':
                    state_input = input("Enter a state name or 'Exit': ")
                    break
                elif site_num.lower() == 'exit':
                    quit()
                else:
                    while not (site_num.isnumeric() and
                        int(site_num) <= len(state_sites)):
                        print("Invalid input.")
                        site_num = input("Enter a number for detailed search or 'exit' or 'back': ")
                    get_nearby_places(state_sites[(int(site_num)-1)])
        else:
            state_input = input("That is not a state. Enter a state name or 'Exit':  ")