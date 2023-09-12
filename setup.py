"""setup.py file for nrsur_catalog package."""
import codecs
import re
import os
import sys
from setuptools import find_packages, setup

NAME = "nrsur_catalog"
HERE = os.path.dirname(os.path.realpath(__file__))
META_PATH = os.path.join("src", NAME, "__init__.py")

# require python 3.8 or higher
if sys.version_info < (3, 8):
    raise RuntimeError("nrsur_catalog requires python 3.8 or higher")


def read(*parts):
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


def find_meta(meta, meta_file=read(META_PATH)):
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta), meta_file, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


INSTALL_REQUIRES = [
    "matplotlib",
    "loguru",
    "bilby[gw]",
]
EXTRA_REQUIRE = dict(
    dev=[
        "jupyter-book>=0.13.2",
        # "zenodo_python @ git+https://github.com/avivajpeyi/zenodo-python.git@main#egg",
        "ploomber-engine>=0.0.23",
        "tabulate",
        "jupytext",  # for converting py-ipynb
        "ghp-import",  # for publishing to github pages
        "sphinx_inline_tabs",  # for tabs (https://sphinx-inline-tabs.readthedocs.io/en/latest/)
        "pytest",
        "GitPython",
        "sphinx-inline-tabs",
        "sphinxcontrib-bibtex",
        "plotly",
        "papermill",
        "nbconvert",
        'itables',
        'pytest-mock',
    ]
)

setup(
    name=NAME,
    version=find_meta("version"),
    author=find_meta("author"),
    author_email=find_meta("email"),
    maintainer=find_meta("author"),
    maintainer_email=find_meta("email"),
    url=find_meta("uri"),
    license=find_meta("license"),
    description=find_meta("description"),
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={NAME: [
        "api/lvk_urls.txt",
        "api/nrsur_urls.txt",
        "style.mplstyle",
    ]},
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRA_REQUIRE,
    zip_safe=True,
    entry_points={
        "console_scripts": [
            f"get_nrsur_event={NAME}.api.download_event:main",
        ]
    },
)
