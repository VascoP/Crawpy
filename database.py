#!/usr/bin/python
from os import path

from sqlalchemy import *
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, column_property

from urlparse import urlparse, urljoin

from bs4 import BeautifulSoup as Soup
from bs4 import SoupStrainer

import requests as Reqs

from datetime import date
import logging


Base = declarative_base()

logging.basicConfig(level=logging.INFO, filename='logs/connection_errors_{}.log'.format(date.today()))


class Webpage(Base):
   # Administrivia
   __tablename__ = 'webpage'
   pk = Column(Integer, primary_key = True)
   first_craw_date = Column(DateTime, default=func.now())
   last_crawl_date = Column(DateTime, default=func.now(), onupdate=func.now())

   # Juice
   full_url = Column(String(4000, convert_unicode=True))     # Max url said to be 2000 characters
   html = Column(LONGTEXT(convert_unicode=True))
   num_crawls = Column(Integer, default = 1)
   num_harvests = Column(Integer, default = 0)
   
   
   def __init__(self, link):
      response = self.get_content(link)
      self.html = response.text
      self.full_url = response.url

   def __repr__(self):
      return "<Webpage('%s')>" % (self.full_url)

   def get_path(self):
      return urlparse(self.full_url).path

   def get_base_url(self):
      return urljoin(urlparse(self.full_url).scheme, urlparse(self.full_url).netloc)

   def extract_links(self):
      url_list = []
      only_a_tags = SoupStrainer("a", href=True)
      
      crawlable = ("http", "https", "")
      
      for url in Soup(self.html, parse_only=only_a_tags).find_all("a", href=True):
         url = url.get("href")
         url_scheme = urlparse(url).scheme
         if url_scheme in crawlable:
            # we got a full url here
            if url_scheme:
               url_list.append(url)
            # rebase that shit
            else:
               url_list.append(urljoin(self.full_url, url))
      return url_list

   def get_content(self, link):
      response = None
      while not response:
         try:
            response = Reqs.get(link)
         except Reqs.ConnectionError, e:
            logging.exception(e)
      return response

   def save_crawl(self, db):
      result = db.session.query(Webpage).filter(Webpage.full_url == self.full_url).first()
      if result is not None:
         result.num_crawls += 1
      else:
         db.session.add(self)
      return db

      

class Database(object):
   session = None

   #sqlite:///db.sqlite
   def __init__(self, db="mysql://root:@localhost/crawlerdb"):
      # Engine and schema creation
      self.engine = create_engine(db, encoding="utf8")
      Base.metadata.create_all(self.engine)
      # Get a session so we can do stuff
      Session = sessionmaker(bind=self.engine)
      self.session = Session()
      
      
   