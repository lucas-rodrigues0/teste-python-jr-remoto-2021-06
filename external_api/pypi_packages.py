import requests


def get_package_pypi(name):
    """Get the package from pypi.org by given name"""
    url = "https://pypi.org/pypi/%s/json" % (name,)
    data = requests.get(url)
    return data
