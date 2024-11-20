def generate_private_chat_id(user1_id, user2_id) -> str:
    return f"{min(user1_id, user2_id)}_{max(user1_id, user2_id)}"
