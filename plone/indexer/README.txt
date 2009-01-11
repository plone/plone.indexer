Introduction
============

This package provides primitives to help delegate ZCatalog indexing operations
to adapters. It doesn't do very much on its own, but can be used by catalog
implementations that want to allow individual index values to be provided
not by the object itself, but by separate adapters.

Writing indexers
================

An indexer is a named adapter that adapts the type of an object and provides
a value to be indexed when the catalog attempts to index the attribute with
that name.

For example, let's say we have two types, page and news item:

    >>> from zope.interface import implements, Interface
    >>> from zope import schema

    >>> class IPage(Interface):
    ...     text = schema.Text(title=u"Body text")
    >>> class Page(object):
    ...     implements(IPage)
    ...     def __init__(self, text):
    ...         self.text = text

    >>> class INewsItem(Interface):
    ...     summary = schema.TextLine(title=u"Short summary")
    ...     story = schema.Text(title=u"Body text")
    ...     audience = schema.TextLine(title=u"Audience")

    >>> class NewsItem(object):
    ...     implements(INewsItem)
    ...     def __init__(self, summary, story, audience):
    ...         self.summary = summary
    ...         self.story = story
    ...         self.audience = audience

Now, pretned that our catalog had an index 'description', which for a page
should contain the first 10 characters from the body text, and for a news
item should contain the contents of the 'summary' field. Furthermore, there
is an index 'audience' that should contain the value of the corresponding
field for news items, but in all uppercase, unless the 'noupper' keyword
argument is passed to catalog_object(). It should do nothing for pages.

We could write indexers for all of these like this

    >>> from plone.indexer.decorator import indexer
    
    >>> @indexer(IPage)
    ... def page_description(object, **kw):
    ...     return object.text[:10]

    >>> @indexer(INewsItem)
    ... def newsitem_description(object, **kw):
    ...     return object.summary

    >>> @indexer(INewsItem)
    ... def newsitem_audience(object, **kw):
    ...     if 'noupper' in kw:
    ...         return object.audience
    ...     return object.audience.upper()

Hint: If you require access to the portal root for any reason, e.g. to acquire
tools, then use kw['portal'] or simply declare that your indexer takes a
'portal' argument.

These need to be registered as named adapters, where the name corresponds to
the index name. In ZCML, that may be:

    <adapter name="description" factory=".indexers.page_description" />
    <adapter name="description" factory=".indexers.newsitem_description" />
    <adapter name="audience" factory=".indexers.newsitem_audience" />

We can omit the 'for' attribute because we passed this to the @indexer
decorator, and we can omit the 'provides' attribute because the thing 
returned by the decorator is actually a class providing the required IIndexer
interface.

For the purposes of the ensuing tests, we'll register these directly.

    >>> from zope.component import provideAdapter
    >>> provideAdapter(page_description, name='description')
    >>> provideAdapter(newsitem_description, name='description')
    >>> provideAdapter(newsitem_audience, name='audience')

If you're only curious about how to write indexers, you can probably stop
here. If you want to know more about how they work and how they are wired into
a framework, read on.

Hooking up indexers to the framework
=====================================

Here is a mock implementation of a ZCatalog.catalog_object() override, based
on the one in Plone. We'll use this for testing. We won't bother with the full
ZCatalog interface, only catalog_object(), and we'll stub out a few things.
This really is for illustration purposes only, to show the intended usage
pattern.

    >>> from plone.indexer.interfaces import IIndexableObjectWrapper
    >>> from zope.component import getMultiAdapter

    >>> class FauxCatalog(object):
    ...
    ...     workflow_vars = {} # for testing only
    ...     
    ...     def __init__(self, portal):
    ...         self.portal = portal
    ...     
    ...     def catalog_object(self, object, uid, idxs=[], **kwargs):
    ...         """Pretend to index 'object' under the key 'uid'. We'll look
    ...         in self.workflow_vars[uid] for a dict of workflow variables
    ...         that will be passed to the indexable object wrapper. We'll
    ...         print the results of the indexing operation to the screen .
    ...         """
    ...         vars = self.workflow_vars.get(uid, {})
    ...         
    ...         # Look up the indexable object wrapper and initialise it
    ...         wrapper = getMultiAdapter((object, self.portal), IIndexableObjectWrapper)
    ...         wrapper.update(vars, **kwargs)
    ...         
    ...         # Perform the actual indexing of attributes in the idxs list
    ...         for idx in idxs:
    ...             try:
    ...                 indexed_value = getattr(wrapper, idx)
    ...                 if callable(indexed_value):
    ...                     indexed_value = indexed_value()
    ...                 print idx, "=", indexed_value
    ...             except (AttributeError, TypeError,):
    ...                 pass

The important things here are:

    - We look up an IndexableObjectWrapper adapter on (object, portal). This
      is just a way to get hold of an implementation of this interface (we'll
      register one in a moment) and allow some coarse-grained overrides.
      
    - The IndexableObjectWrapper has to be updated with workflow variables
      (or other variables) and keyword arguments as passed to catalog_object()
      
    - Cataloging involves looking up attributes on the indexable object 
      wrapper matching the names of indexes (in the real ZCatalog, this is
      actually decoupled, but let's not get carried away). If they are
      callable, they should be called. This is just mimicking what ZCatalog's
      implementation does.
      
This package comes with an implementation of IIndexableObjectWrapper that
knows how to delegate to an IIndexer. Let's now register that as the default
IIndexableObjectWrapper adapter so that the code above will find it.

    >>> from plone.indexer.wrapper import IndexableObjectWrapper
    >>> provideAdapter(IndexableObjectWrapper, (Interface, Interface))

Seeing it in action
===================

Now for the testing. First, we need a faux portal:

    >>> class Portal(object):
    ...     implements(Interface)
    >>> portal = Portal()

Then we need a catalog to test with:

    >>> catalog = FauxCatalog(portal)

Finally, let's create some objects to index.

    >>> page = Page(u"The page body text here")
    >>> news = NewsItem(u"News summary", u"News body text", u"Audience")

First of all, let's demonstrate that our indexers work and apply only to
the types for which they are registered.

    >>> catalog.catalog_object(page, 'p1', idxs=['description', 'audience'])
    description = The page b

    >>> catalog.catalog_object(news, 'n1', idxs=['description', 'audience'])
    description = News summary
    audience = AUDIENCE

Keyword arguments are also passed through to the indexers.

    >>> catalog.catalog_object(news, 'n2', idxs=['audience'], noupper=True)
    audience = Audience

The indexable object wrapper will return the variables provided to update()
if the name matches, in preference of using indexers.

    >>> catalog.workflow_vars['p2'] = dict(state='Published', description='Overridden!')
    >>> catalog.catalog_object(page, 'p2', idxs=['state', 'description'])
    state = Published
    description = Overridden!

Finally, if not adapter can be found, we fall back on getattr() on the object.

    >>> catalog.catalog_object(page, 'p3', idxs=['description', 'text'])
    description = The page b
    text = The page body text here