from Database import Database


db = Database()


def main():
    db.register(
        first_name="John",
        last_name="Doe",
        password="test000000",
        email_address="john.doe@mail.com",
        phone_number="+37379000000",
        device_name="SM-54A6",
        birth_date=None
    )
    db.register(
        first_name="Jean",
        last_name="Dae",
        password="test000001",
        email_address="jean.dae@mail.com",
        phone_number="+37379000001",
        device_name="SM-5200",
        birth_date=None
    )
    db.register(
        first_name="Stephen",
        last_name="King",
        password="test000010",
        email_address="stephen.king@mail.com",
        phone_number="+37379000010",
        device_name="iPhone 12 Pro Max",
        birth_date=None
    )
    db.register(
        first_name="Ramona",
        last_name="Flowers",
        password="test000011",
        email_address="ramona.flowers@mail.com",
        phone_number="+37379000011",
        device_name="A689992",
        birth_date=None
    )

    db.buy_subscription(
        user_id=1,
        subscription_type='G-1'
    )
    db.buy_subscription(
        user_id=2,
        subscription_type='G-6'
    )
    db.buy_subscription(
        user_id=3,
        subscription_type='G-1'
    )


if __name__ == '__main__':
    main()
