"""
Advanced Fiverr Scraper - Bot Detection Bypass
==============================================
Ultra-stealth scraper with multiple anti-detection techniques
"""
import re
import pandas as pd
import time
import random
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc

class AdvancedFiverrScraper:
    def __init__(self):
        self.driver = None
        self.data = []
        self.total_gigs_processed = 0
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
        ]

    def setup_undetected_driver(self):
        """Setup undetected Chrome driver for maximum stealth"""
        print("🔧 Setting up undetected Chrome driver...")

        options = uc.ChromeOptions()

        # Essential stealth options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')

        # Random user agent
        user_agent = random.choice(self.user_agents)
        options.add_argument(f'--user-agent={user_agent}')

        # Window size randomization
        window_sizes = ['1366,768', '1920,1080', '1440,900', '1600,900']
        options.add_argument(f'--window-size={random.choice(window_sizes)}')

        # Disable automation indicators
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # Additional stealth
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')  # Speed up loading
        options.add_argument('--disable-javascript')  # Temporarily disable JS

        # Language and timezone
        options.add_argument('--lang=en-US,en')
        options.add_argument('--timezone=America/New_York')

        # Create undetected driver
        driver = uc.Chrome(options=options, version_main=120)

        # Execute stealth scripts
        stealth_scripts = [
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",
            "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})",
            "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})",
            """
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
            );
            """
        ]

        for script in stealth_scripts:
            try:
                driver.execute_script(script)
            except:
                continue

        # Human-like behavior setup
        self.setup_human_behavior(driver)

        return driver

    def setup_human_behavior(self, driver):
        """Setup human-like browsing behavior"""
        # Random mouse movements
        actions = ActionChains(driver)
        actions.move_by_offset(random.randint(100, 500), random.randint(100, 500))
        actions.perform()

        # Scroll randomly
        driver.execute_script(f"window.scrollTo(0, {random.randint(100, 300)});")

        # Random delays
        time.sleep(random.uniform(0.5, 1.5))

    def human_like_delay(self, min_delay=1, max_delay=3):
        """Human-like random delay"""
        delay = random.uniform(min_delay, max_delay)
        # Add micro-delays to make it more human
        for _ in range(random.randint(2, 5)):
            time.sleep(delay / random.randint(3, 8))
        time.sleep(delay)

    def scrape_with_stealth(self, keyword="logo design", max_pages=3):
        """Main scraping function with maximum stealth"""
        print("🚀 ADVANCED FIVERR SCRAPER - STEALTH MODE")
        print("=" * 60)
        print(f"🎯 Target: '{keyword}'")
        print(f"📄 Pages: {max_pages}")
        print("=" * 60)

        try:
            # Setup undetected driver
            self.driver = self.setup_undetected_driver()

            # Test connection first
            print("🔍 Testing connection...")
            self.driver.get("https://www.fiverr.com")
            self.human_like_delay(2, 4)

            # Check if we're blocked
            title = self.driver.title
            if 'blocked' in title.lower() or 'verification' in title.lower():
                print(f"🚫 BLOCKED: {title}")
                return False

            print(f"✅ Connected successfully: {title}")

            # Start scraping
            for page in range(1, max_pages + 1):
                print(f"\n📄 SCRAPING PAGE {page}/{max_pages}")
                print("-" * 40)

                success = self.scrape_page_stealth(keyword, page)
                if not success:
                    print(f"⚠️ Page {page} failed, continuing...")
                    continue

                # Human-like delay between pages
                self.human_like_delay(3, 6)

            # Show results
            self.show_results(keyword)

        except Exception as e:
            print(f"❌ Scraping error: {e}")
        finally:
            if self.driver:
                self.driver.quit()

    def scrape_page_stealth(self, keyword, page_num):
        """Scrape a single page with stealth techniques"""
        try:
            # Build URL with keyword encoding
            keyword_encoded = keyword.replace(' ', '+')
            url = f"https://www.fiverr.com/search/gigs?query={keyword_encoded}&page={page_num}"

            print(f"🌐 Loading: {url}")

            # Navigate with human-like behavior
            start_time = time.time()
            self.driver.get(url)

            # Wait for page to load with human-like timing
            self.human_like_delay(2, 4)

            # Check for blocks
            current_title = self.driver.title
            if 'blocked' in current_title.lower() or 'verification' in current_title.lower():
                print(f"🚫 BLOCKED on page {page_num}: {current_title}")
                return False

            # Simulate human reading behavior
            self.simulate_reading()

            # Extract data
            print("🔍 Extracting data...")
            gig_count = self.extract_gigs_stealth(page_num, keyword)

            elapsed = time.time() - start_time
            print(f"✅ Page {page_num} completed in {elapsed:.2f}s - {gig_count} gigs")

            return gig_count > 0

        except Exception as e:
            print(f"❌ Page {page_num} error: {e}")
            return False

    def simulate_reading(self):
        """Simulate human reading behavior"""
        # Random scrolling
        scroll_amounts = [200, 400, 600, 300, 500]
        for scroll in random.sample(scroll_amounts, random.randint(2, 4)):
            self.driver.execute_script(f"window.scrollTo(0, {scroll});")
            time.sleep(random.uniform(0.5, 1.5))

        # Random mouse movements
        actions = ActionChains(self.driver)
        for _ in range(random.randint(3, 6)):
            x = random.randint(100, 800)
            y = random.randint(100, 600)
            actions.move_by_offset(x, y).perform()
            time.sleep(random.uniform(0.2, 0.8))

    def extract_gigs_stealth(self, page_num, keyword):
        """Extract gig data with stealth techniques"""
        gig_count = 0

        try:
            # Multiple selector strategies
            selectors = [
                "[data-gig-id]",
                ".gig-card",
                "article[data-gig-id]",
                ".search-item",
                "[class*='gig-']",
                ".gig-wrapper"
            ]

            gigs_found = False
            for selector in selectors:
                try:
                    gigs = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if gigs and len(gigs) > 0:
                        print(f"🎯 Found {len(gigs)} gigs with selector: {selector}")
                        gigs_found = True
                        break
                except:
                    continue

            if not gigs_found:
                print("❌ No gig elements found")
                return 0

            # Process gigs with human-like timing
            for i, gig in enumerate(gigs[:20]):  # Limit for stealth
                try:
                    # Hover over gig like a human would
                    actions = ActionChains(self.driver)
                    actions.move_to_element(gig).perform()
                    time.sleep(random.uniform(0.3, 0.8))

                    # Extract gig data
                    gig_data = self.extract_single_gig(gig, page_num, i+1, keyword)
                    if gig_data:
                        self.data.append(gig_data)
                        gig_count += 1
                        self.total_gigs_processed += 1

                        # Show progress
                        price = gig_data.get('price', 'N/A')
                        rating = gig_data.get('rating', 'N/A')
                        print(f"  ✅ Gig {i+1}: ${price} - {rating}⭐")

                    # Human-like delay between gigs
                    time.sleep(random.uniform(0.5, 1.2))

                except Exception as e:
                    continue

            return gig_count

        except Exception as e:
            print(f"⚠️ Gig extraction error: {e}")
            return 0

    def extract_single_gig(self, gig_element, page_num, gig_num, keyword):
        """Extract data from a single gig element"""
        try:
            # Get all text content
            gig_text = gig_element.text
            if not gig_text or len(gig_text.strip()) < 10:
                return None

            # Extract title
            title = self.extract_title(gig_text)

            # Extract price
            price = self.extract_price(gig_text)

            # Extract rating
            rating = self.extract_rating(gig_text)

            # Extract reviews
            reviews = self.extract_reviews(gig_text)

            # Extract delivery time
            delivery_days = self.extract_delivery_time(gig_text)

            # Extract seller info
            seller_info = self.extract_seller_info(gig_element)

            # Classify work type
            work_type = self.classify_work_type(gig_text)

            # Only return if we have meaningful data
            if title or price or rating:
                return {
                    'page': page_num,
                    'gig_num': gig_num,
                    'title': title,
                    'price': price,
                    'rating': rating,
                    'reviews': reviews,
                    'delivery_days': delivery_days,
                    'seller_name': seller_info.get('name'),
                    'seller_level': seller_info.get('level'),
                    'work_type': work_type,
                    'keyword': keyword,
                    'extraction_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'url': self.driver.current_url
                }

        except Exception as e:
            return None

    def extract_title(self, text):
        """Extract gig title"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        for line in lines[:3]:
            if len(line) > 10 and not line.startswith('$') and not re.match(r'^\d+', line):
                # Clean up common prefixes
                line = re.sub(r'^I will\s+', '', line, flags=re.IGNORECASE)
                return line.strip()
        return None

    def extract_price(self, text):
        """Extract price from text"""
        # Look for various price patterns
        patterns = [
            r'\$([0-9,]+)',
            r'From\s*\$([0-9,]+)',
            r'Starting\s*at\s*\$([0-9,]+)',
            r'([0-9,]+)\s*USD'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Clean and convert to int
                price_str = matches[0].replace(',', '')
                try:
                    price = int(price_str)
                    if 5 <= price <= 10000:  # Reasonable price range
                        return price
                except:
                    continue
        return None

    def extract_rating(self, text):
        """Extract rating from text"""
        # Look for decimal ratings
        rating_patterns = [
            r'([0-9]\.[0-9])\s*stars?',
            r'([0-9]\.[0-9])\s*\(?\s*[0-9]+\s*reviews?\)?',
            r'⭐?\s*([0-9]\.[0-9])'
        ]

        for pattern in rating_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                try:
                    rating = float(matches[0])
                    if 1.0 <= rating <= 5.0:
                        return rating
                except:
                    continue
        return None

    def extract_reviews(self, text):
        """Extract review count"""
        patterns = [
            r'\(([0-9,]+)\s*reviews?\)',
            r'([0-9,]+)\s*reviews?',
            r'\(([0-9,]+)\)'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                review_str = matches[0].replace(',', '')
                try:
                    reviews = int(review_str)
                    if 0 <= reviews <= 100000:
                        return reviews
                except:
                    continue
        return None

    def extract_delivery_time(self, text):
        """Extract delivery time in days"""
        patterns = [
            r'(\d+)\s*days?\s*delivery',
            r'delivery\s*in\s*(\d+)\s*days?',
            r'(\d+)\s*day\s*turnaround',
            r'within\s*(\d+)\s*days?'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                try:
                    days = int(matches[0])
                    if 1 <= days <= 365:
                        return days
                except:
                    continue
        return None

    def extract_seller_info(self, gig_element):
        """Extract seller information"""
        seller_info = {'name': None, 'level': None}

        try:
            # Look for seller name
            seller_selectors = [
                ".seller-name",
                "[class*='seller']",
                ".user-info a",
                ".seller-link"
            ]

            for selector in seller_selectors:
                try:
                    seller_elem = gig_element.find_element(By.CSS_SELECTOR, selector)
                    if seller_elem:
                        seller_info['name'] = seller_elem.text.strip()
                        break
                except:
                    continue

            # Look for seller level
            level_selectors = [
                ".seller-level",
                "[class*='level']",
                ".badge"
            ]

            for selector in level_selectors:
                try:
                    level_elem = gig_element.find_element(By.CSS_SELECTOR, selector)
                    if level_elem:
                        level_text = level_elem.text.strip()
                        if any(word in level_text.lower() for word in ['level', 'top', 'pro', 'vetted']):
                            seller_info['level'] = level_text
                            break
                except:
                    continue

        except:
            pass

        return seller_info

    def classify_work_type(self, text):
        """Classify the type of work"""
        text_lower = text.lower()

        # Logo design
        if any(word in text_lower for word in ['logo', 'brand', 'identity', 'branding']):
            return 'logo_design'

        # Character design
        elif any(word in text_lower for word in ['character', 'mascot', 'avatar', 'cartoon']):
            return 'character_design'

        # Illustration
        elif any(word in text_lower for word in ['illustration', 'drawing', 'artwork', 'digital art']):
            return 'illustration'

        # Web design
        elif any(word in text_lower for word in ['website', 'web design', 'ui', 'ux', 'landing page']):
            return 'web_design'

        # Animation
        elif any(word in text_lower for word in ['animation', 'animated', 'motion', 'video']):
            return 'animation'

        # Other
        else:
            return 'other'

    def show_results(self, keyword):
        """Display comprehensive results"""
        if not self.data:
            print("❌ No data collected")
            return

        print(f"\n🎯 FIVERR SCRAPING RESULTS for '{keyword}'")
        print("=" * 60)
        print(f"📊 Total gigs processed: {len(self.data)}")

        # Extract all data
        prices = [g['price'] for g in self.data if g['price']]
        ratings = [g['rating'] for g in self.data if g['rating']]
        reviews = [g['reviews'] for g in self.data if g['reviews']]
        delivery_times = [g['delivery_days'] for g in self.data if g['delivery_days']]
        work_types = [g['work_type'] for g in self.data if g['work_type']]

        # Pricing analysis
        if prices:
            print(f"\n💰 PRICING ANALYSIS:")
            print(f"   Range: ${min(prices)} - ${max(prices)}")
            print(f"   Average: ${sum(prices)/len(prices):.2f}")
            print(f"   Median: ${sorted(prices)[len(prices)//2]}")

            # Price distribution
            if len(prices) >= 4:
                q1 = sorted(prices)[len(prices)//4]
                q3 = sorted(prices)[3*len(prices)//4]
                print(f"   Quartiles: Q1=${q1}, Q3=${q3}")

        # Quality analysis
        if ratings:
            print(f"\n⭐ QUALITY ANALYSIS:")
            print(f"   Average rating: {sum(ratings)/len(ratings):.2f}")
            print(f"   Range: {min(ratings)} - {max(ratings)}")

        # Work type breakdown
        if work_types:
            from collections import Counter
            type_counts = Counter(work_types)
            print(f"\n🎨 WORK TYPE BREAKDOWN:")
            for work_type, count in type_counts.most_common():
                percentage = (count / len(work_types)) * 100
                print(f"   • {work_type.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")

        # Delivery analysis
        if delivery_times:
            print(f"\n⏰ DELIVERY ANALYSIS:")
            print(f"   Average: {sum(delivery_times)/len(delivery_times):.1f} days")
            print(f"   Range: {min(delivery_times)}-{max(delivery_times)} days")

        # Save to CSV
        self.save_to_csv(keyword)

    def save_to_csv(self, keyword):
        """Save results to CSV"""
        if not self.data:
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"fiverr_{keyword.replace(' ', '_')}_stealth_{timestamp}.csv"

        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)

        print(f"\n💾 Data saved to: {filename}")
        print(f"📊 Total records: {len(self.data)}")

        # Show sample data
        if len(self.data) > 0:
            print(f"\n📋 SAMPLE DATA:")
            sample = self.data[0]
            print(f"   Title: {sample.get('title', 'N/A')}")
            print(f"   Price: ${sample.get('price', 'N/A')}")
            print(f"   Rating: {sample.get('rating', 'N/A')}⭐")
            print(f"   Seller: {sample.get('seller_name', 'N/A')}")

def main():
    """Main function"""
    print("🚀 ADVANCED FIVERR SCRAPER - BOT DETECTION BYPASS")
    print("=" * 60)

    # Get user input
    keyword = input("🎯 Enter keyword (e.g., 'logo design'): ").strip()
    if not keyword:
        keyword = "logo design"
        print(f"Using default: '{keyword}'")

    pages_input = input("📄 Number of pages to scrape (1-10): ").strip()
    try:
        max_pages = int(pages_input)
        if max_pages < 1 or max_pages > 10:
            max_pages = 3
    except:
        max_pages = 3

    print(f"Starting stealth scraping for '{keyword}' ({max_pages} pages)...")

    # Start scraping
    scraper = AdvancedFiverrScraper()
    scraper.scrape_with_stealth(keyword, max_pages)

if __name__ == "__main__":
    main()
