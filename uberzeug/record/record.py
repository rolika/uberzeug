class Record():
    """Base class for all records.
    translate_attributes:   a dictionary of key-value pairs, where values become
        attribute-names. If not provided, the keys of kwargs will be used.
    kwargs: key-value pairs holding the data"""
    def __init__(self, translate_attributes=None, **kwargs) -> None:
        for arg, value in kwargs.items():
            setattr(self, translate_attributes.get(arg, arg), value)

    def __str__(self) -> str:
        raise NotImplementedError