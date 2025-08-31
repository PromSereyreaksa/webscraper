"""
UnnamedDesign Fast Fiverr Scraper
================================
Ultra-fast data extraction before detection kicks in
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

OUTPUT_FILE = "test.csv"

def setup_fast_driver():
    """Setup fastest possible Chrome driver"""
    options = Options()
    
    # Speed optimizations
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-images')  # Don't load images for speed
    options.add_argument('--disable-javascript')  # Disable JS for speed
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-extensions')
    
    # Stealth options
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(options=options)
    
    # Remove automation traces
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

class FastFiverrScraper:
    def __init__(self):
        self.driver = None
        self.data = []
        self.total_gigs_processed = 0
    
    def scrape_fast(self):
        """Lightning-fast scraping through multiple pages"""
        print("🚀 FAST FIVERR SCRAPER - MULTIPLE PAGES!")
        print("=" * 50)
        
        try:
            # Setup driver
            print("⚡ Starting ultra-fast driver...")
            self.driver = setup_fast_driver()
            
            # Scrape multiple pages
            max_pages = 10  # Start with 3 pages
            for page in range(1, max_pages + 1):
                print(f"\n📄 SCRAPING PAGE {page}/{max_pages}")
                print("-" * 30)
                
                success = self.scrape_page(page)
                if not success:
                    print(f"❌ Page {page} failed - stopping")
                    break
                
                # Quick delay between pages
                time.sleep(random.uniform(1, 2))
            
        except Exception as e:
            print(f"❌ Scraping error: {e}")
        finally:
            if self.driver:
                self.driver.quit()
        
        # Show final results
        self.show_results()
    
    def scrape_page(self, page_num):
        """Scrape a single page of results"""
        try:
            # Navigate to specific page
            url = f"https://www.fiverr.com/search/gigs?query=digital+art&page={page_num}"
            print(f"🎯 Loading page {page_num}...")
            
            start_time = time.time()
            self.driver.get(url)
            
            # Wait very briefly for content
            time.sleep(1)
            
            # Extract data IMMEDIATELY
            print("⚡ EXTRACTING DATA NOW...")
            
            # Method 1: Get all text from page
            try:
                page_text = self.driver.execute_script("return document.body.innerText;")
                if page_text and len(page_text) > 1000:  # Has substantial content
                    print(f"📄 Got {len(page_text)} chars from page {page_num}")
                    self.extract_from_page_text(page_text, page_num)
                else:
                    print(f"⚠️ Page {page_num} has limited content")
            except Exception as e:
                print(f"⚠️ Page text extraction failed: {e}")
            
            # Method 2: Find individual gig elements
            gig_count = self.extract_individual_gigs(page_num)
            
            elapsed = time.time() - start_time
            print(f"⏱️ Page {page_num} completed in {elapsed:.2f}s - {gig_count} gigs processed")
            
            return gig_count > 0
            
        except Exception as e:
            print(f"❌ Page {page_num} error: {e}")
            return False
    
    def extract_individual_gigs(self, page_num):
        """Extract data from individual gig posts"""
        gig_count = 0
        
        try:
            # Try multiple selectors to find gig elements
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
                        print(f"🎯 Found {len(gigs)} gigs with '{selector}'")
                        break
                except:
                    continue
            
            if not gigs:
                print("❌ No gig elements found")
                return 0
            
            # Process each gig quickly
            for i, gig in enumerate(gigs[:25]):  # Limit to 15 per page for speed
                try:
                    gig_text = gig.text
                    if gig_text and len(gig_text) > 10:
                        gig_data = self.extract_gig_data(gig_text, page_num, i+1)
                        if gig_data:
                            self.data.append(gig_data)
                            gig_count += 1
                            
                            # Show detailed progress
                            price_str = f"${gig_data['price']}" if gig_data['price'] else "No price"
                            rating_str = f"{gig_data['rating']}⭐" if gig_data['rating'] else "No rating"
                            delivery_str = f"{gig_data['delivery_days']}d" if gig_data['delivery_days'] else "No delivery"
                            work_type_str = gig_data['work_type'].replace('_', ' ').title()
                            
                            print(f"  ✅ Gig {i+1}: {price_str} - {rating_str} - {delivery_str} - {work_type_str}")
                            
                except Exception as e:
                    continue
            
            self.total_gigs_processed += gig_count
            return gig_count
            
        except Exception as e:
            print(f"⚠️ Individual gig extraction error: {e}")
            return 0
    
    def extract_from_page_text(self, text, page_num):
        """Extract data from entire page text"""
        # Find all prices
        prices = re.findall(r'\$(\d+)', text)
        prices = [int(p) for p in prices if 5 <= int(p) <= 1000]
        
        # Find all ratings
        ratings = re.findall(r'(\d\.\d)', text)
        ratings = [float(r) for r in ratings if 3.0 <= float(r) <= 5.0]
        
        # Find review counts
        reviews = re.findall(r'\((\d+)\)', text)
        reviews = [int(r) for r in reviews if 1 <= int(r) <= 5000]
        
        if prices or ratings:
            self.data.append({
                'source': f'page_{page_num}_text',
                'page': page_num,
                'prices': prices,
                'ratings': ratings,
                'reviews': reviews,
                'extraction_time': datetime.now().strftime('%H:%M:%S')
            })
            
            print(f"📊 Page {page_num}: {len(prices)} prices, {len(ratings)} ratings")
    
    def extract_gig_data(self, gig_text, page_num, gig_num):
        """Extract data from individual gig text"""
        # Extract title (first meaningful line)
        lines = [line.strip() for line in gig_text.split('\n') if line.strip()]
        title = None
        for line in lines[:3]:  # Check first 3 lines
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
        
        # Extract review count
        review_matches = re.findall(r'\((\d+)\)', gig_text)
        reviews = None
        if review_matches:
            for r in review_matches:
                r_int = int(r)
                if 1 <= r_int <= 5000:
                    reviews = r_int
                    break
        
        # Extract delivery time - NEW FEATURE
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
        
        # Extract work type/complexity - NEW FEATURE
        work_type = "unknown"
        if any(word in gig_text.lower() for word in ['logo', 'brand', 'identity']):
            work_type = "logo_design"
        elif any(word in gig_text.lower() for word in ['character', 'mascot', 'avatar']):
            work_type = "character_design"
        elif any(word in gig_text.lower() for word in ['illustration', 'drawing', 'art']):
            work_type = "illustration"
        elif any(word in gig_text.lower() for word in ['portrait', 'photo', 'realistic']):
            work_type = "portrait"
        elif any(word in gig_text.lower() for word in ['concept', 'fantasy', 'sci-fi']):
            work_type = "concept_art"
        
        if title or price or rating:  # Only return if we found something useful
            return {
                'source': f'page_{page_num}_gig_{gig_num}',
                'page': page_num,
                'gig_num': gig_num,
                'title': title,
                'price': price,
                'rating': rating,
                'reviews': reviews,
                'delivery_days': delivery_time,
                'work_type': work_type,
                'extraction_time': datetime.now().strftime('%H:%M:%S')
            }
        
        return None
    
    def show_results(self):
        """Show extracted results"""
        if not self.data:
            print("❌ No data extracted")
            return
        
        all_prices = []
        all_ratings = []
        all_reviews = []
        all_titles = []
        all_delivery_times = []
        work_types = []
        
        for session in self.data:
            # Handle both individual gigs and page text data
            if 'prices' in session and session['prices']:
                if isinstance(session['prices'], list):
                    all_prices.extend(session['prices'])
                else:
                    all_prices.append(session['prices'])
            
            if 'ratings' in session and session['ratings']:
                if isinstance(session['ratings'], list):
                    all_ratings.extend(session['ratings'])
                else:
                    all_ratings.append(session['ratings'])
            
            if 'reviews' in session and session['reviews']:
                if isinstance(session['reviews'], list):
                    all_reviews.extend(session['reviews'])
                else:
                    all_reviews.append(session['reviews'])
            
            if 'title' in session and session['title']:
                all_titles.append(session['title'])
            if 'delivery_days' in session and session['delivery_days']:
                all_delivery_times.append(session['delivery_days'])
            if 'work_type' in session and session['work_type']:
                work_types.append(session['work_type'])
            
            # Handle single values
            if 'price' in session and session['price']:
                all_prices.append(session['price'])
            if 'rating' in session and session['rating']:
                all_ratings.append(session['rating'])
        
        print(f"\n🎯 FINAL EXTRACTION RESULTS:")
        print("=" * 35)
        print(f"📊 Total gigs processed: {self.total_gigs_processed}")
        
        if all_prices:
            print(f"\n💰 PRICING ANALYSIS:")
            print(f"   Total prices found: {len(all_prices)}")
            print(f"   Range: ${min(all_prices)} - ${max(all_prices)}")
            print(f"   Average: ${sum(all_prices)/len(all_prices):.2f}")
            
            # Show price distribution
            sorted_prices = sorted(all_prices)
            if len(sorted_prices) >= 4:
                q1 = sorted_prices[len(sorted_prices)//4]
                q3 = sorted_prices[len(sorted_prices)*3//4]
                
                print(f"\n🎯 PRICING TIERS FOR UNNAMEDDESIGN:")
                print(f"   💸 Budget: ${min(all_prices)}-${q1}")
                print(f"   ⭐ Standard: ${q1}-${q3}")
                print(f"   👑 Premium: ${q3}-${max(all_prices)}")
        
        if all_ratings:
            print(f"\n⭐ QUALITY STANDARDS:")
            print(f"   Total ratings: {len(all_ratings)}")
            print(f"   Average: {sum(all_ratings)/len(all_ratings):.2f}")
            print(f"   Range: {min(all_ratings)} - {max(all_ratings)}")
            print(f"   Target for your artists: {sum(all_ratings)/len(all_ratings):.1f}+")
        
        if all_delivery_times:
            print(f"\n⏰ DELIVERY TIME ANALYSIS:")
            print(f"   Average delivery: {sum(all_delivery_times)/len(all_delivery_times):.1f} days")
            print(f"   Range: {min(all_delivery_times)}-{max(all_delivery_times)} days")
            print(f"   Fastest: {min(all_delivery_times)} days")
        
        if work_types:
            from collections import Counter
            type_counts = Counter(work_types)
            print(f"\n🎨 WORK TYPE BREAKDOWN:")
            for work_type, count in type_counts.most_common():
                print(f"   • {work_type.replace('_', ' ').title()}: {count} gigs")
        
        if all_reviews:
            print(f"\n📝 SOCIAL PROOF:")
            print(f"   Average reviews: {sum(all_reviews)/len(all_reviews):.0f}")
            print(f"   Range: {min(all_reviews)}-{max(all_reviews)} reviews")
        
        # Generate pricing recommendations
        if all_prices and all_delivery_times:
            print(f"\n� PRICING RECOMMENDATIONS FOR UNNAMEDDESIGN:")
            
            # Calculate price per day
            price_per_day = []
            for i in range(min(len(all_prices), len(all_delivery_times))):
                if all_delivery_times[i] > 0:
                    price_per_day.append(all_prices[i] / all_delivery_times[i])
            
            if price_per_day:
                avg_per_day = sum(price_per_day) / len(price_per_day)
                print(f"   📈 Average: ${avg_per_day:.2f}/day")
                print(f"   🎯 Your artists should charge: ${avg_per_day * 0.8:.2f}-${avg_per_day * 1.2:.2f}/day")
        
        # Save to CSV
        if all_prices or all_ratings or all_titles:
            self.save_csv_fast(all_prices, all_ratings, all_reviews, all_titles, all_delivery_times, work_types)
        else:
            print("❌ No useful data to save")
    
    def save_csv_fast(self, prices, ratings, reviews, titles, delivery_times, work_types):
        """Quick CSV save with delivery times and work types"""
        max_len = max(len(prices), len(ratings), len(reviews), len(titles), len(delivery_times), len(work_types))
        
        # Pad all lists to same length
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
        
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"💾 Complete data saved to {OUTPUT_FILE}")
        
        # Show pricing per work type
        if prices and work_types:
            print(f"\n💰 PRICING BY WORK TYPE:")
            type_prices = {}
            for i in range(len(prices)):
                if prices[i] and work_types[i]:
                    if work_types[i] not in type_prices:
                        type_prices[work_types[i]] = []
                    type_prices[work_types[i]].append(prices[i])
            
            for work_type, price_list in type_prices.items():
                if price_list:
                    avg_price = sum(price_list) / len(price_list)
                    print(f"   • {work_type.replace('_', ' ').title()}: ${avg_price:.2f} avg ({len(price_list)} samples)")
        
        return df

if __name__ == "__main__":
    scraper = FastFiverrScraper()
    scraper.scrape_fast()
