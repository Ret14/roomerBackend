## Roomer Backend
| Версия 	 |  Дата    	   |                                             Описание изменений                                                                                          	                                              |
|:--------:|:------------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| 1.0    	 | 24.12.2022 	 | Описал запросы и ответы для фильтрации пользователей и квартир                                                                                                                                       	 |
| 1.1    	 | 12.03.2023 	 | Добавил запросы первичной регистрации, авторизации, заполнения профиля,  получения информации об авторизованном пользователе, запрос добавления объявления. Привел описание запросов к единому стилю 	 |                                                            
| 1.2    	 | 17.03.2023 	 |                                                                 Добавил аккаунты для членов команды, исправил синтаксис запросов curl                                                                  |                                                            

[Аккаунты для тестирования](accounts.md)

### Первичная регистрация пользователя
#### Бизнес постановка
Пользователь отправляет username login email для регистрации и получает успешный код ответа либо сообщения о возникших ошибках
#### Примеры запросов
#### Запрос:
    curl -X POST\
      http://176.113.83.93:8000/auth/users/\
    -d '{\
    "email": "somemail@mail.ru",\
    "password": "very_hard_password",\
    "username": "cool_username"\
    }'
#### Ответ:
    Response code: 201
    Response body:
    {
        "email": "somemail@mail.ru",
        "username": "cool_username",
        "id": 301
    }
#### Запрос:
    curl -X POST\
    http://176.113.83.93:8000/auth/users/\
    -d '{\
    "email": "somemail@mail.ru",\
    "password": "short",\
    "username": "cool_username"\
    }'
#### Ответ:
    Response code: 400
    Response body:
    {
        "password": [
            "This password is too short. It must contain at least 8 characters."
        ]
    }

### Авторизация
#### Бизнес постановка:
Пользователь авторизуется и если данные корректны, то получает токен

#### Примеры запросов
#### Запрос:
    curl -X POST\
      http://176.113.83.93:8000/auth/token/login/\
    -d '{\
    "password": "very_hard_password",\
    "username": "cool_username"\
    }'
#### Ответ:
    Response code: 200
    Response body:
    {
        "auth_token": "e464ae9def145a8774ee5d9215a58237c1fd7e2a"
    }
#### Запрос:
    curl -X POST\
      http://176.113.83.93/auth/token/login/\
    -d '{\
    "password": "wrong_password",\
    "username": "cool_username"\
    }'
#### Ответ:
    Response code: 400
    Response body:
    {
        "non_field_errors": [
            "Unable to log in with provided credentials."
        ]
    }
### Получение информации о текущем авторизованном пользователе
#### Бизнес постановка:
Пользователь повторно авторизовался и решил посмотреть информацию своего профиля
#### Запрос:
    curl -X GET\
    http://176.113.83.93:8000/auth/users/me/ \
    -H 'Authorization: Token c0d68713b6753ea14ac12f9b6ca96df6f4b51457'\

#### Ответ:
    Response code: 200
    Response body:
    {
        "id":16,
        "first_name":"",
        "last_name":"",
        "birth_date":"2022-12-23",
        "sex":"F",
        "avatar":"http://176.113.83.93:8000/static/img/default.png",
        "email":"seconnduser11@mail.ru",
        "about_me":"I'm good",
        "employment":"E",
        "alcohol_attitude":"N",
        "smoking_attitude":"N",
        "sleep_time":"N",
        "personality_type":"E",
        "clean_habits":"N",
        "interests":[]
    }

### Заполнение профиля авторизованного пользователя
#### Бизнес постановка:
Пользователь заполняет форму профиля
#### Варианты заполнения некоторых полей:
**sex** = [
    ('M', 'Male'),
    ('F', 'Female')
]

**alcohol/smoking attitude** = [
    ('P', 'Positive'),
    ('N', 'Negative'),
    ('I', 'Indifferent')
]

**sleep time** = [
    ('N', 'Night'),
    ('D', 'Day'),
    ('O', 'Occasionally')
]

**personality** = [
    ('E', 'Extraverted'),
    ('I', 'Introverted'),
    ('M', 'Mixed')
]

**clean habits** = [
    ('N', 'Neat'),
    ('D', 'It Depends'),
    ('C', 'Chaos')
]

**employment** = [
    ('NE', 'Not Employed'),
    ('E', 'Employed'),
    ('S', 'Searching For Work')
]
#### Примеры запросов
#### Запрос:
    curl -X PUT\
    http://176.113.83.93:8000/auth/users/me/\
    -H 'Authorization: Token b704c9fc3655635646356ac2950269f352ea1139'\
    -F first_name=rodion\
    -F last_name=ivannikov\
    -F birth_date=2022-01-30\
    -F sex=F \
    -F avatar=@/home/rodion/Downloads/8405385.jpg\
    -F about_me='some person description'\
    -F employment=E\
    -F alcohol_attitude=I\
    -F smoking_attitude=I\
    -F sleep_time=N\
    -F personality_type=I \
    -F clean_habits=N
