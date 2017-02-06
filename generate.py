import datetime
from jinja2 import Environment, FileSystemLoader
jinja = Environment(loader=FileSystemLoader('templates'))

def date_header(dt):
  dt.strftime("%B %d, %Y")

jinja.filters['dateheader'] = date_header

fixtures = {
    datetime.date(2017, 1, 1): [
      {
        "name": "Trump be stupid",
        "url":  "http://google.com"
      },
      {
        "name": "Trump be mo' stupid",
        "url":  "http://yahoo.com"
      }
    ],

    datetime.date(2017, 1, 2): [
      {
        "name": "Trump is stupidest",
        "url":  "http://yahoo.com"
      }
    ]
}

context = {"days": fixtures}

def main():
  template = jinja.get_template('index.html')
  with open('output/index.html', 'w') as f:
    html = template.render(context)
    f.write(html)

if __name__ == "__main__":
  main()
