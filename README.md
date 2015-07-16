Finspire-front
==============

findspire-front is the software in charge of serving Findspire clients with WEB pages as well as serving JSON/REST WebServices.

Dependencies
------------

There are lots of them. The easiest and safest way to install them all is to use
Vagrant to provision a development VM:

- install vagrant (using your package manager or
  [from the website](http://downloads.vagrantup.com/))
- run `vagrant up` (this will take a few minutes the first time)
- connect using `vagrant ssh` and start the dev server with `./runserver` (which
  will also start needed services), this should be done automatically the first time

Inside the VM, the code is available in the shared folder `/vagrant`.

During the dev, if you add new dependencies, **be sure to update the following files**:

- `requirements.txt` for Python libraries installed with `pip` (use `pip freeze` to list them)
- the `bootstrap-vagrant.sh` script for anything installed with `apt-get`.

Unit tests
----------

There are not so many of them for now :) They are written using the famous
[`nose`](https://nose.readthedocs.org/en/latest/) library, which nicely extends
[`unittest`](http://docs.python.org/2/library/unittest.html) from the standard
library.

At the moment, only the Media and Upload APIs are unit-tested. Which means that
when working on these components, it is *mandatory* to:

- run all the tests before committing;
- add new tests and/or fix existing tests when changing anything.

The tests are located in the `test/` directory. You can run them with `nosetests`:

    $ nosetests tests
