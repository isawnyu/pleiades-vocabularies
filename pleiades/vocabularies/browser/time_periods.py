import json

from zope.publisher.interfaces import IPublishTraverse
from zope.interface import implementer

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from pleiades.rdf.common import RegVocabGrapher
from pleiades.vocabularies.vocabularies import get_vocabulary


@implementer(IPublishTraverse)
class TimePeriodsView(BrowserView):

    index = ViewPageTemplateFile('time_periods.pt')
    term = None

    @property
    def periods(self):
        periods = get_vocabulary('time_periods')
        return periods

    def publishTraverse(self, request, name):
        self.term_id = name
        if name in ['rdf', 'turtle']:
            term = [name]
        else:
            term = [p for p in self.periods if p['id'] == name]
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

    def __json__(self):
        if self.term:
            return json.dumps(self.term)
        else:
            return json.dumps(self.periods)

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
            'Content-Disposition', "filename=time-periods.ttl")
        g = RegVocabGrapher(self.context, self.request).scheme('time_periods')
        return g.serialize(format='turtle')

    def rdf_view(self):
        self.request.response.setStatus(200)
        self.request.response.setHeader(
            'Content-Type', "application/rdf+xml")
        self.request.response.setHeader(
            'Content-Disposition', "filename=time-periods.rdf")
        g = RegVocabGrapher(self.context, self.request).scheme('time_periods')
        return g.serialize(format='pretty-xml')


class PleiadesVocabularyFolderView(BrowserView):

    index = ViewPageTemplateFile('vocabulary_listing.pt')

    def __call__(self):
        return self.index()
