user filtering example:

sex_field_choices = [
    ('M', 'Male'),
    ('F', 'Female')
]
attitude_choices = [
    ('P', 'Positive'),
    ('N', 'Negative'),
    ('I', 'Indifferent')
]
sleep_time_choices = [
    ('N', 'Night'),
    ('D', 'Day'),
    ('O', 'Occasionally')
]
personality_choices = [
    ('E', 'Extraverted'),
    ('I', 'Introverted'),
    ('M', 'Mixed')
]
clean_choices = [
    ('N', 'Neat'),
    ('D', 'It Depends'),
    ('C', 'Chaos')
]
employment_choices = [
    ('NE', 'Not Employed'),
    ('E', 'Employed'),
    ('S', 'Searching For Work')
]

Profile filtering example:

    Request:

    curl -X GET  http://127.0.0.1:8000/profile/?sex=M&employment=E&alcohol_attitude=N&
                 smoking_attitude=N&sleep_time=N&personality_type=E&clean_habits=N

    Response:

    [
    {
        "first_name": "Patricia",
        "last_name": "Scott",
        "birth_date": "2022-12-21",
        "sex": "F",
        "avatar": "http://127.0.0.1:8000/static/img/default.png",
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
    }
    ]

amount_score_choices = [
    (3, 3),
    (4, 4),
    (2, 2),
    (1, 1),
    (5, 5)
]
housing_type_choices = [
    ('F', 'Flat'),
    ('DU', 'Duplex'),
    ('H', 'House'),
    ('DO', 'Dorm')
]
sharing_type_choices = [
    ('P', 'Private'),
    ('S', 'Shared')
]

Housing filtering example:
    
    Request:

    curl -X GET  http://127.0.0.1:8000/housing/?month_price_from=40000&month_price_to=90000&
                 bedrooms_count=>3&bathrooms_count=2&housing_type=DO&sharing_type=S

    Response:

    [
    {
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
            ]
        },
        "description": "Simple happen beat offer rate half.\nGuess what edge",
        "bathrooms_count": 2,
        "bedrooms_count": 4,
        "housing_type": "F",
        "room_attributes": [],
        "sharing_type": "P"
    }
    ]
