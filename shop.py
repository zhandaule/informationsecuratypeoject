import pickle # Для Сериализации. Сериализация (в программировании) — процесс перевода структуры данных в битовую последовательность.
import random # Для рандома 
from cryptography.fernet import Fernet # Для хэширования документа с данными 
import os

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

class Shop(): # Класс с товарами

    def __init__(self, name, price, stock): # Такие как имя, цена и количество на складе
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self): # Функция __string__ для быстрого вывода о товаре
        return f"Product:\nname: {self.name}\nprice: {self.price}\nstock: {self.stock}"

    def __getstate__(self) -> dict:  # Как мы будем "сохранять" класс
        state = {}
        state["name"] = self.name
        state["price"] = self.price
        state["stock"] = self.stock
        return state

    def __setstate__(self, state: dict): # Как мы будем восстанавливать класс из байтов
        self.name = state["name"]
        self.price = state["price"]
        self.stock = state["stock"]

class Queue(): # Класс очереди для корзины
     def __init__(self):
        self.queue = []

     def enqueue(self, item): # Добавляет элемент в конец очереди, аналог stack.push
        self.queue.append(item)

     def dequeue(self): # Обобщенная очередь (dequeue) получает первый или последний элемент, как stack.pop
        if len(self.queue) < 1:
            return None
        return self.queue.pop(0)

     def show(self): # Вывод с проверкой, ну тут понятно
        if len(self.queue) != 0: # Если что - то тут есть то он выводит
            print(self.queue)
        else: # Если нет то выводит Null
            print("It's empty")
            return None

     def clear(self):
        self.queue.clear()

     def num(self): # Просто показывает сколько наших элементов в Корзине
        print(len(self.queue)-1)

cart_name = Queue() # Обьявление очереди

def in_out(): # Функция для сериализации
    destroy = pickle.dumps(dict_p) # Сериализуем
    with open("Kamillot.pkl", "wb") as fp: # <wb> указывает, что файл открыт для записи в бинарном режиме
                                         # <fp> означает «указатель файла», и это был указатель на структуру FILE в C.
        pickle.dump(dict_p, fp)

def out(): # Функция для для чтения с байтов 
    with open("Kamillot.pkl", "rb") as fp: # <rb> указывает, что файл открыт для чтения в бинарном режиме
        dict_p = pickle.load(fp)
    b = pickle.loads(destroy)  # Восстанавливаем экземпляр класса из байтов
    print(b)

def generate_priv_pub_key(): # Шифрование RSA
    key = RSA.generate(2048)
    with open('private.pem', 'wb') as priv:
        priv.write(key.export_key())
    print('\n[+] Приватный ключ "private.pem" сохранен')

    with open('public.pem', 'wb') as pub:
        pub.write(key.publickey().export_key())
    print('[+] Публичный ключ "public.pem" сохранен')
    main()
    return

def encrypt(name): # Шифровка
    with open(f"{name}.txt", 'rb') as enc_file:
        data_enc = enc_file.read()

    if os.path.isfile('public.pem'):
        public_rsa = RSA.import_key(open('public.pem').read())
        session_key = get_random_bytes(16)

        # шифруем сессионный ключ открытым ключом RSA
        chips_rsa = PKCS1_OAEP.new(public_rsa)
        enc_session_key = chips_rsa.encrypt(session_key)

        # шифруем файл с сессионным ключом алгоритм AES
        chips_aes = AES.new(session_key, AES.MODE_EAX)
        chips_text, tag = chips_aes.encrypt_and_digest(data_enc)

        with open(f'{f"{name}.txt"}.bin', 'wb') as file_out:
            for x in (enc_session_key, chips_aes.nonce, tag, chips_text):
                file_out.write(x)
        print(f'{name} зашифрован')
        os.remove(f"{name}.txt")
    else:
        print('\n[+] Нет публичного ключа для шифрования. Сгенерируйте ключи.')
        return None

