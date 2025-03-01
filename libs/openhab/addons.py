from libs.openhab.generic import openhab_post


def install_addon(id):
    request = openhab_post(type="addon", data=None, command="install", id=id)
    response = request.json()
