#!/usr/bin/python3.4
from bottle import route, run, template, hook, response
import ParserExito as PE
import simplejson as json

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

@route('/hello/<name>')
def index(name):
        return template('<b>Hello {{name}}</b>!', name=name)

@route('/exito/fp')
def exito():
    url_exito_fp="https://www.exito.com"
    #PE.parse_exito_fp(url_exito_fp)
    exito_parsed=PE.parse_exito_fp(url_exito_fp)
    if (exito_parsed is None):
        print("ERROR!! jsonExito is NULL\n")
    jsonExito = json.dumps(exito_parsed,indent=4)
    return jsonExito

@route('/exito/matress')
def exito():
    url_exito_matress="http://www.exito.com/Hogar_y_decoracion-Dormitorio-Colchones/_/N-2cnf"
    #PE.parse_exito_fp(url_exito_fp)
    exito_parsed=PE.parse_exito_matress(url_exito_matress)
    if (exito_parsed is None):
        print("ERROR!! jsonExito is NULL\n")
    jsonExito = json.dumps(exito_parsed,indent=4)
    return jsonExito

run(host='192.168.10.101', port=12345)
