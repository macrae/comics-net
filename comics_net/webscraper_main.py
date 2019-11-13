"Main application for scraping comic book covers and metadata from htpps://www.comics.org"

import argparse
import configparser
import datetime
import logging
import os
import pickle
import random
import urllib
from time import sleep
from uuid import uuid4

import jsonlines

import comics_net.webscraper as webscraper


def run_scraper(specs: dict) -> None:
    """
    Run the webscraper on htpps://www.comics.org per the job specification.
    """

    ###############################################################
    # Initialize scraper args
    ###############################################################

    # persist job specs to file
    with jsonlines.open("./metadata/log.jsonl", mode="a") as writer:
        writer.write(specs)

    # unpack job specs
    publisher_id = specs["publisher_id"]
    publisher_page = specs["publisher_page"]
    issue_count = int(specs["issue_count"])
    series = specs["series"]

    # init global vals
    URL = "https://www.comics.org"
    publisher_url = (
        URL + "/publisher/{}/".format(publisher_id) + "?page={}".format(publisher_page)
    )

    ###############################################################
    # Configure logger
    ###############################################################

    # TODO: refactor this...
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    root.addHandler(handler)

    logging.info("Starting scraper on page {}".format(publisher_url))

    # get publisher page
    publisher_soup = webscraper.get_soup(publisher_url)

    # parse series table from publisher page
    series_df = webscraper.parse_series_from_publisher_page(publisher_soup, series)

    # iterate over series dataframe and get issue covers and metadata
    for series_name, series_page_href, issue_count_int in zip(
        series_df["name"], series_df["href"], series_df["issue_count_int"]
    ):
        if issue_count_int < issue_count:
            pass
        else:
            # construct series page url
            series_page_url = URL + series_page_href

            # log series info to stdout
            logging.info(
                "Scraping {} issue(s) of {} from {}".format(
                    issue_count_int, series_name, series_page_url
                )
            )

            # get series page
            series_page_soup = webscraper.get_soup(series_page_url)

            # get cover gallery url for series
            if series_page_soup.find("a", href=True, text="Cover Gallery") is None:
                logging.info("No cover gallery found at {}".format(series_page_url))
                pass
            else:
                cover_gallery_href = series_page_soup.find(
                    "a", href=True, text="Cover Gallery"
                )["href"]
                cover_gallery_url = URL + cover_gallery_href

                logging.info("Cover gallery url = {}".format(cover_gallery_url))

                # get cover gallery page
                cover_gallery_soup = webscraper.get_soup(cover_gallery_url)

                # if cover gallery for series is not paginated...
                if webscraper.cover_gallery_pages(cover_gallery_soup) == 1:
                    cover_refs = webscraper.get_non_redundant_hrefs_from_cover_gallery(
                        cover_gallery_soup
                    )

                    # construct non-redundant issue urls from hrefs
                    issue_hrefs = [x[1] for x in cover_refs]
                    issue_urls = [URL + issue_href for issue_href in issue_hrefs]

                    # scrape issues
                    for issue_url in issue_urls:

                        # get issue page
                        issue_soup = webscraper.get_soup(issue_url)

                        # metadata
                        metadata = {}
                        metadata["series_name"] = series_name.replace("/", "|")

                        # post process the issue title removing extraneous characters
                        metadata["title"] = webscraper.get_issue_title(issue_soup)
                        metadata["on_sale_date"] = webscraper.get_issue_metadata(
                            issue_soup, name="on_sale_date"
                        )

                        logging.info(
                            "Scraping {} from {}".format(metadata["title"], issue_url)
                        )
                        # check if issue is redundant to an issue  already we pulled (variant)
                        if os.path.exists("./metadata/covers.jsonl"):
                            is_duplicate = webscraper.is_duplicate(
                                title=metadata["title"],
                                on_sale_date=metadata["on_sale_date"],
                                metadata_path="./metadata/covers.jsonl",
                            )

                            if is_duplicate:
                                logging.info(
                                    "Not pulling {} because it is a duplicate".format(
                                        metadata["title"]
                                    )
                                )
                                pass
                            else:
                                # get metadata from issue page
                                issue_metadata = webscraper.get_all_issue_metadata(
                                    issue_soup
                                )

                                # update metadata
                                metadata.update(issue_metadata)

                                # get the cover url
                                issue_cover_section = issue_soup.find(
                                    "div", {"class": "cover"}
                                )

                                issue_cover_href = issue_cover_section.find(
                                    "div", {"coverImage"}
                                ).a["href"]
                                issue_cover_url = URL + issue_cover_href

                                # get cover page
                                issue_cover_soup = webscraper.get_soup(issue_cover_url)

                                cover_credits = webscraper.get_cover_credits_from_cover_page(
                                    issue_cover_soup, metadata
                                )

                                metadata.update(cover_credits)

                                # save cover images
                                for variant_name in metadata["covers"]:
                                    urllib.request.urlretrieve(
                                        metadata["covers"][variant_name]["image_url"],
                                        metadata["covers"][variant_name]["save_to"],
                                    )

                                # save metadata
                                with jsonlines.open(
                                    "./metadata/covers.jsonl", mode="a"
                                ) as writer:
                                    writer.write(metadata)

                                # slow down the requests
                                sleep(random.uniform(3, 5))

                        else:
                            # get metadata from issue page
                            issue_metadata = webscraper.get_all_issue_metadata(
                                issue_soup
                            )

                            # update metadata
                            metadata.update(issue_metadata)

                            # get the cover url
                            issue_cover_section = issue_soup.find(
                                "div", {"class": "cover"}
                            )

                            issue_cover_href = issue_cover_section.find(
                                "div", {"coverImage"}
                            ).a["href"]
                            issue_cover_url = URL + issue_cover_href

                            # get cover page
                            issue_cover_soup = webscraper.get_soup(issue_cover_url)

                            # get image urls from cover page
                            cover_credits = webscraper.get_cover_credits_from_cover_page(
                                issue_cover_soup, metadata
                            )

                            metadata.update(cover_credits)

                            # save cover images
                            for variant_name in metadata["covers"]:
                                urllib.request.urlretrieve(
                                    metadata["covers"][variant_name]["image_url"],
                                    metadata["covers"][variant_name]["save_to"],
                                )

                            # save metadata
                            with jsonlines.open(
                                "./metadata/covers.jsonl", mode="a"
                            ) as writer:
                                writer.write(metadata)

                            # slow down the requests
                            sleep(random.uniform(3, 5))

                # if cover gallery for series is paginated...
                elif webscraper.cover_gallery_pages(cover_gallery_soup) > 1:

                    cover_gallery_range = webscraper.cover_gallery_pages(
                        cover_gallery_soup
                    )

                    logging.info("Cover gallery range = {}".format(cover_gallery_range))

                    # iterate over cover gallery pages
                    for i in range(1, cover_gallery_range + 1):
                        cover_gallery_url = str(
                            URL + cover_gallery_href + "/?page={}"
                        ).format(i)

                        logging.info("Cover gallery url = {}".format(cover_gallery_url))

                        cover_gallery_soup = webscraper.get_soup(cover_gallery_url)

                        # get non-redundnat issue hrefs from cover gallery
                        cover_refs = webscraper.get_non_redundant_hrefs_from_cover_gallery(
                            cover_gallery_soup
                        )

                        # construct non-redundant issue urls from hrefs
                        issue_hrefs = [x[1] for x in cover_refs]
                        issue_urls = [URL + issue_href for issue_href in issue_hrefs]

                        # scrape issues
                        for issue_url in issue_urls:

                            # get issue page
                            issue_soup = webscraper.get_soup(issue_url)

                            # metadata
                            metadata = {}
                            metadata["series_name"] = series_name.replace("/", "|")

                            # post process the issue title removing extraneous characters
                            metadata["title"] = webscraper.get_issue_title(issue_soup)
                            metadata["on_sale_date"] = webscraper.get_issue_metadata(
                                issue_soup, name="on_sale_date"
                            )

                            logging.info(
                                "Scraping {} from {}".format(
                                    metadata["title"], issue_url
                                )
                            )
                            # check if issue is redundant to an issue  already we pulled (variant)
                            if os.path.exists("./metadata/covers.jsonl"):
                                is_duplicate = webscraper.is_duplicate(
                                    title=metadata["title"],
                                    on_sale_date=metadata["on_sale_date"],
                                    metadata_path="./metadata/covers.jsonl",
                                )

                                if is_duplicate:
                                    logging.info(
                                        "{} is duplicate".format(metadata["title"])
                                    )
                                    pass
                                else:
                                    # get metadata from issue page
                                    issue_metadata = webscraper.get_all_issue_metadata(
                                        issue_soup
                                    )

                                    # update metadata
                                    metadata.update(issue_metadata)

                                    # get the cover url
                                    issue_cover_section = issue_soup.find(
                                        "div", {"class": "cover"}
                                    )

                                    issue_cover_href = issue_cover_section.find(
                                        "div", {"coverImage"}
                                    ).a["href"]
                                    issue_cover_url = URL + issue_cover_href

                                    # get cover page
                                    issue_cover_soup = webscraper.get_soup(
                                        issue_cover_url
                                    )

                                    cover_credits = webscraper.get_cover_credits_from_cover_page(
                                        issue_cover_soup, metadata
                                    )

                                    metadata.update(cover_credits)

                                    # save cover images
                                    for variant_name in metadata["covers"]:
                                        urllib.request.urlretrieve(
                                            metadata["covers"][variant_name][
                                                "image_url"
                                            ],
                                            metadata["covers"][variant_name]["save_to"],
                                        )

                                    # save metadata
                                    with jsonlines.open(
                                        "./metadata/covers.jsonl", mode="a"
                                    ) as writer:
                                        writer.write(metadata)

                                    # slow down the requests
                                    sleep(random.uniform(3, 5))

                            else:
                                # get metadata from issue page
                                issue_metadata = webscraper.get_all_issue_metadata(
                                    issue_soup
                                )

                                # update metadata
                                metadata.update(issue_metadata)

                                # get the cover url
                                issue_cover_section = issue_soup.find(
                                    "div", {"class": "cover"}
                                )

                                issue_cover_href = issue_cover_section.find(
                                    "div", {"coverImage"}
                                ).a["href"]
                                issue_cover_url = URL + issue_cover_href

                                # get cover page soup
                                issue_cover_soup = webscraper.get_soup(issue_cover_url)

                                cover_credits = webscraper.get_cover_credits_from_cover_page(
                                    issue_cover_soup, metadata
                                )

                                metadata.update(cover_credits)

                                # save cover images
                                for variant_name in metadata["covers"]:
                                    urllib.request.urlretrieve(
                                        metadata["covers"][variant_name]["image_url"],
                                        metadata["covers"][variant_name]["save_to"],
                                    )

                                # save metadata
                                with jsonlines.open(
                                    "./metadata/covers.jsonl", mode="a"
                                ) as writer:
                                    writer.write(metadata)

                                # slow down the requests
                                sleep(random.uniform(3, 5))


def main(main_args):
    parser = argparse.ArgumentParser()

    parser.add_argument("--publisher_id", required=True, help="")
    parser.add_argument("--publisher_page", required=True, help="")
    parser.add_argument("--issue_count", required=False, help="")
    parser.add_argument("--series", required=False, help="")

    args = parser.parse_args(main_args[1:])

    specs = {i: args.__getattribute__(i) for i in args.__dir__() if i[0] != "_"}

    run_scraper(specs)


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
