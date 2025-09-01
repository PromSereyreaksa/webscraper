"""
UnnamedDesign Ultra-Stealth Fiverr Scraper
==========================================
Bypasses PerimeterX, Cloudflare, and advanced bot detection
"""
import re
import time
import random
import json
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd

class UltraStealthFiverrScraper:
    def __init__(self):
        self.driver = None
        self.session = None
        self.data = []
        self.total_gigs_processed = 0

    def setup_ultra_stealth_driver(self):
        """Setup Chrome driver with maximum stealth capabilities"""
        print("🔧 Setting up ultra-stealth Chrome driver...")

        options = Options()

        # Essential system flags
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')

        # Keep JavaScript enabled for real interaction
        # options.add_argument('--disable-javascript')  # DON'T disable JS

        # Advanced stealth options
        options.add_argument('--disable-blink-features=AutomationControlled')
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

        # Realistic browser configuration
        options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-notifications')

        # Language and locale
        options.add_argument('--lang=en-US')
        options.add_argument('--accept-lang=en-US,en')

        # Disable automation indicators (use proper format)
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # Advanced preferences
        options.add_experimental_option("prefs", {
            "profile.password_manager_enabled": False,
            "credentials_enable_service": False,
            "profile.default_content_setting_values.notifications": 2,
            "profile.managed_default_content_settings.images": 1,
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.geolocation": 2,
            "profile.managed_default_content_settings.media_stream": 2,
            "profile.managed_default_content_settings.plugins": 2,
            "profile.managed_default_content_settings.popups": 2,
            "profile.managed_default_content_settings.auto_select_certificate": 2,
            "profile.managed_default_content_settings.fullscreen": 2,
            "profile.managed_default_content_settings.mouselock": 2,
            "profile.managed_default_content_settings.mixed_script": 2,
            "profile.managed_default_content_settings.media_stream_mic": 2,
            "profile.managed_default_content_settings.media_stream_camera": 2,
            "profile.managed_default_content_settings.protocol_handlers": 2,
            "profile.managed_default_content_settings.ppapi_broker": 2,
            "profile.managed_default_content_settings.automatic_downloads": 2,
            "profile.managed_default_content_settings.midi_sysex": 2,
            "profile.managed_default_content_settings.push_messaging": 2,
            "profile.managed_default_content_settings.ssl_cert_decisions": 2,
            "profile.managed_default_content_settings.metro_switch_to_desktop": 2,
            "profile.managed_default_content_settings.protected_media_identifier": 2,
            "profile.managed_default_content_settings.app_banner": 2,
            "profile.managed_default_content_settings.site_engagement": 2,
            "profile.managed_default_content_settings.durable_storage": 2,
        })

        # Create driver
        try:
            self.driver = webdriver.Chrome(options=options)
        except Exception as e:
            print(f"❌ Failed to create Chrome driver: {e}")
            return None

        # Execute comprehensive stealth scripts
        stealth_scripts = [
            # Remove webdriver property
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",

            # Mock plugins
            "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})",

            # Mock languages
            "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})",

            # Mock chrome runtime
            "window.navigator.chrome = {runtime: {}, loadTimes: function() {}, csi: function() {}, app: {}}",

            # Mock platform
            "Object.defineProperty(navigator, 'platform', {get: () => 'Linux x86_64'})",

            # Mock hardware concurrency
            "Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8})",

            # Mock device memory
            "Object.defineProperty(navigator, 'deviceMemory', {get: () => 8})",

            # Mock battery API
            """
            Object.defineProperty(navigator, 'getBattery', {
                value: () => Promise.resolve({
                    charging: true,
                    chargingTime: Infinity,
                    dischargingTime: Infinity,
                    level: 1
                })
            });
            """,

            # Override permissions
            """
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            """,

            # Mock screen properties
            "Object.defineProperty(screen, 'availHeight', {get: () => 1040})",
            "Object.defineProperty(screen, 'availWidth', {get: () => 1920})",
            "Object.defineProperty(screen, 'height', {get: () => 1080})",
            "Object.defineProperty(screen, 'width', {get: () => 1920})",

            # Mock timezone
            "Object.defineProperty(Intl, 'DateTimeFormat', {value: class extends Intl.DateTimeFormat {resolvedOptions() {return {...super.resolvedOptions(), timeZone: 'America/New_York'}}}})",

            # Mock WebGL
            """
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) return 'Intel Inc.';
                if (parameter === 37446) return 'Intel(R) Iris(TM) Graphics 6100';
                return getParameter.call(this, parameter);
            };
            """
        ]

        for script in stealth_scripts:
            try:
                self.driver.execute_script(script)
            except Exception as e:
                print(f"⚠️ Stealth script failed: {e}")
                continue

        print("✅ Ultra-stealth driver ready!")
        return self.driver

    def simulate_human_behavior(self):
        """Simulate realistic human browsing behavior"""
        if not self.driver:
            return

        try:
            print("🤖 Simulating human behavior...")

            # Random initial delay
            time.sleep(random.uniform(2, 4))

            # Random mouse movements
            actions = ActionChains(self.driver)
            for _ in range(random.randint(3, 7)):
                x = random.randint(100, 1800)
                y = random.randint(100, 1000)
                actions.move_by_offset(x, y).perform()
                time.sleep(random.uniform(0.1, 0.3))

            # Random scrolling
            for _ in range(random.randint(2, 5)):
                scroll_amount = random.randint(300, 800)
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(random.uniform(0.8, 2.0))

                # Occasional pause like reading
                if random.random() < 0.3:
                    time.sleep(random.uniform(1, 3))

            # Random mouse clicks (safe areas)
            for _ in range(random.randint(1, 3)):
                x = random.randint(200, 1700)
                y = random.randint(200, 900)
                actions.move_by_offset(x, y).click().perform()
                time.sleep(random.uniform(0.5, 1.5))

            print("✅ Human behavior simulation complete")

        except Exception as e:
            print(f"⚠️ Human behavior simulation failed: {e}")

    def wait_for_page_load(self, timeout=30):
        """Wait for page to fully load with human-like timing"""
        try:
            # Wait for document ready
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )

            # Additional wait for dynamic content
            time.sleep(random.uniform(2, 4))

            # Check for common loading indicators
            loading_indicators = [
                ".loading", ".spinner", "[data-loading]",
                ".skeleton", ".placeholder"
            ]

            for indicator in loading_indicators:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, indicator)
                    if elements:
                        print(f"⏳ Waiting for loading indicator: {indicator}")
                        WebDriverWait(self.driver, 10).until(
                            EC.invisibility_of_element_located((By.CSS_SELECTOR, indicator))
                        )
                except:
                    continue

            return True

        except Exception as e:
            print(f"⚠️ Page load wait failed: {e}")
            return False

    def check_for_blocks(self):
        """Check if page is blocked by bot detection"""
        if not self.driver:
            return False

        try:
            title = self.driver.title.lower()
            body_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()

            block_indicators = [
                'blocked', 'verification', 'human', 'robot', 'captcha',
                'pxcr', 'perimeterx', 'cloudflare', 'access denied',
                'security check', 'rate limit', 'too many requests'
            ]

            for indicator in block_indicators:
                if indicator in title or indicator in body_text:
                    print(f"🚫 BLOCK DETECTED: Found '{indicator}' in page")
                    return True

            # Check for specific error codes
            if 'pxcr' in body_text or 'errcode' in body_text:
                print("🚫 PerimeterX BLOCK DETECTED")
                return True

            return False

        except Exception as e:
            print(f"⚠️ Block check failed: {e}")
            return False

    def scrape_fiverr_search(self, keyword="logo design", pages=3):
        """Main Fiverr scraping function with ultra-stealth"""
        print("🚀 UNNAMEDDESIGN ULTRA-STEALTH FIVERR SCRAPER")
        print("=" * 60)
        print(f"🎯 Target: {keyword}")
        print(f"📄 Pages: {pages}")
        print("🔒 Ultra-stealth mode activated")

        try:
            # Setup ultra-stealth driver
            if not self.setup_ultra_stealth_driver():
                print("❌ Failed to setup stealth driver")
                return

            # Navigate to Fiverr search
            base_url = f"https://www.fiverr.com/search/gigs?query={keyword.replace(' ', '%20')}&page=1"
            print(f"🌐 Navigating to: {base_url}")

            self.driver.get(base_url)

            # Wait for page load
            if not self.wait_for_page_load():
                print("❌ Page failed to load properly")
                return

            # Check for blocks
            if self.check_for_blocks():
                print("💡 Trying recovery techniques...")

                # Try recovery: refresh and wait
                time.sleep(5)
                self.driver.refresh()
                time.sleep(3)

                if self.check_for_blocks():
                    print("❌ Still blocked - trying alternative approach")
                    return self.scrape_fiverr_http_fallback(keyword, pages)

            print(f"✅ Page loaded successfully: {self.driver.title}")

            # Simulate human behavior
            self.simulate_human_behavior()

            # Scrape multiple pages
            for page in range(1, pages + 1):
                print(f"\n📄 SCRAPING PAGE {page}/{pages}")
                print("-" * 40)

                if page > 1:
                    # Navigate to next page
                    next_url = f"https://www.fiverr.com/search/gigs?query={keyword.replace(' ', '%20')}&page={page}"
                    print(f"➡️ Next page: {next_url}")

                    self.driver.get(next_url)

                    if not self.wait_for_page_load():
                        print(f"⚠️ Page {page} failed to load")
                        continue

                    if self.check_for_blocks():
                        print(f"🚫 Page {page} blocked - skipping")
                        continue

                    # Human behavior on each page
                    self.simulate_human_behavior()

                # Extract gigs from current page
                success = self.extract_fiverr_gigs(page, keyword)
                if not success:
                    print(f"⚠️ Failed to extract gigs from page {page}")
                    continue

                # Human-like delay between pages
                if page < pages:
                    delay = random.uniform(4, 8)
                    print(f"😴 Human-like delay: {delay:.1f}s")
                    time.sleep(delay)

            # Show results
            self.show_fiverr_results(keyword)

        except Exception as e:
            print(f"❌ Scraping error: {e}")
        finally:
            if self.driver:
                self.driver.quit()

    def scrape_fiverr_http_fallback(self, keyword="logo design", pages=3):
        """HTTP fallback when Selenium is blocked"""
        print("🔄 HTTP FALLBACK MODE")
        print("=" * 30)

        # Setup stealth HTTP session
        self.setup_stealth_session()

        for page in range(1, pages + 1):
            try:
                url = f"https://www.fiverr.com/search/gigs?query={keyword.replace(' ', '%20')}&page={page}"
                print(f"🌐 HTTP request: Page {page}")

                response = self.session.get(url, timeout=15)

                if response.status_code == 200:
                    print(f"✅ HTTP {response.status_code} - {len(response.text)} chars")

                    if self.extract_fiverr_from_html(response.text, page, keyword):
                        print(f"📊 Extracted data from page {page}")
                    else:
                        print(f"⚠️ No data found in page {page}")

                elif response.status_code == 403:
                    print(f"🚫 HTTP {response.status_code} - Blocked")
                    break
                else:
                    print(f"⚠️ HTTP {response.status_code}")

                # Human-like delay
                time.sleep(random.uniform(3, 6))

            except Exception as e:
                print(f"❌ HTTP error page {page}: {e}")

        if self.data:
            self.show_fiverr_results(keyword)
        else:
            print("❌ No data collected from HTTP fallback")

    def setup_stealth_session(self):
        """Setup HTTP session with advanced stealth headers"""
        self.session = requests.Session()

        # Comprehensive headers to mimic real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'Sec-Purpose': 'prefetch',
        }

        self.session.headers.update(headers)

        # Add realistic cookies
        self.session.cookies.set('__cfduid', 'd' + str(random.randint(1000000000, 9999999999)), domain='.fiverr.com')
        self.session.cookies.set('visitor_id', str(random.randint(100000000, 999999999)), domain='.fiverr.com')
        self.session.cookies.set('_gcl_au', '1.1.' + str(random.randint(1000000000, 9999999999)), domain='.fiverr.com')

        return self.session

    def extract_fiverr_gigs(self, page_num, keyword):
        """Extract gig data from Fiverr page using Selenium"""
        try:
            # Wait for gig elements to load
            gig_selectors = [
                "[data-gig-id]",
                ".gig-card",
                "article",
                ".search-results > div",
                "[data-testid*='gig']",
                ".gig-wrapper",
                ".gig-item"
            ]

            gigs = []
            for selector in gig_selectors:
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements and len(elements) > 5:  # Must have substantial results
                        gigs = elements
                        print(f"🎯 Found {len(gigs)} gigs with selector: {selector}")
                        break
                except:
                    continue

            if not gigs:
                print("❌ No gig elements found")
                return False

            # Extract data from each gig
            for i, gig in enumerate(gigs[:20]):  # Limit to 20 per page
                try:
                    gig_data = self.extract_gig_data_selenium(gig, page_num, i+1, keyword)
                    if gig_data:
                        self.data.append(gig_data)
                        self.total_gigs_processed += 1

                        # Show progress
                        price = gig_data.get('price', 'N/A')
                        rating = gig_data.get('rating', 'N/A')
                        reviews = gig_data.get('reviews', 'N/A')
                        print(f"  ✅ Gig {i+1}: ${price} - {rating}⭐ - {reviews} reviews")

                except Exception as e:
                    continue

            return True

        except Exception as e:
            print(f"❌ Gig extraction error: {e}")
            return False

    def extract_gig_data_selenium(self, gig_element, page_num, gig_num, keyword):
        """Extract detailed gig data from Selenium element"""
        try:
            gig_text = gig_element.text

            # Extract title
            title_selectors = ['h2', 'h3', 'h4', '.job-title', '.title', '.gig-title']
            title = None
            for selector in title_selectors:
                try:
                    title_elem = gig_element.find_element(By.CSS_SELECTOR, selector)
                    title = title_elem.text.strip()
                    if title and len(title) > 5:
                        break
                except:
                    continue

            # Extract seller name
            seller_selectors = ['.seller-name', '.user-name', '.seller-link', '[data-user*=""']
            seller_name = None
            for selector in seller_selectors:
                try:
                    seller_elem = gig_element.find_element(By.CSS_SELECTOR, selector)
                    seller_name = seller_elem.text.strip()
                    if seller_name:
                        break
                except:
                    continue

            # Extract seller level
            seller_level = None
            level_indicators = ['level', 'top rated', 'vetted', 'pro']
            gig_lower = gig_text.lower()
            for level in level_indicators:
                if level in gig_lower:
                    seller_level = level.title()
                    break

            # Extract price
            price = None
            price_patterns = [
                r'\$([\d,]+)',
                r'From\s*\$([\d,]+)',
                r'Starting\s*at\s*\$([\d,]+)'
            ]

            for pattern in price_patterns:
                match = re.search(pattern, gig_text)
                if match:
                    price_str = match.group(1).replace(',', '')
                    try:
                        price = int(price_str)
                        if 5 <= price <= 10000:  # Reasonable price range
                            break
                    except:
                        continue

            # Extract rating
            rating = None
            rating_match = re.search(r'(\d\.\d)', gig_text)
            if rating_match:
                try:
                    rating_val = float(rating_match.group(1))
                    if 3.0 <= rating_val <= 5.0:
                        rating = rating_val
                except:
                    pass

            # Extract reviews
            reviews = None
            review_match = re.search(r'\((\d+)\)', gig_text)
            if review_match:
                try:
                    reviews_val = int(review_match.group(1))
                    if 1 <= reviews_val <= 50000:
                        reviews = reviews_val
                except:
                    pass

            # Extract delivery time
            delivery_time = None
            delivery_patterns = [
                r'(\d+)\s*days?\s*delivery',
                r'delivery\s*in\s*(\d+)\s*days?',
                r'(\d+)\s*day\s*turnaround',
                r'within\s*(\d+)\s*days?'
            ]

            for pattern in delivery_patterns:
                match = re.search(pattern, gig_text.lower())
                if match:
                    try:
                        delivery_time = int(match.group(1))
                        break
                    except:
                        continue

            # Classify work type
            work_type = self.classify_fiverr_work_type(gig_text)

            if title or price or seller_name:
                return {
                    'source': f'selenium_page_{page_num}_gig_{gig_num}',
                    'page': page_num,
                    'gig_num': gig_num,
                    'keyword': keyword,
                    'title': title,
                    'seller_name': seller_name,
                    'seller_level': seller_level,
                    'price': price,
                    'rating': rating,
                    'reviews': reviews,
                    'delivery_days': delivery_time,
                    'work_type': work_type,
                    'extraction_method': 'selenium_ultra_stealth',
                    'extraction_time': datetime.now().strftime('%H:%M:%S')
                }

        except Exception as e:
            print(f"⚠️ Gig data extraction error: {e}")

        return None

    def extract_fiverr_from_html(self, html, page_num, keyword):
        """Extract Fiverr data from HTML content"""
        try:
            gigs_found = 0

            # Extract seller names
            seller_patterns = [
                r'data-user="([^"]+)"',
                r'seller-name[^>]*>([^<]+)',
                r'user-name[^>]*>([^<]+)'
            ]

            sellers = []
            for pattern in seller_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                if matches:
                    sellers.extend(matches)
                    break

            # Extract titles
            title_patterns = [
                r'data-title="([^"]+)"',
                r'gig-title[^>]*>([^<]+)',
                r'job-title[^>]*>([^<]+)'
            ]

            titles = []
            for pattern in title_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                if matches:
                    titles.extend(matches)
                    break

            # Extract prices
            prices = re.findall(r'\$([\d,]+)', html)

            # Extract ratings
            ratings = re.findall(r'(\d\.\d)', html)

            # Extract reviews
            reviews = re.findall(r'\((\d+)\)', html)

            # Create data records
            max_items = max(len(sellers), len(titles), len(prices), len(ratings), len(reviews))

            for i in range(min(max_items, 15)):  # Limit to 15
                gig_data = {
                    'source': f'http_page_{page_num}_gig_{i+1}',
                    'page': page_num,
                    'gig_num': i+1,
                    'keyword': keyword,
                    'extraction_method': 'http_fallback',
                    'extraction_time': datetime.now().strftime('%H:%M:%S')
                }

                if i < len(sellers):
                    gig_data['seller_name'] = sellers[i]
                if i < len(titles):
                    gig_data['title'] = titles[i]
                if i < len(prices):
                    try:
                        gig_data['price'] = int(prices[i].replace(',', ''))
                    except:
                        pass
                if i < len(ratings):
                    try:
                        gig_data['rating'] = float(ratings[i])
                    except:
                        pass
                if i < len(reviews):
                    try:
                        gig_data['reviews'] = int(reviews[i])
                    except:
                        pass

                if any(gig_data.get(key) for key in ['seller_name', 'title', 'price']):
                    self.data.append(gig_data)
                    gigs_found += 1

            return gigs_found > 0

        except Exception as e:
            print(f"❌ HTML extraction error: {e}")
            return False

    def classify_fiverr_work_type(self, gig_text):
        """Classify Fiverr gig work type"""
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
        elif any(word in text_lower for word in ['writing', 'content', 'copywriting']):
            return 'writing'
        else:
            return 'other'

    def show_fiverr_results(self, keyword):
        """Show comprehensive Fiverr analysis"""
        if not self.data:
            print("❌ No data to analyze")
            return

        print(f"\n🎯 UNNAMEDDESIGN FIVERR ANALYSIS for '{keyword}'")
        print("=" * 60)
        print(f"📊 Total gigs processed: {self.total_gigs_processed}")

        # Analyze data
        prices = []
        ratings = []
        reviews_list = []
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
                reviews_list.append(gig['reviews'])
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
            print(f"   Average: ${sum(prices)/len(prices):.0f}")
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

        # Competition Analysis
        if reviews_list:
            print(f"\n🏁 COMPETITION ANALYSIS:")
            print(f"   Average reviews: {sum(reviews_list)/len(reviews_list):.0f}")
            print(f"   Range: {min(reviews_list)}-{max(reviews_list)} reviews")

        # Seller Analysis
        if sellers:
            print(f"\n👥 SELLER ANALYSIS:")
            print(f"   Unique sellers found: {len(set(sellers))}")

        if seller_levels:
            from collections import Counter
            level_counts = Counter(seller_levels)
            print(f"   Seller level distribution:")
            for level, count in level_counts.most_common():
                print(f"      • {level}: {count} sellers")

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
            print(f"   💼 Recommended starting price: ${sweet_spot_min + (sweet_spot_max - sweet_spot_min)//2}")

        if ratings:
            avg_rating = sum(ratings)/len(ratings)
            if avg_rating >= 4.8:
                print("   ✅ High quality standards - aim for 4.8+ ratings")
            elif avg_rating >= 4.5:
                print("   📈 Good quality standards - target 4.5+ ratings")

        # Save data
        self.save_fiverr_data(keyword)

    def save_fiverr_data(self, keyword):
        """Save comprehensive Fiverr data"""
        if not self.data:
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"fiverr_{keyword.replace(' ', '_')}_ultra_stealth_{timestamp}.csv"

        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)

        print(f"\n💾 Data saved to: {filename}")
        print(f"📊 Records: {len(self.data)}")

        # Also save JSON summary
        summary = {
            'keyword': keyword,
            'total_gigs': len(self.data),
            'extraction_time': datetime.now().isoformat(),
            'extraction_method': 'ultra_stealth_selenium',
            'analysis': {
                'prices': [gig.get('price') for gig in self.data if gig.get('price')],
                'ratings': [gig.get('rating') for gig in self.data if gig.get('rating')],
                'work_types': list(set([gig.get('work_type') for gig in self.data if gig.get('work_type')])),
                'seller_levels': list(set([gig.get('seller_level') for gig in self.data if gig.get('seller_level')]))
            }
        }

        json_filename = filename.replace('.csv', '_summary.json')
        with open(json_filename, 'w') as f:
            json.dump(summary, f, indent=2, default=str)

        print(f"📋 Summary saved to: {json_filename}")

def main():
    """Main function with advanced options"""
    print("🚀 UNNAMEDDESIGN ULTRA-STEALTH FIVERR SCRAPER")
    print("=" * 55)
    print("🔒 Bypasses PerimeterX, Cloudflare, and advanced bot detection")
    print("🤖 Includes human behavior simulation and stealth techniques")

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

    # Start ultra-stealth scraping
    scraper = UltraStealthFiverrScraper()
    scraper.scrape_fiverr_search(keyword, pages)

if __name__ == "__main__":
    main()
