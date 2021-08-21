import requests


def package_versions(package_name):
    url = "https://pypi.org/pypi/%s/json" % (package_name,)
    data = requests.get(url)
    if data.status_code == 404:
        return "error"

    versions = data.json()["releases"].keys()
    return versions


def package_validation(package):
    versions = package_versions(package["name"])
    if versions == "error":
        return {"error": "One or more packages doesn't exist"}
    if "version" in package.keys() and package["version"] not in versions:
        return {"error": "One or more packages doesn't exist"}
    if "version" not in package.keys():
        package["version"] = list(versions)[-1]
    return package
