from zope.interface import Interface

class IIndexer(Interface):
    """A component that can provide the value for an catalog index.
    
    Register a named adapter from an indexable object type (e.g. a content
    object) to this interface. The name of the adapter should be the same
    as the name of the indexable attribute in the catalog.
    """
    
    def __call__(self, portal, **kwargs):
        """Return the value to index. portal is the portal root. Keyword
        arguments are passed from the original ZCatalog.catalog_object() call.
        """
        
class IIndexableObjectWrapper(Interface):
    """An adapter of a (object, portal) where object is to be indexed in 
    portal_catalog. The catalog will call getattr() on the wrapper for
    each attribute to be indexed. The wrapper may either implement these
    directly (as methods taking no parameters) or implement __getattr__()
    appropriately.
    
    The update() method will be called before the catalog is given the
    wrapper.
    """
    
    def update(vars, **kwargs):
        """Update the wrapper with variables from e.g. the workflow
        tool, and values passed to catalog_object().
        """