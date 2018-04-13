import pandas as pd

from webscraper import get_issues_from_title

x_men_1990 = get_issues_from_title('6049')
x_men_1991 = get_issues_from_title('593')
x_men_2099 = get_issues_from_title('4019')
x_men_adventures_1992 = get_issues_from_title('2085')
x_men_adventures_1994 = get_issues_from_title('2086')
x_men_adventures_1995 = get_issues_from_title('6047')
x_men_legacy_2008 = get_issues_from_title('17175')
x_men_uncanny_1963 = get_issues_from_title('60')
x_men_unlimited_1993 = get_issues_from_title('893')


def dicts_to_df(issues_from_title):
    rows = []
    for i in range(0, len(issues_from_title)):
        rows.append(pd.concat([
                    pd.DataFrame.from_dict(
                        issues_from_title[i][1], orient='index').T,
                    pd.DataFrame.from_dict(
                        issues_from_title[i][0], orient='index').T],
                    axis=1))
    return pd.concat(rows, axis=0)


x_men_1990_df = dicts_to_df(x_men_1990)
x_men_1990_df['group'] = 'x_men_1990'

x_men_1991_df = dicts_to_df(x_men_1991)
x_men_1991_df['group'] = 'x_men_1991'

x_men_2099_df = dicts_to_df(x_men_2099)
x_men_2099_df['group'] = 'x_men_2099'

x_men_adventures_1992_df = dicts_to_df(x_men_adventures_1992)
x_men_adventures_1992_df['group'] = 'x_men_adventures_1992'

x_men_adventures_1994_df = dicts_to_df(x_men_adventures_1994)
x_men_adventures_1994_df['group'] = 'x_men_adventures_1994'

x_men_adventures_1995_df = dicts_to_df(x_men_adventures_1995)
x_men_adventures_1995_df['group'] = 'x_men_adventures_1995'

x_men_legacy_2008_df = dicts_to_df(x_men_legacy_2008)
x_men_legacy_2008_df['group'] = 'x_men_legacy_2008'

x_men_uncanny_1963_df = dicts_to_df(x_men_uncanny_1963)
x_men_uncanny_1963_df['group'] = 'x_men_uncanny_1963'

x_men_unlimited_1993_df = dicts_to_df(x_men_unlimited_1993)
x_men_unlimited_1993_df['group'] = 'x_men_unlimited_1993'

df = pd.concat([x_men_1990_df,
                x_men_1990_df,
                x_men_2099_df,
                x_men_adventures_1992_df,
                x_men_adventures_1994_df,
                x_men_adventures_1995_df,
                x_men_legacy_2008_df,
                x_men_uncanny_1963_df,
                x_men_unlimited_1993_df], axis=0)


df.to_csv('../metadata/metadata.csv')
