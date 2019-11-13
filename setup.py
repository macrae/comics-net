import os
import subprocess
from distutils.command.build import build
from itertools import chain

from setuptools import find_packages, setup

package_name = "comics_net"

with open(os.path.join(os.getcwd(), "VERSION")) as version_file:
    version = version_file.read().strip()


def parse_requirements(file):
    with open(file, "r") as fs:
        return [
            r
            for r in fs.read().splitlines()
            if (
                len(r.strip()) > 0
                and not r.strip().startswith("#")
                and not r.strip().startswith("--")
            )
        ]


requirements = parse_requirements("requirements.txt")


def mypy_typecheck():
    err_msg = "[SKIP] WARNING: mypy is not installed -- *NOT* type checking"
    try:
        with open(os.devnull, "w") as FNULL:
            exit_code = subprocess.call(
                ["mypy", "-h"], stdout=FNULL, stderr=subprocess.STDOUT
            )
            if exit_code != 0:
                print(err_msg)
                return
    except FileNotFoundError:
        print(err_msg)
        return

    def list_files(directory):
        for dirpath, dirnames, filenames in os.walk(directory):
            for f in filenames:
                fpath = os.path.join(dirpath, f)
                if os.path.isfile(fpath):
                    yield fpath

    def py_file(filename):
        return filename.endswith(".py") or filename.endswith(".pyx")

    project_py_files = list(
        filter(
            lambda x: "setup.py" not in x,
            chain(*[filter(py_file, list_files(loc)) for loc in ["."]]),
        )
    )

    mypy_command = ["mypy", "--ignore-missing-imports"] + project_py_files

    print(f"Typechecking with mypy:")
    exit_code = subprocess.call(mypy_command)
    if exit_code is not 0:
        print("\n\nERROR: type checking failed -- type errors detected")
        exit(exit_code)
    else:
        print("--> project checks out")


class BuildCmd(build):
    def run(self):
        mypy_typecheck()
        build.run(self)


setup(
    name=package_name,
    version=version,
    license="GNU General Public License",
    description="A deep learning utility for comic book covers",
    author="Sean MacRae",
    author_email="s.mac925@gmail.com",
    url="https://github.com/macrae/comics-net",
    packages=find_packages(exclude=["tests"]),
    cmdclass={"build": BuildCmd},
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
)
