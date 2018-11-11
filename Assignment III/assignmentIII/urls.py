from django.urls import re_path
from . import queries

urlpatterns = [
    re_path(r'^query_1/$', queries.query_1),
    re_path(r'^query_2/$', queries.query_2),
    re_path(r'^query_3/$', queries.query_3),
    re_path(r'^query_4/$', queries.query_4),
    re_path(r'^query_5/$', queries.query_5),
    re_path(r'^query_6/$', queries.query_6),
    re_path(r'^query_7/$', queries.query_7),
    re_path(r'^query_8/$', queries.query_8),
    re_path(r'^query_9/$', queries.query_9),
    re_path(r'^query_10/$', queries.query_10),
]
