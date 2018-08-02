Vector Pack
===========

This library implements some different heuristic algorithms for vector packing. 

In addition to the author's own implementations (stillwell_current) it also 
contains a problem set generator described in Caprara and Toth 2001, and interfaces
to python libraries based on OpenOpt, Gabay and Zaourar 2013, and Brandao 2013.

Setup
-----

When using vpack as dependency with pip, you need to download the dependency-links.
This is required because `vsvbp` and `vpsolver` are not available directly on _Pypi_

```
pip install -r requirements.txt --process-dependency-links
```
