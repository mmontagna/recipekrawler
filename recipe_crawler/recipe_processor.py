from crawl.processors.Abstract import AbstractProcessor
from collections import defaultdict
import uuid, cStringIO, gzip, json, boto3, os, datetime
from time import time
from bs4 import BeautifulSoup
from urlparse import urlparse
import json

class GetRecipes(AbstractProcessor):
  def __init__(self):
    pass

  def process(self, crawlRequest, response):
    soup = BeautifulSoup(response.content, 'html.parser')
    ingredients = soup.find_all("span", {"class": "ingredients-item-name"})
    title = soup.find_all("title")[0]
    instructions = soup.find_all('section', {"class": "recipe-instructions"})
    if instructions:
      instructions = " ".join([x for x in instructions[0].text.split("\n") if x])

    recipe = {
      "ingredients": [x.text for x in ingredients],
      "title": title.text.split("|")[0],
      "instructions":  instructions
    }
    if ingredients:
      with open('output.recipes.json', 'a') as f:
        f.write(json.dumps(recipe))
        f.write("\n")
        print(recipe)
