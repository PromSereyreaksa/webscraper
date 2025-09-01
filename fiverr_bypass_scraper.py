"""
UnnamedDesign Fiverr Bot Bypass Scraper
======================================
Advanced Fiverr scraping with multiple bot detection bypass techniques
"""
import re
import pandas as pd
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import json

class FiverrBotBypassScraper:
    def __init__(self):
        self.driver = None
        self.data = []
        self.total_gigs_processed = 0

    def setup_undetected_driver(self):
        """Setup Chrome driver that bypasses bot detection"""
        options = Options()

        # Essential system flags (compatible with current ChromeDriver)
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')

        # Keep JavaScript enabled for real interaction
        # options.add_argument('--disable-javascript')  # DON'T disable JS

        # Stealth options (compatible versions)
        options.add_argument('--disable-blink-features=AutomationControlled')
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

        # Disable automation indicators (compatible way)
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # Set preferences to avoid detection
        options.add_experimental_option("prefs", {
            "profile.password_manager_enabled": False,
            "credentials_enable_service": False,
            "profile.default_content_setting_values.notifications": 2,
            "profile.managed_default_content_settings.images": 1,  # Load images
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.geolocation": 2,
            "profile.managed_default_content_settings.media_stream": 2,
        })

        # Create driver
        driver = webdriver.Chrome(options=options)

        # Execute stealth scripts to hide automation
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
            except Exception as e:
                print(f"⚠️ Stealth script failed: {e}")

        # Add human-like behavior simulation
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

            // Mock connection
            Object.defineProperty(navigator, 'connection', {
                value: {
                    effectiveType: '4g',
                    rtt: 50,
                    downlink: 2
                }
            });
        """)

        return driver

    def human_like_delay(self, min_delay=1, max_delay=3):
        """Add human-like random delays"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)

    def simulate_human_behavior(self, driver):
        """Simulate human browsing behavior"""
        try:
            # Random mouse movements
            actions = ActionChains(driver)
            for _ in range(random.randint(2, 5)):
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                actions.move_by_offset(x, y).perform()
                time.sleep(random.uniform(0.1, 0.3))

            # Random scrolling
            for _ in range(random.randint(1, 3)):
                scroll_amount = random.randint(200, 500)
                driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(random.uniform(0.5, 1.5))

            # Random short pause like reading
            time.sleep(random.uniform(1, 3))

        except Exception as e:
            print(f"⚠️ Human behavior simulation failed: {e}")

    def scrape_fiverr_bypass(self, keyword="logo design", pages=3):
        """Ultra-stealth Fiverr scraping with bot bypass"""
        print("🚀 UNNAMEDDESIGN FIVERR BOT BYPASS SCRAPER")
        print("=" * 50)
        print(f"🎯 Target: {keyword}")
        print(f"📄 Pages: {pages}")
        print("🔒 Bot Bypass Mode: ACTIVATED")

        try:
            # Setup undetected driver
            print("🔧 Setting up undetected Chrome driver...")
            self.driver = self.setup_undetected_driver()

            # Navigate to Fiverr with human-like behavior
            base_url = f"https://www.fiverr.com/search/gigs?query={keyword.replace(' ', '%20')}&page=1"
            print(f"🌐 Navigating to: {base_url}")

            self.driver.get(base_url)
            self.human_like_delay(3, 5)  # Wait like a human

            # Check if blocked
            page_title = self.driver.title
            if 'blocked' in page_title.lower() or 'verification' in page_title.lower() or 'human' in page_title.lower():
                print(f"🚫 BLOCKED: {page_title}")
                print("💡 Trying alternative bypass techniques...")

                # Try alternative bypass method
                return self.scrape_fiverr_alternative(keyword, pages)

            print(f"✅ Page loaded: {page_title}")

            # Simulate human behavior
            self.simulate_human_behavior(self.driver)

            # Scrape multiple pages
            for page in range(1, pages + 1):
                print(f"\n📄 SCRAPING PAGE {page}/{pages}")
                print("-" * 30)

                if page > 1:
                    # Navigate to next page
                    next_url = f"https://www.fiverr.com/search/gigs?query={keyword.replace(' ', '%20')}&page={page}"
                    print(f"➡️  Next page: {next_url}")
                    self.driver.get(next_url)
                    self.human_like_delay(2, 4)

                    # Check if blocked on new page
                    current_title = self.driver.title
                    if 'blocked' in current_title.lower() or 'verification' in current_title.lower():
                        print(f"🚫 BLOCKED on page {page}: {current_title}")
                        break

                success = self.extract_fiverr_gigs(page, keyword)
                if not success:
                    print(f"⚠️ Page {page} extraction failed")
                    continue

                # Human-like delay between pages
                if page < pages:
                    self.human_like_delay(3, 6)

            # Show results
            self.show_fiverr_results(keyword)

        except Exception as e:
            print(f"❌ Scraping error: {e}")
        finally:
            if self.driver:
                self.driver.quit()

    def scrape_fiverr_alternative(self, keyword="logo design", pages=3):
        """Alternative Fiverr scraping method if main method fails"""
        print("🔄 ALTERNATIVE BYPASS METHOD")
        print("=" * 30)

        try:
            # Try with minimal options
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            options.add_argument('--window-size=1366,768')

            self.driver = webdriver.Chrome(options=options)

            # Simple stealth
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            base_url = f"https://www.fiverr.com/search/gigs?query={keyword.replace(' ', '%20')}&page=1"
            print(f"🌐 Alternative navigation to: {base_url}")

            self.driver.get(base_url)
            time.sleep(5)

            page_title = self.driver.title
            if 'blocked' in page_title.lower() or 'verification' in page_title.lower():
                print(f"🚫 ALTERNATIVE METHOD ALSO BLOCKED: {page_title}")
                return

            print(f"✅ Alternative method successful: {page_title}")

            # Continue with extraction
            for page in range(1, pages + 1):
                if page > 1:
                    next_url = f"https://www.fiverr.com/search/gigs?query={keyword.replace(' ', '%20')}&page={page}"
                    self.driver.get(next_url)
                    time.sleep(3)

                self.extract_fiverr_gigs(page, keyword)
                time.sleep(random.uniform(2, 4))

            self.show_fiverr_results(keyword)

        except Exception as e:
            print(f"❌ Alternative method failed: {e}")

    def extract_fiverr_gigs(self, page_num, keyword):
        """Extract gig data from Fiverr page"""
        try:
            # Wait for gigs to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-gig-id]"))
            )

            # Find gig cards
            gig_selectors = [
                "[data-gig-id]",
                ".gig-card",
                "article",
                ".search-results > div",
                "[data-testid*='gig']",
                ".gig-wrapper"
            ]

            gigs = []
            for selector in gig_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements and len(elements) > 5:  # Must have reasonable number of gigs
                        gigs = elements
                        print(f"🎯 Found {len(gigs)} gigs with '{selector}'")
                        break
                except:
                    continue

            if not gigs:
                print("❌ No gig elements found")
                return False

            # Extract data from each gig
            for i, gig in enumerate(gigs[:20]):  # Limit to 20 per page
                try:
                    gig_data = self.extract_gig_data(gig, page_num, i+1, keyword)
                    if gig_data:
                        self.data.append(gig_data)
                        self.total_gigs_processed += 1

                        # Show progress
                        price = gig_data.get('price', 'N/A')
                        rating = gig_data.get('rating', 'N/A')
                        seller = gig_data.get('seller_name', 'Unknown')
                        print(f"  ✅ Gig {i+1}: ${price} - {rating}⭐ - {seller}")

                except Exception as e:
                    continue

            return True

        except Exception as e:
            print(f"❌ Gig extraction error: {e}")
            return False

    def extract_gig_data(self, gig_element, page_num, gig_num, keyword):
        """Extract detailed gig data from Selenium element"""
        try:
            gig_text = gig_element.text

            # Extract seller name
            seller = None
            seller_selectors = ['.seller-name', '.username', '.seller-link', 'a[href*="/users/"]']
            for selector in seller_selectors:
                try:
                    seller_elem = gig_element.find_element(By.CSS_SELECTOR, selector)
                    seller = seller_elem.text.strip()
                    if seller:
                        break
                except:
                    continue

            # Extract title
            title = None
            title_selectors = ['h3', '.gig-title', '.title', 'a[href*="/gig/"]']
            for selector in title_selectors:
                try:
                    title_elem = gig_element.find_element(By.CSS_SELECTOR, selector)
                    title = title_elem.text.strip()
                    if title and len(title) > 10:
                        break
                except:
                    continue

            # Extract price
            price = None
            price_selectors = ['.price', '.gig-price', '[data-price]']
            for selector in price_selectors:
                try:
                    price_elem = gig_element.find_element(By.CSS_SELECTOR, selector)
                    price_text = price_elem.text.strip()
                    price_match = re.search(r'\$?(\d+)', price_text)
                    if price_match:
                        price = int(price_match.group(1))
                        break
                except:
                    continue

            # Fallback: regex from text
            if not price:
                price_matches = re.findall(r'\$(\d+)', gig_text)
                if price_matches:
                    price = int(price_matches[0])

            # Extract rating
            rating = None
            rating_selectors = ['.rating', '.stars', '[data-rating]']
            for selector in rating_selectors:
                try:
                    rating_elem = gig_element.find_element(By.CSS_SELECTOR, selector)
                    rating_text = rating_elem.text.strip()
                    rating_match = re.search(r'(\d\.\d)', rating_text)
                    if rating_match:
                        rating = float(rating_match.group(1))
                        break
                except:
                    continue

            # Fallback: regex from text
            if not rating:
                rating_matches = re.findall(r'(\d\.\d)', gig_text)
                if rating_matches:
                    rating = float(rating_matches[0])

            # Extract reviews
            reviews = None
            review_matches = re.findall(r'\((\d+)\)', gig_text)
            if review_matches:
                reviews = int(review_matches[0])

            # Extract delivery time
            delivery_time = None
            delivery_patterns = [
                r'(\d+)\s*days?\s*delivery',
                r'delivery\s*in\s*(\d+)\s*days?',
                r'(\d+)\s*day',
                r'(\d+)d'
            ]

            for pattern in delivery_patterns:
                matches = re.findall(pattern, gig_text.lower())
                if matches:
                    delivery_time = int(matches[0])
                    break

            # Classify work type
            work_type = self.classify_work_type(gig_text)

            # Calculate seller level
            seller_level = self.extract_seller_level(gig_text)

            if title or price or seller:
                return {
                    'source': f'fiverr_page_{page_num}_gig_{gig_num}',
                    'page': page_num,
                    'gig_num': gig_num,
                    'seller_name': seller,
                    'seller_level': seller_level,
                    'title': title,
                    'price': price,
                    'rating': rating,
                    'reviews': reviews,
                    'delivery_days': delivery_time,
                    'work_type': work_type,
                    'keyword': keyword,
                    'extraction_method': 'selenium_bypass',
                    'extraction_time': datetime.now().strftime('%H:%M:%S')
                }

        except Exception as e:
            print(f"⚠️ Gig data extraction error: {e}")

        return None

    def classify_work_type(self, gig_text):
        """Classify work type based on gig content"""
        text_lower = gig_text.lower()

        if any(word in text_lower for word in ['logo', 'brand', 'identity', 'branding']):
            return 'logo_design'
        elif any(word in text_lower for word in ['website', 'web design', 'ui/ux', 'landing page']):
            return 'web_design'
        elif any(word in text_lower for word in ['mobile app', 'ios', 'android', 'app']):
            return 'mobile_app'
        elif any(word in text_lower for word in ['illustration', 'drawing', 'art', 'digital art']):
            return 'illustration'
        elif any(word in text_lower for word in ['marketing', 'social media', 'advertising']):
            return 'marketing'
        elif any(word in text_lower for word in ['video', 'animation', 'motion graphics']):
            return 'video_animation'
        else:
            return 'other'

    def extract_seller_level(self, gig_text):
        """Extract seller level from gig text"""
        text_lower = gig_text.lower()

        if 'top rated' in text_lower:
            return 'Top Rated'
        elif 'level 2' in text_lower:
            return 'Level 2'
        elif 'level 1' in text_lower:
            return 'Level 1'
        elif 'vetted' in text_lower or 'verified' in text_lower:
            return 'Vetted'
        else:
            return 'New'

    def show_fiverr_results(self, keyword):
        """Show comprehensive Fiverr analysis"""
        if not self.data:
            print("❌ No data collected")
            return

        print(f"\n🎯 UNNAMEDDESIGN FIVERR ANALYSIS for '{keyword}'")
        print("=" * 60)
        print(f"📊 Total gigs processed: {self.total_gigs_processed}")

        # Analyze data
        prices = []
        ratings = []
        reviews = []
        sellers = []
        seller_levels = []
        work_types = []
        delivery_times = []

        for gig in self.data:
            if gig.get('price'):
                prices.append(gig['price'])
            if gig.get('rating'):
                ratings.append(gig['rating'])
            if gig.get('reviews'):
                reviews.append(gig['reviews'])
            if gig.get('seller_name'):
                sellers.append(gig['seller_name'])
            if gig.get('seller_level'):
                seller_levels.append(gig['seller_level'])
            if gig.get('work_type'):
                work_types.append(gig['work_type'])
            if gig.get('delivery_days'):
                delivery_times.append(gig['delivery_days'])

        # Pricing Analysis
        if prices:
            print(f"\n💰 PRICING ANALYSIS:")
            print(f"   Total gigs with prices: {len(prices)}")
            print(f"   Range: ${min(prices)} - ${max(prices)}")
            print(f"   Average: ${sum(prices)/len(prices):.2f}")
            print(f"   Median: ${sorted(prices)[len(prices)//2]}")

            # Price distribution
            sorted_prices = sorted(prices)
            if len(sorted_prices) >= 4:
                q1 = sorted_prices[len(sorted_prices)//4]
                q3 = sorted_prices[len(sorted_prices)*3//4]

                print(f"\n🎯 PRICING TIERS FOR UNNAMEDDESIGN:")
                print(f"   💸 Budget: ${min(prices)}-${q1}")
                print(f"   ⭐ Standard: ${q1}-${q3}")
                print(f"   👑 Premium: ${q3}-${max(prices)}")

        # Quality Analysis
        if ratings:
            print(f"\n⭐ QUALITY STANDARDS:")
            print(f"   Average rating: {sum(ratings)/len(ratings):.2f}")
            print(f"   Range: {min(ratings)} - {max(ratings)}")
            print(f"   Target for your artists: {sum(ratings)/len(ratings):.1f}+")

        # Seller Analysis
        if seller_levels:
            from collections import Counter
            level_counts = Counter(seller_levels)
            print(f"\n🏆 SELLER LEVEL BREAKDOWN:")
            for level, count in level_counts.most_common():
                percentage = (count / len(seller_levels)) * 100
                print(f"   • {level}: {count} sellers ({percentage:.1f}%)")

        # Work Type Analysis
        if work_types:
            from collections import Counter
            type_counts = Counter(work_types)
            print(f"\n🎨 WORK TYPE BREAKDOWN:")
            for work_type, count in type_counts.most_common():
                percentage = (count / len(work_types)) * 100
                print(f"   • {work_type.replace('_', ' ').title()}: {count} gigs ({percentage:.1f}%)")

        # Delivery Analysis
        if delivery_times:
            print(f"\n⏰ DELIVERY TIME ANALYSIS:")
            print(f"   Average delivery: {sum(delivery_times)/len(delivery_times):.1f} days")
            print(f"   Range: {min(delivery_times)}-{max(delivery_times)} days")

        # Business Recommendations
        print(f"\n💡 BUSINESS RECOMMENDATIONS FOR UNNAMEDDESIGN:")
        if prices:
            sweet_spot_min = sorted(prices)[len(prices)//3]
            sweet_spot_max = sorted(prices)[len(prices)*2//3]
            print(f"   🎯 Sweet spot: ${sweet_spot_min}-${sweet_spot_max}")
            print(f"   💼 Target price: ${sweet_spot_min + (sweet_spot_max - sweet_spot_min)//2}")

        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            if avg_rating >= 4.8:
                print("   ✅ High quality market - focus on premium positioning")
            elif avg_rating >= 4.5:
                print("   📈 Competitive market - emphasize quality and speed")

        # Save data
        self.save_fiverr_data(keyword)

    def save_fiverr_data(self, keyword):
        """Save comprehensive Fiverr data"""
        if not self.data:
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"fiverr_{keyword.replace(' ', '_')}_bypass_{timestamp}.csv"

        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)

        print(f"\n💾 Data saved to: {filename}")
        print(f"📊 Records: {len(self.data)}")

        # Also save JSON summary
        summary = {
            'keyword': keyword,
            'total_gigs': len(self.data),
            'extraction_time': datetime.now().isoformat(),
            'analysis': {
                'price_range': [min([g.get('price', 0) for g in self.data if g.get('price')]),
                               max([g.get('price', 0) for g in self.data if g.get('price')])],
                'avg_rating': sum([g.get('rating', 0) for g in self.data if g.get('rating')]) / len([g for g in self.data if g.get('rating')]) if any(g.get('rating') for g in self.data) else 0,
                'work_types': list(set([g.get('work_type') for g in self.data if g.get('work_type')])),
                'seller_levels': list(set([g.get('seller_level') for g in self.data if g.get('seller_level')]))
            }
        }

        json_filename = filename.replace('.csv', '.json')
        with open(json_filename, 'w') as f:
            json.dump(summary, f, indent=2, default=str)

        print(f"📋 Summary saved to: {json_filename}")

def main():
    """Main function with advanced options"""
    print("🚀 UNNAMEDDESIGN FIVERR BOT BYPASS SCRAPER")
    print("=" * 50)
    print("🔒 Advanced bot detection bypass techniques")
    print("🎯 Specialized for Fiverr scraping")

    # Get user input
    keyword = input("🎯 Enter keyword (e.g., 'logo design'): ").strip()
    if not keyword:
        keyword = "logo design"
        print(f"Using default: '{keyword}'")

    pages = input("📄 Number of pages to scrape (default 3): ").strip()
    try:
        pages = int(pages) if pages else 3
    except:
        pages = 3

    # Start Fiverr scraping with bot bypass
    scraper = FiverrBotBypassScraper()
    scraper.scrape_fiverr_bypass(keyword, pages)

if __name__ == "__main__":
    main()
