import urllib.request

from bs4 import BeautifulSoup
from contextlib import closing
from requests import get
from requests.exceptions import RequestException


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

############################################################################
# Get Title Links
############################################################################


############################################################################
# Get Title Issue Links and Metadata
############################################################################

# TODO: add pagination
# "https://www.comics.org/searchNew/?q=marvel+x-men&selected_facets=facet_model_name_exact:issue&selected_facets=country_exact:us&selected_facets=publisher_exact:Marvel&page=2"

raw_html = simple_get(
    "https://www.comics.org/searchNew/?q=marvel+x-men&selected_facets=facet_model_name_exact:issue&selected_facets=country_exact:us&selected_facets=publisher_exact:Marvel")

html = BeautifulSoup(raw_html, 'html.parser')

table_rows = []
for tr in html.select('tr'):
    table_rows.append((tr.text, tr.a))

table_rows = list(filter(lambda x: "ISSUE" in x[0], table_rows))


############################################################################
# Get Issue Cover Images and Meta-data
############################################################################


def get_issue_html(href):
    url = 'https://www.comics.org' + href
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, 'html.parser')
    return html


# set([tag.name for tag in issue_html.find_all()])

issue_html = get_issue_html(table_rows[21][1]['href'])


def get_issue_title(issue_html):
    issue_title = issue_html.select('title')[0].text.\
        replace('\n', '').\
        split('::')[2].\
        strip()
    return issue_title


def get_issue_cover_img(issue_html, save_directory):
    issue_title = get_issue_title(issue_html)
    href = issue_html.find("div", {"class": "cover"}).\
        find("div", {'coverImage'}).a['href']
    url = 'https://www.comics.org' + href
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, 'html.parser')
    images = html.select('img')
    cover_images = list(filter(lambda x:
                               'files1.comics.org//img/' in x['src'], images))
    cover_image = cover_images[0]['src']
    save_to = save_directory + issue_title + '.jpg'
    urllib.request.urlretrieve(cover_image, save_to)
    return save_to


def get_cover_metadata(issue_html):
    metadata = issue_html.find("div", {"class": "cover"}).\
                          find("div", {'coverContent'})
    metadata_labels = list(map(lambda x:
                           x.text.replace(':', '').strip().lower(),
                           metadata.findAll("span", {'credit_label'})))
    metadata_values = list(map(lambda x:
                           x.text.replace(' ?', '').strip(),
                           metadata.findAll("span", {'credit_value'})))
    return dict(zip(metadata_labels, metadata_values))


get_issue_title(issue_html)
get_issue_cover_img(issue_html, './covers')
get_cover_metadata(issue_html)

get_cover_metadata(issue_html)['characters']

# df.to_csv('../metadata/characters.csv')
