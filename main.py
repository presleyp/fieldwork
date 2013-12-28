#!/usr/bin/env python
#
from webapp2 import RequestHandler, WSGIApplication
from os import path
import logging

### templates
from jinja2 import Environment, FileSystemLoader
template_dir = path.join(path.dirname(__file__), 'templates')
env = Environment(loader = FileSystemLoader(template_dir), autoescape = True)

### model
import sqlalchemy as sa
from model import connection, alljoined

### data structures

def pretty(word):
    return word.replace('_', ' ')

class Attribute():
    def __init__(self, dbname, values):
        self.dbname = dbname
        self.pretty = pretty(dbname)
        self.values = values

    def check_values(self, request):
        for value in self.values:
            value.checked = 'checked' if value.dbname in request else ''

    def where_clause(self):
        pieces = [alljoined.c[self.dbname] == value.pretty
                  for value in self.values if value.checked == 'checked']
        return sa.or_(*pieces)

class Value():
    def __init__(self, dbname, checked = ''):
        self.dbname = dbname
        self.pretty = pretty(dbname)
        self.checked = checked


### Page Handlers

class MainHandler(RequestHandler):

    def get_data(self, attributes):
        where_clause = [attribute.where_clause() for attribute in attributes]
        select_stmt = sa.select([alljoined]).where(sa.and_(*where_clause))
        results = connection.execute(select_stmt)
        return results

    def get(self):
        attributes = [Attribute('Type',
                                [Value('CV_Textgrid'),
                                 Value('Rhyme_Textgrid'),
                                 Value('Syllable_Textgrid')]),
                      Attribute('Speaker_Gender',
                                [Value('F'), Value('M')]),
                      Attribute('Target_Tone', [Value('H'),
                                         Value('L'),
                                         Value('HH'),
                                         Value('LL'),
                                         Value('HL'),
                                         Value('LH'),
                                         Value('R'),
                                         Value('F')])]

        for attribute in attributes:
            attribute.check_values(self.request.get_all(attribute.dbname))
        data = self.get_data(attributes)
        cols = [pretty(col.name) for col in alljoined.c]
        home_vars = {'attributes': attributes, 'rows': data, 'cols': cols}
        homepage = env.get_template('home.html').render(home_vars)
        self.response.write(homepage)

    #TODO file download
    #TODO order by
    #TODO select cols

class AboutHandler(RequestHandler):
    def get(self):
        about_page = env.get_template('about.html').render()
        self.response.write(about_page)


### Error Handlers

def handle_404(request, response, exception):
    logging.exception(exception)
    response.write("Sorry, you can't get there from here.")
    response.set_status(404)

def handle_500(request, response, exception):
    logging.exception(exception)
    response.write('A server error occurred.')
    response.set_status(500)

### Routing

app = WSGIApplication([('/', MainHandler),
                       ('/about', AboutHandler)],
                      debug=True)

app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500

### Run

def main():
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()
