from setuptools import setup, find_packages
import os

version = '1.0rc1'

setup(name='plone.indexer',
      version=version,
      description="Hooks to facilitate managing custom index values in Zope 2/CMF applications",
      long_description=open(os.path.join("plone", "indexer", "README.txt")).read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone cmf zope catalog index',
      author='Martin Aspeli',
      author_email='optilude@gmail.com',
      url='http://pypi.python.org/pypi/plone.indexer',
      license='LGPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zope.interface',
          'zope.component',
          'Products.CMFCore',
      ],
      entry_points="""
      """,
      )
