# -*- coding: utf-8 -*-
from zope.component import testing

import doctest
import re
import six
import unittest


class TestWrapperUpdate(unittest.TestCase):

    def test_wrapper_update(self):
        from plone.indexer import indexer
        from zope.interface import Interface

        @indexer(Interface)
        def my_func(obj):
            """My custom docstring."""

        self.assertEqual(my_func.__doc__, 'My custom docstring.')
        self.assertEqual(my_func.__module__, 'plone.indexer.tests')
        self.assertEqual(my_func.__name__, 'my_func')


class Py23DocChecker(doctest.OutputChecker):
    def check_output(self, want, got, optionflags):
        if six.PY2:
            got = re.sub("u'(.*?)'", "'\\1'", got)
        return doctest.OutputChecker.check_output(self, want, got, optionflags)


def test_suite():
    return unittest.TestSuite([
        doctest.DocFileSuite(
            'README.rst',
            package='plone.indexer',
            setUp=testing.setUp,
            tearDown=testing.tearDown,
            checker=Py23DocChecker(),
            ),
        unittest.makeSuite(TestWrapperUpdate),
    ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
