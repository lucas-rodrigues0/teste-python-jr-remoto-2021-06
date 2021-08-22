import json
from django.test import TestCase, Client
from unittest.mock import Mock, patch

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework import serializers

from api.serializers import ProjectSerializer
from api.package_validation import package_validation, package_versions
from .models import Project, PackageRelease


class PackageValidationTestCase(TestCase):
    def setUp(self):
        patcher = patch("requests.get")
        self.addCleanup(patcher.stop)
        self.mock_get = patcher.start()
        self.mock_ok_response = {
            "releases": {
                "1.0.1": ["vers1"],
                "2.0.2": ["vers2"],
                "3.0.3": ["vers3"],
            },
        }
        self.expected_ok_response = self.mock_ok_response["releases"].keys()
        self.expected_error_response = "error"
        self.expected_error_message_response = {
            "error": "One or more packages doesn't exist"
        }

    def test_get_package_versions(self):
        self.mock_get.return_value = Mock(status_code=200)
        self.mock_get.return_value.json.return_value = self.mock_ok_response

        package = "valid_package"
        expected = self.expected_ok_response

        result = package_versions(package)

        self.assertEquals(expected, result)

    def test_get_invalid_package_versions(self):
        self.mock_get.return_value = Mock(status_code=404)

        package = "invalid_package"
        expected = self.expected_error_response

        result = package_versions(package)

        self.assertEquals(expected, result)

    def test_package_validation_success_with_a_defined_version(self):
        self.mock_get.return_value = Mock(status_code=200)
        self.mock_get.return_value.json.return_value = self.mock_ok_response

        package = {"name": "valid_package", "version": "2.0.2"}
        expected = package

        result = package_validation(package)

        self.assertEquals(expected, result)

    def test_package_validation_success_and_add_newest_version(self):
        self.mock_get.return_value = Mock(status_code=200)
        self.mock_get.return_value.json.return_value = self.mock_ok_response

        package = {"name": "valid_package"}
        expected = {"name": "valid_package", "version": "3.0.3"}

        result = package_validation(package)

        self.assertEquals(expected, result)

    def test_package_validation_with_an_invalid_package_version(self):
        self.mock_get.return_value = Mock(status_code=200)
        self.mock_get.return_value.json.return_value = self.mock_ok_response

        package = {"name": "valid_package", "version": "1.2.3"}
        expected = self.expected_error_message_response

        result = package_validation(package)

        self.assertEquals(expected, result)

    def test_package_validation_with_an_invalid_package_name(self):
        self.mock_get.return_value = Mock(status_code=404)

        package = {"name": "invalid_package", "version": "1.2.3"}
        expected = self.expected_error_message_response

        result = package_validation(package)

        self.assertEquals(expected, result)


# class ApiSerializerTestCase(TestCase):
#     def setup(self):
#         self.serializer_data = {
#             "name": "project_name",
#             "packages": [{"name": "valid_package"}],
#         }
#         self.serializer = ProjectSerializer(instance=self.serializer_data)

#     def test_ProjectSerializer_create_project_success(self):
#         data = self.serializer.data
#         self.assertEqual(data.keys(), ["name", "packages"])
#         pass
