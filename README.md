
# Daraz Reviews Scraper

This project is a Python-based web scraper that extracts product reviews from Daraz. It uses Selenium for browser automation (with lazy loading and pagination fixes), BeautifulSoup for parsing the HTML, and Pandas for data manipulation. The script scrapes reviews from a specified Daraz product URL, collects details such as reviewer name, verification status, review date, review content, star rating, product details, likes, and image URLs, and then saves the collected data into a CSV file.

## Project Overview

- **Scraping Reviews:**  
  The script navigates to a Daraz product page, scrolls to load reviews (addressing lazy loading issues), and extracts review data from each page.
  
- **Pagination:**  
  It handles pagination by clicking the "Next" button until no further pages are available or the button is disabled.

- **Data Storage:**  
  The extracted review data is stored in a CSV file named `Daraz_Reviews_LazyLoaded_Fixed.csv`. The CSV contains columns for:
  - Reviewer Name
  - Verification Status
  - Review Date
  - Review Content
  - Star Rating
  - Product Details
  - Number of Likes
  - Image URLs

- **Error Handling:**  
  The script includes error handling to skip reviews if any issues occur during extraction.

## Prerequisites

Before running the script, make sure you have the following installed:
- Python 3.x
- [Selenium](https://selenium-python.readthedocs.io/)
- [webdriver_manager](https://github.com/SergeyPirogov/webdriver_manager)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Pandas](https://pandas.pydata.org/)
- A working installation of Google Chrome

Install the required Python libraries using pip:

```bash
pip install selenium webdriver_manager beautifulsoup4 pandas
```

## Usage

1. **Configure the Script:**
   - The product URL is set within the script. By default, the script uses a Daraz product page URL. You can modify this URL to scrape reviews for a different product.
   - Ensure that any necessary browser options (such as user-agent settings) meet your needs.

2. **Run the Script:**
   Execute the script with Python:

   ```bash
   python scrapping.py
   ```

3. **Review the Output:**
   - The script will display progress messages in the console.
   - Once complete, it saves the scraped review data to `Daraz_Reviews_LazyLoaded_Fixed.csv`.
   - The script also prints the first 10 reviews using Pandas for quick verification.

## Script Details

- **Lazy Loading Fix:**  
  The script scrolls multiple times to ensure that all reviews are loaded before extraction.
  
- **Pagination Handling:**  
  It automatically clicks the "Next" button to load additional review pages until no more reviews are available.

- **Data Extraction:**  
  Using BeautifulSoup, the script extracts key review information such as:
  - Reviewer name
  - Verification status
  - Review date and content
  - Star rating (determined by counting star images)
  - Product details and likes
  - Image URLs from inline CSS styles

## Limitations & Considerations

- **Dynamic Content:**  
  Due to the dynamic nature of the Daraz website, certain elements or classes may change over time. If the script stops working, inspect the webpage to update class names or selectors accordingly.
  
- **Browser Automation:**  
  Selenium controls a real browser instance, so ensure that no pop-ups or other interruptions interfere with the scraping process.
  
- **Ethical Use:**  
  This scraper is provided for educational and personal use. Please respect the website’s robots.txt and terms of service when scraping.

## Contributing

Contributions to improve the scraper or extend its functionality are welcome. Feel free to fork the repository and submit pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
