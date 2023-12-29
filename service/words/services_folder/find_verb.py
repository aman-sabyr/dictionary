import requests
from bs4 import BeautifulSoup
from requests.models import Response
from bs4.element import Tag
from typing import Union


class WebParser:
    def __init__(self):
        self.link = 'https://verbformen.de/?w='
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }

    def createRequest(self, word: str) -> Response:
        """
        creates full link to "verbformen.de" with the word parameter
        example: "https://verbformen.de/?w=machen"
        makes request to this web resource and gets response
        :param word: is a verb, that we need to check
        :return: Response from 'requests' library
        """
        full_link = self.link + word
        response = requests.get(full_link, headers=self.headers)
        return response

    def savePage(self, response: Response) -> None:
        """
        it receives response and creates a new html page from this response
        :param response:
        :return:
        """
        with open('./words/services_folder/buffer_folder/verb.html', 'w+') as f:
            f.write(response.text)

        return None

    def getTag(self) -> Union[bool, Tag]:
        """
        it is trying to find a section tag with id = vVdBxBox
        if there is no any - returns False
        in other case - returns this section and button tags as a tuple
        :param:
        :return:
        """

        with open('./words/services_folder/buffer_folder/verb.html', 'r') as f:
            src = f.read()

        soup = BeautifulSoup(src, 'lxml')
        section = soup.find("section", {"id": "vVdBxBox"})

        if section is None:
            return False
        """
        finds a div tag with special onclick parameter 
        """
        btn = soup.find("div", {"onclick": "Rahmen.aufzu(['vStckLng']); Rahmen.aufzu('vStckKrz')"})
        return (section, btn)

    @staticmethod
    def handleTag(tags: tuple) -> dict:
        """
        receives a Tag object and gets out of it all the information
        :param tags:
        :return:
        """
        res = []
        section, btn = tags

        for i in section.children:
            """
            gets text only from <p> tags and checks if it's not a void string
            """
            if i.name == 'p' and i.text != '\n':
                res.append(i.text)

        for i in res:
            """
            removes all \n, spaces and etc. from word
            """
            res.append(" ".join(i.split()))
            res.remove(i)

        dict_ = {}  # creating new dict where all info will be stored

        """
        res[1] is a long string with information about:
        level, is_separable, is_regular and level
        res[2] is similar to res[1], but with information about:
        original, past_form, participle
        and this block just separates them and stores to res array
        """
        temp = res[1].split(' · ')
        for i in temp:
            res.append(i)
        temp = res[2].split(' · ')
        for i in temp:
            res.append(i)

        """
        before we added new elements to res array, 
        and now we need to remove all unnecessary info
        remove first element from array 
        and then i remove first element one more time
        because indexes moved back to 1 
        """
        res.pop(1)
        res.pop(1)

        """
        in res[0] stored original word, but with two \n in beginning
        i just remove them
        """
        res[0] = res[0].replace('\n', '')

        """
        here i check if the word trennbar is in array
        if it is, then i add to dictionary is_separable = True
        and then remove this element from array
        same with untrennbar
        """
        if 'trennbar' in res:
            dict_.update({
                'is_separable': True
            })
            res.remove('trennbar')
        elif 'untrennbar' in res:
            dict_.update({
                'is_separable': False
            })
            res.remove('untrennbar')

        """
        here i check if res[2] is regelmäßig
        if it is, i add to dictionary is_regular = True
        """
        if res[2] == 'regelmäßig':
            dict_.update({'is_regular': True})
        else:
            dict_.update({'is_regular': False})

        """
        here i just add ti dictionary all other info from array
        """
        dict_.update({
            'original': res[0],
            'level': res[1],
            'past_form': res[-2],
            'participle': res[-1],
        })

        """
        gets the text of the first child from btn and parses the string
        given string from child is multiple words with ,\n between
        gets the first word
        """
        translations = btn.contents[1].text
        translations = " ".join(translations.split())
        translation = translations.split(', ')[0]
        dict_.update({
            'translation': translation
        })

        print(dict_)

        return dict_