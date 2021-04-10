#################################
##### Name: Maia O'Meara
##### Uniqname: maiao
#################################

from bs4 import BeautifulSoup
import requests
import json
import secrets # file that contains your API key


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

    # Accessing NPS site for relevant data
    url = 'https://www.nps.gov/index.htm'
    response = requests.get(url)
    nps_index_text = BeautifulSoup(response.text, 'html.parser')
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
    response = requests.get(url)
    nps_site_text = BeautifulSoup(response.text, 'html.parser')

    # Accessing relevant data for NationalSites class, if statements confirm data exist and creates a blank field if not
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
    pass


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
    pass

park = get_site_instance('https://www.nps.gov/yose/index.htm')
print(park.info())



# <div class="Hero-titleContainer clearfix">
# <a href="/isro/" class="Hero-title " id="anch_10">Isle Royale</a>
# <div class="Hero-designationContainer">
# <span class="Hero-designation">National Park</span>
# <span class="Hero-location">Michigan</span>
# </div>
# </div>

# site = NationalSite(name, address, zipcode, phone, category)

if __name__ == "__main__":
    pass