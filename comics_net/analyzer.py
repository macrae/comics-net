import difflib
import os
import random
import re
from pathlib import Path
from shutil import copyfile
from typing import List, Union

import jsonlines
import numpy as np
import pandas as pd
from pandas import DataFrame
from PIL import Image, ImageEnhance, ImageFilter

# flatten a list of lists
flatten = lambda l: [item for sublist in l for item in sublist]


def resize_im(im: Image, dims: tuple) -> Image:
    """
    Given a PIL image return the resized image to the given dimensions.
    """
    return im.resize(dims)


def save_im(im: Image, save_to: str, im_type: str = "jpeg") -> None:
    """
    Given a PIL image and a directory save the image to the directory; default to
    jpeg as the image format type.
    """
    im.save(save_to, im_type)


# TODO: deprecate this method in favor of load_jsonl()
def load_metadata(metadata_path: str) -> DataFrame:
    """
    Given a path to some metadata return the metadata in a DataFrame.
    """
    logged_metadata = []

    with jsonlines.open(metadata_path, mode="r") as reader:
        for item in reader:
            logged_metadata.append(item)

    return pd.DataFrame(logged_metadata)


def get_issue_number_from_title(title: str) -> Union[int, None]:
    """
    Given an issue title return the issue number from the string.
    """
    issue = re.search(r"([#?])(\d+)\b", title.replace(",", ""))
    if issue is None:
        return np.nan
    else:
        return np.int(issue.group().replace("#", ""))


def match_brackets(characters: str) -> dict:
    """
    Given a string return a dict identifying the span of bracketed text
    in the string, where
    """
    p = re.compile(r"\[(.*?)\]")
    matches = {}
    for m in p.finditer(characters):
        matches[m.group()] = {"start": m.start(), "end": m.end()}
    return matches


def replace_semicolons_in_brackets(characters: str):
    """
    Some character aliases contain a semicolon, for example: Superman [Clark Kent; Kal-El].
    Because we use semicolons as a character delimiter, we need to find and replace
    instances where the semicolon is not a character delimiter.
    """
    p = re.compile(r"\[(.*?)\]")
    matches = []
    for m in p.finditer(characters):
        matches.append((m.start(), m.end(), m.group()))
    for match in matches:
        substring = characters[match[0] : match[1]]
        if substring.count(";") == 1 and (
            ("also as" in substring)
            | ("Kal-El" in substring)
            | ("Kal-L" in substring)
            | ("Kara Zor-El" in substring)
            | ("Martin Stein" in substring)
            | ("Etrigan" in substring)
            | ("James Howlett" in substring)
            | ("Gwendolyne Stacy" in substring)
            | ("Gwen Stacy" in substring)
            | ("Katar Hol" in substring)
            | ("Shayera Hol" in substring)
            | ("Kon-El" in substring)
            | ("Laura Kinney" in substring)
            | ("Kory Ander" in substring)
            | ("Bruce Banner" in substring)
            | ("Eobard Thawne" in substring)
            | ("Victor von Doom" in substring)
            | ("as Cat-Woman" in substring)
            | ("also as Task Force X" in substring)
            | ("Diana Prince" in substring)
            | ("Nathan Dayspring" in substring)
            | ("Susan Storm; Susan Richards" in substring)
            | ("Warren Worthington III" in substring)
            | ("Copycat" in substring)
            | ("Tornado Tyrant" in substring)
            | ("Bro'Dee Walker" in substring)
            | ("Ke'Haan" in substring)
            | ("Flash; Barry Allen" in substring)
            | ("Jennie-Lynn Hayden" in substring)
            | ("Donald Blake" in substring)
            | ("Thor Odinson; " in substring)
        ):
            characters = characters.replace(substring, substring.replace(";", "/"))
        if substring.count(";") > 1:
            pass
    return characters


def look_behind(s: str, end_idx: int) -> str:
    """
    Given a string containing semi-colons, find the span of text after the last
    semi-colon.
    """
    span = s[: (end_idx - 1)]
    semicolon_matches = [
        (m.group(), m.start(), m.end()) for m in re.finditer(r"(?<=(;))", span)
    ]
    if len(semicolon_matches) == 0:
        start_idx = 0
    else:
        start_idx = semicolon_matches[-1][2]
    return span[start_idx:end_idx].strip()


def convert_character_dict_to_str(character_dict: dict) -> str:
    """
    Given a character dict return it as a string that is comparable to how the
    set of characters are encoded in a character string.
    """
    return (
        str(character_dict["Teams"])
        .replace("{", "")
        .replace("}", "")
        .replace("'", "")
        .replace(",", ";")
    )


