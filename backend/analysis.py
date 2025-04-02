fake_post_data = [
    {"day": "Monday", "hour": 14, "engagement": 120},
    {"day": "Tuesday", "hour": 18, "engagement": 200},
    {"day": "Wednesday", "hour": 9, "engagement": 80},
]

def best_posting_time():
    return max(fake_post_data, key=lambda x: x["engagement"])
