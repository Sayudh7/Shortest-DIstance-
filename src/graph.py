# Nepal cities graph
# Each city: (longitude, latitude) — real GPS coordinates

cities = {
    # Central
    "Kathmandu":     (85.3240, 27.7172),
    "Hetauda":       (85.0333, 27.4167),
    "Bharatpur":     (84.4333, 27.6833),

    # Western
    "Pokhara":       (83.9856, 28.2096),
    "Butwal":        (83.4487, 27.6966),
    "Nepalgunj":     (81.6159, 28.0503),
    "Dhangadhi":     (80.5833, 28.6833),
    "Bhairahawa":    (83.4548, 27.5057),
    "Baglung":       (83.5833, 28.2667),
    "Beni":          (83.5167, 28.3500),
    "Damauli":       (84.2833, 27.9667),
    "Tulsipur":      (82.2833, 28.1167),
    "Dang":          (82.3000, 27.8500),

    # Eastern
    "Biratnagar":    (87.2800, 26.4525),
    "Janakpur":      (85.9240, 26.7288),
    "Dharan":        (87.2833, 26.8167),
    "Itahari":       (87.2667, 26.6667),
    "Ilam":          (87.9167, 26.9167),
    "Birtamod":      (87.7667, 26.6500),
    "Damak":         (87.6833, 26.6667),

    # Southern (Terai)
    "Birgunj":       (84.8744, 27.0104),
    "Simara":        (84.9800, 27.1600),
    "Narayanghat":   (84.4333, 27.7000),
    "Gaur":          (85.2833, 26.7667),

    # Far West
    "Mahendranagar": (80.1833, 28.9667),
    "Tikapur":       (81.1167, 28.5167),
}

roads = [
    # --- Kathmandu connections ---
    ("Kathmandu",   "Pokhara",      200),
    ("Kathmandu",   "Birgunj",      145),
    ("Kathmandu",   "Hetauda",       75),
    ("Kathmandu",   "Janakpur",     220),
    ("Kathmandu",   "Bharatpur",    145),
    ("Kathmandu",   "Simara",       130),
    ("Kathmandu",   "Biratnagar",   465),
    ("Kathmandu",   "Dharan",       400),

    # --- Central ---
    ("Hetauda",     "Birgunj",       55),
    ("Hetauda",     "Janakpur",     150),
    ("Hetauda",     "Narayanghat",  100),
    ("Bharatpur",   "Narayanghat",   10),
    ("Bharatpur",   "Birgunj",       75),
    ("Simara",      "Birgunj",       25),
    ("Simara",      "Gaur",          80),
    ("Narayanghat", "Butwal",        95),

    # --- Western ---
    ("Pokhara",     "Butwal",        95),
    ("Pokhara",     "Baglung",       72),
    ("Pokhara",     "Damauli",       60),
    ("Pokhara",     "Beni",          90),
    ("Baglung",     "Beni",          35),
    ("Damauli",     "Bharatpur",     55),
    ("Butwal",      "Bhairahawa",    10),
    ("Butwal",      "Nepalgunj",    175),
    ("Bhairahawa",  "Nepalgunj",    170),
    ("Nepalgunj",   "Tulsipur",      35),
    ("Nepalgunj",   "Dhangadhi",    170),
    ("Tulsipur",    "Dhangadhi",    145),
    ("Dhangadhi",   "Tikapur",       45),
    ("Tikapur",     "Mahendranagar", 80),
    ("Dhangadhi",   "Mahendranagar", 90),
    ("Dang",        "Nepalgunj",    110),
    ("Dang",        "Butwal",       120),
    ("Dang",        "Tulsipur",      75),
    ("Dang",        "Bhairahawa",   130),
    ("Dang",        "Pokhara",      210),

    # --- Eastern ---
    ("Janakpur",    "Gaur",         110),
    ("Janakpur",    "Biratnagar",   260),
    ("Janakpur",    "Itahari",      240),
    ("Biratnagar",  "Itahari",       15),
    ("Biratnagar",  "Dharan",        50),
    ("Biratnagar",  "Birtamod",      30),
    ("Itahari",     "Dharan",        13),
    ("Itahari",     "Damak",         25),
    ("Dharan",      "Ilam",          80),
    ("Birtamod",    "Ilam",          40),
    ("Birtamod",    "Damak",         15),
    ("Damak",       "Ilam",          45),
]