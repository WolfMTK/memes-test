class MemeException(Exception):
    pass


class InvalidFileExtension(MemeException):
    def __str__(self) -> str:
        return ('Invalid file extension.'
                ' Upload a file with `jpeg`, `jpg`, `png` extension')


class NotFoundURLException(MemeException):
    pass


class MemeNotFoundException(MemeException):
    def __str__(self) -> str:
        return 'Meme not found'
