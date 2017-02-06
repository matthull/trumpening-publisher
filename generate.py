import os
import datetime
import dateutil.parser
import json
from itertools import groupby
from operator import itemgetter
from urllib.request import urlopen
from jinja2 import Environment, FileSystemLoader

jinja = Environment(loader=FileSystemLoader('templates'))

def date_header(dt):
  dt.strftime("%B %d, %Y")

jinja.filters['dateheader'] = date_header

def article_from_json(json):
  day = dateutil.parser.parse(json['time']).date()
  url = json['href']
  name = json['description']
  return {"day": day, "url": url, "name": name}

pin_key = os.environ['PINBOARD_KEY']
pin_url = "https://api.pinboard.in/v1/posts/all/?auth_token={pin_key!s}&format=json".format(**locals())
response = urlopen(pin_url).read()
articles_json = json.loads(response.decode('utf-8'))
articles = [article_from_json(j) for j in articles_json]

days = {}
for a in sorted(articles, key=itemgetter('day')):
  day = days[a['day']]
  days[day] = days.get(day) or []
  days[day].append(a)

context = {"days": days}

def main():
  template = jinja.get_template('index.html')
  with open('output/index.html', 'w') as f:
    html = template.render(context)
    f.write(html)

if __name__ == "__main__":
  main()