#### Ответ:
    Response code: 200
    Response body:
    {
        "id": 301,
        "first_name": "rodion",
        "last_name": "ivannikov",
        "birth_date": "2022-01-30",
        "sex": "F",
        "avatar": "http://176.113.83.93:8000/media/avatar/2023/03/12/8405385_RVkXKvi.jpg",
        "email": "rivan@mail.ru",
        "about_me": "some person description",
        "employment": "E",
        "alcohol_attitude": "I",
        "smoking_attitude": "I",
        "sleep_time": "N",
        "personality_type": "I",
        "clean_habits": "N",
        "interests": []
    }
### Фильтрация пользователей
#### Бизнес постановка:
Пользователь задает параметры фильтрации и получает список пользователей, которые им удовлетворяют
#### Комментарий:
Значения для фильтрации - это варианты заполнения полей из задачи сверху
#### Примеры запросов
#### Запрос:
    curl -X GET\
    http://176.113.83.93/profile/\
    ?sex=F&\
    employment=E&\
    alcohol_attitude=N&\
    smoking_attitude=I&\
    sleep_time=N&\
    personality_type=E&\
    clean_habits=N
#### Ответ:
    Response code: 200
    Response body:
    [{
        "first_name": "Patricia",
        "last_name": "Scott",
        "birth_date": "2022-12-21",
        "sex": "F",
        "avatar": "http://176.113.83.93:8000/static/img/default.png",
        "about_me": "Couple bag thank. Could cut pull save fine",
        "employment": "E",
        "alcohol_attitude": "N",
        "smoking_attitude": "I",
        "sleep_time": "O",
        "personality_type": "E",
        "clean_habits": "N",
        "interests": [
            77,
            80,
            82,
            84,
            85,
            86,
            88,
            89,
            90
        ]
    },]
### Фильтрация квартир
#### Бизнес постановка:
Пользователь задает параметры фильтрации и получает список квартир, которые им удовлетворяют
#### Варианты значений некоторых полей:

**bedrooms/bathrooms count** = [ 1, 2, 3, 4, 5 ]
#### Комментарий:
Как параметр фильтрации можно сообщить значения: 1, 2, 3, >3
Для последнего варианта будут учтены записи со значением поля = 4, 5

**housing type** = [
    ('F', 'Flat'),
    ('DU', 'Duplex'),
    ('H', 'House'),
    ('DO', 'Dorm')
]
**sharing type** = [
    ('P', 'Private'),
    ('S', 'Shared')
]

#### Примеры запросов
#### Запрос:
    curl -X GET\
    http://176.113.83.93/housing/\
    ?month_price_from=40000&\
    month_price_to=90000&\
    bedrooms_count=>3&\
    bathrooms_count=2&\
    housing_type=DO&\
    sharing_type=S
#### Ответ:
    Response code: 200
    Response body:
    [{
        "month_price": 54738,
        "host": {
            "first_name": "Sara",
            "last_name": "White",
            "birth_date": "2022-12-21",
            "sex": "F",
            "avatar": "http://127.0.0.1:8000/static/img/default.png",
            "about_me": "Full parent analysis. Recognize someone treatment over",
            "employment": "NE",
            "alcohol_attitude": "I",
            "smoking_attitude": "P",
            "sleep_time": "N",
            "personality_type": "M",
            "clean_habits": "N",
            "interests": [
                78,
                79,
                83,
                87,
                90
            ]},
        "description": "Simple happen beat offer rate half.\nGuess what edge",
        "bathrooms_count": 2,
        "bedrooms_count": 4,
        "housing_type": "F",
        "room_attributes": [],
        "sharing_type": "P",
        "photo": "http://176.113.83.93:8000/static/img/flat_default.jpeg"
    }]

### Добавление объявления
#### Бизнес постановка:
Пользователь решил опубликовать объявление о совместной аренде квартиры. Пользователь указывает необходимую информацию, загружает фото помещения и публикует объявление
#### Примеры запросов
#### Запрос:
    curl -X POST\
        http://176.113.83.93:8000/housing/\
        -H 'Authorization: Token b704c9fc3655635646356ac2950269f352ea1139'\
        -F location='Astrakhan city'\
        -F sharing_type=S\
        -F host=300\
        -F housing_type=F\
        -F file_content=@/home/rodion/Downloads/8405385.jpg\
        -F file_content=@/home/rodion/Downloads/7474638.jpg\
        -F bedrooms_count=5\
        -F bathrooms_count=2
#### Ответ:
    {
        "id": 302,
        "month_price": 5000,
        "host": 300,
        "description": "some apartment",
        "file_content": [
            3,
            4
        ],
        "title": "some apartment",
        "location": "Astrakhan city",
        "bathrooms_count": 2,
        "bedrooms_count": 5,
        "housing_type": "F",
        "room_attributes": [],
        "sharing_type": "S"
    }
#### Комментарий:
file_content - фотографии помещения
