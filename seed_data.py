import sqlite3

connection = sqlite3.connect("campusbridge.db")
cursor = connection.cursor()

# --- Vista Komanwel B already exists from earlier testing ---
# Remove the placeholder test review and replace it with the real one from the survey
cursor.execute("SELECT id FROM properties WHERE name = ?", ("Vista Komanwel B",))
vista_id = cursor.fetchone()[0]

cursor.execute("DELETE FROM reviews WHERE review_text = ?", ("Good location but slow WiFi.",))

cursor.execute(
    "INSERT INTO reviews (property_id, rating, review_text) VALUES (?, ?, ?)",
    (vista_id, 4, "Ease of access to LRT, but the building is old and not much option for food or groceries within walking distance.")
)

# --- Sasar Residence ---
cursor.execute("INSERT INTO properties (name, area, university) VALUES (?, ?, ?)", ("Sasar Residence", None, None))
sasar_id = cursor.lastrowid
cursor.execute(
    "INSERT INTO reviews (property_id, rating, review_text) VALUES (?, ?, ?)",
    (sasar_id, 3, "Near my university, but located in a populated area.")
)

# --- 8th & Stellar ---
cursor.execute("INSERT INTO properties (name, area, university) VALUES (?, ?, ?)", ("8th & Stellar", None, None))
stellar_id = cursor.lastrowid
cursor.execute(
    "INSERT INTO reviews (property_id, rating, review_text) VALUES (?, ?, ?)",
    (stellar_id, 5, "Liked it overall. If you have money, go for it.")
)

# --- Arte Subang West (two separate students, same property) ---
cursor.execute("INSERT INTO properties (name, area, university) VALUES (?, ?, ?)", ("Arte Subang West", "Subang", None))
arte_id = cursor.lastrowid
cursor.execute(
    "INSERT INTO reviews (property_id, rating, review_text) VALUES (?, ?, ?)",
    (arte_id, 2, "Looks great on Google, but not fully like that in reality. The swimming pool tiles are always broken, and a friend was injured and needed stitches. Management took the complaint but did nothing.")
)
cursor.execute(
    "INSERT INTO reviews (property_id, rating, review_text) VALUES (?, ?, ?)",
    (arte_id, 3, "Good amenities like swimming pool and gym, but my unit has bad cleanliness and the landlord isn't very responsive.")
)

# --- APU Hostel ---
cursor.execute("INSERT INTO properties (name, area, university) VALUES (?, ?, ?)", ("APU Hostel", None, "APU"))
apu_id = cursor.lastrowid
cursor.execute(
    "INSERT INTO reviews (property_id, rating, review_text) VALUES (?, ?, ?)",
    (apu_id, 3, "Very small space with high rental.")
)

# --- Bukit Rawang Putra ---
cursor.execute("INSERT INTO properties (name, area, university) VALUES (?, ?, ?)", ("Bukit Rawang Putra", "Rawang", None))
rawang_id = cursor.lastrowid
cursor.execute(
    "INSERT INTO reviews (property_id, rating, review_text) VALUES (?, ?, ?)",
    (rawang_id, 2, "Landlord pressured us to move out with little notice and kept raising the bill without any agreement, threatening to send men after us if we didn't leave. Later, a new agreement made us fully liable for the household after two years, and we felt forced to sign due to financial pressure and time constraints.")
)

connection.commit()
connection.close()

print("Real review data seeded successfully.")