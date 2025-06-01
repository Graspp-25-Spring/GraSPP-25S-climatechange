# pip install selenium requests beautifulsoup4 pandas
# python CN_policy_selenium.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# --- GHG keywords ---
ghg_keywords = [
    "greenhouse gas", "ghg", "net-zero", "carbon neutral",
    "carbon neutrality", "carbon emissions", "climate change",
    "carbon trading", "carbon pricing", "low-carbon", "clean energy"
]

# --- start chromedriver.exe ---
def get_driver():
    options = Options()
    options.add_argument("--headless")  # headless option
    options.add_argument("--disable-gpu")
    driver_path = "D:/文档/DataScience/chromedriver.exe"  # path of chromedriver.exe, remember to change it
    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=options)

# --- take the news link --- e.g., https://english.www.gov.cn/news/page_1.html
def get_article_links(driver, page_url):
    driver.get(page_url)

    # Wait for the news list container to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "TopNews_List_Div"))
    )
    time.sleep(1)  # Add a short delay to ensure full loading, 1s

    links = []

    # Get all anchor tags within list items
    items = driver.find_elements(By.CSS_SELECTOR, ".TopNews_List_Div ul li")

    for item in items:
        try:
            link_elem = item.find_element(By.TAG_NAME, "a")
            href = link_elem.get_attribute("href")
            if href and href.startswith("http"):
                links.append(href)
            elif href and href.startswith("//"):
                links.append("https:" + href)
        except:
            continue

    return list(set(links))

# --- Scrape the news detail page and check for keywords ---
def parse_article(driver, url):
    try:
        driver.get(url)
        time.sleep(random.uniform(1, 2))
        soup = BeautifulSoup(driver.page_source, "html.parser")

        title = soup.title.get_text(strip=True) if soup.title else "N/A"
        content_div = soup.find("div", class_="pages_content") or soup.find("div", class_="content")
        body = content_div.get_text(separator="\n", strip=True) if content_div else soup.get_text()

        blacklist = ["HOME", "NEWS", "INSTITUTIONS", "POLICIES", "ARCHIVE", "App", "中文"]
        for word in blacklist:
            body = body.replace(word, "")

        combined = (title + "\n" + body).lower()

        keyword_counts = {kw: combined.count(kw.lower()) for kw in ghg_keywords}
        total_hits = sum(keyword_counts.values())
        matched_keywords = [kw for kw, count in keyword_counts.items() if count > 0]

        return {
            "title": title,
            "url": url,
            "has_keyword": total_hits > 0,
            "matched_keywords": ", ".join(matched_keywords),
            "keyword_counts": keyword_counts,
            "snippet": body[:300]
        }
    except Exception as e:
        print(f"❌ Error parsing {url}: {e}")
        return None


# --- Main script ---
def run_selenium_scraper(start_page=1, end_page=143, output="english_gov_GHG_selenium.csv"):
    driver = get_driver()
    all_results = []

    for i in range(start_page, end_page + 1):   # ←✅ 加上这个循环
        if i == 1:
            page_url = "https://english.www.gov.cn/policies/latestreleases/"
        else:
            page_url = f"https://english.www.gov.cn/policies/latestreleases/page_{i}.html"

        print(f"🌐 Crawling page {i}: {page_url}")
        article_links = get_article_links(driver, page_url)
        print(f"  → Found {len(article_links)} article links")

        for j, link in enumerate(article_links):
            print(f"    ➤ [{j+1}/{len(article_links)}] {link}")
            result = parse_article(driver, link)
            if result and result["has_keyword"]:
                all_results.append(result)

    driver.quit()

    if all_results:
        df = pd.DataFrame(all_results)
        keyword_df = df["keyword_counts"].apply(pd.Series)
        df = pd.concat([df.drop(columns=["keyword_counts"]), keyword_df], axis=1)
        df.to_csv(output, index=False, encoding="utf-8-sig")
        print(f"\n✅ Finished! {len(df)} articles saved to {output}")
    else:
        print("⚠️ No articles matched. CSV not created.")

# --- Execute (from page 1 to page 143) ---
run_selenium_scraper(start_page=1, end_page=3)