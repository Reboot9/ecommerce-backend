"""
Module have facebook auth API class which validate the token and get user data.
"""
import facebook


class FacebookAuthAPI:
    """
    Facebook class to fetch the user info and return it.
    """

    @staticmethod
    def validate(auth_token: str):
        """
        Validate method Queries the facebook GraphAPI to fetch the user info.

        :param auth_token: Token from frontend part of app
        """
        try:
            graph = facebook.GraphAPI(auth_token)
            profile = graph.request("/me?fields=first_name,last_name,email")
            return profile
        except Exception:
            return "The is invalid or expired."
