"""
UnnamedDesign Advanced Upwork Scraper - Selenium Edition
======================================================
Multi-threaded Selenium scraper for comprehensive market research
"""
import re
import pandas as pd
import time
import random
import json
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class AdvancedUpworkScraper:
    def __init__(self):
        self.data = []
        self.total_jobs_processed = 0
        self.search_categories = [
            "logo-design",
            "graphic-design", 
            "web-design",
            "illustration",
            "brand-identity",
            "ui-ux-design"
        ]
    
    def setup_stealth_driver(self, thread_id=0):
        """Setup advanced stealth Chrome driver"""
        options = Options()
        
        # Performance optimizations
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-images')  # Speed up loading
        
        # Advanced stealth - different from Fiverr approach
        options.add_argument(f'--user-data-dir=/tmp/chrome_profile_{thread_id}')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Rotate user agents per thread
        user_agents = [
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        options.add_argument(f'--user-agent={user_agents[thread_id % len(user_agents)]}')
        
        driver = webdriver.Chrome(options=options)
        
        # Remove automation detection
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def scrape_category_threaded(self, category, max_pages=3):
        """Scrape a specific category with threading"""
        print(f"🎯 UPWORK MARKET RESEARCH: {category.replace('-', ' ').title()}")
        print("=" * 60)
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            
            # Launch threads for different pages
            for page in range(1, max_pages + 1):
                future = executor.submit(self.scrape_single_page, category, page)
                futures.append(future)
            
            # Collect results
            for future in as_completed(futures):
                try:
                    page_data = future.result()
                    if page_data:
                        self.data.extend(page_data)
                        print(f"✅ Thread completed: {len(page_data)} jobs collected")
                except Exception as e:
                    print(f"❌ Thread failed: {e}")
    
    def scrape_single_page(self, category, page_num):
        """Scrape a single page of Upwork jobs"""
        driver = None
        thread_id = random.randint(1000, 9999)
        
        try:
            print(f"🌐 Thread {thread_id}: Scraping {category} page {page_num}...")
            
            # Setup driver
            driver = self.setup_stealth_driver(thread_id)
            
            # Build Upwork search URL
            search_query = category.replace('-', ' ')
            url = f"https://www.upwork.com/nx/search/jobs/?q={search_query}&page={page_num}&per_page=50"
            
            print(f"📍 Loading: {url}")
            
            # Navigate to page
            driver.get(url)
            
            # Wait for page load with random delay
            wait_time = random.uniform(3, 6)
            time.sleep(wait_time)
            
            # Check if we need to handle any popups/modals
            try:
                # Close any signup modals
                close_buttons = driver.find_elements(By.CSS_SELECTOR, '[data-test="modal-close-button"], .modal-close, [aria-label="Close"]')
                for button in close_buttons:
                    try:
                        button.click()
                        time.sleep(1)
                    except:
                        pass
            except:
                pass
            
            # Extract job data
            page_data = self.extract_jobs_from_page(driver, category, page_num, thread_id)
            
            print(f"✅ Thread {thread_id}: Extracted {len(page_data)} jobs from page {page_num}")
            return page_data
            
        except Exception as e:
            print(f"❌ Thread {thread_id} error on page {page_num}: {e}")
            return []
        finally:
            if driver:
                driver.quit()
    
    def extract_jobs_from_page(self, driver, category, page_num, thread_id):
        """Extract job data from the current page"""
        jobs_data = []
        
        try:
            # Wait for job listings to load
            wait = WebDriverWait(driver, 10)
            
            # Try multiple selectors for job cards
            job_selectors = [
                '[data-test*="job-tile"]',
                '.job-tile',
                'article[data-test*="job"]',
                '[data-test="JobTile"]',
                '.up-card-section'
            ]
            
            job_elements = []
            for selector in job_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        job_elements = elements
                        print(f"🎯 Found {len(job_elements)} jobs with '{selector}'")
                        break
                except:
                    continue
            
            if not job_elements:
                print(f"❌ No job elements found on page {page_num}")
                return []
            
            # Process each job
            for i, job_element in enumerate(job_elements[:25]):  # Limit to 25 per page
                try:
                    job_data = self.extract_single_job(job_element, category, page_num, i+1, thread_id)
                    if job_data:
                        jobs_data.append(job_data)
                        self.total_jobs_processed += 1
                        
                        # Show progress
                        budget_str = f"${job_data['budget_min']}-${job_data['budget_max']}" if job_data['budget_min'] else f"${job_data['hourly_rate']}/hr" if job_data['hourly_rate'] else "No budget"
                        proposals_str = f"{job_data['proposals']} proposals" if job_data['proposals'] else "No proposals"
                        
                        print(f"  ✅ Job {i+1}: {budget_str} - {proposals_str} - {job_data['complexity']}")
                        
                except Exception as e:
                    print(f"  ⚠️ Error extracting job {i+1}: {e}")
                    continue
            
            return jobs_data
            
        except Exception as e:
            print(f"❌ Page extraction error: {e}")
            return []
    
    def extract_single_job(self, job_element, category, page_num, job_num, thread_id):
        """Extract data from a single job posting"""
        try:
            # Get all text from the job element
            job_text = job_element.text
            
            if not job_text or len(job_text) < 20:
                return None
            
            # Extract title (usually first line or in h4/h3)
            title = None
            try:
                title_elements = job_element.find_elements(By.CSS_SELECTOR, 'h4, h3, [data-test*="job-title"], .job-title')
                if title_elements:
                    title = title_elements[0].text.strip()
            except:
                pass
            
            if not title:
                # Fallback: get first meaningful line
                lines = [line.strip() for line in job_text.split('\n') if line.strip()]
                for line in lines[:3]:
                    if len(line) > 10 and not line.startswith('$') and not re.match(r'^\\d+', line):
                        title = line
                        break
            
            # Extract budget information
            budget_min = budget_max = hourly_rate = None
            
            # Fixed price budget
            fixed_budget_patterns = [
                r'\\$([\\d,]+)\\s*-\\s*\\$([\\d,]+)',  # $1,000 - $5,000
                r'\\$([\\d,]+)',  # $1,000
                r'([\\d,]+)\\s*-\\s*([\\d,]+)',  # 1000 - 5000
            ]
            
            for pattern in fixed_budget_patterns:
                matches = re.findall(pattern, job_text)
                if matches:
                    if len(matches[0]) == 2:  # Range
                        budget_min = int(matches[0][0].replace(',', ''))
                        budget_max = int(matches[0][1].replace(',', ''))
                    else:  # Single value
                        budget_min = budget_max = int(matches[0].replace(',', ''))
                    break
            
            # Hourly rate
            hourly_patterns = [
                r'\\$([\\d,]+)(?:\\.\\d+)?/hr',
                r'\\$([\\d,]+)(?:\\.\\d+)?\\s*per\\s*hour',
                r'([\\d,]+)(?:\\.\\d+)?/hr'
            ]
            
            for pattern in hourly_patterns:
                matches = re.findall(pattern, job_text.lower())
                if matches:
                    hourly_rate = int(float(matches[0].replace(',', '')))
                    break
            
            # Extract proposals count
            proposals = None
            proposal_patterns = [
                r'(\\d+)\\s*proposals?',
                r'(\\d+)\\s*freelancers?\\s*applied',
                r'(\\d+)\\s*bids?'
            ]
            
            for pattern in proposal_patterns:
                matches = re.findall(pattern, job_text.lower())
                if matches:
                    proposals = int(matches[0])
                    break
            
            # Extract experience level
            experience_level = "intermediate"
            if any(word in job_text.lower() for word in ['entry', 'beginner', 'junior', 'new']):
                experience_level = "entry"
            elif any(word in job_text.lower() for word in ['expert', 'senior', 'advanced', 'lead']):
                experience_level = "expert"
            
            # Extract project duration
            duration = "medium"
            if any(word in job_text.lower() for word in ['quick', 'urgent', '1 day', '2 day', '1 week']):
                duration = "short"
            elif any(word in job_text.lower() for word in ['long', 'ongoing', '3 month', '6 month', 'permanent']):
                duration = "long"
            
            # Extract skills
            skills = []
            common_skills = [
                'photoshop', 'illustrator', 'figma', 'sketch', 'adobe', 'logo design',
                'branding', 'typography', 'web design', 'ui', 'ux', 'graphic design',
                'html', 'css', 'javascript', 'wordpress', 'shopify'
            ]
            
            for skill in common_skills:
                if skill in job_text.lower():
                    skills.append(skill)
            
            # Calculate complexity score (1-10)
            complexity = 5  # Default
            
            # Increase complexity based on factors
            if budget_max and budget_max > 5000:
                complexity += 2
            elif budget_max and budget_max > 1000:
                complexity += 1
            
            if hourly_rate and hourly_rate > 50:
                complexity += 2
            elif hourly_rate and hourly_rate > 25:
                complexity += 1
            
            if experience_level == "expert":
                complexity += 1
            elif experience_level == "entry":
                complexity -= 1
            
            if duration == "long":
                complexity += 1
            
            if len(skills) > 3:
                complexity += 1
            
            complexity = max(1, min(10, complexity))  # Keep between 1-10
            
            # Determine project type
            project_type = "other"
            job_lower = job_text.lower()
            
            if any(word in job_lower for word in ['logo', 'brand', 'identity']):
                project_type = "logo_design"
            elif any(word in job_lower for word in ['web', 'website', 'landing', 'homepage']):
                project_type = "web_design"
            elif any(word in job_lower for word in ['illustration', 'drawing', 'artwork']):
                project_type = "illustration"
            elif any(word in job_lower for word in ['ui', 'ux', 'interface', 'wireframe']):
                project_type = "ui_ux"
            elif any(word in job_lower for word in ['graphic', 'poster', 'flyer', 'banner']):
                project_type = "graphic_design"
            
            # Calculate competition level
            competition = "medium"
            if proposals:
                if proposals < 5:
                    competition = "low"
                elif proposals > 20:
                    competition = "high"
            
            # Extract posting date
            posted_date = None
            date_patterns = [
                r'posted\\s*(\\d+)\\s*hours?\\s*ago',
                r'posted\\s*(\\d+)\\s*days?\\s*ago',
                r'posted\\s*yesterday',
                r'posted\\s*today'
            ]
            
            for pattern in date_patterns:
                matches = re.findall(pattern, job_text.lower())
                if matches:
                    if 'hour' in pattern:
                        posted_date = datetime.now() - timedelta(hours=int(matches[0]))
                    elif 'day' in pattern:
                        posted_date = datetime.now() - timedelta(days=int(matches[0]))
                    elif 'yesterday' in pattern:
                        posted_date = datetime.now() - timedelta(days=1)
                    elif 'today' in pattern:
                        posted_date = datetime.now()
                    break
            
            return {
                'source': f'upwork_thread_{thread_id}_page_{page_num}_job_{job_num}',
                'thread_id': thread_id,
                'page': page_num,
                'job_num': job_num,
                'category': category,
                'title': title,
                'budget_min': budget_min,
                'budget_max': budget_max,
                'hourly_rate': hourly_rate,
                'proposals': proposals,
                'experience_level': experience_level,
                'duration': duration,
                'complexity': complexity,
                'project_type': project_type,
                'competition': competition,
                'skills': ', '.join(skills[:5]),  # Top 5 skills
                'posted_date': posted_date.strftime('%Y-%m-%d %H:%M:%S') if posted_date else None,
                'extraction_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            print(f"Error extracting job: {e}")
            return None
    
    def scrape_market_research(self):
        """Comprehensive market research across all categories"""
        print("🚀 UNNAMEDDESIGN UPWORK MARKET RESEARCH")
        print("=" * 60)
        print("🎯 Categories: Logo Design, Web Design, Illustration, UI/UX")
        print("🔥 Multi-threaded data collection")
        print("📊 Advanced market analysis")
        print("=" * 60)
        
        # Scrape each category
        for category in self.search_categories[:3]:  # Start with 3 categories
            print(f"\\n🔍 RESEARCHING: {category.replace('-', ' ').title()}")
            print("-" * 40)
            
            self.scrape_category_threaded(category, max_pages=2)  # 2 pages per category
            
            # Brief pause between categories
            time.sleep(random.uniform(2, 4))
        
        # Show comprehensive results
        self.show_market_analysis()
    
    def show_market_analysis(self):
        """Show comprehensive market analysis for UnnamedDesign"""
        if not self.data:
            print("❌ No data collected")
            return
        
        print(f"\\n🎯 UNNAMEDDESIGN MARKET RESEARCH RESULTS")
        print("=" * 60)
        print(f"📊 Total jobs analyzed: {len(self.data)}")
        
        # Budget analysis
        fixed_budgets = [job for job in self.data if job['budget_min']]
        hourly_rates = [job for job in self.data if job['hourly_rate']]
        
        if fixed_budgets:
            budgets = [job['budget_max'] or job['budget_min'] for job in fixed_budgets]
            
            print(f"\\n💰 FIXED PRICE BUDGET ANALYSIS:")
            print(f"   Projects with fixed budgets: {len(fixed_budgets)}")
            print(f"   Range: ${min(budgets):,} - ${max(budgets):,}")
            print(f"   Average: ${sum(budgets)/len(budgets):,.2f}")
            print(f"   Median: ${sorted(budgets)[len(budgets)//2]:,}")
            
            # Price tiers
            sorted_budgets = sorted(budgets)
            q1 = sorted_budgets[len(sorted_budgets)//4]
            q3 = sorted_budgets[len(sorted_budgets)*3//4]
            
            print(f"\\n🎯 PRICING TIERS FOR UNNAMEDDESIGN:")
            print(f"   💸 Budget Tier: ${min(budgets):,} - ${q1:,}")
            print(f"   ⭐ Standard Tier: ${q1:,} - ${q3:,}")
            print(f"   👑 Premium Tier: ${q3:,} - ${max(budgets):,}")
        
        if hourly_rates:
            rates = [job['hourly_rate'] for job in hourly_rates]
            
            print(f"\\n⏰ HOURLY RATE ANALYSIS:")
            print(f"   Hourly projects: {len(hourly_rates)}")
            print(f"   Range: ${min(rates)}/hr - ${max(rates)}/hr")
            print(f"   Average: ${sum(rates)/len(rates):.2f}/hr")
        
        # Competition analysis
        jobs_with_proposals = [job for job in self.data if job['proposals']]
        if jobs_with_proposals:
            proposals = [job['proposals'] for job in jobs_with_proposals]
            
            print(f"\\n🔥 COMPETITION ANALYSIS:")
            print(f"   Average proposals: {sum(proposals)/len(proposals):.1f}")
            print(f"   Range: {min(proposals)} - {max(proposals)} proposals")
            
            # Competition levels
            low_comp = len([job for job in self.data if job['competition'] == 'low'])
            med_comp = len([job for job in self.data if job['competition'] == 'medium'])
            high_comp = len([job for job in self.data if job['competition'] == 'high'])
            
            print(f"   🟢 Low competition: {low_comp} jobs")
            print(f"   🟡 Medium competition: {med_comp} jobs")
            print(f"   🔴 High competition: {high_comp} jobs")
        
        # Project type breakdown
        from collections import Counter
        project_types = [job['project_type'] for job in self.data if job['project_type']]
        type_counts = Counter(project_types)
        
        print(f"\\n🎨 PROJECT TYPE DEMAND:")
        for ptype, count in type_counts.most_common():
            percentage = (count / len(self.data)) * 100
            print(f"   • {ptype.replace('_', ' ').title()}: {count} jobs ({percentage:.1f}%)")
        
        # Experience level breakdown
        exp_levels = [job['experience_level'] for job in self.data if job['experience_level']]
        exp_counts = Counter(exp_levels)
        
        print(f"\\n📈 EXPERIENCE LEVEL DEMAND:")
        for level, count in exp_counts.most_common():
            percentage = (count / len(self.data)) * 100
            print(f"   • {level.title()}: {count} jobs ({percentage:.1f}%)")
        
        # Complexity analysis
        complexities = [job['complexity'] for job in self.data if job['complexity']]
        if complexities:
            avg_complexity = sum(complexities) / len(complexities)
            print(f"\\n🎯 COMPLEXITY ANALYSIS:")
            print(f"   Average complexity: {avg_complexity:.1f}/10")
            print(f"   Range: {min(complexities)} - {max(complexities)}")
        
        # Sweet spot analysis
        print(f"\\n🎯 SWEET SPOT OPPORTUNITIES FOR UNNAMEDDESIGN:")
        
        # Find low-competition, good-budget jobs
        sweet_spots = []
        for job in self.data:
            score = 0
            
            # Low competition = good
            if job['competition'] == 'low':
                score += 3
            elif job['competition'] == 'medium':
                score += 1
            
            # Good budget = good
            if job['budget_max'] and 500 <= job['budget_max'] <= 3000:
                score += 2
            elif job['hourly_rate'] and 25 <= job['hourly_rate'] <= 75:
                score += 2
            
            # Intermediate/Entry level = accessible
            if job['experience_level'] in ['entry', 'intermediate']:
                score += 1
            
            if score >= 3:
                sweet_spots.append(job)
        
        if sweet_spots:
            print(f"   🎯 Found {len(sweet_spots)} sweet spot opportunities!")
            
            # Analyze sweet spots
            sweet_budgets = [job['budget_max'] or job['budget_min'] for job in sweet_spots if job['budget_min'] or job['budget_max']]
            if sweet_budgets:
                print(f"   💰 Sweet spot budget range: ${min(sweet_budgets):,} - ${max(sweet_budgets):,}")
                print(f"   💰 Sweet spot average: ${sum(sweet_budgets)/len(sweet_budgets):,.2f}")
        
        # Save comprehensive data
        self.save_market_research_data()
    
    def save_market_research_data(self):
        """Save comprehensive market research data"""
        if not self.data:
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save main CSV
        df = pd.DataFrame(self.data)
        filename = f"unnameddesign_upwork_research_{timestamp}.csv"
        df.to_csv(filename, index=False)
        
        print(f"\\n💾 RESEARCH DATA SAVED:")
        print(f"   📊 Main data: {filename}")
        
        # Save summary analysis
        summary_filename = f"unnameddesign_market_summary_{timestamp}.json"
        
        # Calculate summary stats
        fixed_budgets = [job['budget_max'] or job['budget_min'] for job in self.data if job['budget_min'] or job['budget_max']]
        hourly_rates = [job['hourly_rate'] for job in self.data if job['hourly_rate']]
        
        summary = {
            "research_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "total_jobs_analyzed": len(self.data),
            "categories_researched": list(set([job['category'] for job in self.data])),
            
            "budget_analysis": {
                "fixed_price_jobs": len([job for job in self.data if job['budget_min']]),
                "hourly_jobs": len([job for job in self.data if job['hourly_rate']]),
                "avg_fixed_budget": sum(fixed_budgets)/len(fixed_budgets) if fixed_budgets else 0,
                "avg_hourly_rate": sum(hourly_rates)/len(hourly_rates) if hourly_rates else 0,
                "budget_range": {
                    "min": min(fixed_budgets) if fixed_budgets else 0,
                    "max": max(fixed_budgets) if fixed_budgets else 0
                }
            },
            
            "competition_analysis": {
                "avg_proposals": sum([job['proposals'] for job in self.data if job['proposals']]) / len([job for job in self.data if job['proposals']]) if [job for job in self.data if job['proposals']] else 0,
                "low_competition_jobs": len([job for job in self.data if job['competition'] == 'low']),
                "high_competition_jobs": len([job for job in self.data if job['competition'] == 'high'])
            },
            
            "recommendations": {
                "target_budget_range": "$500 - $3,000 for most opportunities",
                "recommended_hourly_rate": "$25 - $75/hour based on market data",
                "best_project_types": ["logo_design", "web_design", "graphic_design"],
                "competition_strategy": "Focus on low-competition, intermediate-level projects"
            }
        }
        
        with open(summary_filename, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"   📋 Summary: {summary_filename}")
        
        return df

if __name__ == "__main__":
    scraper = AdvancedUpworkScraper()
    scraper.scrape_market_research()
