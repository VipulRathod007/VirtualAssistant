import os
import json

from GenUtility.GenUtilities import GenUtilities
from GenUtility.Tokenizer import Tokenizer


class GUSetupRoutine:
    """
    Represents Setup Routine class
    """

    def __init__(self, inArtifactLoc: str):
        """
        Setup Routine constructor
        :param inArtifactLoc: File path location to save artifacts
        """
        self.__mDirLoc, self.__mFileName = os.path.dirname(inArtifactLoc), os.path.basename(inArtifactLoc)
        GenUtilities.isNoneOrEmpty(self.__mFileName)
        assert self.__mFileName.endswith('.json')
        if not os.path.exists(self.__mDirLoc):
            GenUtilities.createDir(self.__mDirLoc)
        self.__mFileLoc = os.path.abspath(inArtifactLoc)
        self.__mTokenizer = Tokenizer()

    def create(self, inCommands: list[str], inMode: str = 'w') -> bool:
        """
        To create the setup routine
        :param inCommands: List of setup commands
        :param inMode: File access mode
        :return: True if created else false
        """
        try:
            inCommands = list(map(lambda inArg: inArg.strip(), inCommands))
            with open(self.__mFileLoc, inMode) as file:
                json.dump(inCommands, file)
            return True
        except Exception as error:
            print(f'Error: {error}')
            return False

    def read(self) -> list[str]:
        """
        Reads and returns setup routine commands
        """
        try:
            with open(self.__mFileLoc, 'r') as file:
                outCommands = json.load(file)
            return outCommands
        except Exception as error:
            print(f'Error: {error}')

    def append(self, inCommand: str) -> bool:
        """
        To append the given setup routine
        :param inCommand: Setup command
        :return: True if added else false
        """
        try:
            GenUtilities.isNoneOrEmpty(inCommand)
            inCommand = inCommand.strip()
            commands = self.read()
            commands.append(inCommand)
            return self.create(commands)
        except Exception as error:
            print(f'Error: {error}')
            return False

    def delete(self, inCommand: str) -> bool:
        """
        To delete the given setup routine
        :param inCommand: Setup command
        :return: True if deleted else false
        """
        try:
            GenUtilities.isNoneOrEmpty(inCommand)
            commands = self.read()
            for command in commands:
                if self.__mTokenizer.match(command, inCommand.split()):
                    commands.remove(command)
            return self.create(commands)
        except Exception as error:
            print(f'Error: {error}')
            return False
