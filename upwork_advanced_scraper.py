"""
UnnamedDesign Advanced Upwork Scraper
====================================
Professional freelance market analysis tool
- Multi-threaded scraping
- Dynamic keyword input
- Advanced data extraction
- Market analysis and pricing insights
- Export to multiple formats
"""
import re
import requests
import pandas as pd
import time
import random
import json
from datetime import datetime
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote_plus
import threading

class AdvancedUpworkScraper:
    def __init__(self):
        self.session = requests.Session()
        self.data = []
        self.lock = threading.Lock()
        self.total_scraped = 0
        
        # Advanced headers to mimic real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
    
    def scrape_advanced(self):
        """Advanced multi-threaded Upwork scraping"""
        print("🚀 ADVANCED UPWORK SCRAPER FOR UNNAMEDDESIGN")
        print("=" * 60)
        
        # Get user configuration
        config = self.get_user_config()
        
        print(f"\n📊 SCRAPING CONFIGURATION:")
        print(f"   🎯 Keywords: {', '.join(config['keywords'])}")
        print(f"   📄 Pages per keyword: {config['pages_per_keyword']}")
        print(f"   🔥 Threads: {config['threads']}")
        print(f"   💰 Price range: ${config['min_price']}-${config['max_price']}")
        print("=" * 60)
        
        # Multi-threaded scraping
        with ThreadPoolExecutor(max_workers=config['threads']) as executor:
            futures = []
            
            for keyword in config['keywords']:
                for page in range(1, config['pages_per_keyword'] + 1):
                    future = executor.submit(self.scrape_keyword_page, keyword, page, config)
                    futures.append(future)
            
            # Collect results
            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        with self.lock:
                            self.data.extend(result)
                            self.total_scraped += len(result)
                        print(f"✅ Progress: {self.total_scraped} jobs collected")
                except Exception as e:
                    print(f"⚠️ Thread error: {e}")
        
        # Analyze and save results
        self.analyze_and_save(config)
    
    def get_user_config(self):
        """Get advanced configuration from user"""
        print("🔧 ADVANCED CONFIGURATION")
        print("-" * 30)
        
        # Keywords
        keywords_input = input("🎯 Enter keywords (comma-separated, e.g., 'logo design,graphic design,brand identity'): ").strip()
        if not keywords_input:
            keywords = ["logo design", "graphic design", "brand identity"]
            print(f"   Using defaults: {keywords}")
        else:
            keywords = [k.strip() for k in keywords_input.split(',')]
        
        # Pages per keyword
        pages_input = input("📄 Pages per keyword (1-10, default 5): ").strip()
        pages_per_keyword = int(pages_input) if pages_input.isdigit() and 1 <= int(pages_input) <= 10 else 5
        
        # Threads
        threads_input = input("🔥 Number of threads (1-8, default 4): ").strip()
        threads = int(threads_input) if threads_input.isdigit() and 1 <= int(threads_input) <= 8 else 4
        
        # Price range
        min_price_input = input("💰 Minimum price filter ($, default 10): ").strip()
        min_price = int(min_price_input) if min_price_input.isdigit() else 10
        
        max_price_input = input("💰 Maximum price filter ($, default 1000): ").strip()
        max_price = int(max_price_input) if max_price_input.isdigit() else 1000
        
        # Experience level filter
        print("\n📊 Experience level filter:")
        print("   1. All levels")
        print("   2. Entry level only")
        print("   3. Intermediate+ only")
        print("   4. Expert only")
        exp_choice = input("Choose (1-4, default 1): ").strip()
        
        experience_filters = {
            '1': 'all',
            '2': 'entry',
            '3': 'intermediate',
            '4': 'expert'
        }
        experience_level = experience_filters.get(exp_choice, 'all')
        
        return {
            'keywords': keywords,
            'pages_per_keyword': pages_per_keyword,
            'threads': threads,
            'min_price': min_price,
            'max_price': max_price,
            'experience_level': experience_level
        }
    
    def scrape_keyword_page(self, keyword, page, config):
        """Scrape a single page for a keyword"""
        try:
            # Build Upwork search URL
            encoded_keyword = quote_plus(keyword)
            
            # Advanced URL with filters
            base_url = f"https://www.upwork.com/search/projects"
            params = {
                'q': keyword,
                'page': page,
                'sort': 'recency'
            }
            
            # Add experience level filter
            if config['experience_level'] != 'all':
                if config['experience_level'] == 'entry':
                    params['contractor_tier'] = '1'
                elif config['experience_level'] == 'intermediate':
                    params['contractor_tier'] = '2'
                elif config['experience_level'] == 'expert':
                    params['contractor_tier'] = '3'
            
            # Build full URL
            url = base_url + '?' + '&'.join([f"{k}={v}" for k, v in params.items()])
            
            print(f"🌐 Scraping: {keyword} - Page {page}")
            
            # Add random delay to avoid rate limiting
            time.sleep(random.uniform(1, 3))
            
            # Make request
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 429:
                print(f"⚠️ Rate limited for {keyword} page {page}, waiting...")
                time.sleep(random.uniform(5, 10))
                response = self.session.get(url, timeout=15)
            
            if response.status_code != 200:
                print(f"❌ Failed {keyword} page {page}: HTTP {response.status_code}")
                return []
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract job data
            jobs = self.extract_jobs_from_page(soup, keyword, page, config)
            
            if jobs:
                print(f"✅ {keyword} page {page}: {len(jobs)} jobs found")
            else:
                print(f"⚠️ {keyword} page {page}: No jobs found")
            
            return jobs
            
        except Exception as e:
            print(f"❌ Error scraping {keyword} page {page}: {e}")
            return []
    
    def extract_jobs_from_page(self, soup, keyword, page, config):
        """Extract individual job postings from page"""
        jobs = []
        
        # Multiple selectors to find job cards
        job_selectors = [
            'article[data-test="JobTile"]',
            '.job-tile',
            '[data-test="JobTileList"] > div',
            'section[data-test*="job"]',
            '.up-card-section'
        ]
        
        job_elements = []
        for selector in job_selectors:
            elements = soup.select(selector)
            if elements:
                job_elements = elements
                break
        
        if not job_elements:
            # Try generic approach - look for patterns
            job_elements = soup.find_all('div', class_=lambda x: x and 'job' in x.lower())
        
        for i, job_elem in enumerate(job_elements[:20]):  # Limit to 20 per page
            try:
                job_data = self.extract_single_job(job_elem, keyword, page, i+1, config)
                if job_data:
                    jobs.append(job_data)
            except Exception as e:
                continue
        
        return jobs
    
    def extract_single_job(self, job_elem, keyword, page, job_num, config):
        """Extract data from a single job posting"""
        try:
            job_text = job_elem.get_text(separator=' ', strip=True)
            
            if len(job_text) < 50:  # Skip if too little content
                return None
            
            # Extract title
            title = self.extract_title(job_elem, job_text)
            
            # Extract budget/price
            budget_info = self.extract_budget(job_text)
            
            # Skip if outside price range
            if budget_info['budget_min'] and config['min_price']:
                if budget_info['budget_min'] < config['min_price']:
                    return None
            if budget_info['budget_max'] and config['max_price']:
                if budget_info['budget_max'] > config['max_price']:
                    return None
            
            # Extract other details
            skills = self.extract_skills(job_elem, job_text)
            duration = self.extract_duration(job_text)
            experience_level = self.extract_experience_level(job_text)
            proposals = self.extract_proposals(job_text)
            posted_time = self.extract_posted_time(job_text)
            
            # Extract project type
            project_type = self.classify_project_type(title, job_text, skills)
            
            # Calculate complexity score
            complexity_score = self.calculate_complexity(budget_info, skills, experience_level, duration)
            
            return {
                'source': 'upwork',
                'keyword': keyword,
                'page': page,
                'job_num': job_num,
                'title': title,
                'budget_min': budget_info['budget_min'],
                'budget_max': budget_info['budget_max'],
                'budget_type': budget_info['budget_type'],  # hourly vs fixed
                'hourly_rate': budget_info['hourly_rate'],
                'duration': duration,
                'experience_level': experience_level,
                'skills': ', '.join(skills) if skills else None,
                'proposals': proposals,
                'posted_time': posted_time,
                'project_type': project_type,
                'complexity_score': complexity_score,
                'extraction_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            return None
    
    def extract_title(self, job_elem, job_text):
        """Extract job title"""
        # Try multiple approaches for title
        title_selectors = [
            'h2 a',
            'h3 a',
            '[data-test="JobTileTitle"] a',
            '.job-tile-title a',
            'a[href*="/job/"]'
        ]
        
        for selector in title_selectors:
            title_elem = job_elem.select_one(selector)
            if title_elem and title_elem.get_text(strip=True):
                return title_elem.get_text(strip=True)
        
        # Fallback: extract from text patterns
        lines = job_text.split('\\n')
        for line in lines[:3]:
            line = line.strip()
            if len(line) > 10 and len(line) < 100 and not '$' in line:
                return line
        
        return None
    
    def extract_budget(self, job_text):
        """Extract budget information with advanced parsing"""
        budget_info = {
            'budget_min': None,
            'budget_max': None,
            'budget_type': 'unknown',
            'hourly_rate': None
        }
        
        # Fixed price patterns
        fixed_patterns = [
            r'\\$([0-9,]+)\\s*-\\s*\\$([0-9,]+)',  # $100 - $500
            r'Fixed\\s+price[:\\s]*\\$([0-9,]+)',   # Fixed price: $200
            r'Budget[:\\s]*\\$([0-9,]+)',           # Budget: $300
            r'\\$([0-9,]+)\\s+fixed',               # $150 fixed
        ]
        
        for pattern in fixed_patterns:
            match = re.search(pattern, job_text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    # Range format
                    budget_info['budget_min'] = int(match.group(1).replace(',', ''))
                    budget_info['budget_max'] = int(match.group(2).replace(',', ''))
                else:
                    # Single value
                    amount = int(match.group(1).replace(',', ''))
                    budget_info['budget_min'] = amount
                    budget_info['budget_max'] = amount
                
                budget_info['budget_type'] = 'fixed'
                break
        
        # Hourly rate patterns
        if budget_info['budget_type'] == 'unknown':
            hourly_patterns = [
                r'\\$([0-9,]+)\\s*-\\s*\\$([0-9,]+)\\s*\\/hr',  # $15 - $25/hr
                r'\\$([0-9,]+)\\/hr',                           # $20/hr
                r'([0-9,]+)\\s*-\\s*([0-9,]+)\\s*per\\s*hour', # 15 - 25 per hour
            ]
            
            for pattern in hourly_patterns:
                match = re.search(pattern, job_text, re.IGNORECASE)
                if match:
                    if len(match.groups()) == 2:
                        budget_info['budget_min'] = int(match.group(1).replace(',', ''))
                        budget_info['budget_max'] = int(match.group(2).replace(',', ''))
                        budget_info['hourly_rate'] = (budget_info['budget_min'] + budget_info['budget_max']) / 2
                    else:
                        rate = int(match.group(1).replace(',', ''))
                        budget_info['hourly_rate'] = rate
                        budget_info['budget_min'] = rate
                        budget_info['budget_max'] = rate
                    
                    budget_info['budget_type'] = 'hourly'
                    break
        
        return budget_info
    
    def extract_skills(self, job_elem, job_text):
        """Extract required skills"""
        skills = []
        
        # Try to find skills section
        skill_selectors = [
            '[data-test="TokenClamp"] span',
            '.skills span',
            '.up-skill-badge',
            '[class*="skill"] span'
        ]
        
        for selector in skill_selectors:
            skill_elements = job_elem.select(selector)
            for elem in skill_elements:
                skill = elem.get_text(strip=True)
                if skill and len(skill) < 30 and skill not in skills:
                    skills.append(skill)
        
        # Fallback: extract common skills from text
        if not skills:
            common_skills = [
                'Photoshop', 'Illustrator', 'InDesign', 'Logo Design', 'Graphic Design',
                'Brand Identity', 'Typography', 'Web Design', 'UI Design', 'UX Design',
                'Figma', 'Sketch', 'Canva', 'CorelDRAW', 'After Effects'
            ]
            
            for skill in common_skills:
                if skill.lower() in job_text.lower():
                    skills.append(skill)
        
        return skills[:8]  # Limit to 8 skills
    
    def extract_duration(self, job_text):
        """Extract project duration"""
        duration_patterns = [
            r'Less than 1 month',
            r'1 to 3 months',
            r'3 to 6 months',
            r'More than 6 months',
            r'([0-9]+)\\s*days?',
            r'([0-9]+)\\s*weeks?',
            r'([0-9]+)\\s*months?'
        ]
        
        for pattern in duration_patterns:
            match = re.search(pattern, job_text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return None
    
    def extract_experience_level(self, job_text):
        """Extract required experience level"""
        if re.search(r'entry\\s*level|beginner|junior', job_text, re.IGNORECASE):
            return 'Entry Level'
        elif re.search(r'intermediate|mid-?level', job_text, re.IGNORECASE):
            return 'Intermediate'
        elif re.search(r'expert|senior|advanced', job_text, re.IGNORECASE):
            return 'Expert'
        
        return 'Not specified'
    
    def extract_proposals(self, job_text):
        """Extract number of proposals"""
        proposal_patterns = [
            r'([0-9]+)\\s*proposals?',
            r'([0-9]+)\\s*bids?',
            r'([0-9]+)\\s*applicants?'
        ]
        
        for pattern in proposal_patterns:
            match = re.search(pattern, job_text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return None
    
    def extract_posted_time(self, job_text):
        """Extract when job was posted"""
        time_patterns = [
            r'([0-9]+)\\s*hours?\\s*ago',
            r'([0-9]+)\\s*days?\\s*ago',
            r'([0-9]+)\\s*weeks?\\s*ago',
            r'yesterday',
            r'today'
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, job_text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return None
    
    def classify_project_type(self, title, job_text, skills):
        """Classify the type of project"""
        combined_text = f"{title or ''} {job_text}".lower()
        
        # Project type classification
        if any(word in combined_text for word in ['logo', 'brand identity', 'branding']):
            return 'Logo & Branding'
        elif any(word in combined_text for word in ['website', 'web design', 'landing page']):
            return 'Web Design'
        elif any(word in combined_text for word in ['illustration', 'character', 'drawing']):
            return 'Illustration'
        elif any(word in combined_text for word in ['poster', 'flyer', 'banner', 'social media']):
            return 'Marketing Materials'
        elif any(word in combined_text for word in ['ui', 'ux', 'app', 'interface']):
            return 'UI/UX Design'
        elif any(word in combined_text for word in ['package', 'packaging', 'label']):
            return 'Packaging Design'
        elif any(word in combined_text for word in ['business card', 'stationary', 'letterhead']):
            return 'Print Design'
        else:
            return 'General Design'
    
    def calculate_complexity(self, budget_info, skills, experience_level, duration):
        """Calculate project complexity score (1-10)"""
        score = 5  # Base score
        
        # Budget influence
        if budget_info['budget_min']:
            if budget_info['budget_min'] < 50:
                score -= 2
            elif budget_info['budget_min'] < 200:
                score -= 1
            elif budget_info['budget_min'] > 1000:
                score += 2
            elif budget_info['budget_min'] > 500:
                score += 1
        
        # Skills complexity
        if len(skills) > 5:
            score += 1
        if len(skills) > 8:
            score += 1
        
        # Experience level
        if experience_level == 'Expert':
            score += 2
        elif experience_level == 'Intermediate':
            score += 1
        elif experience_level == 'Entry Level':
            score -= 1
        
        # Duration
        if duration and ('month' in duration.lower() or 'weeks' in duration.lower()):
            score += 1
        
        return max(1, min(10, score))  # Keep between 1-10
    
    def analyze_and_save(self, config):
        """Advanced analysis and multiple export formats"""
        if not self.data:
            print("❌ No data collected")
            return
        
        print(f"\n🎯 ADVANCED MARKET ANALYSIS")
        print("=" * 50)
        print(f"📊 Total jobs analyzed: {len(self.data)}")
        
        # Create DataFrame
        df = pd.DataFrame(self.data)
        
        # Advanced Analytics
        self.pricing_analysis(df)
        self.competition_analysis(df)
        self.project_type_analysis(df)
        self.skill_demand_analysis(df)
        self.timing_analysis(df)
        
        # Save in multiple formats
        self.save_multiple_formats(df, config)
        
        # Generate business insights
        self.generate_business_insights(df)
    
    def pricing_analysis(self, df):
        """Advanced pricing analysis"""
        print(f"\n💰 PRICING ANALYSIS")
        print("-" * 30)
        
        # Fixed price projects
        fixed_projects = df[df['budget_type'] == 'fixed']
        if not fixed_projects.empty:
            budgets = fixed_projects['budget_min'].dropna()
            if not budgets.empty:
                print(f"📊 Fixed Price Projects ({len(budgets)} projects):")
                print(f"   Range: ${budgets.min():,.0f} - ${budgets.max():,.0f}")
                print(f"   Average: ${budgets.mean():.0f}")
                print(f"   Median: ${budgets.median():.0f}")
                
                # Price tiers
                q25, q50, q75 = budgets.quantile([0.25, 0.5, 0.75])
                print(f"\n🎯 PRICING TIERS FOR UNNAMEDDESIGN:")
                print(f"   💸 Budget Tier: ${budgets.min():.0f} - ${q25:.0f}")
                print(f"   ⭐ Standard Tier: ${q25:.0f} - ${q75:.0f}")
                print(f"   👑 Premium Tier: ${q75:.0f} - ${budgets.max():.0f}")
        
        # Hourly projects
        hourly_projects = df[df['budget_type'] == 'hourly']
        if not hourly_projects.empty:
            rates = hourly_projects['hourly_rate'].dropna()
            if not rates.empty:
                print(f"\n⏰ Hourly Rate Projects ({len(rates)} projects):")
                print(f"   Range: ${rates.min():.0f} - ${rates.max():.0f}/hr")
                print(f"   Average: ${rates.mean():.0f}/hr")
                print(f"   Median: ${rates.median():.0f}/hr")
    
    def competition_analysis(self, df):
        """Analyze competition levels"""
        print(f"\n🏆 COMPETITION ANALYSIS")
        print("-" * 30)
        
        proposals = df['proposals'].dropna()
        if not proposals.empty:
            print(f"📊 Average proposals per job: {proposals.mean():.1f}")
            print(f"📊 Range: {proposals.min():.0f} - {proposals.max():.0f} proposals")
            
            # Competition levels
            low_competition = (proposals <= 5).sum()
            medium_competition = ((proposals > 5) & (proposals <= 15)).sum()
            high_competition = (proposals > 15).sum()
            
            total = len(proposals)
            print(f"\n🎯 COMPETITION LEVELS:")
            print(f"   🟢 Low competition (≤5 proposals): {low_competition} jobs ({low_competition/total*100:.1f}%)")
            print(f"   🟡 Medium competition (6-15): {medium_competition} jobs ({medium_competition/total*100:.1f}%)")
            print(f"   🔴 High competition (>15): {high_competition} jobs ({high_competition/total*100:.1f}%)")
    
    def project_type_analysis(self, df):
        """Analyze project types and their characteristics"""
        print(f"\n🎨 PROJECT TYPE ANALYSIS")
        print("-" * 30)
        
        type_counts = df['project_type'].value_counts()
        print("📊 Most common project types:")
        for project_type, count in type_counts.head(8).items():
            percentage = (count / len(df)) * 100
            print(f"   • {project_type}: {count} jobs ({percentage:.1f}%)")
        
        # Average pricing by project type
        print(f"\n💰 AVERAGE PRICING BY PROJECT TYPE:")
        for project_type in type_counts.head(5).index:
            type_data = df[df['project_type'] == project_type]
            fixed_budgets = type_data[type_data['budget_type'] == 'fixed']['budget_min'].dropna()
            if not fixed_budgets.empty:
                avg_budget = fixed_budgets.mean()
                print(f"   • {project_type}: ${avg_budget:.0f} average")
    
    def skill_demand_analysis(self, df):
        """Analyze most in-demand skills"""
        print(f"\n⚡ SKILL DEMAND ANALYSIS")
        print("-" * 30)
        
        all_skills = []
        for skills_str in df['skills'].dropna():
            if skills_str:
                skills = [s.strip() for s in skills_str.split(',')]
                all_skills.extend(skills)
        
        if all_skills:
            from collections import Counter
            skill_counts = Counter(all_skills)
            
            print("🔥 Most in-demand skills:")
            for skill, count in skill_counts.most_common(10):
                percentage = (count / len(df)) * 100
                print(f"   • {skill}: {count} jobs ({percentage:.1f}%)")
    
    def timing_analysis(self, df):
        """Analyze posting timing and urgency"""
        print(f"\n⏰ TIMING ANALYSIS")
        print("-" * 30)
        
        posted_times = df['posted_time'].dropna()
        if not posted_times.empty:
            recent_jobs = sum(1 for time in posted_times if 'hour' in time or 'today' in time)
            daily_jobs = sum(1 for time in posted_times if 'day' in time or 'yesterday' in time)
            
            print(f"📊 Job posting frequency:")
            print(f"   • Posted in last 24 hours: {recent_jobs} jobs")
            print(f"   • Posted in last week: {daily_jobs} jobs")
            
            if recent_jobs > 0:
                print(f"   🔥 Market activity: HIGH (many recent postings)")
            else:
                print(f"   📈 Market activity: MODERATE")
    
    def save_multiple_formats(self, df, config):
        """Save data in multiple formats"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = f"upwork_analysis_{timestamp}"
        
        # CSV Export
        csv_filename = f"{base_filename}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"\n💾 Data exported to:")
        print(f"   📄 CSV: {csv_filename}")
        
        # Excel Export with multiple sheets
        excel_filename = f"{base_filename}.xlsx"
        with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
            # Main data
            df.to_excel(writer, sheet_name='All_Data', index=False)
            
            # Summary by project type
            type_summary = df.groupby('project_type').agg({
                'budget_min': ['count', 'mean', 'median'],
                'proposals': 'mean',
                'complexity_score': 'mean'
            }).round(2)
            type_summary.to_excel(writer, sheet_name='Project_Types')
            
            # Price analysis
            price_data = df[df['budget_type'] == 'fixed'][['project_type', 'budget_min', 'complexity_score']]
            price_data.to_excel(writer, sheet_name='Pricing_Analysis', index=False)
        
        print(f"   📊 Excel: {excel_filename}")
        
        # JSON Export for API use
        json_filename = f"{base_filename}.json"
        df.to_json(json_filename, orient='records', indent=2)
        print(f"   📋 JSON: {json_filename}")
    
    def generate_business_insights(self, df):
        """Generate actionable business insights for UnnamedDesign"""
        print(f"\n🎯 BUSINESS INSIGHTS FOR UNNAMEDDESIGN")
        print("=" * 50)
        
        # Market opportunity analysis
        fixed_projects = df[df['budget_type'] == 'fixed']['budget_min'].dropna()
        if not fixed_projects.empty:
            sweet_spot = fixed_projects[(fixed_projects >= 100) & (fixed_projects <= 500)]
            
            print(f"🎯 MARKET OPPORTUNITIES:")
            print(f"   • Sweet spot range ($100-$500): {len(sweet_spot)} projects")
            print(f"   • Average in sweet spot: ${sweet_spot.mean():.0f}")
            print(f"   • This represents {len(sweet_spot)/len(fixed_projects)*100:.1f}% of market")
        
        # Competition insights
        proposals = df['proposals'].dropna()
        if not proposals.empty:
            low_competition = df[df['proposals'] <= 5]
            
            print(f"\n🏆 COMPETITIVE ADVANTAGES:")
            print(f"   • {len(low_competition)} low-competition opportunities")
            print(f"   • Focus on: {low_competition['project_type'].value_counts().head(3).index.tolist()}")
        
        # Pricing recommendations
        if not fixed_projects.empty:
            recommended_min = fixed_projects.quantile(0.25)
            recommended_max = fixed_projects.quantile(0.75)
            
            print(f"\n💰 PRICING RECOMMENDATIONS:")
            print(f"   • Entry pricing: ${recommended_min:.0f} - ${recommended_max*.7:.0f}")
            print(f"   • Standard pricing: ${recommended_max*.7:.0f} - ${recommended_max:.0f}")
            print(f"   • Premium pricing: ${recommended_max:.0f}+")
        
        # Skill recommendations
        all_skills = []
        for skills_str in df['skills'].dropna():
            if skills_str:
                skills = [s.strip() for s in skills_str.split(',')]
                all_skills.extend(skills)
        
        if all_skills:
            from collections import Counter
            skill_counts = Counter(all_skills)
            top_skills = [skill for skill, _ in skill_counts.most_common(5)]
            
            print(f"\n⚡ ESSENTIAL SKILLS TO MASTER:")
            for i, skill in enumerate(top_skills, 1):
                print(f"   {i}. {skill}")

def main():
    """Main execution function"""
    scraper = AdvancedUpworkScraper()
    scraper.scrape_advanced()

if __name__ == "__main__":
    main()
