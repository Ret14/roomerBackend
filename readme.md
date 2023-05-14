## Roomer Backend
| Версия 	 |  Дата    	   |                                             Описание изменений                                                                                          	                                              |
|:--------:|:------------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| 1.0    	 | 24.12.2022 	 | Описал запросы и ответы для фильтрации пользователей и квартир                                                                                                                                       	 |
| 1.1    	 | 12.03.2023 	 | Добавил запросы первичной регистрации, авторизации, заполнения профиля,  получения информации об авторизованном пользователе, запрос добавления объявления. Привел описание запросов к единому стилю 	 |                                                            
| 1.2    	 | 17.03.2023 	 |                                                                 Добавил аккаунты для членов команды, исправил синтаксис запросов curl                                                                  |                                                            
| 1.3    	 | 18.03.2023 	 |                                                                                     Исправил синтаксис команд curl                                                                                     |                                                            
| 1.4    	 | 27.03.2023 	 |                                                                  Добавил параметры age_to, age_from в запрос фильтрации пользователей                                                                  |                                                            
| 1.5    	 | 28.03.2023 	 |                                    Добавил параметр interests в запрос фильтрации пользователей. Вставил комментарий, описывающий алгоритм фильтрации и ограничения                                    |                                                            
| 1.6    	 | 03.04.2023 	 |                                                                              Обновил некоторые примеры запросов и ответов                                                                              |                                                            
| 1.7    	 | 08.04.2023 	 |                                                                            Добавил запрос для пометки прочитанных сообщений                                                                            |                                                            
| 1.8    	 | 15.04.2023 	 |                                                                                   Добавил город в некоторые запросы                                                                                    |                                                            
| 1.9    	 | 01.05.2023 	 |                                                                                Добавил запросы для работы с подписками                                                                                 |                                                            
| 2.0    	 | 02.05.2023 	 |                                                                         Добавил запрос получения объявлений, созданных юзером                                                                          |                                                            
| 2.1    	 | 06.05.2023 	 |                                                                            Добавил запросы изменения и удаления объявления                                                                             |                                                            
| 2.2    	 | 07.05.2023 	 |                                                                      Добавил запросы создания, получения и удаления комментариев                                                                       |                                                            

[Аккаунты для тестирования](accounts.md)

### Первичная регистрация пользователя
#### Бизнес постановка
Пользователь отправляет username login email для регистрации и получает успешный код ответа либо сообщения о возникших ошибках
#### Примеры запросов
#### Запрос:
    curl -X POST \
    http://176.113.83.93:8000/auth/users/ \
    -d 'email=somemail@mail.ru&password=very_hard_password&username=cool_username'
#### Ответ:
    Response code: 201
    Response body:
    {
        "email": "somemail@mail.ru",
        "username": "cool_username",
        "id": 301
    }
#### Запрос:
    curl -X POST \
    http://176.113.83.93:8000/auth/users/ \
    -d 'email=somemail@mail.ru&password=short&username=cool_username'
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
    curl -X POST \
    http://176.113.83.93:8000/auth/token/login/ \
    -d 'password=very_hard_password&username=cool_username'
#### Ответ:
    Response code: 200
    Response body:
    {
        "auth_token": "e464ae9def145a8774ee5d9215a58237c1fd7e2a"
    }
#### Запрос:
    curl -X POST \
    http://176.113.83.93:8000/auth/token/login/ \
    -d 'password=wrong_password&username=cool_username'
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
    curl -X GET \
    http://176.113.83.93:8000/auth/users/me/ \
    -H 'Authorization: Token c0d68713b6753ea14ac12f9b6ca96df6f4b51457'
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
    curl -X PUT \
    http://176.113.83.93:8000/auth/users/me/ \
    -H 'Authorization: Token b704c9fc3655635646356ac2950269f352ea1139'  \
    -F first_name=rodion \
    -F last_name=ivannikov \
    -F birth_date=2022-01-30 \
    -F sex=F \
    -F avatar=@/home/rodion/Downloads/8405385.jpg \
    -F about_me='some person description' \
    -F employment=E \
    -F alcohol_attitude=I \
    -F smoking_attitude=I \
    -F sleep_time=N \
    -F personality_type=I \
    -F city=Москва \
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
        "city": "Москва",
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
    curl -X GET \
    http://176.113.83.93/profile/?sex=M&employment=E&alcohol_attitude=N&smoking_attitude=I&sleep_time=O&personality_type=E&clean_habits=N&age_from=18&age_to=28&interests=2&interests=3&interests=1&interests=6&city=Москва
