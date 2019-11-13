import unittest
from typing import Union
from unittest import mock

import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

import comics_net.webscraper as webscraper

URL = "https://www.comics.org"


def mocked_response_get(url):
    """
    Mock the response of comics_net.webscraper.simple_get()
    """

    def transform_url_to_resource_name(url: str) -> Union[str, Exception]:
        """
        Private method that parses a url into a resource file name.
        """
        if ("publisher" in url) | ("series" in url):
            return (
                url.split(URL)[1][1:]
                .replace("?", "")
                .replace("/", "_")
                .replace("=", "_")
            )
        elif "issue" in url:
            return url.split(URL)[1][1:][:-1].replace("/", "_")
        else:
            return Exception("Could not transform the url into a resource name")

    resource = transform_url_to_resource_name(url)
    f = open("./comics_net/resources/{}".format(resource), "rb")
    try:
        html = f.read()
        return html
    except:
        return None


def test_read_jsonl():
    metadata = webscraper.read_jsonl("./comics_net/resources/metadata.jsonl")
    assert type(metadata) is list


@mock.patch("comics_net.webscraper.simple_get", side_effect=mocked_response_get)
def test_simple_get(mock_get):
    url = "https://www.comics.org/publisher/54/?page=1"
    html = webscraper.simple_get(url)
    assert type(html) is bytes


@mock.patch("comics_net.webscraper.simple_get", side_effect=mocked_response_get)
def test_transform_simple_get_html(mock_get):
    url = "https://www.comics.org/publisher/54/?page=1"
    html = webscraper.simple_get(url)
    soup = webscraper.transform_simple_get_html(html)
    assert type(soup) is BeautifulSoup


@mock.patch("comics_net.webscraper.simple_get", side_effect=mocked_response_get)
def test_get_issue_title(mock_get):
    issue_url = "https://www.comics.org/issue/370657/"
    issue_html = webscraper.simple_get(issue_url)
    issue_soup = webscraper.transform_simple_get_html(issue_html)
    title = webscraper.get_issue_title(issue_soup)
    assert title == "Action Comics #854"


@mock.patch("comics_net.webscraper.simple_get", side_effect=mocked_response_get)
def test_get_issue_metadata(mock_get):
    issue_url = "https://www.comics.org/issue/370657/"
    issue_html = webscraper.simple_get(issue_url)
    issue_soup = webscraper.transform_simple_get_html(issue_html)

    on_sale_date = webscraper.get_issue_metadata(issue_soup, name="on_sale_date")
    assert on_sale_date == "2007-08-15"

    issue_indicia_publisher = webscraper.get_issue_metadata(
        issue_soup, name="issue_indicia_publisher"
    )
    assert issue_indicia_publisher == "DC Comics"


@mock.patch("comics_net.webscraper.simple_get", side_effect=mocked_response_get)
def test_get_all_issue_metadata(mock_get):
    issue_url = "https://www.comics.org/issue/370657/"
    issue_html = webscraper.simple_get(issue_url)
    issue_soup = webscraper.transform_simple_get_html(issue_html)

    issue_metadata = webscraper.get_all_issue_metadata(issue_soup)
    assert type(issue_metadata) is dict

    expected_keys = set(
        [
            "on_sale_date",
            "indicia_frequency",
            "issue_indicia_publisher",
            "issue_brand",
            "issue_price",
            "issue_pages",
            "format_color",
            "format_dimensions",
            "format_paper_stock",
            "format_binding",
            "format_publishing_format",
            "rating",
            "indexer_notes",
            "synopsis",
        ]
    )

    assert set(issue_metadata.keys()).difference(expected_keys) == set()

    issue_url = "https://www.comics.org/issue/21497/"
    issue_soup = webscraper.get_soup(issue_url)

    issue_metadata = webscraper.get_all_issue_metadata(issue_soup)

    assert set(issue_metadata.keys()).difference(expected_keys) == set()


@mock.patch("comics_net.webscraper.simple_get", side_effect=mocked_response_get)
def test_get_issue_cover_metadata(mock_get):
    issue_url = "https://www.comics.org/issue/370657/"
    issue_html = webscraper.simple_get(issue_url)
    issue_soup = webscraper.transform_simple_get_html(issue_html)

    issue_cover_metadata = webscraper.get_issue_cover_metadata(issue_soup)
    assert type(issue_cover_metadata) is dict

    expected_keys = set(
        [
            "cover_pencils",
            "cover_inks",
            "cover_colors",
            "cover_letters",
            "cover_first line of dialogue or text",
            "cover_genre",
            "cover_characters",
            "cover_keywords",
        ]
    )

    assert set(issue_cover_metadata.keys()).difference(expected_keys) == set()

    issue_url = "https://www.comics.org/issue/21497/"
    issue_soup = webscraper.get_soup(issue_url)

    issue_cover_metadata = webscraper.get_issue_cover_metadata(issue_soup)




