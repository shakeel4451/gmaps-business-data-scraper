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