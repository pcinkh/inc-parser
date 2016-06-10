Inc.com scrapper
================

Install Mac OS X:
*****************

.. code-block:: bash

    # download and install Java JDK from http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html

    # install from brew
    brew update
    brew install python3 sqlite phantomjs

    # Python 3.5
    pip3 install virtualenv

    # create vitrualenv
    virtualenv env

    # activate vitrualenv
    source env/bin/activate

    # verify Python version
    python --version
    # Python 3.5.0

    # install python packages
    pip install -r requirements.txt

Run and notices:
****************

.. code-block:: bash

    # run
    p scrap.py

    # scrap.db and data will be reinitialized every time when script runs
