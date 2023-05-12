import cfscrape
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure the Selenium webdriver
options = webdriver.ChromeOptions()
options.add_argument("--interactive")  # Run Chrome in headless mode
driver = webdriver.Chrome(options=options)

# Load the web page
url="https://www.klwines.com/Products?filters=sv2_NewProductFeedYN$eq$1$True$ProductFeed$!dflt-stock-instock!30$eq$(216)$True$ff-30-(216)--$!28$eq$(3)$True$ff-28-(3)--$or,27.or,48!90$eq$1$True$ff-90-1--$&limit=100&offset=0&orderBy=60%20asc,NewProductFeedDate%20desc"
driver.get(url)

# Wait for the CAPTCHA element to be visible
captcha_element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "captcha-element-id"))
)

# Solve the CAPTCHA manually or use third-party services

# Continue with scraping
# Extract the content or perform other scraping operations

# Create a Cloudflare scraper
scraper = cfscrape.create_scraper()

# Set custom headers
headers = {
    'User-Agent': 'Chrome/91.0.4472.124',
    'Referer': 'https://www.klwines.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # Add any other headers you need
}

# Make a request to the protected web page
#url = "https://example.com/protected_page"
response = scraper.get(url, headers=headers)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Perform scraping operations on the parsed HTML
# For example, extract all the links
links = soup.find_all("a")
for link in links:
    print(link.get("href"))

# Close the driver
driver.quit()

