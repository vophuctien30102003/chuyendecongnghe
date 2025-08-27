class YearConverter:
    regex = '[0-9]{4}'
    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04d' % int(value)

class SlugWithUnderscoreConverter:
    regex = '[a-zA-Z0-9_-]+'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return str(value)
