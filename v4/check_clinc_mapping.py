import json
import random

with open("data_full.json", "r", encoding="utf-8") as f:
    data = json.load(f)

LOCAL = {
    "alarm",
    "are_you_a_bot",
    "calculator",
    "calendar",
    "change_accent",
    "change_ai_name",
    "change_language",
    "change_speed",
    "change_user_name",
    "change_volume",
    "cook_time",
    "definition",
    "flip_coin",
    "food_last",
    "fun_fact",
    "goodbye",
    "greeting",
    "how_old_are_you",
    "ingredient_substitution",
    "ingredients_list",
    "maybe",
    "meaning_of_life",
    "measurement_conversion",
    "next_song",
    "no",
    "recipe",
    "repeat",
    "reset_settings",
    "roll_dice",
    "spelling",
    "tell_joke",
    "thank_you",
    "time",
    "timer",
    "todo_list",
    "todo_list_update",
    "translate",
    "user_name",
    "what_are_your_hobbies",
    "what_can_i_ask_you",
    "what_is_your_name",
    "what_song",
    "where_are_you_from",
    "whisper_mode",
    "who_do_you_work_for",
    "who_made_you",
    "yes",
}

ONLINE = {
    "accept_reservations",
    "application_status",
    "book_flight",
    "book_hotel",
    "car_rental",
    "current_location",
    "directions",
    "exchange_rate",
    "flight_status",
    "gas",
    "gas_type",
    "how_busy",
    "international_visa",
    "lost_luggage",
    "restaurant_reviews",
    "restaurant_suggestion",
    "traffic",
    "travel_alert",
    "travel_notification",
    "travel_suggestion",
    "uber",
    "weather",
}

queries = {}

for query, intent in data["train"]:
    queries.setdefault(intent, []).append(query)

print("=" * 80)
print("CLINC150 MAPPING CHECK")
print("=" * 80)

for label, intents in [
    ("LOCAL", sorted(LOCAL)),
    ("ONLINE", sorted(ONLINE)),
]:
    print(f"\n\n{'=' * 80}")
    print(f"{label} INTENTS")
    print(f"{'=' * 80}")

    for intent in intents:
        print(f"\n[{intent}]")

        samples = queries.get(intent, [])

        random.seed(42)
        samples = random.sample(samples, min(10, len(samples)))

        for q in samples:
            print(f"  - {q}")