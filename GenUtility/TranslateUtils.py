from googletrans import Translator as _Translator
from googletrans.constants import LANGUAGES as _LANGUAGES
from googletrans.constants import LANGCODES as _LANGCODES

from GenUtility.GenUtilities import GenUtilities


class GUTranslator:
    """
    Represents General Utilities Translator class
    """

    def __init__(self):
        self.__mTranslator = _Translator()

    def detect(self, inQuery: str):
        """
        To detect the source language
        :param inQuery: Source language text
        :return: Source language name
        """
        try:
            result = self.__mTranslator.detect(inQuery)
            GenUtilities.isNoneOrEmpty(result)
            return GenUtilities.assure(_LANGUAGES, result.lang, ignoreError=True)
        except Exception as error:
            print(f'Error: {error}')
            return None

    def translate(self, inQuery: str, inTargetLanguage: str = _LANGUAGES.get('en')):
        """
        Translates query into the targeted language
        :param inQuery: Source language text
        :param inTargetLanguage: Language to translate the query into. default: English
        :return: Translated language text
        """
        try:
            result = self.__mTranslator.translate(inQuery, GenUtilities.assure(_LANGCODES, inTargetLanguage))
            return result.pronunciation
        except Exception as error:
            print(f'Error: {error}')
            return None