def decrypt(name): # Дишифровка
    if os.path.isfile("private.pem"):
        priv_key_rsa = RSA.import_key(open("private.pem").read())
        with open(f"{name}.txt.bin", "rb") as file_in:
            enc_session_key, nonce, tag, chips_text = [file_in.read(x) for x in (priv_key_rsa.size_in_bytes(), 16, 16, -1)]

        # расшифровка сессионного ключа закрытым ключом RSA
        chips_rsa = PKCS1_OAEP.new(priv_key_rsa)
        session_key = chips_rsa.decrypt(enc_session_key)

        # расшифровка данных сессионным ключом алгоритм AES
        chips_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = chips_aes.decrypt_and_verify(chips_text, tag)
        with open(f"{name}.txt.bin"[:-4], "wb") as file_out:
            file_out.write(data)
        print(f'{name} дешифрован')
        os.remove(f"{name}.txt.bin")
    else:
        print('\n[+] Нет приватного ключа для дешифровки.\nСкопируйте ключ "private.pem" в папку со скриптом!')
        main()
        return

def shop_cart(cart_bl, cart_name, balance, summary, name): # Функция для корзины

    tumbler = True

    while(tumbler):
        ch_1 = int(input('What do you want to do? \n1)Show your cart \n2)Buy all elements \n3)Delete from your cart \n'))

        if ch_1 == 1: #Тута просто показывает все элементы и их общую цену

            print('Your shopping cart: ')
            cart_name.show()
            print('Total price: ')
            summary = (sum((int(cart_bl[i]) for i in range(0, int(len(cart_bl))))))
            print(summary, '\n')


        elif ch_1 == 2: # Проверка на бомжа 2

            if balance < summary:
                print("You don't have enough funds: ")
            else:
                print("Congratulations on your purchase: ")
                balance = balance - summary
                print('Your balance now: ', balance, '\n')

                #Очищаю все от данных
                cart_name.clear()
                cart_bl.clear()

        elif ch_1 == 3: # Удаляю первый элемент

            print(cart_bl)
            cart_name.dequeue()
            cart_bl.pop(0)
            print(cart_bl)

        else:
            tumbler = False # Корзина магазина

def shop_buy(dict_p, cart_bl, balance, summary, name): # Функция для покупки вещей

    enter = int(input("Enter the number of your product: \n"))

    enter = enter - 1

    # Тут выберают продукт, он добовляется в корзину, еще тут пишется сколько товара осталось и все такое

    print("Name:", dict_p[enter]['name'])
    print("Price:", dict_p[enter]['price'])
    print("Stock:", dict_p[enter]['stock'])

    stock_col = dict_p[enter]['stock']
    stock_col = int(stock_col)

    #Проверка на количество
    if stock_col == 0 or stock_col < 0:
        print("Sorry, item is out of stock")
        shop_buy(dict_p, cart_bl, balance, summary, name)
    else:

        cart_name.enqueue(dict_p[enter]['name'])
        dict_p[enter]['stock'] = dict_p[enter]['stock'] - 1
        cart_bl.append(dict_p[enter]['price'])

        

    # Проверка на бомжа (АХХПХАХАХХАХХАХПХАХП)
    if balance == 0 and balance < dict_p[enter]['price']:
        print("You can't buy anything your balance is empty") # Покупка в магазина

def standart_password(): # Тут запись пароля в стандартной форме
    l = 0 
    u = 0
    p = 0
    d = 0

    capitalalphabets="ABCDEFGHIJKLMNOPQRSTUVWXYZ" # Переменные для проверки пароля
    smallalphabets="abcdefghijklmnopqrstuvwxyz"
    specialchar="$@_"
    digits="0123456789"

    standart_password = input("Введите пароль: ")
    
    if (len(standart_password) >= 8):
        for i in standart_password:
        # считает элементы нижнего регистра
            if (i in smallalphabets):
                    l+=1           
        # считает элементы верхнего регистра
            if (i in capitalalphabets):
                    u+=1           
        # считает числа
            if (i in digits):
                    d+=1           
        # считает специальные элементы
            if(i in specialchar):
                    p+=1       
    else:
            print("Попробуйте снова")
            accoaunt()
    if (l>=1 and u>=1 and p>=1 and d>=1 and l+p+u+d==len(standart_password)):
            print("Пароль соответсвует норме")
    else:
            print("Пароль не соотвествует попробуйте снова")
            accoaunt()

    return standart_password

