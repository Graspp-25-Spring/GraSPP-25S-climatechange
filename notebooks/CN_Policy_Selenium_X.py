# pip install selenium requests beautifulsoup4 pandas
# python CN_Policy_Selenium_X.py

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
    "carbon trading", "carbon pricing", "low-carbon", "clean energy", "greenhouse", "carbon", "environment", "emission", "environmental", "emissions", "sustainability",
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
    time.sleep(1.5)  # Add a short delay to ensure full loading, 1.5s

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
        time.sleep(random.uniform(1, 1.5))
        soup = BeautifulSoup(driver.page_source, "html.parser")

        title = soup.title.get_text(strip=True) if soup.title else "N/A"

        # ======== ✅ 提取发布时间 ========
        # 优先从 meta 标签获取
        pub_date = None
        meta_tag = soup.find("meta", attrs={"name": "publishdate"})
        if meta_tag and meta_tag.get("content"):
            pub_date = meta_tag["content"]
        else:
            # 如果没有 meta，就尝试在正文中找形如 "Updated: June 9, 2025" 的文本
            text = soup.get_text()
            import re
            match = re.search(r"Updated:\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})", text)
            if match:
                pub_date = match.group(1)

        # fallback
        if not pub_date:
            pub_date = "N/A"

        # ======== ✅ 提取正文 ========
        content_div = (
            soup.find("div", class_="Artical_Content") or
            soup.find("div", class_="pages_content") or
            soup.find("div", class_="content")
        )

        if content_div:
            paragraphs = content_div.find_all("p")
            body = "\n".join(p.get_text(strip=True) for p in paragraphs)
        else:
            body = soup.get_text()

        # 去除杂质文本
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
            "publish_date": pub_date,   # ✅ 新增字段
            "has_keyword": total_hits > 0,
            "matched_keywords": ", ".join(matched_keywords),
            "keyword_counts": keyword_counts,
            "fulltext": body
        }
    except Exception as e:
        print(f"❌ Error parsing {url}: {e}")
        return None

from selenium.common.exceptions import WebDriverException, InvalidSessionIdException
import os

def run_selenium_scraper(start_page=1, end_page=1022, output="english_policy_GHG_selenium_120.csv", save_interval=10):
    driver = get_driver()
    all_results = []
    output_prefix = os.path.splitext(output)[0]  # 去掉 .csv 后缀

    for i in range(start_page, end_page + 1):
        try:
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
                    result["page_number"] = i
                    all_results.append(result)

        except (WebDriverException, InvalidSessionIdException) as e:
            print(f"❌ Driver error on page {i}: {e}")
            print("🔄 Restarting Chrome driver...")
            try:
                driver.quit()
            except:
                pass
            time.sleep(2)
            driver = get_driver()
            continue

        except Exception as e:
            print(f"⚠️ Unknown error on page {i}: {e}")
            continue

        # === 每 N 页保存一次 ===
        if i % save_interval == 0 and all_results:
            temp_output = f"{output_prefix}_page_{i}.csv"
            print(f"💾 Saving checkpoint: {temp_output}")
            df = pd.DataFrame(all_results)
            keyword_df = df["keyword_counts"].apply(pd.Series)
            df = pd.concat([df.drop(columns=["keyword_counts"]), keyword_df], axis=1)
            df.to_csv(temp_output, index=False, encoding="utf-8-sig")

    driver.quit()

    # === 最终保存总文件 ===
    if all_results:
        df = pd.DataFrame(all_results)
        keyword_df = df["keyword_counts"].apply(pd.Series)
        df = pd.concat([df.drop(columns=["keyword_counts"]), keyword_df], axis=1)
        df.to_csv(output, index=False, encoding="utf-8-sig")
        print(f"\n✅ Finished! {len(df)} articles saved to {output}")
    else:
        print("⚠️ No articles matched. CSV not created.")


# --- Execute (from page 1 to page 1022) ---
run_selenium_scraper(start_page=91, end_page=120)