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

raw_html = simple_get("http://www.comicbookdb.com/title.php?ID=6049")

html = BeautifulSoup(raw_html, 'html.parser')


# TODO: can we find this using a table tag, like "th" or "td"?
table_header = '\nIssue\n\xa0\nTitle\n\xa0\nStory Arc\n\xa0\nCover Date\n'

table_footer = '\n\n\n\n\n          © 2005-2018 ComicBookDB.com - Terms and Conditions - Privacy Policy - DMCA\n\n\n          Special thanks to Brian Wood for the ComicBookDB.com logo design\n        \n\n\n\n\n'

table_rows = []
for tr in html.select('tr'):
    table_rows.append((tr.text, tr.a))

table_header_index = list(map(lambda x: x[0] == table_header, table_rows))
table_header_index = [i for i, x in enumerate(table_header_index) if x][0]

table_footer_index = list(map(lambda x: x[0] == table_footer, table_rows))
table_footer_index = [i for i, x in enumerate(table_footer_index) if x][0]

table = table_rows[(table_header_index + 1):table_footer_index]


def parse_table(row):
    return list(map(
        lambda x: x.replace('\n', '').strip(), row[0].split('\xa0'))) + [row[1]['href']]


issues = list(map(lambda x:
                  dict(zip(['issue', 'title', 'arc', 'cover_date', 'href'],
                           parse_table(x))),
                  table))

############################################################################
# Get Issue Cover Images and Meta-data
############################################################################


def get_issue_link(issue_dict):
    return 'http://www.comicbookdb.com/' + issue_dict['href']


raw_new_html = simple_get(get_issue_link(issues[41]))

new_html = BeautifulSoup(raw_new_html, 'html.parser')

###############
# Get metadata

new_table_rows = []
for tr in new_html.body.select('tr'):
    new_table_rows.append((tr.text, tr.a))

from itertools import compress

fil = list(map(lambda x: "Writer(s):" in x[0], new_table_rows))

# TODO: use the "href" to validate metadata selection instead of grabbing [1]
metadata = list(compress(new_table_rows, fil))


def parse_metadata(metadata):
    desc = metadata[0][0]
    artist_index = desc.find("Cover Artist(s):")
    price_index = desc.find("Cover Price:")
    tagline_index = desc.find("Issue Tagline:")
    format_index = desc.find("Format:")
    arc_index = desc.find("Story Arc(s):")
    characters_index = desc.find("Characters:")
    artist = desc[artist_index:].\
        split('\n')[0].\
        split("Cover Artist(s):")[1].\
        strip()
    price = desc[price_index:].\
        split('\n')[0].\
        split("Cover Price:")[1].\
        strip()
    tagline = desc[tagline_index:].\
        split('\n')[0].\
        split("Issue Tagline:")[1].\
        strip()
    format = desc[format_index:].\
        split('\n')[0].\
        split("Format:")[1].\
        split(' Arc(s)')[0].\
        strip()
    arc = desc[arc_index:].\
        split('\n')[0].\
        split("Story Arc(s):")[1].\
        split('\xa0\xa0\xa0\xa0')[1]
    characters = desc[characters_index:].\
        split("Characters:")[1].split('\n\n')[1].\
        strip()
    return dict(zip(
        ('artist', 'price', 'tagline', 'format', 'arc', 'characters'),
        (artist, price, tagline, format, arc, characters)))

###############
# Get cover image


new_image_rows = []
for img in new_html.select('img'):
    new_image_rows.append((img, img.a))

new_fil = list(
    map(lambda x: 'graphics/comic_graphics' in x[0]['src'], new_image_rows))

# TODO: use the "href" to validate metadata selection instead of grabbing [1]
image = list(compress(new_image_rows, new_fil))[0][0]['src']


def get_issues_from_title(title_id):
    url = 'http://www.comicbookdb.com/title.php?ID=' + str(title_id)
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, 'html.parser')
    table_header = '\nIssue\n\xa0\nTitle\n\xa0\nStory Arc\n\xa0\nCover Date\n'
    table_footer = '\n\n\n\n\n          © 2005-2018 ComicBookDB.com - Terms and Conditions - Privacy Policy - DMCA\n\n\n          Special thanks to Brian Wood for the ComicBookDB.com logo design\n        \n\n\n\n\n'
    table_rows = []
    for tr in html.select('tr'):
        table_rows.append((tr.text, tr.a))
    table_header_index = list(map(lambda x: x[0] == table_header, table_rows))
    table_header_index = [i for i, x in enumerate(table_header_index) if x][0]
    table_footer_index = list(map(lambda x: x[0] == table_footer, table_rows))
    table_footer_index = [i for i, x in enumerate(table_footer_index) if x][0]
    table = table_rows[(table_header_index + 1):table_footer_index]
    issues = list(map(lambda x:
                      dict(zip(['issue', 'title', 'arc', 'cover_date', 'href'],
                               parse_table(x))),
                      table))
    for i in list(range(0, len(issues))):
        if 'javascript:blocking(' in issues[i]['href']:
            id = issues[i]['href'].split('issue_')[1].split("', ")[0]
            issues[i]['href'] = 'issue.php?ID=' + str(id)
    scraped_issues = []
    for issue in issues:
        if issue['issue'] == '':
            continue
        else:
            try:
                raw_new_html = simple_get(get_issue_link(issue))
                new_html = BeautifulSoup(raw_new_html, 'html.parser')
                new_table_rows = []
                for tr in new_html.body.select('tr'):
                    new_table_rows.append((tr.text, tr.a))
                from itertools import compress
                fil = list(map(lambda x: "Writer(s):" in x[0], new_table_rows))
                metadata = list(compress(new_table_rows, fil))
                issue_metadata = parse_metadata(metadata)
                scraped_issues.append((issue_metadata, issue))
                ###############
                # Get cover image
                new_image_rows = []
                for img in new_html.select('img'):
                    new_image_rows.append((img, img.a))
                new_fil = list(map(
                    lambda x: 'graphics/comic_graphics' in x[0]['src'],
                    new_image_rows))
                image = list(compress(new_image_rows, new_fil))[0][0]['src']
                large_image = image.split('_thumb.')[0] + '_large.' + image.split('.')[1]
                image_prefix = (issue['issue'] + '_' +
                                issue['title'] + '_' +
                                issue['arc'] + '_' +
                                issue['cover_date'])
                print('http://www.comicbookdb.com/' + str(large_image))
                urllib.request.urlretrieve(
                    'http://www.comicbookdb.com/' + str(large_image),
                    '../covers/' + str(image_prefix) + ".jpg")
                print(issue)
            except:
                continue
    return scraped_issues


def get_character_list(url):
    url = 'http://comicbookdb.com/search.php?form_search=Marvel&form_searchtype=Character'
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, 'html.parser')

    table_rows = []
    for tr in html.body.select('tr'):
        table_rows.append((tr.text))
