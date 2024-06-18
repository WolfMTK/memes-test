EXAMPLE_CREATE_MEME_RESPONSE = {
    200: {
        'description': 'Successful Response',
        'content': {
            'application/json': {
                'example': {
                    'id': 'ba394529-3dcd-4a46-9534-895b5a0cbf3b',
                }
            }
        }
    },
    400: {
        'description': 'Bad Request',
        'content': {
            'application/json': {
                'examples': {
                    'Ошибка загрузки изображения': {
                        'value': {
                            'detail': 'Oops! Something went wrong'
                        }
                    },
                    'Неверный формат файла': {
                        'value': {
                            'detail': ('Invalid file extension. Upload a '
                                       'file with `jpeg`, `jpg`, '
                                       '`png` extension')
                        }
                    }
                }
            }
        }
    }
}
