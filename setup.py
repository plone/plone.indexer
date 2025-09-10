from pathlib import Path
from setuptools import find_packages
from setuptools import setup


version = "2.0.2"

description = "Hooks to facilitate managing custom index values in Zope 2/CMF applications"  # noqa
long_description = (
    f"{Path('README.rst').read_text()}\n"
    f"{Path('CHANGES.rst').read_text()}\n"
    f"{(Path('src') / 'plone' / 'indexer' / 'README.rst').read_text()}"
)

setup(
    name="plone.indexer",
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="plone cmf zope catalog index",
    author="Plone Foundation",
    author_email="plone-developers@lists.sourceforge.net",
    url="https://pypi.org/project/plone.indexer",
    license="BSD",
    packages=find_packages("src"),
    namespace_packages=["plone"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "setuptools",
        "Products.CMFCore",
        "Zope",
    ],
)
