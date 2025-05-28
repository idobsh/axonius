class Vacation:
    def __init__(
        self,
        location: str,
        checkin_date: str,
        checkout_date: str,
        adults: str,
        children: str,
    ):
        self._location = location
        self._checkin = checkin_date
        self._checkout = checkout_date
        self._adults = adults
        self._children = children

    @property
    def location(self):
        return self._location

    @property
    def adults(self):
        return self._adults

    @property
    def children(self):
        return self._children

    @property
    def num_of_guests(self):
        return int(self._adults) + int(self._children)

    @property
    def checkin(self):
        return self._checkin

    @property
    def checkout(self):
        return self._checkout

    # def get_dates(self):
    #     return self._checkin, self._checkout

    def to_dict(self):
        return {
            "location": self._location,
            "checkin": self._checkin,
            "checkout": self._checkout,
            "adults": self._adults,
            "children": self._children,
        }
