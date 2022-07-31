import re

from GenUtility.GenUtilities import GenUtilities


class Tokenizer:
    """
    Represents Tokenizer class
    """

    def match(self, inSource: str, inOptionalTokens: list[str], inRequiredTokens: list[str] = list()) -> bool:
        """
        Matches each of the query tokens in Source string
        :param inRequiredTokens: Tokens that must match
        :param inSource: Raw string to match the tokens with
        :param inOptionalTokens: Query token to match
        :return: True if each token matched else False
        """
        inOptionalTokens = sorted(list(map(lambda inArg: inArg.lower(), inOptionalTokens)), key=len, reverse=True)
        inRequiredTokens = sorted(list(map(lambda inArg: inArg.lower(), inRequiredTokens)), key=len, reverse=True)
        required = None
        optional = (not GenUtilities.isNoneOrEmpty(
            re.findall('|'.join(inOptionalTokens), inSource.lower()),
            ignoreError=True)
            )
        if len(inRequiredTokens) > 0:
            required = any(map(lambda inArg: inArg in inSource, inRequiredTokens))
        return optional or required
