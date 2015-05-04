Introduction
============

This package provides primitives to help delegate ZCatalog indexing operations
to adapters. It doesn't do very much on its own, but can be used by catalog
implementations that want to allow individual index values to be provided
not by the object itself, but by separate adapters.
