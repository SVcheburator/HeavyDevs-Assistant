class Address(Field):
    def __init__(self, city=None, street=None, house=None, apartment=None):
        self.city = city
        self.street = street
        self.house = house
        self.apartment = apartment
    
    def __str__(self):
        address_parts = [part for part in [self.city, self.street, self.house, self.apartment] if part]
        return ', '.join(address_parts)
