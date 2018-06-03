import pandas as pd
import urllib.parse as urlparse

from webscraper import get_issue_data


def dicts_to_df(dicts):
    rows = []
    for i in range(0, len(dicts)):
        rows.append(pd.DataFrame.from_dict(dicts[i], orient='index').T)
    return pd.concat(rows, axis=0)


def get_all_issue_data(url):
    for i in range(18, 60):
        if i == 1:
            parsed = urlparse.urlparse(url)
            query = urlparse.parse_qs(parsed.query)['q'][0]
            issue_data = get_issue_data(url)
            df = dicts_to_df(issue_data)
            df.to_csv('./metadata/metadata' + query + '-' + str(i) + '.csv')
        elif i > 1:
            try:
                paginate_url = str(url + "&page=" + str(i))
                parsed = urlparse.urlparse(paginate_url)
                query = urlparse.parse_qs(parsed.query)['q'][0]
                issue_data = get_issue_data(paginate_url)
                df = dicts_to_df(issue_data)
                df.to_csv('./metadata/metadata' +
                          query + '-' + str(i) + '.csv')
            except:
                print('all done! at page ', str(i))


x_men_url = "https://www.comics.org/searchNew/?q=marvel+x-men&selected_facets=facet_model_name_exact:issue&selected_facets=country_exact:us&selected_facets=publisher_exact:Marvel"

get_all_issue_data(x_men_url)
