from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import time

# Initialize Selenium WebDriver (replace 'PATH_TO_YOUR_CHROMEDRIVER' with your own path)
driver = webdriver.Chrome()

# Penal 2023
# driver.get('https://www.legis.md/cautare/getResults?doc_id=138778&lang=ro')

# Constitutia 2023
driver.get('https://www.legis.md/cautare/getResults?doc_id=136130&lang=ro#')

# Civil 2023
# driver.get('https://www.legis.md/cautare/getResults?doc_id=136381&lang=ro#')

# Wait for the page to load
time.sleep(2)

# Get the HTML content from the page
html_content = driver.page_source

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Dictionary to store Articol as key and content as value
articol_list = []

# Initialize temporary variables
current_articol_name = None
current_articol_content = ""

# Iterate over all <p> tags in the HTML
for p_tag in soup.find_all('p'):
    # Check if the <p> tag contains a <strong> tag
    strong_tag = p_tag.find('strong')
    if strong_tag:
        # Check if the text contains "Articol"
        if "Articol" in strong_tag.get_text():
            # If we have already started collecting content, save the previous articol
            if current_articol_name:
                articol_list.append({
                    'name': current_articol_name,
                    'content': current_articol_content.strip()
                })

            # Start collecting new articol
            current_articol_name = strong_tag.get_text().strip()
            current_articol_content = ""
        else:
            # Append to existing articol content
            current_articol_content += p_tag.get_text() + " "
    else:
        # Append to existing articol content
        current_articol_content += p_tag.get_text() + " "

# Save the last articol
if current_articol_name:
    articol_list.append({
        'name': current_articol_name,
        'content': current_articol_content.strip()
    })

# Convert the list of dictionaries to JSON
json_string = json.dumps(articol_list, ensure_ascii=False, indent=4)

# Print or save the JSON string
print(json_string)

# Write to a file in the same directory
with open('./../DB/db_constitution.json', 'w', encoding='utf-8') as f:
    f.write(json_string)

# Close the driver
driver.quit()