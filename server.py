# Copyright 2017 Peter de Vocht
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import logging
import json

from datetime import datetime
import en_core_web_sm

from flask import Flask
from flask import request
from flask_cors import CORS

# set current directory as module path
dir = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(dir))

# use spacy small model
nlp = en_core_web_sm.load()

# endpoint, allow CORS
app = Flask(__name__)
CORS(app, resources={r"/parse/*": {"origins": "*"}})

# unicode characters that need special attention
white_space = {'\t',  '\r',  '\n', '\u0008', '\ufeff', '\u303f', '\u3000', '\u2420', '\u2408', '\u202f', '\u205f', '\u2000', '\u2002', '\u2003', '\u2004', '\u2005', '\u2006', '\u2007', '\u2008', '\u2009', '\u200a', '\u200b'}
full_stops = {'\u002e', '\u06d4', '\u0701', '\u0702', '\ufe12', '\ufe52', '\uff0e', '\uff61'}
single_quotes = {'\u02bc', '\u055a', '\u07f4', '\u07f5', '\u2019', '\uff07', '\u2018', '\u201a', '\u201b', '\u275b', '\u275c'}
double_quotes = {'\u00ab', '\u00bb', '\u07f4', '\u07f5', '\u2019', '\uff07', '\u201c', '\u201d', '\u201e', '\u201f', '\u2039', '\u203a', '\u275d', '\u276e', '\u2760', '\u276f'}
hypens = {'\u207b', '\u208b', '\ufe63', '\uff0d', '\u2014'}


# cleanup UTF-8 characters that could confuse spaCy
def _cleanup_text(text_binary):
    text = text_binary.decode('UTF-8')
    string_list = []
    for ch in text:
        if ch in full_stops:
            string_list.append(".")
        elif ch in single_quotes:
            string_list.append("'")
        elif ch in double_quotes:
            string_list.append('"')
        elif ch in hypens:
            string_list.append("-")
        elif ch in white_space:
            string_list.append(" ")
        else:
            string_list.append(ch)
    return ''.join(string_list)


# convert spacy to serializable set
def _parse_text(text):
    # convert from spacy internal to dict
    def _convert_spacy_sentence(sent):
        token_list = []
        for token in sent:
            ancestors = []
            for an in token.ancestors:
                ancestors.append(an.i)
            text = token.text.strip()
            if len(text) > 0:  # keep the tags we want - add others here
                token_list.append({'text': text, 'i': token.i, 'tag': token.tag_, 'dep': token.dep_,
                                   'lemma': token.lemma_, 'pos': token.pos_, 'lefts': [t.i for t in token.lefts],
                                   'rights': [t.i for t in token.rights], 'head': token.head.i,
                                   'ent_type': token.ent_type_, 'ancestors': ancestors})
        return token_list

    # spaCy magic
    tokens = nlp(text)
    sentence_list = []
    for sent in tokens.sents:
        sentence_list.append(_convert_spacy_sentence(sent))
    return sentence_list


# sanity check - check service is running from /
@app.route('/')
def index():
    return "spaCy parser service layer"


# the parser - where all the magic happens
# try post file: curl -H "Content-Type: plain/text" -X POST --data "@some-file.txt" http://localhost:9000/parse
@app.route('/parse', methods=['POST'])
def parse():
    t1 = datetime.now()

    text = _cleanup_text(request.data)
    sentence_list = _parse_text(text)

    delta = datetime.now() - t1
    parse_data = {"processing_time": int(delta.total_seconds() * 1000), "sentence_list": sentence_list}

    return json.dumps(parse_data), 200, {'ContentType': 'application/json'}


# non-gunicorn use - debug only
if __name__ == "__main__":
    logging.info("test only - using gunicorn to run properly, see README.md")
    app.run(host="0.0.0.0",
            port=9000,
            debug=True,
            use_reloader=False)
