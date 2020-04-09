import re

def words(text):  #находит все слова в тексте независимо от регистра
    return re.findall('[a-z]+', text.lower())

def words_counter (filename): #преобразует список слов в словарь с парами <слово> <количество вхождений> (на основе списка частотности из 50000слов русского языка)
    with open (filename, encoding='utf-8') as f:
        text=f.read()
        my_dict={}
        text=text.splitlines()
        for line in text:
            talken, number=line.split()
            number=int(number)
            my_dict[talken]=number
        return (my_dict)
RUSWORDS=words_counter('a.txt', encoding='utf-8')
russian_letters='абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def prob(word, N=sum(RUSWORDS.values())): #вероятность того, что то или иное слово иммется в виду (в зависимости от его частотности относительно суммы всех вхождений)
    return RUSWORDS[word] / N


def edits1(word):  #применение к слову расстояния Дамерау - Левенштейна (поиск слов с рассточнием 1): возвращает все слова с расстоянием в единицу к данному
    b=len(word)
    deletes    = [word[0:i]+word[i+1:] for i in range(b)]
    transposes = [word[0:i]+word[i+1]+word[i]+word[i+2:] for i in range(b-1)]
    replaces   = [word[0:i]+c+word[i+1:] for i in range(b) for c in russian_letters]
    inserts    = [word[0:i]+c+word[i:] for i in range(b+1) for c in russian_letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): #слова, отстоящие на расстоянии 2
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1))


def known(words): 
    return set(w for w in words if w in RUSWORDS)

def correct(word):  #выбор наиболее подходящего варианта исправления на основе теоремы Байеса
    candidates=known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates(word), key=prob)
    
def main(filename):
    with open(filename, encoding='utf-8') as f:
        my_text=f.read()
        my_words=words(my_text)
        list_of_all_words=[]
        corrected_words=[]
        list_of_all_words.append(my_words)
        for elem in list_of_all_words:
            corrected_word=correct(elem)
            corrected_words.append(corrected_word)
        return corrected_words
        