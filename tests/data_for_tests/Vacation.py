class Vacation():
    def __init__(self, location:str, checkin_date:str, checkout_date:str, adults:int, children:int):
        self._location = location
        self._checkin = checkin_date
        self._checkout = checkout_date
        self._adults = adults
        self._children = children
        self._num_of_guests = adults+children

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
        return self._num_of_guests
    
    def get_dates(self):
        return self._checkin, self._checkout
    