def captcha(): # Функция для проверки на робота (капча)

    a = random.randint(1, 52)
    b = random.randint(1, 52)
    c = random.randint(1, 52)
    d = random.randint(1, 52)
    e = random.randint(0, 9)
    f = random.randint(0, 9)

    count = random.randint(0, 3)
    count1 = random.randint(0, 4)

    abcd  = [a, b, c, d]

    for i in range(len(abcd)): # Заполнение капчи
        if abcd[i] == 1:
            abcd[i] = 'A'
        elif abcd[i] == 2:
            abcd[i] = 'B'
        elif abcd[i] == 3:
            abcd[i] = 'C'
        elif abcd[i] == 4:
            abcd[i] = 'D'
        elif abcd[i] == 5:
            abcd[i] = 'E'
        elif abcd[i] == 6:
            abcd[i] = 'F'
        elif abcd[i] == 7:
            abcd[i] = 'G'
        elif abcd[i] == 8:
            abcd[i] = 'H'
        elif abcd[i] == 9:
            abcd[i] = 'I'
        elif abcd[i] == 10:
            abcd[i] = 'J'
        elif abcd[i] == 11:
            abcd[i] = 'K'
        elif abcd[i] == 12:
            abcd[i] = 'L'
        elif abcd[i] == 13:
            abcd[i] = 'M'
        elif abcd[i] == 14:
            abcd[i] = 'N'
        elif abcd[i] == 15:
            abcd[i] = 'O'
        elif abcd[i] == 16:
            abcd[i] = 'P'
        elif abcd[i] == 17:
            abcd[i] = 'Q'
        elif abcd[i] == 18:
            abcd[i] = 'R'
        elif abcd[i] == 19:
            abcd[i] = 'S'
        elif abcd[i] == 20:
            abcd[i] = 'T'
        elif abcd[i] == 21:
            abcd[i] = 'U'
        elif abcd[i] == 22:
            abcd[i] = 'V'
        elif abcd[i] == 23:
            abcd[i] = 'W'
        elif abcd[i] == 24:
            abcd[i] = 'X'
        elif abcd[i] == 25:
            abcd[i] = 'Y'
        elif abcd[i] == 26:
            abcd[i] = 'Z'
        if abcd[i] == 27:
            abcd[i] = 'a'
        elif abcd[i] == 28:
            abcd[i] = 'b'
        elif abcd[i] == 29:
            abcd[i] = 'c'
        elif abcd[i] == 30:
            abcd[i] = 'd'
        elif abcd[i] == 31:
            abcd[i] = 'e'
        elif abcd[i] == 32:
            abcd[i] = 'f'
        elif abcd[i] == 33:
            abcd[i] = 'g'
        elif abcd[i] == 34:
            abcd[i] = 'h'
        elif abcd[i] == 35:
            abcd[i] = 'i'
        elif abcd[i] == 36:
            abcd[i] = 'j'
        elif abcd[i] == 37:
            abcd[i] = 'k'
        elif abcd[i] == 38:
            abcd[i] = 'l'
        elif abcd[i] == 39:
            abcd[i] = 'm'
        elif abcd[i] == 40:
            abcd[i] = 'n'
        elif abcd[i] == 41:
            abcd[i] = 'o'
        elif abcd[i] == 42:
            abcd[i] = 'p'
        elif abcd[i] == 43:
            abcd[i] = 'q'
        elif abcd[i] == 44:
            abcd[i] = 'r'
        elif abcd[i] == 45:
            abcd[i] = 's'
        elif abcd[i] == 46:
            abcd[i] = 't'
        elif abcd[i] == 47:
            abcd[i] = 'u'
        elif abcd[i] == 48:
            abcd[i] = 'v'
        elif abcd[i] == 49:
            abcd[i] = 'w'
        elif abcd[i] == 50:
            abcd[i] = 'x'
        elif abcd[i] == 51:
            abcd[i] = 'y'
        elif abcd[i] == 52:
            abcd[i] = 'z'
    
    abcd.insert(count, str(e))
    abcd.insert(count1, str(f))
    
    abcdef = abcd[0] + abcd[1] + abcd[2] + abcd[3] + abcd[4] + abcd[5]

    print(abcdef)

    flag_cpch = True
    insert_word = ' '

    while (flag_cpch):
        insert_word = (input('Введите капчу с экрана: '))
        if insert_word != abcdef:
            print('Не правильно, попробуйте снова')
            captcha()
        else:
            print('Правильно, можете продолжать ваши покупки')
            flag_cpch = False

