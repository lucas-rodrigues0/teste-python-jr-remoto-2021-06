from rest_framework import serializers

from external_api.pypi_packages import get_package_pypi


def package_versions(package_name):
    """Get package from the public Api.

    If package not found return a error string.

    Returns a list of versions from the package.
    """
    data = get_package_pypi(package_name)
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
    if versions == "error" or (
        "version" in package.keys() and package["version"] not in versions
    ):
        raise serializers.ValidationError(
            {"error": "One or more packages doesn't exist"}, code=400
        )

    if "version" not in package.keys():
        package["version"] = list(versions).pop()
    return package