#### Ответ:
    Response code: 200
    Response body:
    [
    {
        "id": 91,
        "first_name": "Michelle",
        "last_name": "Martinez",
        "birth_date": "1996-10-11",
        "sex": "M",
        "avatar": "http://0.0.0.0:8000/media/static/img/default.jpg",
        "email": "martinaaron@example.com",
        "about_me": "Time arm from force analysis. Wind thank impact miss into.\nTree page across once station. Meeting themselves piece relationship. Protect put carry.\nFar take hold his us. Take inside research her attack yet.\nPerform listen size resource. Investment remember may knowledge. Health chair morning hold listen his media.\nInternational table make. Opportunity against dog start vote simply.\nTravel nature drop sport really hair. Plant them wish learn edge body. Institution often they stop beyond former ground. Those own forward break.",
        "city": "Москва",
        "employment": "E",
        "alcohol_attitude": "N",
        "smoking_attitude": "I",
        "sleep_time": "O",
        "personality_type": "E",
        "clean_habits": "N",
        "interests": [
            {
                "id": 3,
                "interest": "son"
            },
            {
                "id": 6,
                "interest": "amount"
            },
            {
                "id": 8,
                "interest": "much"
            },
            {
                "id": 10,
                "interest": "interview"
            },
            {
                "id": 18,
                "interest": "wait"
            },
            {
                "id": 20,
                "interest": "discover"
            },
            {
                "id": 24,
                "interest": "challenge"
            }
        ]
    }
    ]
#### Комментарий:
Как происходит фильтрация по интересам: Считается кол-во переданных id интересов, умножается на 0.4 и округляется в большую сторону до целых. Это количество общих интересов в интересах юзера и интересах, переданных в запросе. Если число общих интересов у юзера и в запросе меньше, чем высчитанное число общих интересов, то он исключается из подборки фильтра. Максимум можно передать 30 id интересов
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
    curl -X GET \
    http://176.113.83.93/housing/?month_price_from=40000&month_price_to=90000&bedrooms_count=>3&bathrooms_count=2&housing_type=DO&sharing_type=S
#### Ответ:
    Response code: 200
    Response body:
    [{
        "id": 302,
        "month_price": 54738,
        "host": {
            "id": 8,
            "first_name": "Mary",
            "last_name": "Collins",
            "birth_date": "2017-07-28",
            "sex": "M",
            "avatar": "http://0.0.0.0:8000/media/avatar/default.jpg",
            "email": "natalieholmes@example.net",
            "about_me": "Many water meeting. Begin fight institution school white team.\nExplain current simply process sit. His can sing husband matter.\nPrevent hear trouble it grow. Should research executive black tough building. General during cost what.\nBody himself home message woman. Stock determine human find discussion military ability. First through dinner whose worker offer American.\nCustomer force both something hair. Well account movement can start.",
            "city": "Москва",
            "employment": "NE",
            "alcohol_attitude": "P",
            "smoking_attitude": "N",
            "sleep_time": "O",
            "personality_type": "I",
            "clean_habits": "C",
            "interests": [
                {
                    "id": 10,
                    "interest": "interview"
                },
                {
                    "id": 15,
                    "interest": "me"
                },
                {
                    "id": 17,
                    "interest": "past"
                },
                {
                    "id": 19,
                    "interest": "whatever"
                },
                {
                    "id": 24,
                    "interest": "challenge"
                },
                {
                    "id": 28,
                    "interest": "successful"
                }
            ]
        },
        "description": "some apartment",
        "file_content": [
            {
                "photo": "http://0.0.0.0:8000/media/housing/2023/04/03/8405370_ozVWNYh.jpg"
            }
        ],
        "bathrooms_count": 2,
        "bedrooms_count": 4,
        "housing_type": "F",
        "room_attributes": [],
        "sharing_type": "P",
    }]

