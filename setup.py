from setuptools import find_packages
from setuptools import setup

import os


version = "1.0.8.dev0"
description = "Hooks to facilitate managing custom index values in Zope 2/CMF applications"  # noqa
long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CHANGES.rst").read(),
        open(os.path.join("plone", "indexer", "README.rst")).read(),
    ]
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
    packages=find_packages(),
    namespace_packages=["plone"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "setuptools",
        "Products.CMFCore",
    ],
)