@mock.patch("comics_net.webscraper.simple_get", side_effect=mocked_response_get)
def test_get_cover_credits_from_cover_page(mock_get):
    issue_cover_url = "https://www.comics.org/issue/36858/cover/4/"
    issue_cover_html = webscraper.simple_get(issue_cover_url)
    issue_cover_soup = webscraper.transform_simple_get_html(issue_cover_html)

    metadata = webscraper.read_jsonl("./comics_net/resources/metadata.jsonl")

    issue_cover_credits = webscraper.get_cover_credits_from_cover_page(issue_cover_soup, metadata[0])

    assert (type(issue_cover_credits)) is dict

    expected_keys = set(["covers"])

    assert set(issue_cover_credits.keys()).difference(expected_keys) == set()

    assert set(issue_cover_credits["covers"].keys()) == {"Direct"}

    expected_keys = set(
        [
            "cover_pencils",
            "cover_inks",
            "cover_colors",
            "cover_letters",
            "cover_genre",
            "cover_characters",
            "cover_keywords",
            "cover_image_file_name",
            "save_to",
            "image_url",
        ]
    )

    assert (
        set(issue_cover_credits["covers"]["Direct"].keys()).difference(
            expected_keys
        )
        == set()
    )

    issue_cover_url = "https://www.comics.org/issue/21497/cover/4/"
    issue_cover_soup = webscraper.get_soup(issue_cover_url)

    issue_cover_credits = webscraper.get_cover_credits_from_cover_page(issue_cover_soup, metadata[0])

    assert "cover_awards" not in issue_cover_credits["covers"]["Original"].keys()

@mock.patch("comics_net.webscraper.simple_get", side_effect=mocked_response_get)
def test_get_cover_credits_from_cover_page_2(mock_get):

    issue_cover_url = "https://www.comics.org/issue/1179057/cover/4/"
    issue_cover_html = webscraper.simple_get(issue_cover_url)
    issue_cover_soup = webscraper.transform_simple_get_html(issue_cover_html)

    metadata = webscraper.read_jsonl("./comics_net/resources/metadata.jsonl")

    issue_cover_credits = webscraper.get_cover_credits_from_cover_page(
        issue_cover_soup, metadata[0])

    assert len(issue_cover_credits['covers'].keys()) == 2
    assert "Original" in list(issue_cover_credits['covers'].keys())
    assert "Scribblenauts Unmasked Variant Cover" in list(issue_cover_credits['covers'].keys())


def test_get_brackets():
    assert webscraper.get_brackets("Action Comics [Direct]") == "[Direct]"


def test_strip_brackets_from_title():
    assert webscraper.strip_brackets("Action Comics [Direct]") == "Action Comics"


def test_check_if_issue_is_reprinting():
    assert webscraper.is_reprinting("Action Comics [Direct]") is False
    assert webscraper.is_reprinting("Action Comics [Second Printing]") is True
    assert webscraper.is_reprinting("Action Comics [2nd Printing]") is True
    assert webscraper.is_reprinting("Action Comics [3rd Printing]") is True
    assert webscraper.is_reprinting("Action Comics [4th Printing]") is True


def test_is_newsstand_or_canadian():
    assert webscraper.is_newsstand_or_canadian("Action Comics #854 [Direct]") is False
    assert webscraper.is_newsstand_or_canadian("Action Comics #854 [Newsstand]") is True
    assert webscraper.is_newsstand_or_canadian("Action Comics #854 [Canadian]") is True


def test_is_redundant():
    assert webscraper.is_redundant(title="Action Comics #854 [Direct]") is False
    assert webscraper.is_redundant(title="Action Comics #854 [Newsstand]") is True
    assert webscraper.is_redundant(title="Action Comics #854 [Canadian]") is True


def test_is_duplicate():
    assert (
        webscraper.is_duplicate(
            title="Action Comics #854",
            on_sale_date="2007-08-15",
            metadata_path="./comics_net/resources/metadata.jsonl",
        )
        is True
    )

    assert (
        webscraper.is_duplicate(
            title="Action Comics #855",
            on_sale_date="2007-08-15",
            metadata_path="./comics_net/resources/metadata.jsonl",
        )
        is False
    )

    assert (
        webscraper.is_duplicate(
            title="Action Comics #854",
            on_sale_date="2007-08-22",
            metadata_path="./comics_net/resources/metadata.jsonl",
        )
        is False
    )


def test_get_variant_cover_name():
    variant_name = webscraper.get_variant_cover_name(
        "Action Comics [Sean MacRae Variant]"
    )
    assert variant_name == "Sean MacRae Variant"

    variant_name = webscraper.get_variant_cover_name(
        "Action Comics [Andy Kubert Variant]"
    )
    assert variant_name == "Andy Kubert Variant"

    variant_name = webscraper.get_variant_cover_name("Action Comics [Direct]")
    assert variant_name == "Direct"

    variant_name = webscraper.get_variant_cover_name("Action Comics")
    assert variant_name == "Original"


@mock.patch("comics_net.webscraper.simple_get", side_effect=mocked_response_get)
def test_parse_series_from_publisher_page(mock_get):
    publisher_url = "https://www.comics.org/publisher/54/?page=1"
    publisher_html = webscraper.simple_get(publisher_url)
    publisher_soup = webscraper.transform_simple_get_html(publisher_html)

    df = webscraper.parse_series_from_publisher_page(publisher_soup)

    assert type(df) is DataFrame
    assert len(df) > 0


@mock.patch("comics_net.webscraper.simple_get", side_effect=mocked_response_get)
def test_cover_gallery_pages(mock_get):
    cover_gallery_url = "https://www.comics.org/series/7768/covers/"
    cover_gallery_html = webscraper.simple_get(cover_gallery_url)
    cover_gallery_soup = webscraper.transform_simple_get_html(cover_gallery_html)

    assert webscraper.cover_gallery_pages(cover_gallery_soup) == 2

    cover_gallery_url = "https://www.comics.org/series/31350/covers/"
    cover_gallery_html = webscraper.simple_get(cover_gallery_url)
    cover_gallery_soup = webscraper.transform_simple_get_html(cover_gallery_html)

    assert webscraper.cover_gallery_pages(cover_gallery_soup) == 1
