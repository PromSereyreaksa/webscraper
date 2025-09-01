"""
UnnamedDesign Advanced Multi-Threaded Fiverr Scraper
==================================================
Multi-threaded scraping with dynamic keywords and custom output files
"""
import re
import pandas as pd
import time
import random
import threading
import queue
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Global variables for user input
SEARCH_KEYWORD = ""
TOTAL_THREADS = 4
PAGES_PER_THREAD = 3
OUTPUT_FILE = ""
USE_PROXY = False
PROXY_LIST = []

def get_user_input():
    """Get user input for scraping parameters"""
    global SEARCH_KEYWORD, TOTAL_THREADS, PAGES_PER_THREAD, OUTPUT_FILE, USE_PROXY, PROXY_LIST

    print("🚀 UNNAMEDDESIGN MULTI-THREADED FIVERR SCRAPER")
    print("=" * 55)

    # Get keyword
    SEARCH_KEYWORD = input("🎯 Enter search keyword (e.g., 'logo design'): ").strip()
    if not SEARCH_KEYWORD:
        SEARCH_KEYWORD = "logo design"
        print(f"   Using default: '{SEARCH_KEYWORD}'")

    # Get output file name
    default_output = f"{SEARCH_KEYWORD.replace(' ', '_')}_data.csv"
    OUTPUT_FILE = input(f"📁 Output file name (default: '{default_output}'): ").strip()
    if not OUTPUT_FILE:
        OUTPUT_FILE = default_output

    # Get thread count
    try:
        TOTAL_THREADS = int(input("🔥 Number of threads (default 4): ").strip() or "4")
    except:
        TOTAL_THREADS = 4

    # Get pages per thread
    try:
        PAGES_PER_THREAD = int(input("📄 Pages per thread (default 3): ").strip() or "3")
    except:
        PAGES_PER_THREAD = 3

    # Get proxy settings
    proxy_choice = input("🛡️ Use proxy rotation? (y/n, default n): ").strip().lower()
    if proxy_choice == 'y':
        USE_PROXY = True
        print("📋 Enter proxy list (one per line, format: ip:port or user:pass@ip:port)")
        print("   Press Enter twice when done:")
        proxies = []
        while True:
            proxy = input("   Proxy: ").strip()
            if not proxy:
                break
            proxies.append(proxy)
        
        if proxies:
            PROXY_LIST = proxies
            print(f"✅ Added {len(PROXY_LIST)} proxies")
        else:
            print("⚠️ No proxies entered, running without proxy")
            USE_PROXY = False
    else:
        USE_PROXY = False

    print(f"\n⚙️ CONFIGURATION:")
    print(f"   Keyword: '{SEARCH_KEYWORD}'")
    print(f"   Output: '{OUTPUT_FILE}'")
    print(f"   Threads: {TOTAL_THREADS}")
    print(f"   Pages per thread: {PAGES_PER_THREAD}")
    print(f"   Total pages: {TOTAL_THREADS * PAGES_PER_THREAD}")
    if USE_PROXY:
        print(f"   Proxies: {len(PROXY_LIST)} configured")
    else:
        print(f"   Proxies: Disabled")
    print("=" * 55)

