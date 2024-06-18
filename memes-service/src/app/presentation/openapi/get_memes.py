EXAMPLE_GET_MEMES_RESPONSE = {
    200: {
        'description': 'Successful Response',
        'content': {
            'application/json': {
                'example': {
                    'total': 14,
                    'limit': 2,
                    'offset': 0,
                    'memes': [
                        {
                            'id': 'd7b62fbd-63d8-491e-ba08-12d8e403b54a',
                            'text': 'Какой-то мем',
                            'urlImage': 'http://localhost:9000/images/22d128f9-ea5b-4d26-b55f-fa3e10d74a2b.jpg'
                        },
                        {
                            'id': '019f9fdb-7bf3-4e30-80ea-f730711bd462',
                            'text': 'Какой-то мем',
                            'urlImage': 'http://localhost:9000/images/22d128f9-ea5b-4d26-b55f-fa3e10d74a2b.jpg'
                        }
                    ]
                }
            }
        }
    }
}
