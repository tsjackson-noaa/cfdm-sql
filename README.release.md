* Change the version and date in cfdm/core/__init__.py (__version__
  and __date__ variables)

* If required, change the CF conventions version in
  cfdm/core/__init__.py (__cf_version__ variable)

* Make sure that README.md is up to date.

* Make sure that Changelog.rst is up to date.

* Make sure that any new attributes, methods and keyword arguments (as
  listed in the change log) have on-line documentation. This may
  require additions to the .rst files in docs/source/class/

* Create a link to the new documentation in docs/source/releases.rst

* If groups are ready then remove the Hierarchical Groups placeholders
  in the documentation files: setup.py, README.md,
  docs/source/introduction.rst, docs/source/tutorial.rst (and delete
  this instruction).

* Make sure that the correct path to the cfdm library is in the
  PYTHONPATH environment variable:

export PYTHONPATH=$PWD:$PYTHONPATH

* Create a source tarball using `python setup.py sdist`

* Test the tarball release using `./test_release <vn>`
  (e.g. ./test_release 1.8.1). Do this for python2.7 and python3.

* Test tutorial code:

cd docs/source
./extract_tutorial_code
./reset_test_tutorial
cd test_tutorial
python ../tutorial.py

* Update the latest documentation using `./release_docs <vn> latest`
  (e.g. ./release_docs 1.8.1 latest).
  
* Create an archived copy of the documentation using
  `./release_docs <vn> archive` (e.g. ./release_docs 1.8.1 archive)

* Push recent commits using `git push origin master`

* Tag the release using `./tag <vn>` (e.g. ./tag 1.8.1)

* Upload the source tarball to PyPi
