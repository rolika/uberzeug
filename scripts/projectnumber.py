import re


PROJECTNUMBER_PATTERN = r"(?P<year>\d{2})[/ _-](?P<serial>\d{1,3})"
MIN_YEAR = 0
MAX_YEAR = 99
MIN_SERIAL = 0
MAX_SERIAL = 999


class Projectnumber():
    """ Class for handling projectnumbers.
    A "legal" projectnumber looks like year/serial, where year is
    represented with two digits, and serial with one to three digits.
    Example: 24/1, 24/12, 24/123. In our case there are no more than 500
    projects in a year, so three digits leave place for growing.
    The 0 serial isn't allowed, but it can be used to bypass things.
    In practice, the projectnumber can be anything, two and one to three digits
    separated by a slash, underscore, space or hyphen.
    For a filename we use the format year_serial, where year is two digits,
    serial is always three digits with leading zeroes. This is also beneficial
    for ordering."""
    def __init__(self, text:str) -> None:
        """At initialization we try tor extract a valid projectnumber."""
        self.year = -1
        self.serial = -1
        regex = re.compile(PROJECTNUMBER_PATTERN)
        extract = regex.search(text)
        if extract:
            self.year = int(extract["year"])
            self.serial = int(extract["serial"])
    
    def __bool__(self) -> bool:
        """Return true if this is a valid projectnumber."""
        return (MIN_YEAR <= self.year <= MAX_YEAR) and\
               (MIN_SERIAL <= self.serial <= MAX_SERIAL)
    
    def __str__(self) -> str:
        """Projectnumber as a string is the filename-format."""
        assert bool(self)
        return "{}_{:0>3}".format(self.year, self.serial)
    
    def __eq__(self, other:object) -> bool:
        """Two projectnumbers are equal if both year and serial are equal."""
        return (self.year == other.year) and (self.serial == other.serial)
    
    @property
    def legal(self) -> str:
        """This is the human readable legal form."""
        assert bool(self)
        return "{}/{}".format(self.year, self.serial)


if __name__ == "__main__":
    one = Projectnumber("Some Folder Name 24 2")
    two = Projectnumber("24_002")
    print(one, two)
