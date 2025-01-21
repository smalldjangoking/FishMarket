def create_order(cleaned_data):
    ...

def order_preparation(cleaned_data):
    if cleaned_data.get("user_id", None) is None:
