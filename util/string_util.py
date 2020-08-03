
class StringUtil:
    @classmethod
    def snake_to_camel(cls, snake_str):
        components = snake_str.split('_')
        return components[0].title() + ''.join(x.title() for x in components[1:])
