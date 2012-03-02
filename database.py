#!/usr/bin/python
from os import path

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, column_property
from sqlalchemy.ext.declarative import declarative_base

from urlparse import urlparse, urljoin

from bs4 import BeautifulSoup as Soup
from bs4 import SoupStrainer

import requests as Reqs



Base = declarative_base()


class Webpage(Base):
   # Administrivia
   __tablename__ = 'webpage'
   pk = Column(Integer, primary_key = True)
   first_craw_date = Column(DateTime, default=func.now())
   last_crawl_date = Column(DateTime, default=func.now(), onupdate=func.now())

   # Juice
   full_url = Column(String)
   html = Column(String)
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
      only_a_tags = SoupStrainer("a", href=True)
      url_list = [url.get("href") if urlparse(url.get("href")).scheme else urljoin(self.full_url, url.get("href")) for url in Soup(self.html, parse_only=only_a_tags).find_all("a", href=True)]
      return url_list

   def get_content(self, link):
      return Reqs.get(link)

   def save_crawl(self, db):
      result = db.session.query(Webpage).filter(Webpage.full_url == self.full_url).first()
      if result is not None:
         result.num_crawls += 1
      else:
         db.session.add(self)
      return db

      

class Database(object):
   session = None

   def __init__(self, db="sqlite:///db.sqlite"):
      # Engine and schema creation
      self.engine = create_engine(db)
      Base.metadata.create_all(self.engine)
      # Get a session so we can do stuff
      Session = sessionmaker(bind=self.engine)
      self.session = Session()
      
      
   