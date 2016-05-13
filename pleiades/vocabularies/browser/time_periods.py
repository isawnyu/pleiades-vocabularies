import json

from zope.publisher.interfaces import IPublishTraverse
from zope.interface import implementer

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

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
        term = [p for p in self.periods if p['id'] == name]
        if term:
            self.term = term[0]
        return self

    def __call__(self):
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

