from libs.openhab.generic import OpenhabClient


def install_addon(openhab: OpenhabClient, id: str):
    openhab = OpenhabClient()

    request = openhab.post(type="addon", data=None, command="install", id=id)
    response = request.json()

    return response


def cleanup_string(string: str) -> str:
    result = string.replace("ä", "ae")
    result = result.replace("Ä", "Ae")
    result = result.replace("ö", "oe")
    result = result.replace("Ö", "Oe")
    result = result.replace("ü", "ue")
    result = result.replace("Ü", "Ue")
    result = result.replace("ß", "ss")
    result = result.replace("-", " ")
    result = result.replace(":", " ")
    result = result.replace("  ", " ")
    result = result.replace(" ", "_")
    result = result.replace("(", "_")
    result = result.replace(")", "_")
    result = result.replace("__", "_")

    # if the result start with a number, replace it with a random character
    if result[0].isdigit():
        result = f"a_{result}"

    return result
