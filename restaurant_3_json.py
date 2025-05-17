import json

#MENU WAS IMAGE BASED, SO HAD TO CREATE THE MENU DATA MANUALLY

# Restaurant info from the menu images
restaurant_info = {
    "restaurant_name": "SardaarJi",
    "contact": "84 700 77000",
    "location": "Andheri-E, Bandra-W, Lokhandwala, Juhu, Powai, Nagpur"
}

menu_items = []

# SLIDERS / NAAN-TURNOVERS - Veg
veg_sliders = [
    "Paneer Makhanwala Slider",
    "Paneer Tikka Masala Slider",
    "Paneer Zaikydaar Slider",
    "Paneer Kadhai Slider",
    "Paneer Baghdadi slider",
    "Tawa Mushroom Slider",
    "Tawa Paneer Slider"
]
for name in veg_sliders:
    menu_items.append({
        "name": name,
        "description": "",
        "price": "179",
        "category": "SLIDERS / NAAN-TURNOVERS - Veg (Half)",
        **restaurant_info
    })
    menu_items.append({
        "name": name,
        "description": "",
        "price": "259",
        "category": "SLIDERS / NAAN-TURNOVERS - Veg (Full)",
        **restaurant_info
    })

# SLIDERS / NAAN-TURNOVERS - Non-Veg
nonveg_sliders = [
    ("Butter chicken Slider", "189", "279"),
    ("Chicken Tikka Masala Slider", "189", "279"),
    ("Chicken Bhunna Slider full", "189", "279"),
    ("Chicken Kadhai Slider", "189", "279"),
    ("Chicken Baghdadi Slider", "189", "279")
]
for name, half_price, full_price in nonveg_sliders:
    menu_items.append({
        "name": name,
        "description": "",
        "price": half_price,
        "category": "SLIDERS / NAAN-TURNOVERS - Non-Veg (Half)",
        **restaurant_info
    })
    menu_items.append({
        "name": name,
        "description": "",
        "price": full_price,
        "category": "SLIDERS / NAAN-TURNOVERS - Non-Veg (Full)",
        **restaurant_info
    })

# Mutton Bhunna Slider (only one price)
menu_items.append({
    "name": "Mutton Bhunna Slider",
    "description": "",
    "price": "298",
    "category": "SLIDERS / NAAN-TURNOVERS - Non-Veg",
    **restaurant_info
})

# ROLLS - Veg
veg_rolls = [
    ("Tandoori Aloo Roll", "149"),
    ("Paneer Makhanwala Roll", "169"),
    ("Paneer Zaikydaar Roll", "169"),
    ("Paneer Tikka Roll", "169"),
    ("Tawa Mushroom Roll", "169")
]
for name, price in veg_rolls:
    menu_items.append({
        "name": name,
        "description": "",
        "price": price,
        "category": "ROLLS - Veg",
        **restaurant_info
    })

# ROLLS - Non-Veg
nonveg_rolls = [
    "Butter Chicken Roll",
    "Chicken Tikka Roll",
    "Chicken Bhunna Roll",
    "Chicken Zaikedaar Roll"
]
for name in nonveg_rolls:
    menu_items.append({
        "name": name,
        "description": "",
        "price": "179",
        "category": "ROLLS - Non-Veg",
        **restaurant_info
    })

# Wheat option
menu_items.append({
    "name": "Wheat Roll (Extra)",
    "description": "",
    "price": "20",
    "category": "ROLLS - Wheat Option",
    **restaurant_info
})

# STARTERS - Veg
veg_starters = [
    ("Tandoori Aloo", "169"),
    ("Tandoori Mushroom", "219"),
    ("Veg Sheek Kebab", "239"),
    ("Afghani Mushroom", "259"),
    ("Achari Paneer Tikka", "269"),
    ("Lahori Paneer Tikka", "269"),
    ("Paneer Roulade", "298"),
    ("Paneer Chutney wala Tikka", "269"),
    ("Paneer Sufiana Tikka", "269"),
    ("Baby Corn Amritsari", "229"),
    ("Pahadi Paneer Tikka", "269")
]
for name, price in veg_starters:
    menu_items.append({
        "name": name,
        "description": "",
        "price": price,
        "category": "STARTERS - Veg",
        **restaurant_info
    })

# STARTERS - Non-Veg
nonveg_starters = [
    "Chicken Lahori Tikka",
    "Chicken Reshmi Tikka",
    "Chicken Malai Tikka",
    "Murg Kalimiri Kabab",
    "Classic Tandoori Chicken",
    "Achari Tandoori Chicken",
    "Pahadi Tandoori Chicken",
    "Kalimiri Tandoori Chicken",
    "Chicken Tikka Angara",
    "Chicken Lasooni Kebab",
    "Drums of Heaven Kebab",
    "Chicken Shammi Kebab",
    "Chicken Gilafi Sheekh",
    "Mutton Sheekh Kebab",
    "Rampur Mutton Skeekh",
    "Mouth Melting Ghosht Shammi Kebab",
    "Lucknowi Lamb Golati with Sirmali Roti",
    "Fish Amritsari Tikka",
    "Kalimiri Prawns",
    "Tandoori Garlic Prawns",
    "Hariyali Fresh Fish Tikka"
]
nonveg_starters_prices = [279, 289, 289, 289, 359, 379, 379, 379, 279, 279, 289, 319, 289, 379, 379, 398, 398, 298, 529, 529, 298]
for name, price in zip(nonveg_starters, nonveg_starters_prices):
    menu_items.append({
        "name": name,
        "description": "",
        "price": str(price),
        "category": "STARTERS - Non-Veg",
        **restaurant_info
    })

