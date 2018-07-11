# -*- coding: utf-8 -*-
from Acquisition import aq_base
from plone.indexer.interfaces import IIndexableObject
from plone.indexer.interfaces import IIndexableObjectWrapper
from plone.indexer.interfaces import IIndexer
from Products.CMFCore.utils import getToolByName
from Products.ZCatalog.interfaces import IZCatalog
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import providedBy
from zope.interface.declarations import getObjectSpecification
from zope.interface.declarations import ObjectSpecification
from zope.interface.declarations import ObjectSpecificationDescriptor


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


@implementer(IIndexableObject, IIndexableObjectWrapper)
@adapter(Interface, IZCatalog)
class IndexableObjectWrapper(object):
    """A simple wrapper for indexable objects that will delegate to IIndexer
    adapters as appropriate.
    """
    __providedBy__ = WrapperSpecification()

    def __init__(self, object, catalog):
        self.__object = object
        self.__catalog = catalog
        self.__vars = {}

        portal_workflow = getToolByName(catalog, 'portal_workflow', None)
        if portal_workflow is not None:
            self.__vars = portal_workflow.getCatalogVariablesFor(object)

    def _getWrappedObject(self):
        return self.__object

    def __str__(self):
        try:
            return self.__object.__str__()
        except AttributeError:
            return object.__str__(self)

    def __getattr__(self, name):
        # First, try to look up an indexer adapter
        indexer = queryMultiAdapter(
            (self.__object, self.__catalog),
            IIndexer, name=name,
        )
        if indexer is not None:
            return indexer()

        # Then, try workflow variables
        if name in self.__vars:
            return self.__vars[name]

        # first lets see if there is an attribute at all,
        # here we may already raise an AttributeError, which is fine
        value_or_callable = getattr(self.__object, name)
        try:
            # then lets see if the object provides the attribute directly,
            # w/o acquisition.
            getattr(aq_base(self.__object), name)
        except AttributeError:
            # it does not!
            # PythonScripts are the only way to add indexers TTW.
            # If there is a PythonScript acquired, thats fine:
            if (
                getattr(
                    value_or_callable,
                    'meta_type',
                    None,
                ) == 'Script (Python)'
            ):
                return value_or_callable
            raise
        # here we know it is a direct attribute.
        # we return the attribute acquistion wrapped in order to enable
        # callables to use acquisition.
        return value_or_callable