### Добавление объявления
#### Бизнес постановка:
Пользователь решил опубликовать объявление о совместной аренде квартиры. Пользователь указывает необходимую информацию, загружает фото помещения и публикует объявление
#### Примеры запросов
#### Запрос:
    curl -X POST \
        http://176.113.83.93:8000/housing/ \
        -H 'Authorization: Token b704c9fc3655635646356ac2950269f352ea1139' \
        -F location='Astrakhan city' \
        -F title='cool apartment' \
        -F description='some apartment' \
        -F sharing_type=S \
        -F host=5 \
        -F housing_type=F \
        -F file_content=@/home/rodion/Downloads/8405385.jpg \
        -F bedrooms_count=2 \
        -F month_price=5000 \
        -F bathrooms_count=2
#### Ответ:    
    Response code: 201
    Response body:
    {
    "id": 301,
    "month_price": 5000,
    "host": {
        "id": 5,
        "first_name": "Jesus",
        "last_name": "Fuller",
        "birth_date": "1993-04-14",
        "sex": "F",
        "avatar": "/media/avatar/default.jpg",
        "email": "dwerner@example.com",
        "about_me": "Commercial special network foreign one agent candidate how. Member baby share sit.\nShould wide dog car do his part. Pick too blue street. Other majority final when new clear these.\nFinish summer else page region start size. Want decade firm section economic television. Employee public figure ground much.\nGovernment make article drop. Difficult president at. General professional career two. Itself group computer forget would section him.\nMove source wonder relate service. Tv important hope about catch than method. Bag down stock computer.\nSea stuff no response.\nBillion pick report past always future scene heavy. Usually already bed fall character door green save. Front sound war address morning explain.\nSignificant now energy. Lay return identify. Anything event yet effect quite reflect upon.\nMight history strong economy break word source. Only result race government trouble.",
        "city": "Москва",
        "employment": "NE",
        "alcohol_attitude": "P",
        "smoking_attitude": "P",
        "sleep_time": "D",
        "personality_type": "E",
        "clean_habits": "N",
        "interests": [
            {
                "id": 2,
                "interest": "image"
            },
            {
                "id": 6,
                "interest": "amount"
            },
            {
                "id": 9,
                "interest": "mention"
            },
            {
                "id": 11,
                "interest": "why"
            },
            {
                "id": 12,
                "interest": "step"
            },
            {
                "id": 13,
                "interest": "themselves"
            },
            {
                "id": 17,
                "interest": "past"
            },
            {
                "id": 22,
                "interest": "chair"
            },
            {
                "id": 23,
                "interest": "father"
            },
            {
                "id": 28,
                "interest": "successful"
            }
        ]
    },
    "description": "some apartment",
    "file_content": [
        1
    ],
    "title": "cool apartment",
    "location": "Astrakhan city",
    "bathrooms_count": 2,
    "bedrooms_count": 2,
    "housing_type": "F",
    "room_attributes": [],
    "sharing_type": "S"
    }
#### Комментарий:
file_content - фотографии помещения. host - id пользователя, который создает объявление

### Изменение статуса сообщения на "прочитано"
#### Примеры запросов
#### Запрос:
    curl -X PUT \
    http://176.113.83.93:8000/chats/1/mark_checked/ \
    -H 'Authorization: Token b704c9fc3655635646356ac2950269f352ea1139'
