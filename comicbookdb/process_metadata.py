import numpy as np
import pandas as pd

metadata = pd.read_csv('../metadata/metadata.csv')
characters = pd.read_csv('../metadata/characters.csv')
character_list = characters['link'].unique().tolist()


def marvel_characters(issue_character_list):
    d = {}
    for character in character_list:
        d[character] = character in issue_character_list
    return d


rows = []
for i in range(0, len(metadata)):
    print(i)
    if metadata['characters'][i] is np.nan:
        pass
    else:
        issue_characters = marvel_characters(metadata['characters'][i])

        def character_dicts_to_df(characters):
            return pd.DataFrame.from_dict(characters, orient='index').T
        d = character_dicts_to_df(issue_characters)
        d['issue'] = metadata['issue'][i]
        d['title'] = metadata['title'][i]
        d['group'] = metadata['group'][i]
        rows.append(d)

character_df = pd.concat(rows, axis=0).\
    replace(False, np.nan).\
    dropna(axis=1, how='all').\
    fillna(0.0)


df = pd.merge(
    metadata, character_df, how='left', on=['issue', 'title', 'group'])


format_split = pd.DataFrame(
    df['format'].map(lambda x: x.split(';')).tolist(),
    columns = ['format_color', 'format_book', 'format_no_pages'])

df = pd.concat([df, format_split], axis=1)

df = df.drop(['Unnamed: 0', 'format', 'characters'], axis=1)


df['image_file_name'] =  df['issue'] + '_' + df['title'] + '_' + df['arc'] + '_' + df['cover_date'] + '.jpg'


df.to_csv('../metadata/final_metadata.csv')
