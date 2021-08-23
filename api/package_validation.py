import requests
from rest_framework import serializers


def package_versions(package_name):
    """GET a package from the public PyPI Api.

    If package not found return a error string.

    Returns a list of versions from the package.
    """
    url = "https://pypi.org/pypi/%s/json" % (package_name,)
    data = requests.get(url)
    if data.status_code == 404:
        return "error"

    versions = data.json()["releases"].keys()
    return versions


def package_validation(package):
    """Validate if the given package and their versions exists.

    If no version is given, get the latest version.

    Return the package validated.
    """
    versions = package_versions(package["name"])
    if versions == "error":
        raise serializers.ValidationError(
            {"error": "One or more packages doesn't exist"}, code=400
        )
    if "version" in package.keys() and package["version"] not in versions:
        raise serializers.ValidationError(
            {"error": "One or more packages doesn't exist"}, code=400
        )
    if "version" not in package.keys():
        package["version"] = list(versions)[-1]
    return package
