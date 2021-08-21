import requests


def package_versions(package_name):
    url = "https://pypi.org/pypi/%s/json" % (package_name,)
    data = requests.get(url)
    if data.status_code == 404:
        return "One or more packages don't exist"

    versions = data.json()["releases"].keys()
    return versions
