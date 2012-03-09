# crawpy
An attempt at a python web crawler

### Usage

Create a mysql table. If you don't know how to do this I recommend using phpmyadmin. Collation should be `utf8_general_ci`.
Now you can add links to the database directly or you can edit the `SEED_LINKS` list in `settings.py` and run `python explorer.py --seed`.
If you're in a hurry you can leave `settings.py` alone and just seed from the command line with `python explorer.py http://myfirstseed.com http://mysecondseed.net ...`.

The seeding procedure is only required if you have no uncrawled links in your database (ie: first time running the crawler)
Customize `settings.py` with your database *settings*
Run as many `explorer.py` as desired.
After getting a few pages, start a `harvester.py`
You can run as many explorers as you like

### How it works
Each explorer gets uncrawled links from the database and retrieves their html contents.
The harvester gets an unharvested html content from the database, extracts links, and stores them in as uncrawled links.

### Todo

* Automate explorer/harvester relation
* Better error handling