#### Ответ:
    Response code: 200
    Response body:
    {
    "id": 1,
    "chat_id": 286,
    "date_time": "2023-04-08T12:27:29.477137Z",
    "text": "Hot must thus effort walk everybody rest. Tv parent phone major politics usually.\nMyself reveal list.",
    "donor": {
        "id": 108,
        "first_name": "Alan",
        "last_name": "Guzman",
        "birth_date": "1995-07-24",
        "sex": "M",
        "avatar": "http://0.0.0.0:8000/media/static/img/default.jpg",
        "email": "warnold@example.com",
        "about_me": "Buy eight student view talk commercial. Control difference nor now.\nCommon church street activity imagine. Choose against name ability anything employee. Near like civil over.\nReally our clearly letter air police both. Professional consumer unit school suddenly American company myself. Make week send away rather.\nStep special between true owner eight than. Method out employee. Standard character when production other everybody. Course throw view budget.\nDinner blood million guess understand street.",
        "city": "Москва",
        "employment": "NE",
        "alcohol_attitude": "I",
        "smoking_attitude": "N",
        "sleep_time": "N",
        "personality_type": "M",
        "clean_habits": "C",
        "interests": [
            {
                "id": 2,
                "interest": "image"
            },
            {
                "id": 3,
                "interest": "son"
            },
            {
                "id": 5,
                "interest": "kitchen"
            },
            {
                "id": 7,
                "interest": "event"
            },
            {
                "id": 13,
                "interest": "themselves"
            },
            {
                "id": 15,
                "interest": "me"
            },
            {
                "id": 19,
                "interest": "whatever"
            },
            {
                "id": 23,
                "interest": "father"
            },
            {
                "id": 27,
                "interest": "present"
            }
        ]
    },
    "recipient": {
        "id": 185,
        "first_name": "Justin",
        "last_name": "Andrews",
        "birth_date": "2006-01-19",
        "sex": "M",
        "avatar": "http://0.0.0.0:8000/media/static/img/default.jpg",
        "email": "jessica03@example.net",
        "about_me": "Class represent painting term charge other break cover. Final why receive far economic. Let everyone although hotel air. Exactly over decade above under among.\nDraw nor outside remember car actually. On send tend. Country song force car sit candidate.\nWait against business character. Good certainly front add despite always material food. Together produce that what foreign stand. Spring significant similar issue.\nThis enjoy boy former PM task enter economic. Before catch around environment rock include entire. Example expect front prevent read woman current.\nSeek exist worker future share pattern. Feel seat property. Low but daughter fear newspaper money ahead.\nAmong material work wife read. Score reason reason how firm. Over why statement become.\nNatural black anything arrive go stay might.",
        "city": "Москва",
        "employment": "NE",
        "alcohol_attitude": "I",
        "smoking_attitude": "I",
        "sleep_time": "N",
        "personality_type": "I",
        "clean_habits": "D",
        "interests": [
            {
                "id": 1,
                "interest": "three"
            },
            {
                "id": 2,
                "interest": "image"
            },
            {
                "id": 9,
                "interest": "mention"
            },
            {
                "id": 10,
                "interest": "interview"
            },
            {
                "id": 14,
                "interest": "floor"
            },
            {
                "id": 17,
                "interest": "past"
            },
            {
                "id": 19,
                "interest": "whatever"
            },
            {
                "id": 20,
                "interest": "discover"
            },
            {
                "id": 21,
                "interest": "mother"
            },
            {
                "id": 24,
                "interest": "challenge"
            }
        ]
    },
    "is_checked": true
    }
#### Комментарий:
Число в url - id сообщения

### Получение списка городов
#### Примеры запросов
#### Запрос:
    curl -X GET \
    http://176.113.83.93:8000/cities/
#### Ответ:
    Response code: 200
    Response body:
    [
        {
            "id": 1,
            "city": "Москва"
        },
        {
            "id": 2,
            "city": "Санкт-Петербург"
        },
        {
            "id": 3,
            "city": "Новосибирск"
        },
        ...
    ]
### Подписка на пользователя
#### Комментарий:
user_id - id текущего пользователя,
follow_id - id пользователя, на которого делается подписка
#### Примеры запросов
#### Запрос:
    curl -X POST \
        http://176.113.83.93:8000/follow/?user_id=304&follow_id=3 \
        -H 'Authorization: Token b704c9fc3655635646356ac2950269f352ea1139'

#### Ответ:
    Response code: 201
    Response body:
    {}

### Отписка от пользователя
#### Комментарий:
user_id - id текущего пользователя,
follow_id - id пользователя, на которого делается подписка
#### Примеры запросов
#### Запрос:
    curl -X DELETE \
        http://176.113.83.93:8000/follow/?user_id=304&follow_id=3 \
        -H 'Authorization: Token b704c9fc3655635646356ac2950269f352ea1139'

#### Ответ:
    Response code: 201
    Response body:
    {}

### Получение списка пользователей, на которых подписан текущий пользователь
#### Комментарий:
user_id - id текущего пользователя,
#### Примеры запросов
#### Запрос:
    curl -X GET \
        http://176.113.83.93:8000/follow/?user_id=304 \
        -H 'Authorization: Token b704c9fc3655635646356ac2950269f352ea1139'

