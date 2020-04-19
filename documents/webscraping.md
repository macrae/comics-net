## Acknowledge

Acknowledge all of the excellent work the folks at comics.org are doing to index the world's comic book collection. Tip of the hat to..., and ... for...

## Web-scraping for the Unacquainted

Here I present the nuts and bolts of the web-scraper module I created for `comics-net`. I don't consider `comics-net` a _proper_ Python package in the least; it is the mildewing tech debt of Data Science. Tech debt, like financial debt, has many forms and, depending on conditions, can either be responsible or ill-advised. For example, taking out a small business loan so you can grow inventory to scale distribution can be considered good debt because if it is an investment in the future of your business that may pay dividends down the road, but financing a shopping spree at Manolo Blahnik on a line of credit with a 30% APR that will be paid down by making the minimum payment each month is bad debt. And a similar argument can be made for Data Science - and why I'm never going to obsess over making the web scraping component of `comics-net` robust. It's kludgey, at times, showing a great disregard for proper software development, but my aim is not to support a web scraping module for people who want to scrape their own custom dataset from comics.org. My goal is to collect an extensive and interesting enough dataset that I can curate and publish it once - and refer to it as a data artifact in my modeling endeavors. As such, this is tech debt that will pay dividends down the road in terms of the most important of all pieces to this puzzle, labeled data, and we'll accept and pay the interest on this tech debt. If the payments on this tech debt down the road prove too high, we'll need to pay it down, but it's a cost I'm willing to incur for the payout of what Data Science learning I can have.

First and foremost, I need labeled data, and I need a lot of it. My bias is towards moving quickly through the research and development cycle, at least once. That way, I can identify any big unknown-unknowns and chart-out the general lay of the land. Over optimizing any part in the R&D cycle - the first time through - can come at the cost of how long it takes to form an understanding of the entire problem space; the data, downstream dependencies, integration complexity, or customer requirements. Our understanding can change, and to maximize the likelihood that we're working on the right thing (or the next most valuable thing), we want to expose as much of the problem and solution space as possible, and the best way to do that is by simply trying to create the thing you want, end-to-end.

That's to say: this web-scraping module is not for standalone use. I added docstrings, type hints, and tests for my .own benefit. The purpose of this article is to detail how a person interested in web-scraping for the sole purpose of hobbling together a semi-reproducible, set of data and labels may go about that.

## JSONL

JavaScript Object Notation (JSON) is a standard data exchange format. It replaced XML in the mid-aughts as the preferred standard for sending and receiving data.

JSON (sans L) is array-formatted and requires that the entire array be parsed to return selected entries from some JSON file. JSONL is new-line delimited, and there's no need to load the entire dataset into memory to index it. You can easily append new records to JSONL, which is why I selected this data standard. I wanted to log the events of the web scraper at runtime, where there's a high frequency of I/O. Using standard JSON, I would have to read the entire JSON dataset, add the new record, and then write it back to JSON.

There are other benefits to JSONL. For machine learning, JSONL can be treated as an iterable, and selecting a single row can be performed without the requirement of loading the complete dataset into memory. For batch training models on large data (what is large anymore?), it's desirable to be able to select from the file the index of the next batch.


## Create a Log and Append to it
This is a pro tip that I had to learn the hard way. If the script that you are running does a bunch of things repeatedly, don't wait until you've collected a bunch of the things in memory and then wait until the very end to write it to memory, log each step to a file as you go... that way - whenever you invariably get snagged by some corner case that fails 80% of the way through the job, you won't lose all the information you've been scraping. And if you build your application to reason about the log - after that bug is squashed you can just kick of the job again, and it will pick up at the 80% mark where it failed before.


## Beautiful Soup

The grappling hook of the `comcics_net.webscraper` utility belt is `get_soup`:

```
def get_soup(url: str) -> BeautifulSoup:
 """
 Given a url returns a tree-based interface for parsing HTML.
 """
 html = simple_get(url)
 return transform_simple_get_html(html)
```

This method takes a URL and returns a BS4 object, the workhorse of this whole module.

Peek into `simple_get` and `transform_simple_get_html`.

### The BeautifulSoup class

If you're web-scraping in Python, start with BeautifulSoup. It parses HTML (a tree-like data structure) into Python objects, and makes navigating, searching and modifying parse trees far more ergonomical.

### Understand the URL Subdirectory

A standard URL consists of a schema (http:// or https://), subdomain (google, stackoverflow), top-level domain (.com, .edu, .io) and a subdirectory. The subdirectory defines which particular page or section of a webpage you're on. Some website design is highly interpretable for the subdirectory structure. If so, it may be straight forward to navigate the site programmatically by generating URLs on the fly. After poking around the site in Chrome for a bit, I decided to use the `publisher,` `page` subdirectory keys as the entry URL.

```
https://www.comics.org/publisher/54/?page=1
```

This URL is for publisher 54 (Detective Comics), page 1 (see picture below). Each publisher page contains a table of their published Series with some metadata. The "Covers" field contains a link that can be followed to the Series page of that particular Series and you'll see that the URL subdirectory changes to:

```
https://www.comics.org/series/3370/covers/
```

From there it's an exercise in collecting each of the Issue links, following them to the issues page.

```
https://www.comics.org/issue/42256/
```

Scraping the cover metadata from the issue page, then following the issue page link to the cover image page

```
https://www.comics.org/issue/42256/cover/4/
```

And downloading the attached jpeg and logging the issue metadata and image in our logger.

To perform the above navigation required parsing many different HTML tree structs. I found it easier to think about each page as a Class with defined attributes and then write methods that take a Class type, for example, an issue page would be referred to as `issue_soup` and do something very specific with that soup object, like parse it for the title of the issue. A bunch of methods that take a BS4 object and return some features of the page. For example:

```
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
```

This is a typical pattern I repurposed as I poked around and deduced what meta-data
features I wanted to extract, how.

There's some real nasty stuff in `webscraper`, methods that I look back on now and shudder. To make heads or tails out of any of these methods now? No way! Segue into: a little bit about Data Science tech debt and how to think about writing it off or paying it down.

## Save Yourself Some Time w/ a `main()`

If you thought that `comics_net.webscraper` had some tech debt, you ain't seen `comics _net.webscraper_main` yet. It takes all of the - relatively well-named - methods in `webscraper` and composes them into a teetering collection of nested `if/else` statements that each address some one-off, not documented detail of the statically-generated comics.org website. This was developed through elimination. Thomas Edison's old quote about a million-ways that don't work-true... having a main that appears to work as expected, only to throw an `Exception()` after running for twenty minutes because I didn't consider the case when ...

## Parameterize Your `main()`

By URL. How are your URLs structured? I converged on a pattern around issue URLs early, and I regretted not using a more generic interface for web scraping and parameterizing the `main()` to run on an artist or search results pages.

## Use stdlog

So you see what's happening. Just hitting execute and then waiting in the dark for your computer to return what you asked it to - especially if it takes more than minutes. Add a progress bar. Add an index count. Add some logging messages just saying what you did - like: "Loaded 378 records from s3://comics-net/avengers". You'll be thankful you did once you start cranking your web scraper to run all night.

## Don't get blocked

Add a `wait()` statement. I added `random.random(2, 5),` so on average, the request would wait somewhere before 2 and 5 seconds before proceeding to the next pull.