def diff_strings(string1, string2):
    """
    Given two strings, compute the character difference of string2 less string1.
    Notice that order matters,  e.g. string1 - string2 may not equal string2 - string1.
    """
    diff = ""
    for idx, val in enumerate(difflib.ndiff(string1, string2)):
        if val[0] == "+":
            diff += val[2]
    return diff


def convert_characters_to_list(characters: str) -> list:
    """
    Given a character string return the parsed list of unique characters.
    """
    t = replace_semicolons_in_brackets(characters)

    stack = 0
    startIndex = None
    results = []

    # TODOL: pull this out into it's own function
    matches = []
    for i, c in enumerate(t):
        if c == "[":
            if stack == 0:
                startIndex = i + 1  # string to extract starts one index later

            # push to stack
            stack += 1
        elif c == "]":
            # pop stack
            stack -= 1

            if stack == 0:
                matches.append((startIndex, i))
                results.append(t[startIndex:i])

    character_dict: dict = {}
    character_dict["Teams"] = {}
    character_dict["Individuals"] = {}

    for span in matches:
        entity = t[span[0] : span[1]]
        if entity.count(";") == 0:
            person_name = look_behind(t, span[0])
            person_identity = entity
            character_dict["Individuals"][person_name] = person_identity

        elif entity.count(";") > 1:
            team_name = look_behind(t, span[0])
            team_members = list(filter(lambda x: x != "", entity.split("; ")))
            character_dict["Teams"][team_name] = team_members

    team_string = convert_character_dict_to_str(character_dict)

    remainder = diff_strings(team_string, t)

    remainder = list(filter(lambda x: x != "", remainder.split("; ")))

    character_dict["Individuals"] = remainder

    character_list = []
    for k in character_dict["Teams"]:
        character_list.append(character_dict["Teams"][k])

    character_list.append(character_dict["Individuals"])

    return flatten(character_list)


def get_random_sample_of_covers(df_covers: DataFrame, character: str, n: int) -> dict:
    """
    Given a DataFrame of covers (TODO: specify that schema) and a character return a
    dict (TODO: specify that schema) of n randomly sampled covers for that character.
    """
    df_covers = df_covers[
        df_covers["cover_characters_list_aliases"].apply(lambda x: character in x)
    ].reset_index(drop=True)
    s = list(range(0, max(df_covers.index)))
    random.shuffle(s)

    covers: dict = dict()
    for i in s[:n]:
        covers["cover_{}".format(i)] = {}

        image_path = df_covers["save_to"].iloc[i]
        characters = df_covers[df_covers["save_to"] == image_path][
            "cover_characters_list_aliases"
        ].iloc[0]
        synopsis = df_covers["synopsis"].iloc[i]

        covers["cover_{}".format(i)]["image_path"] = image_path
        covers["cover_{}".format(i)]["characters"] = characters
        covers["cover_{}".format(i)]["synopsis"] = synopsis

    return covers


# TODO:  add option to create dataset using this pattern...
# path\
#   train\
#     clas1\
#     clas2\
#     ...
#   valid\
#     clas1\
#     clas2\
#     ...
#   test\


def create_training_dirs(
    df_cover_characters: DataFrame, characters_dict: dict, save_dir: str
):
    """
    Given a DataFrame of covers (TODO: specify that schema) and a dict of characters to
    create a dataset for, create two directories  (images/ & annotations/) containing
    randomly sampled covers from those characters w/ annotations (labels & synopses).
    """
    cover_samples = {}
    for character in characters_dict:
        cover_samples[character] = get_random_sample_of_covers(
            df_cover_characters, character, n=characters_dict[character]
        )
        for cover in cover_samples[character]:
            indices = [
                1 if x in cover_samples[character][cover]["characters"] else 0
                for x in list(characters_dict.keys())
            ]
            cover_samples[character][cover]["label"] = [
                x[0]
                for x in filter(
                    lambda x: x[1] == 1, zip(characters_dict.keys(), indices)
                )
            ]

    all_dicts = []

    for hero_key in cover_samples.keys():
        for cover_key in cover_samples[hero_key].keys():
            title = (
                cover_samples[hero_key][cover_key]["image_path"].split("/")[-1].strip()
            )

            all_dicts.append(
                {
                    "id": title,
                    "label": cover_samples[hero_key][cover_key]["label"],
                    "image_path": cover_samples[hero_key][cover_key]["image_path"],
                }
            )

    dicts = list({v["id"]: v for v in all_dicts}.values())
    random.shuffle(dicts)
    print(
        "We started with {} covers. After de-duping for character overlap we have {}.".format(
            len(all_dicts), len(dicts)
        )
    )

    if not os.path.exists(save_dir):
        os.makedirs(save_dir + "/images")

    for cover in dicts:

        save_image_to = save_dir + "/images/" + str(cover["id"]).replace("\t", " ")

        im = Image.open("." + cover["image_path"])
        im = resize_im(im, dims=(400, 600))

        # save image
        save_im(im, save_image_to, im_type="jpeg")

        # write annotations/labels (if not imagenet style)
        name = str(cover["id"]).replace("\t", " ")
        label = (
            str(cover["label"])
            .replace("[", "")
            .replace("]", "")
            .replace("'", "")
            .replace(", ", "|")
            .strip()
        )
        record = [name, label]
        if len(record) == 2:
            # save label
            with open(save_dir + "/labels.txt", "a") as f:
                f.write("\t".join(record))
                f.write("\n")
        else:
            print("wtf happend?")
            print(record)


