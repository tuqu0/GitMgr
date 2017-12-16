# GitMgr

Manage GIT repositories

This script permits to update GIT repositories automatically and export GIT URLs.


Example:

- Update GIT Projects stored in the parent folder without user validation
  ./gitMgr.py -r .. -u -s

- Export GIT Projects URLs stored in the parent folder
  ./gitMgr.py -r .. -e gits.txt

- Download GIT Projects from configuration file gits.txt in tools directory
  ./gitMgr.py -r ./tools/ -i gits.txt