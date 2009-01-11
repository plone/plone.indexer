"""This module defines a decorator that 
"""

from zope.component import adapter
from plone.indexer.delegate import DelegatingIndexerFactory

class indexer(adapter):
    """The @indexer decorator can be used like this:

        >>> from plone.indexer.decorator import indexer
        >>> @indexer(IMyType)
        ... def some_attribute(object, **kw):
        ...     return "some indexable value"
    
    If you require the portal root, you can do:
    
        >>> from plone.indexer.decorator import indexer
        >>> @indexer(IMyType)
        ... def some_attribute(object, portal, **kw):
        ...     return "some indexable value"
    
    because 'portal' is guaranteed to be in the keyword arguments.
    
    Note that the @indexer decorator is a superset of the @adapter decorator
    from zope.component.
    
    Once you've done this, you can register the adapter in ZCML:

        <adapter factory=".myindexers.some_attribute" name="some_attribute" />
    
    At this point, the indexable object wrapper will ensure that when
    some_attribute is indexed on an object providing IMyType
    """

    def __init__(self, *interfaces):
        adapter.__init__(self, *interfaces)

    def __call__(self, callable):
        factory =  DelegatingIndexerFactory(callable)
        return adapter.__call__(self, factory)
