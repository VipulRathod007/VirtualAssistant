import errno
import os
from typing import Any


class GenUtilities:
    """
    Contains the general utility functions
    """

    @classmethod
    def assure(cls, inParam: dict, inArg: Any, ignoreError: bool = False):
        """
        Assure if the given inArg is a key of inParam
        :param inParam: Input parameter
        :param inArg: Input argument to check for
        :param ignoreError: Flag to ignore error
        :return: Value mapped to inArg in inParam if found else False
        """
        if inParam is not None and inArg in inParam and inParam[inArg] is not None:
            return inParam[inArg]
        else:
            # If set to True, No Exception gets thrown
            # But returns False, in case given inArg is not a key of inParam
            if ignoreError:
                return False
            else:
                raise KeyError(f"Invalid Expression: {inParam}[{inArg}]")

    @classmethod
    def createDir(cls, inDirPath: str, inMode: int = 0o777):
        """
        Creates the absent directories from the given path.
        :param inDirPath: Absolute directory path
        :param inMode: Creation mode
        :return: None
        """
        try:
            os.makedirs(inDirPath, inMode)
        except OSError as err:
            # Re-raise the error unless it's for already existing directory
            if err.errno != errno.EEXIST or not os.path.isdir(inDirPath):
                raise

    @classmethod
    def getEnvVariableValue(cls, inVarName: str):
        """
        Returns Environment Variable's Value from the given key
        :param inVarName: Name of environment variable
        :return: The value set to an environment variable
        """
        if not GenUtilities.isNoneOrEmpty(inVarName):
            return GenUtilities.assure(dict(os.environ), inVarName)
        else:
            raise InputException(inVarName)

    @classmethod
    def isNoneOrEmpty(cls, *inArgs, ignoreError: bool = False) -> bool:
        """
        Checks if any of the given argument is None or Empty
        :param ignoreError: Ignores an error if True else throws InputException
        :param inArgs: Input arguments passed in to check
        :return: False if all the input arguments are non-empty else True
        """
        result = any(map(lambda inArg: inArg is None or len(inArg) == 0, inArgs))
        if not ignoreError and result:
            raise InputException(str(inArgs))
        else:
            return result


class InputException(BaseException):
    """
    Represents InputException
    """

    def __init__(self, inVal: str):
        self.__val__ = inVal
        super(InputException, self).__init__(self.__val__)

    def __str__(self):
        return f'Error: Invalid value "{self.__val__}"'
