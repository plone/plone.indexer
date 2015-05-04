import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


version = '1.0.3'

long_description = (
    read('README.rst')
    + '\n' +
    read('plone', 'indexer', 'README.rst')
    + '\n' +
    read('CHANGES.rst')
    + '\n'
    )

setup(name='plone.indexer',
      version=version,
      description="Hooks to facilitate managing custom index values in "
                  "Zope 2/CMF applications",
      long_description=long_description,
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          "License :: OSI Approved :: BSD License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
        ],
      keywords='plone cmf zope catalog index',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/plone.indexer',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zope.interface',
          'zope.component',
          'Products.CMFCore',
          'Products.ZCatalog',
      ],
      )
