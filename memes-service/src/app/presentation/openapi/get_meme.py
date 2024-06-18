EXAMPLE_GET_MEME_RESPONSE = {
    200: {
        'description': 'Successful Response',
        'content': {
            'application/json': {
                'example': {
                    'id': 'd7b62fbd-63d8-491e-ba08-12d8e403b54a',
                    'text': 'Какой-то мем',
                    'urlImage': 'http://localhost:9000/images/22d128f9-ea5b-4d26-b55f-fa3e10d74a2b.jpg'
                }
            }
        }
    },
    400: {
        'description': 'Bad Request',
        'content': {
            'application/json': {
                'example': {
                    'detail': 'Meme not found'
                }
            }
        }
    }
}
