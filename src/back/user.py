

class User:
    def __init__(self, id, first_name, last_name, password_hash, birth_date, created_at):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = password_hash
        self.birth_date = birth_date
        self.created_at = created_at

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'
    
class UserPhone:
    def __init__(self, id, phone_number, created_at):
        self.id = id
        self.phone_number = phone_number
        self.created_at = created_at

    def __repr__(self):
        return f'<UserPhone {self.phone_number} {self.user_id}>'
    
class UserEmail:
    def __init__(self, id, email, created_at):
        self.id = id
        self.email = email
        self.created_at = created_at

    def __repr__(self):
        return f'<UserEmail {self.email} {self.user_id}>'
    
class UserDevice:
    def __init__(self, id, device_name, device_sn, created_at):
        self.id = id
        self.device_name = device_name
        self.device_sn = device_sn
        self.created_at = created_at

    def __repr__(self):
        return f'<UserDevice {self.device_id} {self.user_id}>'