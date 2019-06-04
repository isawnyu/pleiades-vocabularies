import json

from zope.publisher.interfaces import IPublishTraverse
from zope.interface import implementer

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ZPublisher.BaseRequest import DefaultPublishTraverse

from pleiades.rdf.common import RegVocabGrapher
from pleiades.vocabularies.vocabularies import get_vocabulary


VOCAB_TITLES = {
    'time-periods': 'Time Periods',
    'place-types': 'Feature (or Place) Categories',
    'location-types': 'Location Categories',
    'relationship-types': 'Connection Types',
    'association-certainty': 'Association Certainty',
    'attestation-confidence': 'Attestation Confidence',
    'ancient-name-languages': 'Language and Script',
    'name-types': 'Name Types',
    'name-accuracy': 'Name Accuracy',
    'name-completeness': 'Name Completeness',
    'arch-remains': 'Archeological Remains',
}


@implementer(IPublishTraverse)
class VocabView(BrowserView):

    index = ViewPageTemplateFile('vocab.pt')
    term = None

    def __init__(self, context, request, vocabname):
        self.context = context
        self.request = request
        self.vocabname = vocabname

    @property
    def vocabkey(self):
        return self.vocabname.replace('-', '_')

    @property
    def terms(self):
        return get_vocabulary(self.vocabkey)

    def publishTraverse(self, request, name):
        self.term_id = name
        if name in ['rdf', 'turtle', 'json']:
            term = [name]
        else:
            term = [p for p in self.terms if p['id'] == name]
        if term:
            self.term = term[0]
        return self

    def __call__(self):
        # publish traverse requires we handle export formats here for now
        if self.term == 'rdf':
            return self.rdf_view()
        if self.term == 'turtle':
            return self.turtle_view()
        response = self.request.response
        response.setHeader('vary', 'Accept')
        accept = self.request.environ.get('HTTP_ACCEPT', '').split(',')
        user_preferences = []
        for value in accept:
            parts = value.split(";")
            weight = 1.0
            if len(parts) == 2:
                try:
                    weight = float(parts[1].split("=")[1])
                except (IndexError, ValueError):
                    weight = 0.3
            user_preferences.append((weight, parts[0].strip()))
        user_preferences.sort(reverse=True)

        for weight, preferred in user_preferences:
            if 'json' in preferred or 'javascript' in preferred:
                response.setHeader('Content-Type', 'application/json')
                return self.__json__()
            if 'html' in preferred:
                return self.index()

        return self.index()

    def title(self):
        if self.term:
            return self.term['title']
        else:
            return VOCAB_TITLES.get(self.vocabname, self.vocabname)

    def __json__(self):
        if self.term:
            return json.dumps(self.term)
        else:
            return json.dumps(self.terms)

    def to_ad(self, year):
        sign = (year > 0) * 2 - 1
        if sign >= 0:
            return "AD %d" % year
        else:
            return "%d BC" % (sign * year)

    def turtle_view(self):
        self.request.response.setStatus(200)
        self.request.response.setHeader(
            'Content-Type', "text/turtle; charset=utf-8")
        self.request.response.setHeader(
            'Content-Disposition', "filename={}.ttl".format(self.vocabname))
        g = RegVocabGrapher(self.context, self.request).scheme(self.vocabkey)
        return g.serialize(format='turtle')

    def rdf_view(self):
        self.request.response.setStatus(200)
        self.request.response.setHeader(
            'Content-Type', "application/rdf+xml")
        self.request.response.setHeader(
            'Content-Disposition', "filename={}.rdf".format(self.vocabname))
        g = RegVocabGrapher(self.context, self.request).scheme(self.vocabkey)
        return g.serialize(format='pretty-xml')


@implementer(IPublishTraverse)
class PleiadesVocabularyPublishTraverse(DefaultPublishTraverse):

    def publishTraverse(self, request, name):
        if name in VOCAB_TITLES.keys():
            return VocabView(self.context, request, name)
        return super(PleiadesVocabularyPublishTraverse, self).publishTraverse(
            request, name)


class SearchUtilities(BrowserView):

    def __init__(self, context, request):
        super(SearchUtilities, self).__init__(context, request)
        self.catalog = getToolByName(context, 'portal_catalog')

    def get_place_type_data(self):
        featureTypes = set(self.catalog.uniqueValuesFor('getFeatureType'))
        places_in_use = sorted(featureTypes)
        place_types = get_vocabulary('place_types')
        places = {p['id']: p['title'] for p in place_types}
        data = [{'id': p, 'title': places[p]} \
            for p in places_in_use if p and p in places]
        return sorted(data, key=lambda k: k['title'].lower())
