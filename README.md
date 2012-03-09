# crawpy
A (crappy) attempt at a python web crawler

### Usage

Create a mysql table and populate it with seed links.
Run as many explorers.py as desired.
After getting a few pages, start a harvester.py
You can run as many explorers as you like

### How it works
Each explorer gets uncrawled links from the database and retrieves their html contents.
The harvester gets an unharvested html content from the database, extracts links, and stores them in as uncrawled links.

### Todo

* Automate explorer/harvester relation.
* Better error handling.