#### Ответ:
    Response code: 201
    Response body:
    [
    {
        {"id": 1,
        "following": {
            "id": 1,
            "first_name": "Barbara",
            "last_name": "Roberts",
            "birth_date": "2006-12-31",
            "sex": "M",
            "avatar": "http://0.0.0.0:8000/media/avatar/default_0.jpg",
            "email": "kyleblair@example.net",
            "about_me": "Almost wonder employee attorney. Theory type successful together.\nStudy modern miss dog Democrat quickly. Often late produce you true soldier. Food break onto friend.\nAdministration even relate head color. Staff beyond chair recently and off.\nQuite ago play paper office hospital have wonder. Painting create wife. Look road article quickly.\nPer structure attorney author feeling job. Mean always beyond write. Employee toward like total now.\nSmall citizen class morning. Others kind company likely.\nThemselves true power home price check real. Score from animal exactly drive well good. Pull opportunity throughout take car.\nSecurity stock ball organization recognize civil. Pm her then nothing increase.",
            "city": "Владикавказ",
            "employment": "S",
            "alcohol_attitude": "P",
            "smoking_attitude": "P",
            "sleep_time": "O",
            "personality_type": "M",
            "clean_habits": "D",
            "interests": [
                {
                    "id": 7,
                    "interest": "event"
                },
                {
                    "id": 11,
                    "interest": "why"
                },
                {
                    "id": 12,
                    "interest": "step"
                },
                {
                    "id": 20,
                    "interest": "discover"
                },
                {
                    "id": 23,
                    "interest": "father"
                },
                {
                    "id": 24,
                    "interest": "challenge"
                }
            ]
        }
    },
    {
        "id": 2,
        "following": {
            "id": 2,
            "first_name": "Monica",
            "last_name": "Thompson",
            "birth_date": "2004-02-27",
            "sex": "M",
            "avatar": "http://0.0.0.0:8000/media/avatar/default_4.jpg",
            "email": "nstewart@example.org",
            "about_me": "Fact catch even front happen behavior single along. Clearly word face house nature. Boy room value film tax.\nIdea foreign increase between training. Front something speech buy break marriage also.\nTurn phone heart window. Assume be seek article. Better news face.\nResearch describe base detail yourself one coach court. Ask tell reduce total. Sell cut market either political young something.",
            "city": "Тольятти",
            "employment": "NE",
            "alcohol_attitude": "I",
            "smoking_attitude": "P",
            "sleep_time": "N",
            "personality_type": "I",
            "clean_habits": "D",
            "interests": [
                {
                    "id": 10,
                    "interest": "interview"
                },
                {
                    "id": 11,
                    "interest": "why"
                },
                {
                    "id": 12,
                    "interest": "step"
                },
                {
                    "id": 15,
                    "interest": "me"
                },
                {
                    "id": 16,
                    "interest": "help"
                },
                {
                    "id": 18,
                    "interest": "wait"
                },
                {
                    "id": 20,
                    "interest": "discover"
                },
                {
                    "id": 22,
                    "interest": "chair"
                },
                {
                    "id": 23,
                    "interest": "father"
                },
                {
                    "id": 28,
                    "interest": "successful"
                }
            ]
        }
    }
    ]

### Проверка подписан ли текущий пользователь на другого пользователя
#### Комментарий:
user_id - id текущего пользователя,

follow_id - id пользователя, которого ищем в подписках
#### Примеры запросов
#### Запрос:
    curl -X GET \
        http://176.113.83.93:8000/follow/check_follower/?user_id=44&follow_id=2 \
        -H 'Authorization: Token b704c9fc3655635646356ac2950269f352ea1139'

#### Ответ:
    Response code: 200
#### Запрос:
    curl -X GET \
        http://176.113.83.93:8000/follow/check_follower/?user_id=44&follow_id=88888 \
        -H 'Authorization: Token b704c9fc3655635646356ac2950269f352ea1139'

#### Ответ:
    Response code: 404

### Получение списка объявлений, созданных текущим пользователем
#### Комментарий:
host_id - id текущего пользователя,
#### Примеры запросов
#### Запрос:
    curl -X GET \
        http://176.113.83.93:8000/housing/?host_id=1 \
        -H 'Authorization: Token b704c9fc3655635646356ac2950269f352ea1139'

#### Ответ:
    Response code: 201
    [
        {
            "id": 8,
            "month_price": 31264,
            "host": {
                "id": 1,
                ...
                ]
            },
            "description": "Month relate do must industry.\nEvery his American card these employee. Including suggest ball interview threat impact.\nHot read power green let. Pull work according director join weight. Sit show memory.\nSomeone less future only million. Machine cultural mouth view step eight.\nBoth especially call owner church over. Nothing benefit situation operation treat ability so simply.\nWish international blue animal popular. Among policy fine together local play finally read. Indeed own by clearly course common.\nStyle explain structure economic film get floor prepare.\nBody study few remain nearly. Dream music person technology suffer wear success. Daughter rule see board.\nGuess enough main team. Up hundred value skill eight.\nSchool nothing generation factor hot scene. Land understand your account near. Be anyone their write question.\nLittle choice social. Lead fast ability nearly.",
            "file_content": [
                {
                    "photo": "http://0.0.0.0:8000/media/housing/flat_default_0.jpg"
                },
                {
                    "photo": "http://0.0.0.0:8000/media/housing/flat_default_1.jpg"
                },
                {
                    "photo": "http://0.0.0.0:8000/media/housing/flat_default_2.jpg"
                },
                {
                    "photo": "http://0.0.0.0:8000/media/housing/flat_default_3.jpg"
                }
            ],
            "title": "Cold determine purpose history. Another special window forward.",
            "location": "50.75767 -1.5443 Lymington GB Europe/London",
            "bathrooms_count": 4,
            "bedrooms_count": 3,
            "housing_type": "DU",
            "room_attributes": [],
            "sharing_type": "P"
        }
    ]

