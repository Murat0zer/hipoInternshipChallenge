import requests
from django import template
from django.shortcuts import render
from django.utils import timezone

from .models import SearchKeyword

register = template.Library()

API_KEY = '1ddb7df62cbdc4e07f6ec75ca78e2960'
BASE_URL = 'https://api.flickr.com/services/rest/'


def index(request):
    context = {'results': {'photos': {'photo': {}, 'page': 0, 'pages': 0}}}
    keyword_objects = SearchKeyword.objects.order_by('-search_date')[:20]
    request_keyword_param = request.GET.get('keyword', '')
    if request_keyword_param:
        if already_searched(request_keyword_param, keyword_objects):
            SearchKeyword.objects.filter(search_keyword_text=request_keyword_param).update(search_date=timezone.now())
        else:
            SearchKeyword.objects.create(search_keyword_text=request_keyword_param, search_date=timezone.now())

        per_page = request.GET.get('per_page', 20)
        page = request.GET.get('page', 1)
        response_type = 'json'
        method = 'flickr.photos.search'
        payload = {'method': method, 'api_key': API_KEY, 'tags': request_keyword_param, 'format': response_type,
                   'nojsoncallback': '1', 'per_page': per_page, 'page': page}

        results = requests.get(BASE_URL, payload)
        context['results'] = results.json()

    context['top_search_keyword_list'] = SearchKeyword.objects.order_by('-search_date')[:20]
    return render(request, 'flickrClient/index.html', context)


def already_searched(keyword, keyword_objects):
    for persisted_search_keyword in keyword_objects:
        if persisted_search_keyword.search_keyword_text == keyword:
            return True
