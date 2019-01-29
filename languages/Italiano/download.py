import urllib.request
from html.parser import HTMLParser

#  The web service from which we download HTML. Don't worry about
#  no https, it's ok if this is not secure.
url = "http://www.italian-verbs.com/italian-verbs/conjugation.php"

#  At the time of writing this code, the web service contains
#  italian verbs in the HTML for the following categories.
#  The top-level keys (e.g. 'indicativo') are found in the HTML,
#  as well as the keys in each category (e.g. 'presente'). The
#  values (e.g. 'Il Presente') are the names of the tenses which
#  the quiz will present to the user.
VERB_CATEGORIES = {
    'indicativo': {
        'presente': 'Il Presente',
        'imperfetto': 'L\'Imperfetto',
        'passato remoto': 'Il Passato Remoto',
        'futuro semplice': 'Il Futuro Semplice',
        'passato prossimo': 'Il Passato Prossimo',
        'trapassato prossimo': 'Il Trapassato Prossimo',
        'trapassato remoto': 'Il Trapassato Remoto',
        'futuro anteriore': 'Il Futuro Anteriore',
    },
    'congiuntivo': {
        'presente': 'Il Congiuntivo',
        'imperfetto': 'L\'Imperfetto del Congiuntivo',
        'passato': 'Il Congiuntivo Passato',
        'trapassato': 'Il Trapassato Congiuntivo',
    },
    'condizionale': {
        'presente': 'Il Condizionale',
        'passato': 'Il Condizionale Passato'
    },
    'imperativo': {
        'presente': 'L\'Imperativo'
    },
}


class ItalianVerbsHTMLParser(HTMLParser):

    def __init__(self, verb, subject_pronouns):
        self.verb = verb
        self.subject_pronouns = subject_pronouns

        #  As the Parser parses HTML, it will come across elements
        #  containing data. If the data matches one of the categories
        #  or tenses in VERB_CATEGORIES, then we know the following HTML
        #  data will contain the verb conjugation.
        self.category = None
        self.tense = None

        #  Collect the verb conjugations as we go.
        self.conjugations = {}

        super(ItalianVerbsHTMLParser, self).__init__()

    def handle_data(self, data):
        #  Inspect each data element to see if it contains the information
        #  we're looking for: 1) Verb categories, 2) Tense names, or
        #  3) conjugations.

        if self._data_refers_to_verb_category(data):
            self.category = data.lower()

        elif self._data_refers_to_verb_tense(data):
            self.tense = data.lower()

        elif self._data_refers_to_verb_conjugation(data):
            #  Add tense entry, if necessary
            tense_name = VERB_CATEGORIES[self.category][self.tense]
            if tense_name not in self.conjugations:
                self.conjugations[tense_name] = {}

            #  Satisfying the conditions required for this code block ensure
            #  that the data contains multiple words, so the following code
            #  is safe.
            words = data.split()
            if words[0] == "che":
                pronoun = "che " + words[1]
                conjugation = " ".join(words[2:])
            else:
                pronoun = words[0]
                conjugation = " ".join(words[1:])

            self.conjugations[tense_name][pronoun] = conjugation

        verb_not_found_message = (
            "Please, check the correct spelling in Italian of the desired verb"
        )
        if verb_not_found_message in data:
            raise ValueError(
                "The verb %s could not be downloaded from %s" % (self.verb, url)
            )

    def _data_refers_to_verb_category(self, data):
        return data.lower() in VERB_CATEGORIES

    def _data_refers_to_verb_tense(self, data):
        return (
            self.category in VERB_CATEGORIES and
            data.lower() in VERB_CATEGORIES[self.category]
        )

    def _data_refers_to_verb_conjugation(self, data):
        # Split the data into words
        words = data.split(" ")

        #  Verb conjudations always have subject pronoun + conjugation
        if len(words) < 2:
            return False

        first_word, second_word = words[:2]
        return (
            first_word in self.subject_pronouns or
            first_word == "che" and second_word in self.subject_pronouns
        )

    def feed(self, html):
        super(ItalianVerbsHTMLParser, self).feed(html)
        return self.conjugations


def request_html_for_verb(verb):
    global url
    request_str = url + "?parola=%s" % verb
    return urllib.request.urlopen(request_str).read().decode('utf-8')


def parse_html_for_conjugations(html, verb, subject_pronouns):
    parser = ItalianVerbsHTMLParser(verb, subject_pronouns)
    return parser.feed(html)


def download_conjugations(verb, subject_pronouns):
    html = request_html_for_verb(verb)
    conjugations = parse_html_for_conjugations(html, verb, subject_pronouns)
    return conjugations
