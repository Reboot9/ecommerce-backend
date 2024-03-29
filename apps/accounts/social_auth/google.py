"""
Google Auth API Module.
"""
from google.auth.transport import requests
from google.oauth2 import id_token


class GoogleAuthAPI:
    """
    Google auth class which validate token and return data.
    """

    @staticmethod
    def validate(auth_token: str):
        """
        Validate method Queries the Google oAUTH2 api to fetch the user info.

        :param auth_token: token from frontend part application
        :return: user_info | str
        """
        try:
            idinfo = id_token.verify_oauth2_token(auth_token, requests.Request())

            if "accounts.google.com" in idinfo["iss"]:
                return idinfo
            else:
                return "Something goes wrong.."

        except Exception:
            return "The token is either invalid or has expired."
