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
from model import connection, from_clause, columns

### data structures

class Attribute():
    def __init__(self, pretty, dbname, values):
        self.pretty = pretty
        self.dbname = `dbname`
        self.nospaces = self.pretty.lower().replace(' ', '_')
        self.values = values

    def check_values(self, request):
        for value in self.values:
            value.checked = 'checked' if value.nospaces in request else ''

    def where_clause(self):
        return ' OR '.join([self.dbname + '=' + value.dbname
                     for value in self.values if value.checked == 'checked'])

class Value():
    def __init__(self, pretty, dbname, checked = ''):
        self.pretty = pretty
        self.dbname = `dbname`
        self.nospaces = self.pretty.lower().replace(' ', '_')
        self.checked = checked


### Page Handlers

class MainHandler(RequestHandler):

    def get_data(self, attributes):
        where_clause = [attribute.where_clause() for attribute in attributes]
        select_stmt = sa.select(columns, from_obj = from_clause).where(sa.and_(*where_clause))
        results = connection.execute(select_stmt)
        return results

    def get(self):
        attributes = [Attribute('Analysis Type', 'AnalysisType.type',
                                [Value('CV Textgrid', 'CV Textgrid'),
                                 Value('Rhyme Textgrid', 'Rime Textgrid'),
                                 Value('Syllable Textgrid', 'Syllable Textgrid')]),
                      Attribute('Speaker Gender', 'Speaker.gender',
                                [Value('Female', 'F'), Value('Male', 'M')]),
                      Attribute('Tone', 'Sentence.target_tone', [Value('High', 'H'),
                                                                 Value('Low', 'L'),
                                                                 Value('High High', 'HH'),
                                                                 Value('Low Low', 'LL'),
                                                                 Value('High Low', 'HL'),
                                                                 Value('Low High', 'LH'),
                                                                 Value('Rising', 'R'),
                                                                 Value('Flat', 'F')])]

        for attribute in attributes:
            attribute.check_values(self.request.get_all(attribute.nospaces))
        data = self.get_data(attributes)
        home_vars = {'attributes': attributes, 'rows': data}
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
