from django.db import models


class SearchKeyword(models.Model):
    search_keyword_text = models.CharField(max_length=200)
    search_date = models.DateTimeField('date searched')

    def __str__(self):
        return self.search_keyword_text



