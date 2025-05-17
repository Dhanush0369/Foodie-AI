from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pdfplumber
import re
import json
from typing import List, Dict
import time
import os

from selenium.webdriver.chrome.options import Options

# Setup download directory
download_dir = os.path.abspath("menus")
os.makedirs(download_dir, exist_ok=True)

# Chrome options for PDF download
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True,
})

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)

try:
    driver.get("https://www.tajhotels.com/en-in/hotels/taj-city-centre-gurugram/restaurants/thai-pavilion-gurugram")

    # Wait for the name element
    name_element = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-heading-l.css-gw9im6")
    ))
    menu_element = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-link-m.css-1phsdvn")
    ))
    contact_elements = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, ".MuiBox-root.css-7k5hf")
    ))
    location_element = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, ".MuiBox-root.css-idtzn5")
    ))

    restaurant_name = name_element.text
    phone_number = contact_elements[1].text
    location = location_element.text

    print("Name:", restaurant_name)
    print("Phone:", phone_number)
    print("Location:", location)

    # Scroll menu element into view and wait for any overlays to disappear
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", menu_element)
    time.sleep(2)  # Wait for scroll/animation

    # Try clicking, fallback to JS click if intercepted
    try:
        menu_element.click()
    except Exception as e:
        print(f"Normal click failed: {e}")
        driver.execute_script("arguments[0].click();", menu_element)

    # Wait for download to start (adjust as needed)
    time.sleep(5)

finally:
    driver.quit()


# PARSING THE MENU PDF AND STORING IN JSON FORMAT

# --- Vegetarian and Category Keywords ---
veg_keywords = [
    "tofu", "vegetable", "mushroom", "corn", "broccoli", "baby corn", "paneer",
    "spring roll", "phak", "greens", "jasmine rice"
]
category_keywords = {
    "SEAFOOD": ["prawn", "shrimp", "fish", "crab", "seafood", "john dory", "snapper"],
    "APPETIZER": ["salad", "satay", "cake", "spring roll", "dim sum"],
    "MEAT": ["chicken", "lamb", "duck", "pork", "moo", "kai"],
    "VEGETABLE": ["tofu", "phak", "vegetable", "corn", "greens", "mushroom", "broccoli"],
    "CURRY": ["curry", "gaeng", "massaman", "penang", "red curry", "green curry"],
    "DESSERT": ["souffle", "ice cream", "banana", "chocolate"],
    "NOODLE": ["noodle", "pad thai", "bamee", "mee", "rice tartlets"]
}

# --- PDF Extraction ---
def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# --- Menu Parsing ---
def parse_menu(raw_text: str) -> List[Dict]:
    raw_text = raw_text.replace('\n', ' ')
    raw_text = re.sub(r'\s+', ' ', raw_text)
    # Pattern: Name | Kcal, Weight gm | Price
    pattern = re.compile(
        r'(?P<name>[\w\s\'\-&\(\)]+?)\s*\|\s*(?P<calories>\d{2,5})\s*Kcal,\s*(?P<weight>\d{2,4})\s*gm\s*\|\s*(?P<price>\d{3,4})',
        re.IGNORECASE
    )
    matches = list(pattern.finditer(raw_text))
    menu = []
    for i, match in enumerate(matches):
        name = match.group("name").strip()
        calories = int(match.group("calories"))
        weight = int(match.group("weight"))
        price = int(match.group("price"))
        # Try to find a description between this item and the next
        if i < len(matches) - 1:
            desc_segment = raw_text[match.end():matches[i + 1].start()]
        else:
            desc_segment = raw_text[match.end():]
        desc_match = re.search(r'([A-Z][a-z].+?)(?=\s+[A-Z][\w\s]{2,40}\s*\|)', desc_segment)
        description = desc_match.group(1).strip() if desc_match else ""
        item = {
            "name": name,
            "calories": calories,
            "weight_g": weight,
            "description": description,
            "price": price
        }
        menu.append(item)
    return menu

# --- Cleaning and Enrichment ---
def clean_name(name: str) -> str:
    name = name.strip()
    parts = name.split()
    max_len = 6
    return ' '.join(parts[:max_len])

def guess_category(item):
    desc = item.get("description", "").lower()
    name = item.get("name", "").lower()
    for cat, keywords in category_keywords.items():
        if any(word in name or word in desc for word in keywords):
            return cat
    return "MAIN"

def is_veg(item):
    desc = item.get("description", "").lower()
    name = item.get("name", "").lower()
    return any(word in name or word in desc for word in veg_keywords)

def enrich_menu(menu: List[Dict]) -> List[Dict]:
    enriched = []
    for item in menu:
        # Clean name
        item["name"] = clean_name(item["name"])
        # Description fallback
        if not item.get("description"):
            item["description"] = "No description available"
        # Add metadata and fix keys
        enriched_item = {
            "restaurant_name": restaurant_name,
            "Phone": phone_number,
            "Location": location,
            "name": item["name"],
            "category": guess_category(item),
            "description": item.get("description", ""),
            "price": item["price"],
            "vegetarian": is_veg(item)
        }
        # Only add calories/weight_g if present and nonzero
        if "calories" in item and item["calories"]:
            enriched_item["calories"] = item["calories"]
        if "weight_g" in item and item.get("weight_g"):
            enriched_item["weight_g"] = item["weight_g"]
        elif "weight_g" not in item and "weight" in item and item["weight"]:
            enriched_item["weight_g"] = item["weight"]
        enriched.append(enriched_item)
    return enriched

# --- Save as JSON ---
def save_to_json(menu: List[Dict], output_path: str):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(menu, f, ensure_ascii=False, indent=2)

# --- Main ---
if __name__ == "__main__":
    pdf_path = "menus/thai-menu-2022.pdf"  # Adjust path as needed
    output_json = "data/thai_pavilion_final_menu.json"
    print("Extracting and cleaning...")
    raw_text = extract_text_from_pdf(pdf_path)
    menu_data = parse_menu(raw_text)
    enriched_menu = enrich_menu(menu_data)
    save_to_json(enriched_menu, output_json)
    print(f"Done. Structured data saved to {output_json} with {len(enriched_menu)} items.")

