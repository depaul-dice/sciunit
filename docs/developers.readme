# Instructions for developers working with Sciunit
# working with Ubuntu OS

# download Sciunit source code and rename project folder
git clone https://bitbucket.org/geotrust/sciunit2.git sciunit2-python3
cd sciunit2-python3

# install python3.x (>= version 3.7) 
# following is a suggested link:
# https://phoenixnap.com/kb/how-to-install-python-3-ubuntu

# install git version control system
sudo apt update
sudo apt install git

# install pip for python3
sudo apt-get install python3-pip

# install these packages
pip install --user --upgrade pytest-metadata
pip install --user --upgrade tox
sudo apt install cmake

# install the requiremenst from these two files:
# test-requirements.txt and requirements.txt.
# you can run the following:
pip install -r requirements.txt
pip install -r test-requirements.txt

# make sure you are up-to-date with the master branch
git pull origin master

# run the following command from the project folder to run all tests.
# All tests should pass. If there are any errors, follow
# error messages and resolve them first.
tox

# at this point, you can start adding your code to Sciunit 
# DO NOT start working in the master branch.
# make sure you checkout your own branch.
git checkout -b new_branch_name

# make sure all changes in your branch are committed locally and 
# pushed to the remote repository periodically.
# note: to push the changes, you would first need to be added as a contributor
git push origin master

# after you are done making changes, run tox again to make sure all tests pass.
# to test the installation in production, install your source code locally
pip install sciunit2-python3/

# after your changes are finalized in your branch, send a merge request with master
# after a code review and successful merge, package the code and upload to PyPI.
# you would need the credentials for the Sciunit account on PyPI
pip install --user --upgrade twine
python setup.py sdist bdist_wheel
twine upload dist/*


Some notes for understanding sciunit (for beginner developers):

Sciunit uses application virtualization (AV) tool provenance-to-use (PTU) built on top of Code, Data, and Environment (CDE) to containerize an application as it executes.
ptu creates a directory structure called cde-package
A tar archive of cde-package/ is sent to vvpkg for deduplication

1. Committing a package to the deduplicated storage:
	a. take an execution directory (cde-package/) as input 
	b. convert it into a tar archive
	c. vvpkg performs deduplication on the archive and stores it into blocks
2. Reconstructing an execution directory from the de-duplicated storage:
	a. extract relevant blocks from the vvpkg storage.
	b. create a tar archive by concatenating the blocks from the original file entries.
	c. untar the archive to get the execution directory
3.  'create' command does the following:
	a. creates an empty dir for the project
	b. opens the project
4. 'exec' does the following:
	a. creates a sciunit.db file in the project dir. 
	b. creates cde-package dir in the sciunit folder
	c. calls commit
		At the end of exec, *.json, vvpkg.bin and vvpkg.db files have 
		been created in the project folder.
5. 'commit' does this:
	a. archives the cde-package directory and writes it to vvpkg
	b. deletes the cde-package directory
	c. adds the new execution to sciunit db
6. 'repeat' does this:
	a. does ContextCheckout (see #7)
	b. reads execution commands from cde.log
	c. writes new cde.log with new arguments for the same execution commands
	d. creates a Script object from cde.log and executes it as a subprocess
7. ContextCheckout does this:
	a. removes any existing cde-package/ present
	b. checks out the given execution from the database using 'checkout' command.
	c. untar the archive obtained from checkout
	This builds cde-package directory as it was present at the time of the given execution.
