"Methods for scraping comic book covers and metadata from htpps://www.comics.org"

import datetime
import random
import re
import urllib.request
from contextlib import closing
from functools import reduce
from os import path
from re import search
from time import sleep
from typing import List, Optional, Union

import jsonlines
import pandas as pd
from bs4 import BeautifulSoup
from pandas import DataFrame
from requests import get
from requests.exceptions import RequestException

# gloabl vals
URL = "https://www.comics.org"


def read_jsonl(path: str) -> List[dict]:
    """
    Read a jsonlines file and return a list of dicts.
    """
    data = []
    with jsonlines.open(path, mode="r") as reader:
        for item in reader:
            data.append(item)
    return data


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def simple_get(url: str) -> Union[bytes, None]:
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """

    def is_good_response(resp):
        """
        Returns true if the response seems to be HTML, false otherwise
        """
        content_type = resp.headers["Content-Type"].lower()
        return (
            resp.status_code == 200
            and content_type is not None
            and content_type.find("html") > -1
        )

    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error("Error during requests to {0} : {1}".format(url, str(e)))
        return None


def transform_simple_get_html(raw_html: Optional[bytes]) -> BeautifulSoup:
    """
    Takes the raw HTML response of a GET request and returns a tree-based
    interface for parsing HTML.
    """
    return BeautifulSoup(raw_html, "html.parser")


def get_soup(url: str) -> BeautifulSoup:
    """
    Given a url returns a tree-based interface for parsing HTML.
    """
    html = simple_get(url)
    return transform_simple_get_html(html)


# TODO: rename this method
def cover_gallery_pages(cover_gallery_soup: BeautifulSoup) -> int:
    """
    Return the number of pages in the cover gallery.
    """
    cover_gallery_pages = list(
        filter(
            lambda x: x.isdigit(),
            [
                x.contents[0]
                for x in cover_gallery_soup.find_all(
                    "a", {"class": "btn btn-default btn-sm"}
                )
            ],
        )
    )

    if cover_gallery_pages == list():
        return 1
    else:
        return max([int(x) for x in cover_gallery_pages])


def get_issue_title(issue_soup: BeautifulSoup) -> str:
    """
    Return the title of the issue page.
    """
    return (
        issue_soup.find("title")
        .contents[0]
        .replace("\n", "")
        .strip()
        .split(" :: ")[-1]
        .replace("/", "|")
    )


#  TODO: rename name -> key
def get_issue_metadata(issue_soup: BeautifulSoup, name: str) -> str:
    """
    Return the value of the key
    """
    if len(issue_soup.find_all("dd", id=name)) > 0:
        if (name != "issue_indicia_publisher") & (name != "issue_brand"):
            return issue_soup.find_all("dd", id=name)[0].contents[0].strip()
        else:
            try:
                return issue_soup.find_all("dd", id=name)[0].find("a").contents[0]
            except:
                return ""
    else:
        return ""


def get_all_issue_metadata(issue_soup) -> dict:
    d = dict()
    d["on_sale_date"] = get_issue_metadata(issue_soup, "on_sale_date")
    d["indicia_frequency"] = get_issue_metadata(issue_soup, "indicia_frequency")
    d["issue_indicia_publisher"] = get_issue_metadata(
        issue_soup, "issue_indicia_publisher"
    )
    d["issue_brand"] = get_issue_metadata(issue_soup, "issue_brand")
    d["issue_price"] = get_issue_metadata(issue_soup, "issue_price")
    d["issue_pages"] = get_issue_metadata(issue_soup, "issue_pages")
    d["format_color"] = get_issue_metadata(issue_soup, "format_color")
    d["format_dimensions"] = get_issue_metadata(issue_soup, "format_dimensions")
    d["format_paper_stock"] = get_issue_metadata(issue_soup, "format_paper_stock")
    d["format_binding"] = get_issue_metadata(issue_soup, "format_binding")
    d["format_publishing_format"] = get_issue_metadata(
        issue_soup, "format_publishing_format"
    )
    d["rating"] = get_issue_metadata(issue_soup, "rating")
    d["indexer_notes"] = " | ".join(
        [x.contents[0].replace("\n", "").strip() for x in issue_soup.find_all("p")]
    )

    all_issue_credits = list(
        zip(
            issue_soup.find_all("span", {"class": "credit_label"}),
            issue_soup.find_all("span", {"class": "credit_value"}),
        )
    )

    try:
        d["synopsis"] = " | ".join(
            list(
                filter(
                    lambda x: x != "",
                    [
                        x[1].contents[0] if x[0].contents[0] == "Synopsis" else ""
                        for x in all_issue_credits
                    ],
                )
            )
        )
    except:
        d["synopsis"] = ""
    return d


def get_issue_cover_metadata(issue_soup):
    """
    Gets all the metadata from the cover section of the issue page.
    """
    d = dict()
    # get cover section
    cover_soup = issue_soup.find("div", {"class": "cover"})

    # cover credits: editing, script, pencils, inks, colors, letters, characters, etc...
    cover_credits = list(
        zip(
            [
                x.contents[0]
                for x in cover_soup.find_all("span", {"class": "credit_label"})
            ],
            [
                x.contents[0]
                for x in cover_soup.find_all("span", {"class": "credit_value"})
            ],
        )
    )

    d.update({"cover_{}".format(x.lower()): y for x, y in cover_credits})
    d.pop("cover_reprints", None)
    d.pop("cover_awards", None)
    return d


# get image divs from cover page
def get_cover_credits_from_cover_page(cover_img_soup, metadata) -> dict:
    cover_divs = cover_img_soup.find_all("div", {"class": "issue_covers"})[0].find_all(
        "div"
    )

    # go into variant url and pull metadata
    cover_images = [x.find_all("a")[0].contents[0]["src"] for x in cover_divs]

    cover_names = [
        get_variant_cover_name(x.find_all("a")[1].contents[0]) for x in cover_divs
    ]

    cover_urls = [URL + x.find_all("a")[0]["href"] for x in cover_divs]

    covers = list((zip(cover_names, cover_urls, cover_images)))

    covers_dict: dict = dict()
    for cover in covers:
        name = cover[0]
        url = cover[1]
        image = cover[2]

        covers_dict[name] = {}
        covers_dict[name]["cover_url"] = url
        covers_dict[name]["image_url"] = image

    issue_cover_credits: dict = dict()
    issue_cover_credits["covers"] = {}

    for variant_name in covers_dict:
        if is_reprinting(variant_name) | is_newsstand_or_canadian(variant_name):
            pass
        else:
            issue_url = covers_dict[variant_name]["cover_url"]
            image_url = covers_dict[variant_name]["image_url"]

            # get issue page
            issue_html = simple_get(issue_url)
            issue_soup = transform_simple_get_html(issue_html)

            cover = issue_soup.find("div", {"class": "cover"})

            cover_credits_list = list(
                zip(
                    [
                        x.contents[0]
                        for x in cover.find_all("span", {"class": "credit_label"})
                    ],
                    [
                        x.contents[0]
                        for x in cover.find_all("span", {"class": "credit_value"})
                    ],
                )
            )

            issue_title = get_issue_title(issue_soup)
            issue_title_variant = get_variant_cover_name(issue_title)

            cover_credits: dict = {
                "cover_{}".format(x[0].lower()): x[1] for x in cover_credits_list
            }
            cover_credits.pop("cover_reprints", None)
            cover_credits.pop("cover_awards", None)

            save_as = "{}: {} {} ({})".format(
                metadata["series_name"],
                strip_brackets(metadata["title"]),
                variant_name,
                metadata["on_sale_date"],
            ).replace("/", "|")
            # Example of save_as...
            # Aquaman: Aquaman #2 Direct (1985-11-19)

            save_to = "./covers/" + save_as + ".jpg"

            # cover_credits["cover_image_file_name"] = save_as
            cover_credits["save_to"] = save_to

            cover_credits["image_url"] = image_url

            issue_cover_credits["covers"][issue_title_variant] = cover_credits


    return issue_cover_credits


def get_non_redundant_hrefs_from_cover_gallery(cover_gallery_soup):
    """
    Given a cover gallery bs4 object, return the non-redundant hrefs for each issue.
    """
    cover_refs = [
        (x.get_text(), x["href"]) for x in cover_gallery_soup.find_all("a", href=True)
    ]

    cover_refs = filter(
        lambda x: "/issue/" in x[1] and "/cover/" not in x[1], cover_refs
    )

    cover_refs = [(get_brackets(x[0]), x[1]) for x in cover_refs]

    return list(filter(lambda x: not is_redundant(x[0]), cover_refs))


def get_brackets(title: str) -> Union[str, None]:
    """
    Return the substring of the first instance of bracketed text.
    """
    regex_brackets = re.search(r"\[(.*?)\]", title)
    if regex_brackets is None:
        return None
    else:
        return regex_brackets.group()


def strip_brackets(title: str) -> str:
    """
    Return the string without the first instance of bracketed text.
    """
    brackets = get_brackets(title)
    if brackets is None:
        if "--" in title:
            return title.split("--")[0].strip()
        else:
            return title
    else:
        debracketed_title = title.split(brackets)[0].strip()
        if "--" in debracketed_title:
            return debracketed_title.split("--")[0].strip()
        else:
            return debracketed_title


def is_reprinting(title: str) -> bool:
    """
    Check if a string contains some substrings.
    """
    is_2nd_printing = ("2nd Printing" in title) | ("Second Printing" in title)
    is_3rd_printing = ("3rd Printing" in title) | ("Third Printing" in title)
    is_4th_printing = ("4th Printing" in title) | ("Fourth Printing" in title)
    is_5th_printing = ("5th Printing" in title) | ("Fifth Printing" in title)
    is_6th_printing = "6th Printing" in title
    is_7th_printing = "7th Printing" in title
    is_8th_printing = "8th Printing" in title
    is_9th_printing = "9th Printing" in title
    is_10th_printing = "10th Printing" in title
    return (
        is_2nd_printing
        | is_3rd_printing
        | is_4th_printing
        | is_5th_printing
        | is_6th_printing
        | is_7th_printing
        | is_8th_printing
        | is_9th_printing
        | is_10th_printing
    )


def is_newsstand_or_canadian(title) -> bool:
    """
    Check if an issue is a duplicate Newsstand issue.
    """
    return (
        ("newsstand" in title.lower())
        | ("canadian" in title.lower())
        | ("whitman" in title.lower())
        | ("british " in title.lower())
    )


def is_variant(title) -> bool:
    """
    Check if an issue is variant cover.
    """
    return "variant" in title.lower()


def is_redundant(title: str) -> bool:
    """
    Check if an issue is a redundant to a direct sale issue.
    """
    if title is None:
        return False
    else:
        return (
            is_reprinting(title) | is_newsstand_or_canadian(title) | is_variant(title)
        ) | (("cover" in title.lower()) & ("direct" not in title.lower()))


def is_duplicate(title: str, on_sale_date: str, metadata_path: str) -> bool:
    """
    Check if an issue is a redundant to a direct sale issue.
    """
    metadata = read_jsonl(metadata_path)
    df = pd.DataFrame(metadata)
    titles = list(df["title"].unique())

    # check if title is duplicate
    title_is_duplicate = reduce(
        lambda x, y: x | y, [strip_brackets(title) in strip_brackets(x) for x in titles]
    )

    # check if
    if title_is_duplicate:
        on_sale_dates = df[df["title"].apply(strip_brackets) == strip_brackets(title)][
            "on_sale_date"
        ].values
        date_is_duplicate = on_sale_date in on_sale_dates
        return title_is_duplicate & date_is_duplicate
    else:
        return False


def get_variant_cover_name(cover_name: str) -> str:
    """
    Generate the name of the cover to use in metadata.
    """
    variant_name = get_brackets(cover_name)
    if variant_name is None:
        return "Original"
    else:
        return variant_name.replace("[", "").replace("]", "")


def parse_series_from_publisher_page(publisher_soup:  BeautifulSoup, series: str=None) -> DataFrame:
    """
    Parse series table from publisher page.
    """
    name = [
        x.find("a").contents[0]
        for x in publisher_soup.find_all("td", {"class": "name"})
    ]
    href = [
        x.find("a")["href"] for x in publisher_soup.find_all("td", {"class": "name"})
    ]
    year = [x.contents[0] for x in publisher_soup.find_all("td", {"class": "year"})]
    issue_count = [
        x.contents[0] for x in publisher_soup.find_all("td", {"class": "issue_count"})
    ]
    published = [
        x.contents[0] for x in publisher_soup.find_all("td", {"class": "published"})
    ]

    # create dataframe of publisher series (on page)
    df = pd.DataFrame(
        list(zip(name, href, year, issue_count, published)),
        columns=["name", "href", "year", "issue_count", "published"],
    )

    # parse issue count as int from issue_count column
    def parse_int_from_string(s):
        return int(search(r"\d+", s).group())

    df["issue_count_int"] = df["issue_count"].apply(lambda x: parse_int_from_string(x))

    if series is None:
        return df
    else:
        return df[df["name"] == series]
