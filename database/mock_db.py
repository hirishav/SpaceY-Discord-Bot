# In-memory mock database for Space Y
# WARNING: This resets every time the bot restarts.
# Used purely to demonstrate the command UI/UX in this stage.

import time

# users[user_id] = {
#     "coins": 0,
#     "xp": 0,
#     "inventory": {},
#     "cooldowns": {
#         "daily": 0,
#         "weekly": 0,
#         "farm": 0,
#         "hunt": 0,
#         "adventure": 0,
#         "training": 0,
#         "duel": 0,
#         "quest": 0
#     },
#     "progress": {
#        "horse_tier": 0
#     }
# }
users = {}

def get_user(user_id: int):
    if user_id not in users:
        users[user_id] = {
            "coins": 0,
            "xp": 0,
            "inventory": {},
            "cooldowns": {},
            "progress": {
                "horse_tier": 0
            }
        }
    return users[user_id]

def add_coins(user_id: int, amount: int):
    user = get_user(user_id)
    user["coins"] += amount
    return user["coins"]

def remove_coins(user_id: int, amount: int):
    user = get_user(user_id)
    if user["coins"] >= amount:
        user["coins"] -= amount
        return True
    return False

def get_coins(user_id: int):
    return get_user(user_id)["coins"]

def add_xp(user_id: int, amount: int):
    user = get_user(user_id)
    user["xp"] += amount
    return user["xp"]

def set_cooldown(user_id: int, command: str, seconds: int):
    user = get_user(user_id)
    user["cooldowns"][command] = time.time() + seconds

def get_cooldown(user_id: int, command: str):
    user = get_user(user_id)
    return user["cooldowns"].get(command, 0)

def is_on_cooldown(user_id: int, command: str):
    return get_cooldown(user_id, command) > time.time()

def add_item(user_id: int, item: str, amount: int = 1):
    user = get_user(user_id)
    user["inventory"][item] = user["inventory"].get(item, 0) + amount

def format_time_remaining(end_time):
    remaining = int(end_time - time.time())
    if remaining <= 0:
        return "Ready"
    
    hours, remainder = divmod(remaining, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0 or hours > 0:
        parts.append(f"{minutes}m")
    parts.append(f"{seconds}s")
    
    return " ".join(parts)
