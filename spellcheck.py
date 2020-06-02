import re

def words(text):  #работает с текстом из файла, полученного на входе: находит все слова в нем, в которых больше 1 буквы независимо от регистра
    return re.findall('[а-я\-]{2,}', text.lower())

def words_counter (filename): #работает со списком частотностей: преобразует его в словарь с парами <слово><его частотность>
    with open (filename) as f:
        text=f.read()
        my_dict={}
        text=text.splitlines()
        for line in text:
            talken, number=line.split(' ')
            number=int(number)
            my_dict[talken]=number
        return my_dict
RUSWORDS=words_counter('ru_50k.txt')
russian_letters='абвгдеёжзийклмнопрстуфхцчшщъыьэюя-'

def prob(word, N=sum(RUSWORDS.values())): #рассчитывает вероятность того, что нам нужно именно это слово  (по его частотности), используется в функции correct() для расчета наиболее возможного варианта исправления для слова с опечаткой
    return RUSWORDS[word] / N
    


def edits1(word): #возвращает множество слов с расстоянием Левенштейна 1 для слова с опечаткой: все слова, которые могут получиться в результате удаления, или транспозиции, или удаления буквы, или вставки буквы
    b=len(word)
    deletes    = [word[0:i]+word[i+1:] for i in range(b)] #операция удаления (в слове с опечаткой - 1 лишняя буква)
    transposes = [word[0:i]+word[i+1]+word[i]+word[i+2:] for i in range(b-1)] #транспозиция (две буквы нужно поменять местами)
    replaces   = [word[0:i]+c+word[i+1:] for i in range(b) for c in russian_letters] #замена неправильной буквы
    inserts    = [word[0:i]+c+word[i:] for i in range(b+1) for c in russian_letters] #вставка недостающей буквы
    return set(deletes + transposes + replaces + inserts)
 

def edits2(word): #находит все слова с расстоянием 2: применяет edits1() к элементам множества, полученного в edits1()
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in RUSWORDS)


def known(words): 
    return set(w for w in words if w in RUSWORDS)
    
def candidates (word):
    return (known([word]) or known(edits1(word)) or edits2(word) or [word])

def correct(word): #выбирает наиболее возможный вариант исправления из словаря RUSWORDS: слово с наибольшей частотой встречаемости и наименьшим расстоянием Левенштейна относительно слова с опечаткой
    return max(candidates(word), key=prob)
    
def main(filename):
    with open(filename) as f:
        my_text=f.read()
        list_of_all_words=words(my_text) #нахождение в тексте всех слов (функция words())
        corrected_words=[]
        right_words=[]
        for elem in list_of_all_words:
            corrected_word=correct(elem) #нахождение наиболее подходящего исправления для каждого слова
            if corrected_word!=elem: #"отсеиваем" все слова с расстоянием Левенштейна 0 (они не будут считаться в "ошибках" в переменной 'mistakes_numb')
                corrected_words.append(corrected_word)
        mistakes_numb=len(corrected_words) #подсчет количества слов с ошибками
        perc=mistakes_numb/len(list_of_all_words)*100 #какой процент занимают слова с опечатками от всего текста?
    with open('all_mistakes.txt', 'w', encoding='utf-8') as myf: #в новый файл записываем все исправленные слова, оценку на основе данных переменной 'perc'
        myf.write(str(corrected_words))
        if perc<=20:
            myf.write('Оценка 5! Молодец!')
        elif perc>20 and perc<=40:
            myf.write('Оценка 4')
        elif perc>40 and perc<=60:
            myf.write('Оценка 3')
        else:
            myf.write('Оценка 2! Надо переписать!')


main('hameleon.txt') #пример вызова программы, 'hameleon.txt' - файл с опечатками