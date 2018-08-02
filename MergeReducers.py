import dataclasses

__all__ = 'MergeReducers',


class MergeReducersMeta(type):
    def __new__(cls, name, bases, namespace):
        new_namespace = {
            '__annotations__': {},
        }
        reducers = {}

        for name_, value in namespace.items():
            if not isinstance(value, type):
                new_namespace[name_] = value
                continue

            reducer = value
            dataclass_fields = dataclasses.fields(reducer)
            field_names = [field.name for field in dataclass_fields]
            reducers[name_] = reducer, field_names

            for field in dataclass_fields:
                new_namespace[field.name] = field
                new_namespace['__annotations__'][field.name] = field.type

        self = super().__new__(cls, name, bases, new_namespace)
        self = dataclasses.dataclass(self, frozen=True)
        self.reducers = reducers
        return self


class MergeReducers(metaclass=MergeReducersMeta):
    def _dict_slice(self, keys):
        return {
            key: getattr(self, key)
            for key in keys
        }

    def reduce(self, action=None):
        data_slices = {
            name: reducer(**self._dict_slice(field_names))
            for name, (reducer, field_names) in self.reducers.items()
        }
        new_data_slices = {
            name: (data_slice, data_slice.reduce(action))
            for name, data_slice in data_slices.items()
        }

        if all(
                old_data_slice is new_data_slice
                for old_data_slice, new_data_slice in new_data_slices.values()
        ):
            return self

        new_data = {}

        for _, new_data_slice in new_data_slices.values():
            new_data.update(vars(new_data_slice))

        return type(self)(**new_data)