def setup_stealth_driver(thread_id=0, proxy=None):
    """Setup stealth Chrome driver with optional proxy"""
    options = Options()

    # Essential system flags
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    # Keep JS enabled for real interaction
    # options.add_argument('--disable-javascript')  # Enable JS for real data

    # Add proxy if provided
    if proxy:
        if '@' in proxy:
            # Authenticated proxy: user:pass@ip:port
            auth_part, server_part = proxy.split('@')
            user, password = auth_part.split(':')
            ip, port = server_part.split(':')
            proxy_url = f"http://{user}:{password}@{ip}:{port}"
        else:
            # Simple proxy: ip:port
            proxy_url = f"http://{proxy}"
        
        options.add_argument(f'--proxy-server={proxy_url}')
        print(f"🛡️ Thread {thread_id}: Using proxy {proxy}")

    # Advanced stealth options
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-background-timer-throttling')
    options.add_argument('--disable-backgrounding-occluded-windows')
    options.add_argument('--disable-renderer-backgrounding')
    options.add_argument('--disable-field-trial-config')
    options.add_argument('--disable-back-forward-cache')
    options.add_argument('--disable-hang-monitor')
    options.add_argument('--disable-ipc-flooding-protection')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-prompt-on-repost')
    options.add_argument('--disable-component-update')
    options.add_argument('--disable-domain-reliability')
    options.add_argument('--disable-client-side-phishing-detection')
    options.add_argument('--disable-background-networking')

    # Realistic user agent
    options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    # Window size like a real user
    options.add_argument('--window-size=1920,1080')

    # Disable automation indicators
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("prefs", {
        "profile.password_manager_enabled": False,
        "credentials_enable_service": False,
        "profile.default_content_setting_values.notifications": 2,
        "profile.managed_default_content_settings.images": 1,
        "profile.default_content_settings.popups": 0,
        "profile.managed_default_content_settings.geolocation": 2,
        "profile.managed_default_content_settings.media_stream": 2,
    })

    driver = webdriver.Chrome(options=options)

    # Execute stealth scripts
    stealth_scripts = [
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",
        "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})",
        "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})",
        "window.navigator.chrome = {runtime: {}, loadTimes: function() {}, csi: function() {}, app: {}}",
        "Object.defineProperty(navigator, 'platform', {get: () => 'Linux x86_64'})",
    ]

    for script in stealth_scripts:
        try:
            driver.execute_script(script)
        except:
            pass

    # Add human-like behavior
    driver.execute_script("""
        // Override permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );

        // Mock battery
        Object.defineProperty(navigator, 'getBattery', {
            value: () => Promise.resolve({
                charging: true,
                chargingTime: Infinity,
                dischargingTime: Infinity,
                level: 1
            })
        });
    """)

    return driver

def get_proxy_for_thread(thread_id):
    """Get a proxy for the thread (round-robin rotation)"""
    if not USE_PROXY or not PROXY_LIST:
        return None
    
    proxy_index = (thread_id - 1) % len(PROXY_LIST)
    return PROXY_LIST[proxy_index]

def validate_proxy(proxy):
    """Test if a proxy is working"""
    try:
        if '@' in proxy:
            # Authenticated proxy
            auth_part, server_part = proxy.split('@')
            user, password = auth_part.split(':')
            ip, port = server_part.split(':')
            proxy_url = f"http://{user}:{password}@{ip}:{port}"
        else:
            # Simple proxy
            proxy_url = f"http://{proxy}"
        
        # Test the proxy with a simple request
        import requests
        test_response = requests.get('http://httpbin.org/ip', 
                                   proxies={'http': proxy_url, 'https': proxy_url}, 
                                   timeout=5)
        if test_response.status_code == 200:
            return True
    except:
        pass
    return False

