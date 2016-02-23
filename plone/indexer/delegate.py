# -*- coding: utf-8 -*-
from functools import update_wrapper
from plone.indexer.interfaces import IIndexer
from zope.interface import implementer
from zope.interface.declarations import implementedBy
from zope.interface.declarations import Implements


@implementer(IIndexer)
class DelegatingIndexer(object):
    """An indexer that delegates to a given callable
    """

    def __init__(self, context, catalog, callable):
        self.context = context
        self.catalog = catalog
        self.callable = callable

    def __call__(self):
        return self.callable(self.context)


class DelegatingIndexerFactory(object):
    """An adapter factory for an IIndexer that works by calling a
    DelegatingIndexer.
    """

    def __init__(self, callable):
        self.callable = callable
        self.__implemented__ = Implements(implementedBy(DelegatingIndexer))
        update_wrapper(self, callable)

    def __call__(self, object, catalog=None):
        return DelegatingIndexer(object, catalog, self.callable)
