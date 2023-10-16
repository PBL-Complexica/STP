

class User:
    def __init__(self, id=None, first_name=None, last_name=None, password_hash=None, birth_date=None,
                 phone_number=None, email=None, device_name=None, device_sn=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = password_hash
        self.birth_date = birth_date
        self.phone_number = phone_number
        self.email = email
        self.device_name = device_name
        self.device_sn = device_sn

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'
