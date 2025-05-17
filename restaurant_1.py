import os
import re
import json
import time
import pdfplumber
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Setup directories
download_dir = os.path.abspath("menus")
os.makedirs(download_dir, exist_ok=True)

data_dir = os.path.abspath("data")
os.makedirs(data_dir, exist_ok=True)

# Configure Chrome for PDF download
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True,
})
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://www.heritagegurgaon.in")
    
    # Click the "Contact" section to extract details
    contact_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#contact']")))
    contact_link.click()
    
    contact_elements = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//p[img[@class='contact-icon-img']]")
    ))

    # Extract restaurant info
    restaurant_name = "HERITAGE"
    phone_number = contact_elements[1].text
    location = contact_elements[2].text

    print("Phone:", phone_number)
    print("Location:", location)
    
    
    menu_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#menu']")))
    menu_link.click()
    
    menu_element = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'menu final.pdf')]")))


    driver.execute_script("arguments[0].scrollIntoView(true);", menu_element)
    time.sleep(1) 

    # Use JS to click to avoid intercepts
    driver.execute_script("arguments[0].click();", menu_element)


    # Wait for the file to be downloaded completely
    menu_path = os.path.join(download_dir, "menu final.pdf")
    timeout = 30
    elapsed = 0
    while not os.path.exists(menu_path):
        time.sleep(1)
        elapsed += 1
        if elapsed >= timeout:
            raise TimeoutError("❌ PDF download timed out!")

    print("PDF downloaded at:", menu_path)

finally:
    driver.quit()
    
# PARSING THE MENU PDF AND STORING AS JSON

# Define category aliases and parser helpers
CATEGORY_ALIASES = {
    "soups": "Soups", "beverages": "Beverages", "mocktails": "Mocktails", "shakes": "Shakes",
    "juices": "Juices", "veg starter": "Veg Starter", "non-veg starter": "Non-Veg Starter",
    "quick snacks": "Quick Snacks", "veg main course": "Veg Main Course",
    "non-veg main course": "Non-Veg Main Course", "rice": "Rice", "biryani": "Biryani",
    "non-veg biryani": "Non-Veg Biryani", "combo meals": "Combo Meals", "dessert": "Dessert",
    "raita": "Raita", "salad": "Salad", "breads": "Breads", "momos": "Momos",
    "chinese": "Chinese", "veg starter (chinese)": "Veg Starter (Chinese)",
    "non-veg starter (chinese)": "Non-Veg Starter (Chinese)",
    "non-veg main course (from oriental)": "Non-Veg Main Course (Oriental)",
    "veg main course (from oriental)": "Veg Main Course (Oriental)", "rice & noodles": "Rice & Noodles"
}

def clean_category(line):
    line = line.strip().lower()
    for key in CATEGORY_ALIASES:
        if key in line:
            return CATEGORY_ALIASES[key]
    return None

# Parse the PDF into structured menu items
price_pattern = re.compile(r"(.+?)\s+(\d{2,4}(?:/\d{2,4})?)$")
menu = []
current_category = None
last_item = None

with pdfplumber.open(menu_path) as pdf:
    for page in pdf.pages:
        lines = page.extract_text().split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            category = clean_category(line)
            if category:
                current_category = category
                continue

            match = price_pattern.match(line)
            if match:
                item_name = match.group(1).strip(". ")
                price = match.group(2)
                menu.append({
                    "name": item_name,
                    "description": "",
                    "price": price,
                    "category": current_category,
                    "restaurant_name": restaurant_name,
                    "contact": phone_number,
                    "location": location
                })
                last_item = menu[-1]
            else:
                if last_item:
                    if last_item["description"]:
                        last_item["description"] += " " + line
                    else:
                        last_item["description"] = line

#  Save output
output_path = os.path.join(data_dir, "heritage_menu_info.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(menu, f, indent=2, ensure_ascii=False)

print(f"Final menu with restaurant info saved to {output_path}")
