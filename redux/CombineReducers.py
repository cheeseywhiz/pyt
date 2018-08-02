__all__ = 'CombineReducers',


class CombineReducers:
    @classmethod
    def _annotations(cls):
        annotations = {}

        for base in reversed(cls.mro()):
            annotations.update(getattr(base, '__annotations__', {}))

        return annotations

    @property
    def _type_hint_dict(self):
        get_type_hint = self._annotations().get
        return {
            field: (get_type_hint(field), value)
            for field, value in vars(self).items()
        }

    def reduce(self, action=None):
        new_dict = {
            field: type_hint.reduce(value, action)
            for field, (type_hint, value) in self._type_hint_dict.items()
        }

        new_data = type(self)(**new_dict)
        return self if self == new_data else new_data
