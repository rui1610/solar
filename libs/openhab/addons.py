from libs.openhab.generic import OpenhabClient


def install_addon(openhab: OpenhabClient, id: str):
    openhab = OpenhabClient()

    request = openhab.post(type="addon", data=None, command="install", id=id)
    response = request.json()
