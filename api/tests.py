from django.test import TestCase
from unittest import mock
from api.package_validation import package_versions


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == "https://pypi.org/pypi/Django/json":
        return MockResponse(
            {
                "releases": {
                    "1.0.0": "version1",
                    "2.2.0": "version2",
                    "3.1.3": "version3",
                }
            },
            200,
        )
    elif args[0] == "https://pypi.org/pypi/graphene/json":
        return MockResponse(
            {
                "releases": {
                    "1.3.0": "version1",
                    "2.1.0": "version2",
                    "2.2.3": "version2",
                }
            },
            200,
        )

    return MockResponse(None, 404)


class PackageVersionsTestCase(TestCase):
    @mock.patch("requests.get", side_effect=mocked_requests_get)
    def test_get_package_versions():
        package = "Django"
        assert package_versions(package)
