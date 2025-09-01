"""
UnnamedDesign Advanced Stealth Scraper
=====================================
Ultra-stealth scraping with multiple bypass techniques
"""
import re
import requests
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

class AdvancedStealthScraper:
    def __init__(self, platform="upwork"):
        self.platform = platform
        self.driver = None
        self.session = None
        self.data = []
        self.total_jobs_processed = 0

    def setup_ultra_stealth_driver(self):
        """Setup the most stealthy Chrome driver possible"""
        options = Options()

        # Essential system flags
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')

        # Keep JavaScript enabled for real interaction
        # options.add_argument('--disable-javascript')  # DON'T disable JS

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
            "profile.managed_default_content_settings.images": 1,  # Load images
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

    def setup_stealth_session(self):
        """Setup HTTP session with advanced stealth headers"""
        self.session = requests.Session()

        # Advanced headers that mimic real browsers
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
        }

        self.session.headers.update(headers)

        # Add realistic cookies
        self.session.cookies.set('__cfduid', 'd1234567890abcdef', domain='.upwork.com')
        self.session.cookies.set('visitor_id', '123456789', domain='.upwork.com')

        return self.session

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

        except Exception as e:
            print(f"⚠️ Human behavior simulation failed: {e}")

    def scrape_upwork_stealth(self, keyword="logo design", pages=3):
        """Ultra-stealth Upwork scraping"""
        print("🚀 UNNAMEDDESIGN ADVANCED STEALTH SCRAPER")
        print("=" * 50)
        print(f"🎯 Target: {keyword}")
        print(f"📄 Pages: {pages}")
        print("🔒 Stealth Mode: ACTIVATED")

        try:
            # Setup ultra-stealth driver
            print("🔧 Setting up ultra-stealth driver...")
            self.driver = self.setup_ultra_stealth_driver()

            # Navigate to Upwork with human-like behavior
            base_url = f"https://www.upwork.com/nx/jobs/search/?q={keyword.replace(' ', '%20')}"
            print(f"🌐 Navigating to: {base_url}")

            self.driver.get(base_url)
            self.human_like_delay(3, 5)  # Wait like a human

            # Check if blocked
            page_title = self.driver.title
            if 'blocked' in page_title.lower() or 'verification' in page_title.lower():
                print(f"🚫 BLOCKED: {page_title}")
                print("💡 Trying alternative approach...")

                # Try HTTP approach as fallback
                return self.scrape_upwork_http(keyword, pages)

            print(f"✅ Page loaded: {page_title}")

            # Simulate human behavior
            self.simulate_human_behavior(self.driver)

            # Scrape multiple pages
            for page in range(1, pages + 1):
                print(f"\n📄 SCRAPING PAGE {page}/{pages}")
                print("-" * 30)

                if page > 1:
                    # Navigate to next page
                    next_url = f"{base_url}&page={page}"
                    print(f"➡️  Next page: {next_url}")
                    self.driver.get(next_url)
                    self.human_like_delay(2, 4)

                success = self.extract_upwork_jobs(page)
                if not success:
                    print(f"⚠️ Page {page} extraction failed")
                    continue

                # Human-like delay between pages
                if page < pages:
                    self.human_like_delay(3, 6)

            # Show results
            self.show_upwork_results(keyword)

        except Exception as e:
            print(f"❌ Scraping error: {e}")
        finally:
            if self.driver:
                self.driver.quit()

    def scrape_upwork_http(self, keyword="logo design", pages=3):
        """HTTP-based Upwork scraping as fallback"""
        print("🔄 FALLBACK: HTTP-based scraping")
        print("=" * 30)

        self.setup_stealth_session()

        for page in range(1, pages + 1):
            try:
                url = f"https://www.upwork.com/nx/jobs/search/?q={keyword.replace(' ', '%20')}&page={page}"
                print(f"🌐 HTTP request: Page {page}")

                response = self.session.get(url, timeout=10)

                if response.status_code == 200:
                    print(f"✅ HTTP {response.status_code} - {len(response.text)} chars")
                    self.extract_upwork_from_html(response.text, page, keyword)
                elif response.status_code == 403:
                    print(f"🚫 HTTP {response.status_code} - Blocked")
                    break
                else:
                    print(f"⚠️ HTTP {response.status_code}")

                time.sleep(random.uniform(2, 4))

            except Exception as e:
                print(f"❌ HTTP error page {page}: {e}")

        if self.data:
            self.show_upwork_results(keyword)
        else:
            print("❌ No data collected from HTTP approach either")

    def extract_upwork_jobs(self, page_num):
        """Extract job data from Upwork page"""
        try:
            # Wait for jobs to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-job-id]"))
            )

            # Find job cards
            job_selectors = [
                "[data-job-id]",
                ".job-tile",
                ".job-card",
                "article",
                ".up-card"
            ]

            jobs = []
            for selector in job_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        jobs = elements
                        print(f"🎯 Found {len(jobs)} jobs with '{selector}'")
                        break
                except:
                    continue

            if not jobs:
                print("❌ No job elements found")
                return False

            # Extract data from each job
            for i, job in enumerate(jobs[:15]):  # Limit to 15 per page
                try:
                    job_data = self.extract_job_data(job, page_num, i+1)
                    if job_data:
                        self.data.append(job_data)
                        self.total_jobs_processed += 1

                        # Show progress
                        budget = job_data.get('budget', 'N/A')
                        proposals = job_data.get('proposals', 'N/A')
                        print(f"  ✅ Job {i+1}: ${budget} - {proposals} proposals")

                except Exception as e:
                    continue

            return True

        except Exception as e:
            print(f"❌ Job extraction error: {e}")
            return False

    def extract_upwork_from_html(self, html, page_num, keyword):
        """Extract jobs from HTML content"""
        try:
            # Look for job data in HTML
            job_patterns = [
                r'data-job-id="([^"]+)"',
                r'class="[^"]*job[^"]*"[^>]*>(.*?)</div>',
                r'<article[^>]*>(.*?)</article>',
            ]

            jobs_found = 0
            for pattern in job_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
                if matches:
                    print(f"📊 Found {len(matches)} potential jobs via regex")
                    break

            # Extract basic data from HTML
            budgets = re.findall(r'\$[\d,]+(?:\s*-\s*\$[\d,]+)?', html)
            proposals = re.findall(r'(\d+)\s+proposals?', html, re.IGNORECASE)

            if budgets:
                print(f"💰 Found {len(budgets)} budget mentions")
            if proposals:
                print(f"📝 Found {len(proposals)} proposal counts")

            # Create basic data records
            max_items = max(len(budgets), len(proposals))
            for i in range(min(max_items, 10)):  # Limit to 10
                job_data = {
                    'source': f'http_page_{page_num}_job_{i+1}',
                    'page': page_num,
                    'job_num': i+1,
                    'keyword': keyword,
                    'extraction_method': 'http_regex',
                    'extraction_time': datetime.now().strftime('%H:%M:%S')
                }

                if i < len(budgets):
                    job_data['budget_raw'] = budgets[i]
                if i < len(proposals):
                    job_data['proposals'] = int(proposals[i])

                self.data.append(job_data)
                jobs_found += 1

            if jobs_found > 0:
                print(f"✅ Extracted {jobs_found} basic job records from HTML")

        except Exception as e:
            print(f"❌ HTML extraction error: {e}")

    def extract_job_data(self, job_element, page_num, job_num):
        """Extract detailed job data from Selenium element"""
        try:
            job_text = job_element.text

            # Extract title
            title_selectors = ['h2', 'h3', 'h4', '.job-title', '.title']
            title = None
            for selector in title_selectors:
                try:
                    title_elem = job_element.find_element(By.CSS_SELECTOR, selector)
                    title = title_elem.text.strip()
                    if title:
                        break
                except:
                    continue

            # Extract budget
            budget = None
            budget_patterns = [
                r'\$([\d,]+)',
                r'(\d+)\s*-\s*\$([\d,]+)',
                r'Budget:\s*\$([\d,]+)',
            ]

            for pattern in budget_patterns:
                match = re.search(pattern, job_text)
                if match:
                    if len(match.groups()) == 2:
                        budget = f"{match.group(1)}-{match.group(2)}"
                    else:
                        budget = match.group(1)
                    break

            # Extract proposals
            proposals = None
            proposal_match = re.search(r'(\d+)\s+proposals?', job_text, re.IGNORECASE)
            if proposal_match:
                proposals = int(proposal_match.group(1))

            # Extract posting time
            posting_time = None
            time_patterns = [
                r'Posted\s+(.+?)(?:\n|$)',
                r'(\d+)\s+(?:hours?|days?|weeks?)\s+ago',
            ]

            for pattern in time_patterns:
                match = re.search(pattern, job_text, re.IGNORECASE)
                if match:
                    posting_time = match.group(1).strip()
                    break

            # Classify job type
            job_type = self.classify_job_type(job_text)

            # Calculate complexity score
            complexity = self.calculate_complexity(job_text, budget, proposals)

            if title or budget:
                return {
                    'source': f'selenium_page_{page_num}_job_{job_num}',
                    'page': page_num,
                    'job_num': job_num,
                    'title': title,
                    'budget': budget,
                    'proposals': proposals,
                    'posting_time': posting_time,
                    'job_type': job_type,
                    'complexity_score': complexity,
                    'extraction_method': 'selenium',
                    'extraction_time': datetime.now().strftime('%H:%M:%S')
                }

        except Exception as e:
            print(f"⚠️ Job data extraction error: {e}")

        return None

    def classify_job_type(self, job_text):
        """Classify job type based on content"""
        text_lower = job_text.lower()

        if any(word in text_lower for word in ['logo', 'brand', 'identity']):
            return 'logo_design'
        elif any(word in text_lower for word in ['website', 'web design', 'ui/ux']):
            return 'web_design'
        elif any(word in text_lower for word in ['mobile app', 'ios', 'android']):
            return 'mobile_app'
        elif any(word in text_lower for word in ['illustration', 'drawing', 'art']):
            return 'illustration'
        elif any(word in text_lower for word in ['marketing', 'social media']):
            return 'marketing'
        else:
            return 'other'

    def calculate_complexity(self, job_text, budget, proposals):
        """Calculate job complexity score 1-10"""
        score = 5  # Base score

        # Budget factor
        if budget:
            try:
                budget_num = int(budget.replace('$', '').replace(',', '').split('-')[0])
                if budget_num > 1000:
                    score += 2
                elif budget_num > 500:
                    score += 1
                elif budget_num < 100:
                    score -= 1
            except:
                pass

        # Competition factor
        if proposals:
            if proposals > 50:
                score += 1
            elif proposals < 10:
                score -= 1

        # Content complexity
        complex_words = ['advanced', 'complex', 'sophisticated', 'professional', 'expert']
        simple_words = ['simple', 'basic', 'easy', 'quick']

        if any(word in job_text.lower() for word in complex_words):
            score += 1
        if any(word in job_text.lower() for word in simple_words):
            score -= 1

        return max(1, min(10, score))

    def show_upwork_results(self, keyword):
        """Show comprehensive Upwork analysis"""
        if not self.data:
            print("❌ No data to analyze")
            return

        print(f"\n🎯 UNNAMEDDESIGN UPWORK ANALYSIS for '{keyword}'")
        print("=" * 60)
        print(f"📊 Total jobs processed: {self.total_jobs_processed}")

        # Analyze budgets
        budgets = []
        proposals = []
        job_types = []
        complexities = []

        for job in self.data:
            if job.get('budget'):
                try:
                    budget_str = str(job['budget']).replace('$', '').replace(',', '')
                    if '-' in budget_str:
                        budget_val = int(budget_str.split('-')[0])
                    else:
                        budget_val = int(budget_str)
                    budgets.append(budget_val)
                except:
                    pass

            if job.get('proposals'):
                proposals.append(job['proposals'])

            if job.get('job_type'):
                job_types.append(job['job_type'])

            if job.get('complexity_score'):
                complexities.append(job['complexity_score'])

        # Budget Analysis
        if budgets:
            print(f"\n💰 BUDGET ANALYSIS:")
            print(f"   Range: ${min(budgets)} - ${max(budgets)}")
            print(f"   Average: ${sum(budgets)/len(budgets):.0f}")
            print(f"   Median: ${sorted(budgets)[len(budgets)//2]}")

            # Budget tiers
            sorted_budgets = sorted(budgets)
            q1 = sorted_budgets[len(sorted_budgets)//4]
            q3 = sorted_budgets[len(sorted_budgets)*3//4]

            print(f"\n🎯 PRICING TIERS FOR UNNAMEDDESIGN:")
            print(f"   💸 Budget: ${min(budgets)}-${q1}")
            print(f"   ⭐ Standard: ${q1}-${q3}")
            print(f"   👑 Premium: ${q3}-${max(budgets)}")

        # Competition Analysis
        if proposals:
            print(f"\n🏁 COMPETITION ANALYSIS:")
            print(f"   Average proposals: {sum(proposals)/len(proposals):.1f}")
            print(f"   Range: {min(proposals)}-{max(proposals)} proposals")

            low_comp = len([p for p in proposals if p < 10])
            med_comp = len([p for p in proposals if 10 <= p <= 30])
            high_comp = len([p for p in proposals if p > 30])

            print(f"   📊 Competition Distribution:")
            print(f"      Low (<10 proposals): {low_comp} jobs")
            print(f"      Medium (10-30): {med_comp} jobs")
            print(f"      High (>30): {high_comp} jobs")

        # Job Type Analysis
        if job_types:
            from collections import Counter
            type_counts = Counter(job_types)
            print(f"\n🎨 JOB TYPE BREAKDOWN:")
            for job_type, count in type_counts.most_common():
                percentage = (count / len(job_types)) * 100
                print(f"   • {job_type.replace('_', ' ').title()}: {count} jobs ({percentage:.1f}%)")

        # Complexity Analysis
        if complexities:
            print(f"\n🧠 COMPLEXITY ANALYSIS:")
            avg_complexity = sum(complexities) / len(complexities)
            print(f"   Average complexity: {avg_complexity:.1f}/10")

            simple = len([c for c in complexities if c <= 3])
            medium = len([c for c in complexities if 4 <= c <= 7])
            complex_jobs = len([c for c in complexities if c >= 8])

            print(f"   📊 Complexity Distribution:")
            print(f"      Simple (1-3): {simple} jobs")
            print(f"      Medium (4-7): {medium} jobs")
            print(f"      Complex (8-10): {complex_jobs} jobs")

        # Business Recommendations
        print(f"\n💡 BUSINESS RECOMMENDATIONS FOR UNNAMEDDESIGN:")
        if budgets:
            sweet_spot_min = sorted(budgets)[len(budgets)//3]
            sweet_spot_max = sorted(budgets)[len(budgets)*2//3]
            print(f"   🎯 Sweet spot: ${sweet_spot_min}-${sweet_spot_max}")
            print(f"   💼 Target: ${sweet_spot_min + (sweet_spot_max - sweet_spot_min)//2} average")

        if proposals:
            avg_props = sum(proposals) / len(proposals)
            if avg_props > 30:
                print("   ⚠️ High competition - focus on niche specialization")
            elif avg_props < 15:
                print("   ✅ Low competition - great opportunity!")

        # Save data
        self.save_upwork_data(keyword)

    def save_upwork_data(self, keyword):
        """Save comprehensive Upwork data"""
        if not self.data:
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"upwork_{keyword.replace(' ', '_')}_advanced_{timestamp}.csv"

        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)

        print(f"\n💾 Data saved to: {filename}")
        print(f"📊 Records: {len(self.data)}")

        # Also save JSON summary
        summary = {
            'keyword': keyword,
            'total_jobs': len(self.data),
            'extraction_time': datetime.now().isoformat(),
            'analysis': {
                'budgets': [job.get('budget') for job in self.data if job.get('budget')],
                'proposals': [job.get('proposals') for job in self.data if job.get('proposals')],
                'job_types': list(set([job.get('job_type') for job in self.data if job.get('job_type')])),
            }
        }

        json_filename = filename.replace('.csv', '.json')
        with open(json_filename, 'w') as f:
            json.dump(summary, f, indent=2, default=str)

        print(f"📋 Summary saved to: {json_filename}")

def main():
    """Main function with advanced options"""
    print("🚀 UNNAMEDDESIGN ADVANCED STEALTH SCRAPER")
    print("=" * 50)
    print("🔒 Ultra-stealth mode with multiple bypass techniques")
    print("🎯 Targets: Upwork, Fiverr, and other platforms")

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

    platform = input("🌐 Platform (upwork/fiverr, default upwork): ").strip().lower()
    if platform not in ['upwork', 'fiverr']:
        platform = 'upwork'

    # Start advanced scraping
    scraper = AdvancedStealthScraper(platform)

    if platform == 'upwork':
        scraper.scrape_upwork_stealth(keyword, pages)
    else:
        print("🔄 Fiverr scraping coming soon...")

if __name__ == "__main__":
    main()
