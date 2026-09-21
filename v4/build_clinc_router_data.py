import json
import pandas as pd

# -----------------------------
# INTENTS WE WANT TO USE
# -----------------------------

LOCAL_INTENTS = {
    "are_you_a_bot",
    "calculator",
    "change_accent",
    "change_ai_name",
    "change_language",
    "change_speed",
    "change_user_name",
    "change_volume",
    "cook_time",
    "definition",
    "flip_coin",
    "fun_fact",
    "goodbye",
    "greeting",
    "how_old_are_you",
    "ingredient_substitution",
    "ingredients_list",
    "meaning_of_life",
    "measurement_conversion",
    "no",
    "repeat",
    "reset_settings",
    "roll_dice",
    "spelling",
    "tell_joke",
    "thank_you",
    "timer",
    "translate",
    "user_name",
    "what_are_your_hobbies",
    "what_can_i_ask_you",
    "what_is_your_name",
    "where_are_you_from",
    "whisper_mode",
    "who_do_you_work_for",
    "who_made_you",
    "yes",
}

ONLINE_INTENTS = {
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


# -----------------------------
# LOAD CLINC150
# -----------------------------

with open("data_full.json", "r", encoding="utf-8") as f:
    data = json.load(f)


rows = []

# Use only the official training split for now.
# Validation/test will remain untouched for later evaluation.
for item in data["train"]:

    query = item[0]
    intent = item[1]

    if intent in LOCAL_INTENTS:
        rows.append({
            "query": query,
            "label": "local"
        })

    elif intent in ONLINE_INTENTS:
        rows.append({
            "query": query,
            "label": "online"
        })


# -----------------------------
# CREATE DATAFRAME
# -----------------------------

df = pd.DataFrame(rows)

print("=" * 60)
print("CLINC150 ROUTER DATASET")
print("=" * 60)

print("\nTotal rows:", len(df))

print("\nClass distribution:")
print(df["label"].value_counts())

print("\nDuplicate queries:", df["query"].duplicated().sum())


# -----------------------------
# REMOVE EXACT DUPLICATES
# -----------------------------

df = df.drop_duplicates(subset=["query", "label"])

print("\nAfter removing exact duplicates:")
print("Total rows:", len(df))

print("\nClass distribution:")
print(df["label"].value_counts())


# -----------------------------
# SAVE
# -----------------------------

output_file = "clinc_router_data.csv"

df.to_csv(output_file, index=False)

print("\nSaved:", output_file)
print("=" * 60)