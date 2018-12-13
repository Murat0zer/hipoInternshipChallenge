from django.shortcuts import render
from django.utils import timezone

from .models import SearchKeyword


def index(request):
    keyword_objects = SearchKeyword.objects.order_by('-search_date')[:20]
    request_keyword_param = request.GET.get('keyword', '')
    if request_keyword_param:
        if already_searched(request_keyword_param, keyword_objects):
            SearchKeyword.objects.filter(search_keyword_text=request_keyword_param).update(
                search_keyword_text=request_keyword_param, search_date=timezone.now())
        else:
            SearchKeyword.objects.create(search_keyword_text=request_keyword_param, search_date=timezone.now())

    context = {'top_search_keyword_list': SearchKeyword.objects.order_by('-search_date')[:20]}
    return render(request, 'flickrClient/index.html', context)


def already_searched(keyword, keyword_objects):
    for persisted_search_keyword in keyword_objects:
        if persisted_search_keyword.search_keyword_text == keyword:
            return True
