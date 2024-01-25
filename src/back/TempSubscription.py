class TempSubscription:
    def __init__(
        self,
        user_id: str,
        subscription_id: str,
        subscription_type_name: str,
        generation_time: str,
        valid_from: str,
    ):
        self.user_id = user_id
        self.subscription_id = subscription_id
        self.subscription_type_name = subscription_type_name
        self.generation_time = generation_time
        self.valid_from = valid_from
    
    def get_subscription_data(self):
        return {
            "user_id": self.user_id,
            "subscription_id": self.subscription_id,
            "subscription_type_name": self.subscription_type_name,
            "generation_time": self.generation_time,
            "valid_from": self.valid_from,
        }
