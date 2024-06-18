EXAMPLE_DELETE_MEME_RESPONSE = {
    204: {
        'description': 'No content'
    },
    400: {
        'description': 'Bad Request',
        'content': {
            'application/json': {
                'examples': {
                    'Мем не найден': {
                        'value': {
                            'detail': 'Meme not found'
                        }
                    },
                    'Ошибка загрузки изображения': {
                        'value': {
                            'detail': 'Oops! Something went wrong'
                        }
                    },
                }
            }
        }
    }
}