### Изменение объявления
#### Комментарий:
id в url - id записи, которую изменяем,
#### Примеры запросов
#### Запрос:
    curl -X PUT \
        http://176.113.83.93:8000/housing/301/ \
        -H 'Authorization: Token b704c9fc3655635646356ac2950269f352ea1139'  \
        -F location='Astrakhan city' \
        -F title='cool apartment' \
        -F description='some apartment' \
        -F sharing_type=S \
        -F housing_type=F \
        -F file_content=@/home/rodion/Downloads/8405385.jpg \
        -F bedrooms_count=2 \
        -F month_price=6010 \
        -F bathrooms_count=2

#### Ответ:
    Response code: 201
    {
        "id": 301,
        "month_price": 6010,
        "host": {
            "id": 8,
            ...
            "interests": [
                ...
            ]
        },
        "description": "some apartment",
        "file_content": [
            {
                "photo": "http://0.0.0.0:8000/media/housing/2023/05/04/8405385.jpg"
            }
        ],
        "title": "cool apartment",
        "location": "Astrakhan city",
        "bathrooms_count": 2,
        "bedrooms_count": 2,
        "housing_type": "F",
        "room_attributes": [],
        "sharing_type": "S"
    }

### Удаление объявления
#### Комментарий:
id в url - id записи, которую удаляем
#### Примеры запросов
#### Запрос:
    curl -X DELETE \
        http://176.113.83.93:8000/housing/301/ \
        -H 'Authorization: Token b704c9fc3655635646356ac2950269f352ea1139' \
#### Ответ:
    Response code: 200

### Создание комментария
#### Пояснения:
author_id - id пользователя, который оставляет комментарий

receiver_id - id пользователя, о котором оставляют комментарий

is_anon - true при анонимном комментарии, false при публичном

**score choices** = [ 1, 2, 3, 4, 5 ]

#### Примеры запросов
#### Запрос:
    curl -X POST \
        http://176.113.83.93:8000/review/ \
        -H 'Authorization: Token b704c9fc3655635646356ac2950269f352ea1139' \
        -F author_id=402 \
        -F receiver_id=403 \
        -F score=2 \
        -F is_anon=false \
        -F comment='He is a very very good guy' 
#### Ответ:
    Response code: 201

### Получение комментариев о пользователе
#### Пояснения:
receiver_id - id пользователя, комментарии о котором хотим получить
#### Примеры запросов
#### Запрос:
    curl -X GET \
        http://176.113.83.93:8000/review/?receiver_id=403 \
        -H 'Authorization: Token b704c9fc3655635646356ac2950269f352ea1139'
#### Ответ:
    Response code: 200
    [{
        "id": 2,
        "score": 2,
        "author": {
            "id": 402,
            ...
        },
        "receiver": 403,
        "comment": "He is a very very good guy",
        "is_anon": false
    },
    ...
    ]

### Удаление комментария
#### Пояснения:
число в url - id комментария, который удаляем
#### Примеры запросов
#### Запрос:
    curl -X DELETE \
        http://176.113.83.93:8000/review/2/ \
        -H 'Authorization: Token b704c9fc3655635646356ac2950269f352ea1139'
#### Ответ:
    Response code: 200