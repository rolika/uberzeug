from typing import Iterable


class CliMenu():
    """Create and handle a simple command line menu."""
    def __init__(self,
                 menuitems:Iterable,
                 title="",
                 start_at:int=1) -> None:
        self._menuitems = menuitems  # items must have __str__ if not literals
        self._first = int(start_at)  # throws ValueError if not a correct int
        self._last = None
        self._title = title

    def _build(self) -> dict:
        return {self._last: item\
                for self._last, item in enumerate(self._menuitems, self._first)}

    def show(self) -> None:
        if self._title:
            print(self._title)
        for i, item in self._build().items():
            print(f"{i:>3}.)  {str(item)}")

    def listen(self):
        assert self._last
        while True:
            choice = input("Melyiket választod? ")
            try:
                choice = int(choice)
                if choice in range(self._first, self._last+1):
                    return choice - self._first
            except ValueError:
                pass
            print(f"{self._first} és {self._last} között kell választanod.")
