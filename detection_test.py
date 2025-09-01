"""
Test: Has Fiverr's Detection Changed?
Compare different approaches to see what gets blocked
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_original_working_flags():
    """Test your exact original working setup"""
    print("🧪 TESTING: Original Working Chrome Flags")
    print("=" * 50)
    
    options = Options()
    # Your EXACT original working flags
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage') 
    options.add_argument('--disable-javascript')  # The magic flag
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Test the exact URL format you used before
        url = "https://www.fiverr.com/search/gigs?query=logo+design&page=1"
        print(f"🌐 Loading: {url}")
        
        start_time = time.time()
        driver.get(url)
        
        time.sleep(3)
        
        title = driver.title
        elapsed = time.time() - start_time
        
        print(f"📄 Title: {title}")
        print(f"⏱️ Load time: {elapsed:.2f}s")
        
        # Check for blocking
        if 'human' in title.lower() or 'verification' in title.lower() or 'blocked' in title.lower():
            print("🚫 RESULT: BLOCKED - Fiverr's detection caught us!")
            print("   This confirms they updated their system!")
        else:
            print("✅ RESULT: SUCCESS - Original flags still work!")
            
            # Quick check - can we get any page content?
            try:
                page_text = driver.execute_script("return document.body.innerText;")
                if page_text and len(page_text) > 1000:
                    print(f"📝 Got {len(page_text)} chars of content")
                    
                    # Look for gig indicators  
                    if 'fiverr' in page_text.lower() and ('$' in page_text or 'gig' in page_text.lower()):
                        print("✅ Content looks like real Fiverr data")
                    else:
                        print("⚠️ Content might be error page")
                else:
                    print("❌ Very little content - likely blocked")
            except:
                print("❌ Can't execute JavaScript - likely blocked")
        
        input("Press Enter to close browser and see the page...")
        
    finally:
        driver.quit()

def test_no_automation_flags():
    """Test completely vanilla Chrome"""
    print("\n🧪 TESTING: Vanilla Chrome (No Flags)")
    print("=" * 50)
    
    options = Options()
    # Absolutely minimal - just like a normal browser
    
    driver = webdriver.Chrome(options=options)
    
    try:
        url = "https://www.fiverr.com/search/gigs?query=logo+design&page=1"
        print(f"🌐 Loading: {url}")
        
        driver.get(url)
        time.sleep(3)
        
        title = driver.title
        print(f"📄 Title: {title}")
        
        if 'human' in title.lower() or 'verification' in title.lower():
            print("🚫 RESULT: Even vanilla Chrome gets blocked!")
            print("   Selenium itself is being detected!")
        else:
            print("✅ RESULT: Vanilla Chrome works!")
        
        input("Press Enter to close...")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    print("🔍 FIVERR DETECTION ANALYSIS")
    print("Testing if Fiverr updated their bot detection...")
    print("\n")
    
    test_original_working_flags()
    
    continue_test = input("\nTest vanilla Chrome too? (y/n): ").lower()
    if continue_test == 'y':
        test_no_automation_flags()
    
    print("\n🎯 CONCLUSION:")
    print("If both tests get blocked, Fiverr definitely updated their detection!")
    print("The solution is to use a completely different approach (like HTTP requests).")
