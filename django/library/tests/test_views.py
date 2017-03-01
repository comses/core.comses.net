from wagtail_comses_net.test_helpers.view import ViewSetTestCase, letters, MAX_EXAMPLES
from hypothesis import strategies as st
from hypothesis.extra.django.models import models
from hypothesis import given, settings
from ..models import Codebase
from ..views import CodebaseViewSet
from ..serializers import CodebaseSerializer
from django.contrib.auth.models import User, Group, Permission
from home.tests.test_views import generate_with_user
from rest_framework.test import force_authenticate
from django.urls import reverse


def generate_with_codebase(submitter):
    return models(Codebase,
                  title=letters(),
                  description=letters(),
                  uuid=st.uuids(),
                  repository_url=st.just(''),
                  doi=st.just(None),
                  images=st.just([]),
                  identifier=st.uuids(),
                  submitter=st.just(submitter),
                  relationships=st.just([]))


@st.composite
def generate_codebases(draw):
    visitors = draw(models(Group))
    usernames = ['0000000000',
                 '0000000001']
    user_profiles = [draw(generate_with_user(username)) for username in usernames]
    users, profiles = zip(*user_profiles)
    visitors.permissions = Permission.objects.filter(codename__startswith='view_')
    visitors.user_set = User.objects.all()
    codebases = draw(st.lists(generate_with_codebase(users[0]), min_size=2, max_size=2))
    return profiles, codebases


class CodebaseViewSetTestCase(ViewSetTestCase):
    model_cls = Codebase
    modelviewset_cls = CodebaseViewSet
    serializer_cls = CodebaseSerializer
    detail_url_name = 'library:codebase-detail'
    list_url_name = 'library:codebase-list'

    def create_add_response(self, user: User, data):
        data.pop('id')
        data['identifier'] = str(st.uuids().example())

        http_method = self.action_http_map['add']
        request_factory = getattr(self.factory, http_method)
        request = request_factory(reverse(self.list_url_name), data=data, format='json')
        force_authenticate(request, user)
        response = self.modelviewset_cls.as_view(
            {'put': 'update', 'get': 'retrieve', 'post': 'create', 'delete': 'destroy'})(request)
        return response

    @settings(max_examples=MAX_EXAMPLES)
    @given(generate_codebases(), st.sampled_from(('change', 'add', 'view')))
    def test_add_change_view(self, data, action):
        profiles, codebases = data
        owner, user = profiles

        self.check_authorization(action, owner, codebases[0])
        self.check_authorization(action, user, codebases[1])

    @settings(max_examples=MAX_EXAMPLES)
    @given(generate_codebases())
    def test_delete(self, data):
        profiles, codebases = data
        owner, user = profiles

        self.check_authorization('delete', owner, codebases[0])
        self.check_authorization('delete', user, codebases[1])

    @settings(max_examples=MAX_EXAMPLES)
    @given(generate_codebases())
    def test_anonymous(self, data):
        profiles, codebases = data

        self.check_anonymous_authorization(codebases[0])