# TODO: update file_name to take an os.path in lieu of a string
def search_row(file_name: str, string: str) -> Union[int, None]:
    """Searches a file for the first row containing a string and returns the row index.
    If no match is found returns None.

    Args:
        file_name: path to file
        string: substring to find

    Returns:
        int: first row containing substring
    """
    with open(file_name, "r") as f:
        for i, row in enumerate(f):
            if string in row:
                return i
    return None


# TODO: update file_name to take an os.path in lieu of a string
def replace_line(file_name: str, row: int, text: str) -> None:
    """Replaces a row in a file with the text.

    Args:
        file_name: path to file to update
        row: index to update
        text: text to update

    Returns:
        None: this method has side-effects
    """
    lines = open(file_name, "r").readlines()
    lines[row] = text + "\n"
    out = open(file_name, "w")
    out.writelines(lines)
    out.close()


def update_label(image_bunch: str, file_name: str, label: List[str]) -> None:
    """Given an image bunch directory, the file name of an image, and a label to update
    the image bunch with, update the labels file with the new label.

    Args:
        image_bunch: directory to image bunch
        file_name: name of image to update label of
        label: new label

    Returns:
        None: this method has side-effects
    """
    labels = image_bunch + "labels.txt"
    labels_updated = image_bunch + "labels_updated.txt"

    # check if labels_updated.txt exists, if not then create it
    if not os.path.exists(labels_updated):
        copyfile(labels, labels_updated)

    # check if file_name exists in labels_updated.txt, if not then Exception
    row_index = search_row(labels, file_name)

    # update row in labels_updated.txt replacing existing label, with new_label
    new_label = (
        str(label).replace("[", "").replace("]", "").replace("'", "").replace(", ", "|")
    )

    record = [file_name, new_label]
    row_update = "\t".join(record)

    replace_line(labels_updated, row_index, row_update)


def remove_images(image_bunch: str, files_to_exclude: List[str]) -> None:
    """Given an image bunch and a list of files to exclude, create a new image bunch
    excluding the given files.

    Args:
        image_bunch: directory to image bunch
        files_to_exclude: list of file names to exclude from image_bunch/images/

    Returns:
        None: this method has side-effects
    """
    # create new image_bunch_updated/ dir and image_bunch_updated/images dir
    Path(image_bunch + "_updated/images").mkdir(parents=True, exist_ok=True)

    # if file_name in image_bunch/images not in file_names, copy it to image_bunch_updated/images
    for file_name in os.listdir(image_bunch + "/images"):
        if file_name not in files_to_exclude:
            copyfile(
                src=str(image_bunch + "/images/{}".format(file_name)),
                dst=str(image_bunch + "_updated/images/{}".format(file_name)),
            )

    # check if labels_updated.txt exists, if not then create it
    if not os.path.exists(str(image_bunch + "/labels_updated.txt")):
        copyfile(
            src=str(image_bunch + "/labels.txt"),
            dst=str(image_bunch + "/labels_updated.txt"),
        )

    # if file_nme in image_bunch/labels_updated.txt not in file_names, copy it to image_bunch_updated/labels_updated.txt
    updated_labels = []
    with open(str(image_bunch + "/labels_updated.txt"), "r") as f:
        for row in f:
            exclude = np.array(
                [file_name in row for file_name in files_to_exclude]
            ).any()
            if exclude:
                continue
            else:
                updated_labels.append(row)

    # write updated labels
    with open(str(image_bunch + "_updated/labels_updated.txt"), "w") as f:
        for row in updated_labels:
            f.write(row)
