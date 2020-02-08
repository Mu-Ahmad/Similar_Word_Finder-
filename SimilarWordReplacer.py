import requests as re
from time import sleep
from bs4 import BeautifulSoup as bs


def parse(url):
    try:
        return re.get(url, verify=False)
    except:
        print('Wait, slow connection!\nYou might need to restart the program!')
        sleep(15)
        parse(url)


def findSynonyms(word):
    url = f'https://www.lexico.com/synonym/{word}'
    relevent_synonym_list = []
    types = []
    i = 0
    try:
        syn_r = re.get(url)
    except:
        syn_r = parse(url)

    syn_soup = bs(syn_r.text, 'html.parser')
    del syn_r
    for _ in syn_soup.find_all('span', {'class': 'pos'}):
        types.append(_.text)
    # for synonyms in syn_soup.find_all('div', {'class': 'synList'}):
    for synonyms in syn_soup.find_all('div', {'class': 'row'}):
        relevent_synonym_list = [words.text for words in synonyms.find_all('strong', {
                                                                           'class': 'syn'})]
        general_synonym_list = []
        for words in synonyms.find_all('span', {'class': 'syn'}):
            for s_word in words.text[1:].replace(' ', '').split(','):
                general_synonym_list.append(s_word)

        print('_'*90)
        print(f'{word.upper()} ({types[i]}):')
        print('-'*90)
        print(
            f'>>> These {len(relevent_synonym_list)} are the More Relevent words to "{word.upper()}({types[i]})":\n', relevent_synonym_list)
        print('-'*90)
        print(
            f'>>> These {len(general_synonym_list)} are Genral words related to "{word.upper()}({types[i]})":\n', general_synonym_list)
        print('_'*90)
        i += 1
    if not relevent_synonym_list:
        print(
            '>>> We are Sorry!\n1 million words we know.\nBut, no word similar to this could be found in our database!')


def replaceWord(word):
    path = input('Enter the text file name:')
    newWord = input('Enter the new word:')
    filepath = f'{path}.txt'
    newFilePath = f'New{path}.txt'
    with open(filepath, 'r') as file:
        content = file.read()
    content = content.replace(word.lower(), newWord.lower())
    content = content.replace(word.upper(), newWord.upper())
    content = content.replace(word.capitalize(), newWord.capitalize())
    with open(newFilePath, 'w') as newfile:
        newfile.write(content)
        print('The Changes Have Been Made Successfully!')


def initiateSequence():
    word = input('Enter the desired word to find the synonyms:')
    findSynonyms(word)
    choice = input(f'Would you like to replace this word >> {word} << ? y/n')
    if choice.lower() == 'y':
        replaceWord(word)
    print('loading.....')
    # sleep(10)
    initiateSequence()


try:
    initiateSequence()
except Exception as e:
    print(e)
    print('Check Your URL or INTERNET Connection or FileName')
    initiateSequence()
