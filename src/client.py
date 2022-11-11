# Web Demo Project
# Client side
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
import html.parser
import urllib.parse
import urllib.request


# Constants
ABOUT = "Web Demo Project \nCtrl-C to stop\n"
URL = "http://localhost:8000/"
INTRO = "\
Ten-Item Personality Inventory (TIPI)\n\
(Gosling, Renfro & Swann, 2003)\n\
Please write a number (1-7) next to each statement to indicate the extent to \
which you agree or disagree with that statement.\n"
VALUES = ("1", "2", "3", "4", "5", "6", "7")


# HTTP opener
opener = urllib.request.build_opener()
opener.addheaders = [("User-agent", "Mozilla/5.0")]


# HTML parser
class _DemoParser(html.parser.HTMLParser):
    """Internal parser."""
    def __init__(self):
        super().__init__()
        self._last_tag = ""
        self._last_attr = ""
        self.items = []
        self.names = []
        self.factors = []
        self.spans = []
    def handle_starttag(self, tag, attrs):
        self._last_tag = tag
        self._last_attr = dict(attrs).get("class")
        if self._last_tag == "input" and dict(attrs).get("value") == "1":
            self.names.append(dict(attrs).get("name"))
    def handle_data(self, data):
        if data := data.strip():
            if self._last_attr == "item":
                self.items.append(data)
            if self._last_attr == "factor":
                self.factors.append(data)
            if self._last_tag == "span":
                self.spans.append(data)


# Functions

def main():
    """Web Client."""
    try:
        print(ABOUT)
        # GET
        test_page = opener.open(URL).read().decode("utf-8")
        test_parser = _DemoParser()
        test_parser.feed(test_page)
        print(INTRO)
        answers = {}
        for name, item in zip(test_parser.names, test_parser.items):
            while (answer := input(f'"{item}" = ')) not in VALUES:
                print("> Invalid! Try again.")
                continue
            answers[name] = answer
        # POST
        data = urllib.parse.urlencode(answers).encode("ascii")
        results_page = opener.open(URL, data).read().decode("utf-8")
        results_parser = _DemoParser()
        results_parser.feed(results_page)
        # Output
        print("\n* Your results *")
        for factor, value in zip(results_parser.factors, results_parser.spans):
            print(factor, value)
    except Exception as error:
        print("ERROR:", error)
    except KeyboardInterrupt:
        print("Client stopped.")


########################################################################
# EXECUTION

if __name__ == "__main__":
    main()

