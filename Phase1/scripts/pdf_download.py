#!/usr/bin/env python3
"""
Bid Document Downloader for publicpurchase.com
Logs in, downloads PDFs, filters by keywords, highlights matches.
No emojis. 100% local.
"""

import os
import time
import logging
import requests
from urllib.parse import urljoin, parse_qs
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import fitz  # PyMuPDF

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get base directory (Agent/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

# Configuration
CHROMEDRIVER_PATH = os.path.join(BASE_DIR, "Tools", "chromedriver.exe")
TEMP_FOLDER = Path(os.path.join(BASE_DIR, "RAG", "temp"))
FINAL_FOLDER = Path(os.path.join(BASE_DIR, "RAG", "final"))

# Create folders if not exist
TEMP_FOLDER.mkdir(parents=True, exist_ok=True)
FINAL_FOLDER.mkdir(parents=True, exist_ok=True)

LOGIN_URL = "https://www.publicpurchase.com/gems/login/login?dst=%2Fvendor%2Fhome%2Fhome"
VENDOR_HOME = "https://www.publicpurchase.com/gems/vendor/home/home"

# Edit keywords here
KEYWORDS = [" Solicitation ", "emailed", "faxed"]

# Credentials
USERNAME = os.getenv('PP_USERNAME')
PASSWORD = os.getenv('PP_PASSWORD')

if not USERNAME or not PASSWORD:
    logger.error("[ERROR] PP_USERNAME and PP_PASSWORD must be set in .env file")
    raise ValueError("Missing credentials in .env")


class BidDocumentDownloader:
    def __init__(self):
        self.driver = None

    def setup_driver(self):
        try:
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--start-maximized')

            import tempfile
            user_data_dir = tempfile.mkdtemp()
            chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
            chrome_options.add_argument('--remote-debugging-port=9222')

            service = Service(executable_path=CHROMEDRIVER_PATH)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")

            logger.info("[BROWSER] WebDriver initialized successfully")
            return True
        except Exception as e:
            logger.error(f"[ERROR] Failed to setup WebDriver: {str(e)}")
            return False

    def login(self):
        try:
            logger.info("[LOGIN] Navigating to login page...")
            self.driver.get(LOGIN_URL)

            wait = WebDriverWait(self.driver, 30)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            logger.info("[LOGIN] Entering credentials...")
            username_field = wait.until(EC.presence_of_element_located((By.NAME, "uname")))
            password_field = self.driver.find_element(By.NAME, "pwd")
            login_button = self.driver.find_element(By.XPATH, "//input[@type='button' and @value='Login']")

            username_field.clear()
            username_field.send_keys(USERNAME)
            password_field.clear()
            password_field.send_keys(PASSWORD)
            login_button.click()

            wait.until(EC.url_contains("vendor/home"))
            time.sleep(2)
            logger.info("[LOGIN] Logged in successfully!")
            return True
        except Exception as e:
            logger.error(f"[ERROR] Login failed: {str(e)}")
            return False

    def find_bid_links(self):
        try:
            logger.info("[BIDS] Navigating to vendor home...")
            self.driver.get(VENDOR_HOME)
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            selectors = ['a[href*="bidView?bidId"]']
            bid_links = []

            for selector in selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for el in elements:
                    href = el.get_attribute('href')
                    text = el.text.strip() or f"Bid_{href.split('bidId=')[-1]}"
                    if href:
                        bid_links.append({'url': href, 'title': text})

            seen = set()
            unique_bids = []
            for b in bid_links:
                if b['url'] not in seen:
                    seen.add(b['url'])
                    unique_bids.append(b)

            logger.info(f"[BIDS] Found {len(unique_bids)} unique bid(s)")
            return unique_bids
        except Exception as e:
            logger.error(f"[ERROR] Error finding bids: {str(e)}")
            return []

    def extract_documents_from_page(self):
        try:
            doc_selectors = [
                'a[href*="bidDoc"]',
                'a[href*="download"]',
                'a[href$=".pdf"]'
            ]
            documents = []

            for selector in doc_selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for el in elements:
                    href = el.get_attribute('href')
                    text = el.text.strip()
                    if href:
                        full_url = urljoin("https://www.publicpurchase.com", href)
                        if text:
                            filename = text
                        else:
                            filename = f"document_{len(documents)+1}.pdf"
                        if not filename.lower().endswith('.pdf'):
                            filename += '.pdf'
                        documents.append({'url': full_url, 'filename': filename})

            # Remove duplicates by docId and sectionId
            seen_docs = set()
            unique_docs = []

            for doc in documents:
                url = doc['url']
                # Parse query parameters
                if '?' in url:
                    query = url.split('?', 1)[1]
                    params = parse_qs(query)
                    doc_id = params.get('docId', [None])[0]
                    section_id = params.get('sectionId', [None])[0]
                else:
                    doc_id = None
                    section_id = None

                doc_key = (doc_id, section_id)

                if doc_key not in seen_docs:
                    seen_docs.add(doc_key)
                    unique_docs.append(doc)

            logger.info(f"[DOCS] Found {len(unique_docs)} unique document(s) on page")
            return unique_docs
        except Exception as e:
            logger.error(f"[ERROR] Error extracting documents: {str(e)}")
            return []

    def is_valid_pdf(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                header = f.read(4)
                return header == b'%PDF'
        except Exception:
            return False

    def search_keywords_in_pdf(self, pdf_path, keywords):
        try:
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc[page_num]
                for keyword in keywords:
                    if page.search_for(keyword):
                        doc.close()
                        return True
            doc.close()
            return False
        except Exception as e:
            logger.error(f"[ERROR] Error searching in {pdf_path}: {str(e)}")
            return False

    def highlight_keywords_in_pdf(self, input_path, output_path, keywords):
        try:
            if not self.is_valid_pdf(input_path):
                logger.error(f"[INVALID] Not a PDF file: {input_path}")
                return False

            doc = fitz.open(input_path)
            found_any = False

            for page_num in range(len(doc)):
                page = doc[page_num]
                for keyword in keywords:
                    text_instances = page.search_for(keyword)
                    if text_instances:
                        found_any = True
                        for inst in text_instances:
                            highlight = page.add_highlight_annot(inst)
                            highlight.set_colors({"stroke": [1, 1, 0]})  # Yellow
                            highlight.update()

            if found_any:
                doc.save(output_path)
                logger.info(f"[HIGHLIGHTED] Saved: {output_path.name}")
                doc.close()
                return True
            else:
                logger.warning(f"[NO KEYWORDS] No matches in: {input_path.name}")
                doc.close()
                return False

        except Exception as e:
            logger.error(f"[ERROR] Highlighting failed for {input_path}: {str(e)}")
            return False

    def download_document(self, doc_url, filename, bid_title):
        try:
            # Clean filename
            clean_base = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).strip()
            if not clean_base.lower().endswith('.pdf'):
                clean_base += '.pdf'
            temp_filename = f"temp_{clean_base}"
            temp_path = TEMP_FOLDER / temp_filename

            # Delete if exists
            if temp_path.exists():
                temp_path.unlink()
                logger.info(f"[TEMP] Deleted existing: {temp_filename}")

            # Download
            cookies = {cookie['name']: cookie['value'] for cookie in self.driver.get_cookies()}
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://www.publicpurchase.com/'
            }

            logger.info(f"[DOWNLOAD] Starting: {filename}")
            response = requests.get(doc_url, cookies=cookies, headers=headers, stream=True, timeout=60)
            response.raise_for_status()

            # Get file size from headers
            file_size = int(response.headers.get('content-length', 0))

            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            # Fallback: get size from file if header missing
            if file_size == 0:
                file_size = temp_path.stat().st_size

            logger.info(f"[TEMP] Saved ({file_size} bytes): {temp_filename}")

            # Validate PDF
            if not self.is_valid_pdf(temp_path):
                logger.error(f"[INVALID] Not a PDF: {filename} — deleting")
                temp_path.unlink()
                return False

            # Search keywords
            if not self.search_keywords_in_pdf(temp_path, KEYWORDS):
                logger.info(f"[NO MATCH] Keywords not found in: {filename}")
                temp_path.unlink()
                return False

            logger.info(f"[MATCH] Keywords found in: {filename}")

            # Save to final folder
            safe_title = "".join(c for c in bid_title[:50] if c.isalnum() or c in ('-', '_'))
            bid_folder = FINAL_FOLDER / safe_title
            bid_folder.mkdir(exist_ok=True)

            final_filename = f"highlighted_{clean_base}"
            final_path = bid_folder / final_filename

            if self.highlight_keywords_in_pdf(temp_path, final_path, KEYWORDS):
                logger.info(f"[SAVED] Final: {final_path}")
                temp_path.unlink()  # Cleanup
                return True
            else:
                logger.error(f"[FAILED] Highlighting failed for: {filename}")
                temp_path.unlink()
                return False

        except Exception as e:
            logger.error(f"[ERROR] Processing failed for {filename}: {str(e)}")
            if 'temp_path' in locals() and temp_path.exists():
                temp_path.unlink()
            return False

    def run(self):
        try:
            logger.info("[START] Starting Public Purchase Document Downloader")
            logger.info(f"[CONFIG] Filtering for keywords: {KEYWORDS}")

            # Clear temp folder at start
            for file in TEMP_FOLDER.glob("*"):
                try:
                    file.unlink()
                    logger.info(f"[CLEANUP] Deleted old temp file: {file.name}")
                except Exception as e:
                    logger.warning(f"[CLEANUP] Failed to delete {file.name}: {str(e)}")

            if not self.setup_driver():
                logger.error("[ERROR] WebDriver setup failed")
                return False

            if not self.login():
                logger.error("[ERROR] Login failed — aborting")
                return False

            bid_links = self.find_bid_links()
            if not bid_links:
                logger.warning("[WARNING] No bids found — nothing to download")
                return True

            downloaded_count = 0
            matched_count = 0

            for i, bid in enumerate(bid_links):
                try:
                    logger.info(f"[BID] Processing bid {i+1}/{len(bid_links)}: {bid['title']}")

                    self.driver.get(bid['url'])
                    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                    docs = self.extract_documents_from_page()
                    for doc in docs:
                        if self.download_document(doc['url'], doc['filename'], bid['title']):
                            matched_count += 1
                        downloaded_count += 1

                    time.sleep(3)

                except Exception as e:
                    logger.error(f"[ERROR] Error processing {bid['title']}: {str(e)}")
                    continue

            logger.info("[COMPLETE] Processing complete!")
            logger.info(f"   Total PDFs processed: {downloaded_count}")
            logger.info(f"   Saved (matched keywords): {matched_count}")
            logger.info(f"   Location: {FINAL_FOLDER}")
            return True

        except Exception as e:
            logger.error(f"[CRASH] Unexpected error: {str(e)}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("[BROWSER] Browser closed")


def main():
    downloader = BidDocumentDownloader()
    success = downloader.run()

    if success:
        print("[SUCCESS] Agent completed. Check logs for keyword stats.")
    else:
        print("[FAILED] Download failed. Check logs above.")


if __name__ == "__main__":
    main()