def accoaunt(name): # Функция для создания аккаунта1

    question = input("1 - Вы хотите создать новый аккаунт? \n2 - У меня уже есть существующий аккаунт\n")
    
    if question == '1':
        print('Пожалуйста вводите ваши данные на латинице:')
        
        name = input("Введите имя пользоваталя: ")
        file = open(f"{name}.txt","w")
        wr_name = "Name " + name + "\n"
        file.write(wr_name)
        
        print("Пароль должен соответсвовать требованиям: \n1 - Не быть меньше 8 символов \n2 - Должен содержать символ в верхнем регистре \n3 - Должен содержать хоть один спец символ \n4 - Должен содержать как минимум одну цифр")
        
        password = standart_password()
        password = "Password "+ password +"\n"
        file.write(password)
        
        balance = input("Введите ваш текуйщий баланс: ")
        balance = "Balance "+ balance +"\n"
        file.write(balance)
        
        file.write("Статус пользователь")
        print("Ваш аккаунт был успешно создан")
        print("Теперь попытайтесь войти в свой аккаунт: ")

        file.close()
        encrypt(name)
    elif question == '2':
        pass
    else:
        pass

def main(name): # Главное тело кода

    accoaunt(name)

    print("Пожалуйста войдите в свой аккаунт: ")
    
    name = input("Введите имя вашего аккаунта: ")
    password=input("Введите пароль вашего аккаунта: ")

    captcha()
    
    data = {}

    decrypt(name)

    try:
        file = open(f"{name}.txt")
    except:
        print("Аккаунт не найден, попробуйте снова или создайте новый аккаунт")
        accoaunt()

    for line in file:
            key,value=line.split()
            data[key] = value
    print(data)
    if data["Name"]==name and data["Password"]==password:
        print("Добро пожаловать: ")
    else:
        print("Неверный пароль")
        accoaunt(name)
    balance = data["Balance"]
    balance = int(balance)
    print("Your balance know: ", balance)
    file.close()

    flag = True
    summary = 0

    dict_p = [] 
    cart_bl = [] 

    
    while(flag):

        with open("Kamillot.pkl", "rb") as fp: # Крч прикол том что он разьбивает на байты а потом собирает все в класс, файлы не читаемые но какая разница, главное что программа понимает
            dict_p = pickle.load(fp) # Ха в честь Камилы назвал, я горд собой (Файл такой же не читаемый как её почерк ПХАХАХАХХАХАХАХПХ) теперь точно горд собой
        #Это самое не говорите ей только про эту шутку, а то мне не видать довольствий долгое время

        for element in dict_p: # Классика, просто вывод нашего списка
            print(element)

        ch = int(input('Do you want to buy something?: \n1)Yes \n2)No \n3)Goto shop cart \n'))

        if ch == 1:

            shop_buy(dict_p, cart_bl, balance, summary, name)

            destroy = pickle.dumps(dict_p) # destroy Типа уничтожить до бинарных частиц (ахаххахаха)
            with open("Kamillot.pkl", "wb") as fp:
                pickle.dump(dict_p, fp) # Да метод огурчиком крч, (Огурчик Рик?)

        elif ch == 2:
            flag = False

        elif ch == 3: # Это Корзина магазина
            shop_cart(cart_bl, cart_name, balance, summary, name)
        else:
            flag = True
    
    encrypt(name)
        


if __name__ == "__main__":
    name = ' '
    main(name)