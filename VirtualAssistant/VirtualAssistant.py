import re
import os
import json
import time
import random
import shutil
import pyttsx3
import platform
import subprocess
import webbrowser
import speech_recognition
from enum import IntEnum
from urllib import parse
from pyjokes import pyjokes
from selenium import webdriver, common
from wikipedia import wikipedia, exceptions


from GenUtility.GenUtilities import GenUtilities
from GenUtility.Tokenizer import Tokenizer
from GenUtility.TranslateUtils import GUTranslator
from GenUtility.Browser import BrowserFactory, Browser


class Voice(IntEnum):
    """
    Enum class represent Voices
    """
    MALE = 0
    FEMALE = 1


class VirtualAssistant:
    """
    Represents VirtualAssistant
    """

    # Constants
    DUMPLOCATION = os.path.join(os.curdir, '.ignore')

    def __init__(self, inGenderCode: Voice = random.randint(Voice.MALE, Voice.FEMALE)):
        if not os.path.exists(VirtualAssistant.DUMPLOCATION):
            os.mkdir(VirtualAssistant.DUMPLOCATION)
        self.__mStandByMode = False
        self.__mEngine = pyttsx3.init()
        self.__mTokenizer = Tokenizer()
        self.__mGUTranslator = GUTranslator()
        # self.__mBrowser = BrowserFactory.getInstance(GenUtilities.getEnvVariableValue(BrowserFactory.BROWSERDRIVER))
        self.__mBrowser = BrowserFactory.getInstance(r'C:\Users\vrathod\Downloads\chromedriver.exe')
        self.__mBrowser.minimize_window()
        voices = self.__mEngine.getProperty('voices')
        self.__mEngine.setProperty('voice', voices[inGenderCode].id)

        self.__mRecognizer = speech_recognition.Recognizer()
        self.__mRecognizer.pause_threshold = 0.5

        with open('app.config', 'r') as file:
            self.__mConfig = json.load(file)
        file.close()

        self.__mAppName = self.__mConfig['meta']['app']['name']
        self.__mDevName = self.__mConfig['meta']['dev']['nickname']

    def __del__(self):
        # TODO: Fix error
        # self.__mBrowser.close()
        # self.__mBrowser.quit()
        if os.path.exists(VirtualAssistant.DUMPLOCATION):
            shutil.rmtree(VirtualAssistant.DUMPLOCATION, ignore_errors=True)

    def activate(self):
        self.speak(f"{self.__mAppName} activated")
        self.speak(f'Hii {self.__mDevName}.')
        self.speak('Ready to take command')

    def browse(self, inQuery: str):
        """
        To search the query using the register browser
        :param inQuery: THe query to search for
        :return: None
        """
        GenUtilities.isNoneOrEmpty(inQuery)
        self.__mBrowser.implicitly_wait(2)
        self.__mBrowser.maximize_window()
        BrowserFactory.openNewTab(f'https://www.google.com/search?q={parse.quote(inQuery)}')
        self.__mBrowser.minimize_window()

    def clearTerminal(self):
        """
        Clears the terminal
        """
        os.system('cls' if platform.system().lower() == 'windows' else 'clear')

    def deActivate(self):
        self.__mBrowser = None
        self.speak('Signing off today!')
        self.speak(f'Bye {self.__mDevName}')
        self.speak(f'{self.__mAppName} deactivated!')

    def introduce(self):
        self.speak(f'Hello World! I am {self.__mAppName}')
        self.speak(f"{self.__mConfig['meta']['app']['bio']}")

    def listen(self) -> str:
        """
        Listen utility
        :return: The spoken query in Text
        """
        with speech_recognition.Microphone() as source:
            self.__mRecognizer.adjust_for_ambient_noise(source)
            query = ''
            while GenUtilities.isNoneOrEmpty(query, ignoreError=True):
                print('Listening....')
                audio = self.__mRecognizer.listen(source)
                try:
                    query = self.__mRecognizer.recognize_google(audio, language='en-in')
                    print(f'Query: {query}')
                    return query
                except Exception as e:
                    print(f'Error: "{e}"')
                    if not self.__mStandByMode:
                        self.speak('Error occurred.')
                        self.speak('Please say it again')
                    else:
                        print('Error occurred.\nPlease say it again')

    def play(self, inQuery: str) -> None:
        """
        To search and play the query from YouTube
        :param inQuery: Query to search
        :return: None
        """
        baseURL = r'https://www.youtube.com/'
        try:
            GenUtilities.isNoneOrEmpty(inQuery)
            BrowserFactory.open(f'{baseURL}results?search_query={parse.quote(inQuery)}')
            matchedResults = self.__mBrowser.find_elements('id', 'contents')
            GenUtilities.isNoneOrEmpty(matchedResults)
            targetObj = matchedResults[0]
            targetObj.click()
            self.__mBrowser.maximize_window()
            time.sleep(10)
        except Exception as error:
            print(error)
            self.play(inQuery)

    def run(self):
        self.activate()
        while True:
            query = self.listen().lower()

            if self.__mTokenizer.match(query, ['introduce', 'say hi', 'say hello'], [self.__mAppName]):
                self.introduce()
            elif self.__mTokenizer.match(query, ['hold', 'hold on', 'stand by', 'standby']):
                self.standBy()
            elif self.__mTokenizer.match(query, ['tell me', 'say', 'say me', 'tell'], ['joke']):
                self.sayJoke()
            elif self.__mTokenizer.match(query, ['clear', 'clean'], ['terminal']):
                self.clearTerminal()
            elif query.startswith('browse'):
                self.browse(query.replace('browse ', ''))
            elif self.__mTokenizer.match(query, ['play'], ['youtube']):
                self.play(query.replace('play ', ''))
            elif self.__mTokenizer.match(query, ['wikipedia of'], ['show']):
                self.searchWikipedia(query.replace('wikipedia of ', ''), showPage=True)
            elif self.__mTokenizer.match(query, ['wikipedia of']):
                self.searchWikipedia(query.replace('wikipedia of ', ''), showPage=False)
            elif query.startswith('run'):
                self.runExecutable(query.replace('run ', ''))
            elif self.__mTokenizer.match(query, ['translate']):
                self.translate(query)
            elif self.__mTokenizer.match(query, ['wake up', 'activate', 'start', 'initiate']):
                self.activate()
            elif self.__mTokenizer.match(query, ['sleep', 'deactivate', 'abort', 'dismiss']):
                self.deActivate()
                break
            else:
                self.speak('Snap, Couldn\'t figure it out!')

    def runExecutable(self, inAppName: str):
        """
        Executes runnable application
        :param inAppName: Application name
        :return: None
        """
        GenUtilities.isNoneOrEmpty(inAppName)
        inAppName = inAppName.replace(' ', '')
        if GenUtilities.assure(self.__mConfig['operations']['executables'], inAppName.lower(), ignoreError=True):
            subprocess.call(self.__mConfig['operations']['executables'][inAppName.lower()])
        else:
            self.speak(f'Sorry, No default configuration set for {inAppName}')

    def sayJoke(self):
        """
        To fetch joke
        TODO: Enhance - setting up Language & Category
        :return: None
        """
        joke = pyjokes.get_joke()
        GenUtilities.isNoneOrEmpty(joke)
        self.speak(joke)

    def searchWikipedia(self, inQuery: str, showPage: bool = False):
        """
        Searches for the query on Wikipedia
        TODO: Enhance with rich functionalities i.e Brief content
        :param inQuery: Query to search for
        :param showPage: True to show the HTML page else False
        :return: None
        """
        GenUtilities.isNoneOrEmpty(inQuery)
        try:
            queryPage = wikipedia.page(inQuery)
            print(queryPage.summary)
            self.speak(queryPage.summary)
            if showPage:
                with open(os.path.join(VirtualAssistant.DUMPLOCATION, 'result.html'), 'w', encoding='utf-8') as file:
                    file.write(str(queryPage.html()))
                file.close()
                os.startfile(os.path.join(VirtualAssistant.DUMPLOCATION, 'result.html'))
        except exceptions.WikipediaException as error:
            self.speak(str(error))

    def speak(self, inMessage: str):
        """
        Speak Utility
        :param inMessage: Text to speak out
        :return: None
        """
        GenUtilities.isNoneOrEmpty(inMessage)
        self.__mEngine.say(inMessage)
        self.__mEngine.runAndWait()

    def standBy(self):
        """
        Turns off taking command
        :return: None
        """
        self.__mStandByMode = True

    def translate(self, inQuery: str):
        """
        Translation utility
        :param inQuery: Source text
        :return: Translated text
        """
        try:
            matchedStr = re.match(r'translate ([A-Za-z0-9 ]+) in ([A-Za-z]+)', inQuery.lower())
            if len(matchedStr.groups()) != 2:
                print(f"Expected targets (i.e Query and language) not found: {inQuery}")
            query, language = matchedStr.groups()
            result = self.__mGUTranslator.translate(query, language)
            GenUtilities.isNoneOrEmpty(result)
            print(f'"{query}" means "{result}" in {language}')
            self.speak(f'"{query}" means "{result}" in {language}')
        except Exception as error:
            print(f'Error: {error}')
