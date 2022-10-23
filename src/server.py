# Web Demo Project
# Server side
#
#
# Copyright (C) 2022 Maksim Petrenko
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


# Standard library
import os
import random
import sqlite3
from wsgiref import simple_server
import urllib.parse


# Constants
DATABASE = "database.db"
STATIC = "static" + os.sep
TEST = STATIC + "test_template.html"
RESULTS = STATIC + "results_template.html"
SQL_SELECT = "SELECT ITEM, NAME FROM TIPI"
CSS = STATIC + "style.css"
PROMPT = "Server ready at http://localhost:8000/ \nCtrl-C to stop"
REV = {"7": 1, "6": 2, "5": 3, "4": 4, "3": 5, "2": 6, "1": 7}


# Globals
conn = sqlite3.connect(DATABASE)
with open(TEST, encoding="utf-8") as FILE:
    test = FILE.read()
with open(RESULTS, encoding="utf-8") as FILE:
    results = FILE.read()


# Web Application
def application(environ, start_response):
    """Web Application"""
    status = "200 OK"
    # GET
    if environ["REQUEST_METHOD"] == "GET":
        # HTML
        if environ["PATH_INFO"] == "/":
            mime_type = "text/html"
            with conn:
                data = [*conn.execute(SQL_SELECT)]
            random.shuffle(data)
            body = [test.format(*data).encode("utf-8")]
        # CSS
        elif environ["PATH_INFO"] == "/style.css":
            mime_type = "text/css"
            body = environ["wsgi.file_wrapper"](open(CSS, "rb"))
        # Not Found
        else:
            status = "404 Not Found"
            mime_type = "text/plain"
            body = [b"404 Not Found"]
    # POST
    if environ["REQUEST_METHOD"] == "POST":
        # HTML
        mime_type = "text/html"
        size = int(environ["CONTENT_LENGTH"])
        query = environ["wsgi.input"].read(size).decode("ascii")
        data = urllib.parse.parse_qs(query)
        # Processing
        extra = (int(data["extra"][0]) + REV[data["extra_rev"][0]]) / 2
        agree = (int(data["agree"][0]) + REV[data["agree_rev"][0]]) / 2
        consc = (int(data["consc"][0]) + REV[data["consc_rev"][0]]) / 2
        emot = (int(data["emot"][0]) + REV[data["emot_rev"][0]]) / 2
        opens = (int(data["open"][0]) + REV[data["open_rev"][0]]) / 2
        body = [results.format(
            extra, agree, consc, emot, opens).encode("utf-8")]
    # Output
    headers = [("Content-type", mime_type)]
    start_response(status, headers)
    return body


########################################################################

if __name__ == "__main__":
    # Web Server
    httpd = simple_server.make_server("localhost", 8000, application)
    print(PROMPT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        conn.close()
        print("Server stopped")

