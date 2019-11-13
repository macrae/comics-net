# Deep Learning Utility for Comic Books

This project applies neural networks to comic book covers to perform a variety of
machine learning tasks, such as: 1) character classification (is a specific character
on a cover?) or 2) comic book synopsis generation (create arbitrary descriptions of an
issue based on the language of other issue synopses).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine
for development and testing.

### Prerequisites

Python3.6.9 is required to build and run the application. The list of third-party
dependencies can be found in the `requirements.txt` and `requirements-dev.txt` files.

### Installing

Create a Python3.6.9 virtual environment.

```
python3 -m venv .venv
```

If you get an error saying "returned non-zero exit status 1",
make sure you have Python3 and pip3 upgraded to the current version and
if that doesn't work, re-run the above command as:

```
python3 -m venv --without-pip .venv
```

Activate the virtual environemnt

```
source .venv/bin/activate
```

Install the third-party dependencies.

```
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
```

## Running the tests

We are using [pytest](https://docs.pytest.org/en/2.9.1/getting-started.html) for test
writing. Run this snippet in a terminal window to run the tests.

```
python3 -m pytest comics-net/* -vvsx
```

You can also run the test suite with a coverage report. Although it may not be possible to achieve 100% coverage - nor does 100% coverage ensure a well written test suite - it is still a useful heuristic in assessing overall application health.

```
pytest --cov-report html --cov functions --verbose
```

After running the coverage report, open the summary in your browser with the following.

```
open htmlcov/index.html
```

### Break down into end to end tests

...

```
test_get_task() # authenticates and gets task status
```

### And coding style tests

Check for PEP8 style guide adherence.

```
test_pep8(self)
```

## Using the Project

...

## Contributing

Please read [CONTRIBUTING.md](https://gitlab.healthcareit.net/smacrae/jira-api/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

Describe how we version here.

## Authors

* **Sean MacRae** - *Initial work* - [macrae](https://github.com/macrae)

See also the list of [contributors](https://github.com/macrae/comics-net/graphs/contributors) who participated in this project.

## License

This project is licensed under the GNU License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

...
