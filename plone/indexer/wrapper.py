from zope.interface import implements
from zope.interface import providedBy
from zope.interface.declarations import getObjectSpecification
from zope.interface.declarations import ObjectSpecification
from zope.interface.declarations import ObjectSpecificationDescriptor

from zope.component import queryAdapter

from plone.indexer.interfaces import IIndexableObjectWrapper
from plone.indexer.interfaces import IIndexer

class WrapperSpecification(ObjectSpecificationDescriptor):
    """A __providedBy__ decorator that returns the interfaces provided by
    the wrapped object when asked.
    """

    def __get__(self, inst, cls=None):
        if inst is None:
            return getObjectSpecification(cls)
        else:
            provided = providedBy(inst._IndexableObjectWrapper__object)
            cls = type(inst)
            return ObjectSpecification(provided, cls)

class IndexableObjectWrapper(object):
    """A simple wrapper for indexable objects that will delegate to IIndexer
    adapters as appropriate.
    """
    
    implements(IIndexableObjectWrapper)
    __providedBy__ = WrapperSpecification()
    
    def __init__(self, object, portal):
        self.__object = object
        self.__portal = portal
        self.__kwargs = {}
        self.__vars = {}

    def update(self, vars, **kwargs):
        self.__vars = vars
        self.__kwargs = kwargs

    def __str__(self):
        try:
            return self.__object.__str__()
        except AttributeError:
            return object.__str__(self)

    def __getattr__(self, name):
        
        # First, try workflow variables
        if name in self.__vars:
            return self.__vars[name]
            
        # Then try to look up IIndexer adapters
        indexer = queryAdapter(self.__object, IIndexer, name=name)
        if indexer is not None:
            return indexer(portal=self.__portal, **self.__kwargs)
        
        # Finally see if the object provides the attribute directly
        return getattr(self.__object, name)
