import unittest

from zope.testing import doctestunit
from zope.component import testing

def test_suite():
    return unittest.TestSuite([
        doctestunit.DocFileSuite(
            'README.txt', package='plone.indexer',
            setUp=testing.setUp, tearDown=testing.tearDown),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
