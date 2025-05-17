# Foodie-AI   
Web-Scraping ➜ JSON Knowledge Base ➜ FAISS ➜ Falcon-7B Chatbot (Streamlit UI)

A full-stack Generative-AI demo that lets users ask natural-language questions about real restaurant menus and instantly receive accurate, contextual answers.

---

## Key Features
| Layer | Tech | Highlights |
|-------|------|------------|
| Web scraping | **Selenium** | • Headless Chrome<br>• Downloads PDF menus automatically<br>• Extracts *name, location, contact* from page DOM |
| Parsing | **pdfplumber**, `re` | • Parses every menu page-by-page<br>• Cleans text, normalises rupee symbols & units<br>• Saves one JSON record *per dish* (schema below) |
| Vector Embedding | **all-MiniLM-L6-v2** + **FAISS** | • 384-dimensional embeddings (1 JSON = 1 vector)<br>• Mapped metadata for fast filtering (by restaurant / category) |
| LLM & RAG | **mistralai/Mistral-7B-Instruct-v0.3** | • Retrieval Augmented Generation pipeline<br>• Caches conversation state in Streamlit session |
| UI | **Streamlit** | • Chat-style interface with Markdown rendering<br> |

---

##  JSON Schema

```jsonc
{
  "name": "CHICKEN TIKKA BUTTER MASALA",
  "description": "TRADITIONAL CHICKEN TIKKA PCS COOKED WITH THICK SPICY AND BUTTER GRAVY",
  "price": "499",
  "category": "Veg Main Course",
  "restaurant_name": "HERITAGE",
  "contact": "call us 9311442255/77/99",
  "location": "sco 55 old judicial complex, Civil lines mor chowk gurgaon, 122001"
}
```

## Directory Info
```bash
chatbot_images/    # contains conversation images
data/              # menus items stored in json
menus/             # menu pdfs acquired through webscraping
```

---

## Conversation Images
### Menu Queries
![CTM serving restaurants](chatbot_images/CTM_menu.png)
![Desert options in a Restaurant](chatbot_images/dessert.png)
![Mutton dishes accross Restaurants](chatbot_images/mutton_menu.png)

### Price Queries
![Naan prices ](chatbot_images/naan_prices.png)
![Kadhai paneer prices](chatbot_images/kadhai_paneer.png)

### Location And contact Queries
![Heritage Location](chatbot_images/heritage_add.png)
![SaardarJI Location ](chatbot_images/saardarJi_add.png)

### Taste Queries
![Spicy Dishes](chatbot_images/spicy.png)