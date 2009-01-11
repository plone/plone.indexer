from zope.interface import implements
from zope.interface.declarations import Implements, implementedBy
from plone.indexer.interfaces import IIndexer

class DelegatingIndexer(object):
    """An indexer that delegates to a given callable
    """
    implements(IIndexer)
    
    def __init__(self, context, callable):
        self.context = context
        self.callable = callable
        
    def __call__(self, portal, **kwargs):
        kwargs = kwargs.copy()
        kwargs.setdefault('portal', portal)
        return self.callable(self.context, **kwargs)

class DelegatingIndexerFactory(object):
    """A factory for a DelegatingIndexer
    """
    
    def __init__(self, callable):
        self.callable = callable
        self.__implemented__ = Implements(implementedBy(DelegatingIndexer))
        
    def __call__(self, object):
        return DelegatingIndexer(object, self.callable)