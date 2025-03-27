from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import csv

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

# Initialize WebDriver
print("🚀 Starting WebDriver...", flush=True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()  # Force full-screen to load all content

# Daraz Product URL
url = "https://www.daraz.pk/products/16-5-i584925286-s3128968807.html"
print(f"🔗 Opening Daraz product page: {url}", flush=True)
driver.get(url)

# Wait for page to load completely
time.sleep(5)

# Create a list to store extracted data
review_data = []


# Function to extract reviews from a single page
def extract_reviews():
    # **Lazy Loading Fix**: Scroll multiple times to ensure all reviews load
    last_height = (driver.execute_script("return document.documentElement.scrollHeight") / 3)
    for _ in range(6):  # Scroll down multiple times
        driver.execute_script(f"window.scrollTo(0, {last_height});")
        time.sleep(2)

    # Wait for reviews to be present
    try:
        item_review = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "item"))
        )

    except:
        print("⚠️ Warning: No reviews loaded yet. Trying again...", flush=True)

    # Parse page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find all review containers
    reviews = soup.find_all("div", class_="item")

    if not reviews:
        print("❌ No reviews found on this page. Stopping...", flush=True)
        return False  # Stop pagination when no new reviews are found

    print(f"✅ Found {len(reviews)} reviews on this page.", flush=True)

    for review in reviews:
        try:
            # Reviewer Name
            reviewer_tag = review.find("div", class_="middle")
            reviewer = reviewer_tag.find("span").text.strip() if reviewer_tag else "Unknown"

            # Verification Status
            verification_tag = review.find("span", class_="verify")
            verification_status = verification_tag.text.strip() if verification_tag else "Not Verified"

            # Review Date
            review_date_tag = review.find("span", class_="title right")
            review_date = review_date_tag.text.strip() if review_date_tag else "Unknown"

            # Review Content
            content_tag = review.find("div", class_="content")
            content = content_tag.text.strip() if content_tag else "No Content"

            # Star Rating (Counting Stars)
            star_rating = len(review.find_all("img", class_="star"))

            # Product Details
            product_details_tag = review.find("div", class_="skuInfo")
            product_details = product_details_tag.text.strip() if product_details_tag else "Not Available"

            # Number of Likes
            likes_tag = review.find("span", class_="left-content").find_next("span")
            likes = likes_tag.text.strip() if likes_tag else "0"

            # Image URLs
            images = review.find_all("div", class_="image")
            image_urls = [img["style"].split('url("')[1].split('")')[0] for img in images] if images else []

            # Append data to the list
            review_data.append([
                reviewer, verification_status, review_date, content, star_rating, product_details, likes,
                ", ".join(image_urls)
            ])

        except Exception as e:
            print(f"⚠️ Skipping review due to error: {e}", flush=True)

    return True  # Continue pagination


# Function to navigate through pages and extract reviews
def scrape_all_pages():
    page = 1
    while True:
        print(f"🔄 Scraping page {page}...", flush=True)
        has_reviews = extract_reviews()

        # Stop if no reviews are found on the current page
        if not has_reviews:
            break

        # Pagination Fix: Correctly find and click the next button
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button.next-btn.next-btn-normal.next-btn-medium.next-pagination-item.next"))
            )

            # Stop if the "Next" button is disabled (check the disabled attribute)
            if next_button.get_attribute("disabled") is not None:
                print("✅ Reached the last page. Stopping...", flush=True)
                break

            next_button.click()
            time.sleep(10)  # Wait for the next page to load
            page += 1
        except Exception as e:
            print("🚫 No more pages found or error in pagination. Stopping...", flush=True)
            break


# Start scraping
scrape_all_pages()

# Close the driver
driver.quit()

# Save data to CSV file
csv_filename = "Daraz_Reviews_LazyLoaded_Fixed.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(
        ["Reviewer Name", "Verification Status", "Review Date", "Review Content", "Star Rating", "Product Details",
         "Number of Likes", "Image URLs"])
    writer.writerows(review_data)

# Confirm success
print(f"✅ Daraz product reviews successfully saved to {csv_filename}", flush=True)

# Display first few reviews
df = pd.read_csv(csv_filename)
print(df.head(10))  # Show first 10 reviews