# BIRYANI - Veg
veg_biryani = [
    ("Veg Biryani", "259"),
    ("Veg dum Biryani", "269"),
    ("Paneer Tikka Biryani", "279"),
    ("Hyderabadi Veg Biryani", "279"),
    ("Tawa Pulao", "219"),
    ("Spinach Daal Khichadi", "198"),
    ("Jeera Rice", "129"),
    ("Steamed Basmati Rice", "99")
]
for name, price in veg_biryani:
    menu_items.append({
        "name": name,
        "description": "",
        "price": price,
        "category": "BIRYANI - Veg",
        **restaurant_info
    })

# BIRYANI - Non-Veg (Bone and Boneless)
nonveg_biryani = [
    ("Chicken Dum Biryani", "279", "298"),
    ("Butter Chicken Biryani", "-", "298"),
    ("Hyderabadi Biryani", "279", "298"),
    ("Chicken Tawa Pulao", "279", "298"),
    ("Mutton Biryani", "339", "-"),
    ("Prawns Biryani", "379", "-")
]
for name, bone_price, boneless_price in nonveg_biryani:
    if bone_price != "-":
        menu_items.append({
            "name": name,
            "description": "",
            "price": bone_price,
            "category": "BIRYANI - Non-Veg (Bone)",
            **restaurant_info
        })
    if boneless_price != "-":
        menu_items.append({
            "name": name,
            "description": "",
            "price": boneless_price,
            "category": "BIRYANI - Non-Veg (Boneless)",
            **restaurant_info
        })

# MAIN - COURSE (Gravies) - Veg
veg_main_course = [
    ("Veg Makhanwala", "249"),
    ("Paneer Makhanwala", "279"),
    ("Tandoori Paneer Tikka Khada Masala", "298"),
    ("Daal Tadka", "198"),
    ("Daal Fry", "198"),
    ("Daal Makhani", "219"),
    ("Veg Kadhai", "249"),
    ("Paneer Kadhai", "279"),
    ("Paneer Tikka masala", "289"),
    ("Paneer Baghdadi", "279"),
    ("Mushroom Do Pyaza", "269"),
    ("Tandoori Aloo Masala", "239"),
    ("Tawa Mushroom Gravy", "279"),
    ("Veg Kolhapuri", "279"),
    ("Burnt Garlic Palak Paneer", "279"),
    ("Baby Corn Mushroom Masala", "269"),
    ("Adraki Aloo", "209")
]
for name, price in veg_main_course:
    menu_items.append({
        "name": name,
        "description": "",
        "price": price,
        "category": "MAIN - COURSE (Gravies) - Veg",
        **restaurant_info
    })

# MAIN - COURSE (Gravies) - Non-Veg
nonveg_main_course = [
    ("Butter Chicken Boneless", "298"),
    ("Chicken Tikka Masala", "298"),
    ("Chicken Bunna", "289"),
    ("Chicken Kadhai", "298"),
    ("Chicken Nawabi", "298"),
    ("Chicken Baghdadi", "298"),
    ("Roghani Chicken Tangadi", "319"),
    ("Nimbu Chicken", "298"),
    ("Chicken Mughalai", "298"),
    ("Chicken Peshwari", "298"),
    ("Gosht Khada masala", "349"),
    ("Methi Mutton", "349"),
    ("Mutton Roghan", "349"),
    ("Josh/Masala/Bhunna/Kadhai/Handi", "349"),
    ("Fish Goan Curry", "329"),
    ("Fish Tikka Masala", "349")
]
for name, price in nonveg_main_course:
    menu_items.append({
        "name": name,
        "description": "",
        "price": price,
        "category": "MAIN - COURSE (Gravies) - Non-Veg",
        **restaurant_info
    })

# MOMOS - Veg
veg_momos = [
    ("Veg Steam Momos", "139"),
    ("Veg Tandoori Momos", "159"),
    ("Veg Schezwan Momos", "169")
]
for name, price in veg_momos:
    menu_items.append({
        "name": name,
        "description": "",
        "price": price,
        "category": "MOMOS - Veg",
        **restaurant_info
    })

# MOMOS - Non-Veg
nonveg_momos = [
    ("Chicken Steam Momos", "149"),
    ("Chicken Tandoori Momos", "169"),
    ("Chicken Schezwan Momos", "179")
]
for name, price in nonveg_momos:
    menu_items.append({
        "name": name,
        "description": "",
        "price": price,
        "category": "MOMOS - Non-Veg",
        **restaurant_info
    })

# BREADS
breads = [
    ("Tandoori Roti", "29"),
    ("Butter Tandoori Roti", "39"),
    ("Plain Paratha", "39"),
    ("Lachcha Paratha (Plain)", "49"),
    ("Lachcha Paratha (Ajwain)", "59"),
    ("Lachcha Paratha (Pudina)", "59"),
    ("Lachcha Paratha (Methi)", "59"),
    ("Alloo Paratha", "109"),
    ("Paneer Paratha", "119"),
    ("Cheese Filling Naan", "79"),
    ("Cheese Paratha", "59"),
    ("Plain Naan", "39"),
    ("Butter Naan", "49"),
    ("Cheese Naan", "59"),
    ("Garlic Naan", "59"),
    ("Kulcha Plain", "39"),
    ("Kulcha Onion", "49"),
    ("Kulcha Masala", "49"),
    ("Kulcha Garlic", "49")
]
for name, price in breads:
    menu_items.append({
        "name": name,
        "description": "",
        "price": price,
        "category": "BREADS",
        **restaurant_info
    })

# Save to JSON
with open("data/sardaarji_full_menu.json", "w", encoding="utf-8") as f:
    json.dump(menu_items, f, indent=2, ensure_ascii=False)

print(f"Extracted {len(menu_items)} menu items. Data saved to sardaarji_full_menu.json")
