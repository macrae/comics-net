# Deep Learning for Comic Books

This project applies neural networks to comic book covers and synopses to perform a
variety of machine learning tasks, for example, character classification and comic book
synopsis generation.

### Prerequisites

Python3.6.9 is required to build and run the application. The list of third-party
dependencies can be found in the `requirements.txt` and `requirements-dev.txt` files.

### Installing

Create, activate and install dependencies into a Python3.6 environment.

```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
```

## Running Tests

```
python3 -m pytest comics_net/
```

## Using the Project

This project consists of two main applications: 1) webscraping and exploratory data
analysis of comic book covers and metadata, and 2) deep learning on comic book covers
and synopses to perform a variety of machine learning tasks, such as classification
and text generation.

The good news is that the webscraping of a significant number of comic book covers and
their metadata has already been performed and the datasets already published to a public
repository for your convenience.

### Datasets

A the complete curated dataset of comic book covers with metadata and annotations for
this project can be found here: [s3://])(https://aws.s3.com).

Within the `comics_net` module there is a `URLs` object with attributes to different
training dataset locations, for example `URLs.justic_league` will get you the location
to a Justice League curated dataset which contains characters present on any issue of
any series of the Justice League.

|Group	|# Images	|# Labels	|   	|   	|
|---	|---	|---	|---	|---	|
|Justice League	|11,409	|35	|   	|   	|
|Avengers	|10,978	|27	|	|   	|
|Legion of Super-Heroes	|5,536	|14	|   	|   	|
|Archies	|5,439	|27	|   	|   	|
|X-Men	|5,008	|27	|   	|   	|
|Defenders	|2,021	|8	|   	|   	|
|Fantastic Four	|1,917	|4	|   	|   	|
|Suicide Squad	|913	|4	|   	|   	|
|Inhumans	|528	|5	|   	|   	|
|Guardians of the Galaxy	|379	|5	|   	|   	|
|Green Lantern Corps	|221	|1	|   	|   	|
|Outsiders	|181	|1	|   	|   	|
|Doom Patrol	|168	|2	|   	|   	|
|Alpha Flight	|100	|1	|   	|   	|
|More than 500 	|35,993	|53	|   	|   	|
|More than 750   	|30,964	|30	|   	|   	|
|More than 1,000	|27,027	|21	|   	|   	|
|More than 2,000	|19,879	|9	|   	|   	|
|More than 4,000   	|12,191	|3	|   	|   	|

## Authors

* **Sean MacRae** - *Initial work* - [macrae](https://github.com/macrae)

## License

`<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.`

## Acknowledgments

Thanks to the good folks at [comics.org](https://comics.org) for their hard work building
and maintaining one of the richest databases of graphic novel covers and metadata. I
could not have done this without you!
