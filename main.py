from playwright.sync_api import sync_playwright
import pandas as pd
import time

def scrape_google_maps(search_query):
  leads=[]

  formatted_query=search_query.replace(" ","+")
  target_url=f"https://www.google.com/maps/search/{formatted_query}"

  with sync_playwright() as p:
    print(f"🗺️ Launching Maps Harvester for: '{search_query}'...")
    browser=p.chromium.launch(headless=False)
    context=browser.new_context(viewport={"width":1920,"height":1080},locale="en-US")
    page=context.new_page()

    print(f"🌍 Navigating to Google Maps...")
    page.goto(target_url,timeout=60000)

    try:
      page.wait_for_selector('div[role="feed"]')
      print("✅ Feed located. Starting Targeted Infinite Scroll...")
    except Exception:
      print("❌ Could not find the results panel. Google might be showing a different layout.")
      browser.close()
      return
    
    for _ in range(5):
      page.evaluate("""
        let feed=document.querySelector('div[role="feed"]');
        if(feed){
          feed.scrollBy(0,1000);
        }
      """)
      print("⏬ Scrolling panel down...")
      time.sleep(2.5)

  cards=page.locator('div[role="feed"] > div').all()
  print(f"📦 Found {len(cards)} potential elements. Extracting data...")

  for card in cards:
    try:
      card_text=card.inner_text()

      if not card_text or len(card_text.split('\n'))<3:
        continue

      lines=card_text.split('\n')
      name=lines[0]

      rating="N/A"
      phone="N/A"

      for line in lines:
        if "(" in line and ")" in line and "." in line[:5]:
          rating=line
        elif "+" in line or "-" in line or (line.replace(" ","").isdigit() and len(line)>8):
          phone=line
    except:
      print()