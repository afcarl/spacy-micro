import spacy
import json
import os


# the text parser
class Parser:

    def __init__(self):
        # set spacey data path, where spacy files are installed
        spacy_path = '/opt/spacy'
        if not os.path.isfile(os.path.join(spacy_path, 'cookies.txt')):
            spacy_path = '/opt/kai/spacy'

        print("loading spacy from " + spacy_path)
        spacy.util.set_data_path(spacy_path)

        self.en_nlp = spacy.load('en')  # , create_make_doc=KAISpacyTokenizer)
        print("loading spacy done!")


    # cleanup text to ASCII to avoid nasty python UTF-8 errors
    def cleanup_text(self, data):
        try:
            return data.decode("utf-8")
        except:
            text = ""
            for ch in data:
                if 32 <= ch <= 255:
                    text += chr(ch)
                else:
                    text += " "
            return text


    # convert from spacy to the above Token format for each sentence
    def convert_sentence(self, sent):
        sentence = []
        for token in sent:
            ancestors = []
            for an in token.ancestors:
                ancestors.append(str(an.i))
            text = str(token)
            sentence.append(Token(text, token.i, token.tag_, token.dep_, ancestors))
        return sentence

    # convert a document to a set of entity tagged, pos tagged, and dependency parsed entities
    def parse_document(self, text):
        doc = self.en_nlp(text)
        sentence_list = []
        token_list = []
        num_tokens = 0
        for sent in doc.sents:
            sentence = self.convert_sentence(sent)
            token_list.extend(sentence)
            sentence_list.append(sentence)
            num_tokens += len(sentence)
        return sentence_list, token_list, num_tokens