class FastFiverrScraper:
    def __init__(self):
        self.data = []
        self.all_data = []
        self.total_gigs_processed = 0
        self.driver = None

    def parallel_scrape_keyword(self, keyword, total_threads=4, pages_per_thread=3):
        """Launch multiple threads to scrape in parallel"""
        print(f"🚀 MULTI-THREADED FIVERR SCRAPER")
        print(f"🎯 Keyword: '{keyword}'")
        print(f"🔥 Threads: {total_threads}")
        print(f"📄 Pages per thread: {pages_per_thread}")
        print("=" * 50)

        # Create thread pool
        scrapers = []
        futures = []

        with ThreadPoolExecutor(max_workers=total_threads) as executor:
            # Launch each thread with its page range
            for thread_id in range(total_threads):
                start_page = thread_id * pages_per_thread + 1
                end_page = start_page + pages_per_thread - 1

                scraper = ThreadedFiverrScraper(keyword, thread_id + 1, None)
                future = executor.submit(scraper.scrape_thread_pages, start_page, end_page)
                futures.append(future)
                scrapers.append(scraper)

            # Collect results
            for future in as_completed(futures):
                try:
                    thread_data = future.result()
                    if thread_data:
                        self.all_data.extend(thread_data)
                        print(f"🔄 Thread completed - {len(thread_data)} records collected")
                except Exception as e:
                    print(f"⚠️ Thread failed: {e}")

        # Consolidate data
        self.data = self.all_data

        # Show results
        self.show_threaded_results(keyword, total_threads)

    def show_threaded_results(self, keyword, threads_used):
        """Show results from multi-threaded scraping"""
        if not self.data:
            print("❌ No data collected from any threads")
            return

        print(f"\n🎯 MULTI-THREADED RESULTS for '{keyword}':")
        print("=" * 50)
        print(f"📊 Total records: {len(self.data)}")
        print(f"🔥 Threads used: {threads_used}")

        # Process data
        all_prices = []
        all_ratings = []
        all_reviews = []
        all_titles = []
        all_delivery_times = []
        work_types = []

        for record in self.data:
            if 'prices' in record and record['prices']:
                if isinstance(record['prices'], list):
                    all_prices.extend(record['prices'])
                else:
                    all_prices.append(record['prices'])

            if 'price' in record and record['price']:
                all_prices.append(record['price'])

            if 'ratings' in record and record['ratings']:
                if isinstance(record['ratings'], list):
                    all_ratings.extend(record['ratings'])
                else:
                    all_ratings.append(record['ratings'])

            if 'rating' in record and record['rating']:
                all_ratings.append(record['rating'])

            if 'reviews' in record and record['reviews']:
                if isinstance(record['reviews'], list):
                    all_reviews.extend(record['reviews'])
                else:
                    all_reviews.append(record['reviews'])

            if 'title' in record and record['title']:
                all_titles.append(record['title'])
            if 'delivery_days' in record and record['delivery_days']:
                all_delivery_times.append(record['delivery_days'])
            if 'work_type' in record and record['work_type']:
                work_types.append(record['work_type'])

        # Show analysis
        if all_prices:
            print(f"\n💰 PRICING ANALYSIS:")
            print(f"   Prices found: {len(all_prices)}")
            print(f"   Range: ${min(all_prices)} - ${max(all_prices)}")
            print(f"   Average: ${sum(all_prices)/len(all_prices):.2f}")

        if all_ratings:
            print(f"\n⭐ QUALITY ANALYSIS:")
            print(f"   Ratings found: {len(all_ratings)}")
            print(f"   Average: ${sum(all_ratings)/len(all_ratings):.2f}")

        if all_delivery_times:
            print(f"\n⏰ DELIVERY ANALYSIS:")
            print(f"   Average: {sum(all_delivery_times)/len(all_delivery_times):.1f} days")

        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{keyword.replace(' ', '_')}_data_{timestamp}.csv"

        if all_prices or all_ratings or all_titles:
            self.save_threaded_csv(all_prices, all_ratings, all_reviews, all_titles, all_delivery_times, work_types, filename)

    def save_threaded_csv(self, prices, ratings, reviews, titles, delivery_times, work_types, filename):
        """Save multi-threaded results to CSV"""
        max_len = max(len(prices), len(ratings), len(reviews), len(titles), len(delivery_times), len(work_types))

        # Pad lists
        prices += [None] * (max_len - len(prices))
        ratings += [None] * (max_len - len(ratings))
        reviews += [None] * (max_len - len(reviews))
        titles += [None] * (max_len - len(titles))
        delivery_times += [None] * (max_len - len(delivery_times))
        work_types += [None] * (max_len - len(work_types))

        df = pd.DataFrame({
            'title': titles,
            'price': prices,
            'rating': ratings,
            'reviews': reviews,
            'delivery_days': delivery_times,
            'work_type': work_types,
            'extraction_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

        df.to_csv(filename, index=False)
        print(f"💾 Multi-threaded data saved to {filename}")
        return df

class ThreadedFiverrScraper:
    def __init__(self, keyword, thread_id, output_queue):
        self.keyword = keyword
        self.thread_id = thread_id
        self.driver = None
        self.data = []
        self.gigs_processed = 0
        self.output_queue = output_queue

    def start_thread_driver(self):
        """Start driver for this thread"""
        try:
            proxy = get_proxy_for_thread(self.thread_id) if USE_PROXY else None
            self.driver = setup_stealth_driver(self.thread_id, proxy)
            return True
        except Exception as e:
            print(f"❌ Thread {self.thread_id} failed to start driver: {e}")
            return False

    def scrape_thread_pages(self, start_page, end_page):
        """Scrape pages assigned to this thread"""
        if not self.start_thread_driver():
            return []

        try:
            # Stagger thread starts to avoid detection
            stagger_delay = random.uniform(2.0, 5.0) + (self.thread_id * 2.0)
            print(f"🕐 Thread {self.thread_id}: Starting in {stagger_delay:.1f}s...")
            time.sleep(stagger_delay)

            print(f"🔥 Thread {self.thread_id}: Scraping pages {start_page}-{end_page} for '{self.keyword}'")

            for page in range(start_page, end_page + 1):
                success = self.scrape_single_page(page)
                if not success:
                    print(f"⚠️ Thread {self.thread_id}: Page {page} failed - skipping...")
                    continue

                # Spacing between pages
                page_delay = random.uniform(1.5, 3.0)
                time.sleep(page_delay)

        except Exception as e:
            print(f"❌ Thread {self.thread_id} error: {e}")
        finally:
            if self.driver:
                self.driver.quit()

        print(f"✅ Thread {self.thread_id} completed: {self.gigs_processed} gigs processed")
        return self.data

    def scrape_single_page(self, page_num):
        """Scrape a single page"""
        try:
            # Build URL
            keyword_encoded = self.keyword.replace(' ', '+')
            url = f"https://www.fiverr.com/search/gigs?query={keyword_encoded}&page={page_num}"

            print(f"  🌐 Thread {self.thread_id}: Loading page {page_num}...")
            print(f"  📍 URL: {url}")

            # Open page
            self.driver.get(url)

            # Wait for page load
            time.sleep(2.0)

            # Check if blocked
            page_title = self.driver.title
            print(f"  📄 Page loaded: {page_title}")

            if 'human' in page_title.lower() or 'verification' in page_title.lower() or 'blocked' in page_title.lower():
                print(f"🚫 Thread {self.thread_id}: BLOCKED - {page_title}")
                return False

            print(f"  🔍 Scraping page {page_num}...")

            # Extract data
            page_text = self.driver.execute_script("return document.body.innerText;")
            if page_text and len(page_text) > 500:
                self.extract_from_page_text(page_text, page_num)

            # Extract individual gigs
            gig_count = self.extract_individual_gigs(page_num)

            print(f"  ✅ Thread {self.thread_id} - Page {page_num}: {gig_count} gigs extracted")
            return gig_count > 0

        except Exception as e:
            print(f"⚠️ Thread {self.thread_id} - Page {page_num} error: {e}")
            return False

    def extract_individual_gigs(self, page_num):
        """Extract individual gigs"""
        gig_count = 0

        try:
            gig_selectors = [
                "[data-gig-id]",
                ".gig-card",
                "article",
                ".search-results > div",
                "[data-testid*='gig']"
            ]

            gigs = []
            for selector in gig_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        gigs = elements
                        break
                except:
                    continue

            # Process gigs
            for i, gig in enumerate(gigs[:20]):
                try:
                    gig_text = gig.text
                    if gig_text and len(gig_text) > 10:
                        gig_data = self.extract_gig_data(gig_text, page_num, i+1)
                        if gig_data:
                            self.data.append(gig_data)
                            gig_count += 1
                            self.gigs_processed += 1
                except:
                    continue

            return gig_count

        except Exception as e:
            return 0

    def extract_from_page_text(self, text, page_num):
        """Extract from page text"""
        prices = re.findall(r'\$(\d+)', text)
        prices = [int(p) for p in prices if 5 <= int(p) <= 1000]

        ratings = re.findall(r'(\d\.\d)', text)
        ratings = [float(r) for r in ratings if 3.0 <= float(r) <= 5.0]

        reviews = re.findall(r'\((\d+)\)', text)
        reviews = [int(r) for r in reviews if 1 <= int(r) <= 5000]

        if prices or ratings:
            self.data.append({
                'source': f'thread_{self.thread_id}_page_{page_num}_text',
                'thread_id': self.thread_id,
                'page': page_num,
                'prices': prices,
                'ratings': ratings,
                'reviews': reviews,
                'keyword': self.keyword,
                'extraction_time': datetime.now().strftime('%H:%M:%S')
            })

    def extract_gig_data(self, gig_text, page_num, gig_num):
        """Extract individual gig data"""
        # Extract title
        lines = [line.strip() for line in gig_text.split('\n') if line.strip()]
        title = None
        for line in lines[:3]:
            if len(line) > 10 and not line.startswith('$') and not re.match(r'^\d+', line):
                title = line
                break

        # Extract price
        price_matches = re.findall(r'\$(\d+)', gig_text)
        price = None
        if price_matches:
            for p in price_matches:
                p_int = int(p)
                if 5 <= p_int <= 1000:
                    price = p_int
                    break

        # Extract rating
        rating_matches = re.findall(r'(\d\.\d)', gig_text)
        rating = None
        if rating_matches:
            for r in rating_matches:
                r_float = float(r)
                if 3.0 <= r_float <= 5.0:
                    rating = r_float
                    break

        # Extract reviews
        review_matches = re.findall(r'\((\d+)\)', gig_text)
        reviews = None
        if review_matches:
            for r in review_matches:
                r_int = int(r)
                if 1 <= r_int <= 5000:
                    reviews = r_int
                    break

        # Extract delivery time
        delivery_time = None
        delivery_patterns = [
            r'(\d+)\s*days?\s*delivery',
            r'delivery\s*in\s*(\d+)\s*days?',
            r'(\d+)\s*day\s*turnaround',
            r'within\s*(\d+)\s*days?',
            r'(\d+)d\s*delivery'
        ]

        for pattern in delivery_patterns:
            matches = re.findall(pattern, gig_text.lower())
            if matches:
                delivery_time = int(matches[0])
                break

        # Extract work type
        work_type = "unknown"
        gig_lower = gig_text.lower()
        if any(word in gig_lower for word in ['logo', 'brand', 'identity']):
            work_type = "logo_design"
        elif any(word in gig_lower for word in ['character', 'mascot', 'avatar']):
            work_type = "character_design"
        elif any(word in gig_lower for word in ['illustration', 'drawing', 'art']):
            work_type = "illustration"
        elif any(word in gig_lower for word in ['portrait', 'photo', 'realistic']):
            work_type = "portrait"
        elif any(word in gig_lower for word in ['concept', 'fantasy', 'sci-fi']):
            work_type = "concept_art"

        if title or price or rating:
            return {
                'source': f'thread_{self.thread_id}_page_{page_num}_gig_{gig_num}',
                'thread_id': self.thread_id,
                'page': page_num,
                'gig_num': gig_num,
                'title': title,
                'price': price,
                'rating': rating,
                'reviews': reviews,
                'delivery_days': delivery_time,
                'work_type': work_type,
                'keyword': self.keyword,
                'extraction_time': datetime.now().strftime('%H:%M:%S')
            }

        return None

def main():
    """Main function with user input"""
    # Get user configuration
    get_user_input()

    # Start scraping
    scraper = FastFiverrScraper()
    scraper.parallel_scrape_keyword(SEARCH_KEYWORD, TOTAL_THREADS, PAGES_PER_THREAD)

if __name__ == "__main__":
    main()