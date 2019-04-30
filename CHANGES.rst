Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

1.0.6 (2019-04-29)
------------------

Bug fixes:


- Fixed: doctests on Python 2 were not correctly checked.  [maurits] (#7)


1.0.5 (2018-09-26)
------------------

Fixes:

- fix https://github.com/plone/Products.CMFPlone/issues/2469:
  "Subobjects are indexing attributes of parent".
  Allow only direct attributes and acquired PythonScripts,
  but not acquired attributes.
  Indexers and PythonScripts are able to handle this explicitly,
  because they get the acquisition-wrapped object.
  [jensens]

- Fix tests to work in Python 3
  [pbauer]


1.0.4 (2016-02-25)
------------------

Fixes:

- Replace deprecated ``zope.testing.doctestunit`` import with ``doctest``
  module from stdlib.
  [thet]

- Reformat according to the Plone styleguide.
  [thet]


1.0.3 (2015-05-05)
------------------

- Add missing dependency on Products.ZCatalog.
  [gforcada]


1.0.2 (2013-01-13)
------------------

- Changed the @indexer decorator to maintain the information about the wrapped
  function (__doc__, __module__, __name__, etc).
  [dokai]


1.0.1 (2012-12-14)
------------------

- Relicense under modified BSD license; per Plone Foundation board
  approval on 2012-05-31.
  See: http://plone.org/foundation/materials/foundation-resolutions/plone-framework-components-relicensing-policy
  [supton]

- Add MANIFEST.in.
  [WouterVH]


1.0 - 2010-07-18
----------------

- Fixed reSt markup in the changelog.
  [hannosch]

- Update license to GPL version 2 only.
  [hannosch]


1.0rc2 - 2009-04-05
-------------------

- Added _getWrappedObject() method to get hold of the underlying object.
  Note that this means you can't have an index/metadata column with this name.
  [optilude]

- Corrected IZCatalog import location to point to the interfaces module.
  [hannosch]


1.0rc1 - 2009-03-26
-------------------

- Updated the interface to match the developments of similar functionality
  on CMF trunk. This means that indexers are now multi-adapters on
  (object, catalog), and the keyword arguments (including the implicit
  'portal' parameter) are gone.
  [optilude]


1.0a1 - 2009-03-05
------------------

- Initial release
