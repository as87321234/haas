''' UTILITY.py '''
import yaml

class UtilityLib:
    """ UtilityLib """

    def __init__(self):
        self.unique_id = ''

    def __str__(self):
        return ''

    @staticmethod
    def get_secret_password(key: str ):

        """ getSecretPassword """

        with open('config/secrets.yaml', encoding='utf-8') as file:
            credentials = yaml.full_load(file)

            try:
                # load yml file to dictionary
                # access values from dictionary
                bearer = credentials[key]
                return bearer

            except yaml.YAMLError as exc:
                print(exc)
                return None
