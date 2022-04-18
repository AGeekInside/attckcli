from re import I
import requests


def download_json(url: str, verify=True):
    downloaded_json = requests.get(url, verify=verify).json()

    return downloaded_json

