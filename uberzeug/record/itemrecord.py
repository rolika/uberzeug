class ItemRecord():
    """Handles a single item."""

    def __init__(self, **kwargs) -> None:
        for arg, value in kwargs.items():
            setattr(self, arg, value)
    
    def __bool__(self) -> bool:
        try:
            return bool(self.name) and\
                   bool(self.unit) #and\
                   #bool(self.manufacturer)
        except AttributeError:
            return False


if __name__ == "__main__":
    item1 = ItemRecord(name="Thermofin F15", manufacturer="Bauder", unit="m2")
    item2 = ItemRecord(name="Thermoplan T15", manufacturer="Bauder")
    item3 = ItemRecord(name="Thermoplex P15", manufacturer="")
    if item1:
        print("This is true.")
    if not item2:
        print("This is false, no unit provided.")
    if not item3:
        print("This is false also, no manufacturer provided.")
