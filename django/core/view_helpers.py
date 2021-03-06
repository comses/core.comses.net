import logging

from rest_framework.response import Response
from wagtail.search.backends import get_search_backend
from wagtail.search.models import Query
from wagtail.search.query import MATCH_ALL

logger = logging.getLogger(__name__)

search_backend = get_search_backend()


def get_search_queryset(query, queryset, operator="or", fields=None, tags=None, criteria=None):

    if not query:
        query = ''

    if not tags:
        tags = ''

    order_by_relevance = not queryset.ordered

    if query:
        if tags:
            criteria.update(tags__name__in=[t.lower() for t in tags])
            operator = 'and'
        if criteria:
            queryset = queryset.filter(**criteria)
    query = f'{query} {tags}'.strip().lower()
    if query:
        Query.get(query).add_hit()
    else:
        query = MATCH_ALL

    results = search_backend.search(query,
                                    queryset,
                                    operator=operator,
                                    fields=fields,
                                    order_by_relevance=order_by_relevance)
    results.model = queryset.model
    return results


def retrieve_with_perms(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    data = serializer.data
    data = add_change_delete_perms(instance, data, request.user)
    return Response(data)


def add_change_delete_perms(instance, data, user):
    data['has_change_perm'] = user.has_perm('{}.change_{}'.format(instance._meta.app_label, instance._meta.model_name), instance)
    data['has_delete_perm'] = user.has_perm('{}.delete_{}'.format(instance._meta.app_label, instance._meta.model_name), instance)
    return data
