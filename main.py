from playwright.sync_api import sync_playwright
import pandas as pd
import time

def scrape_google_maps(search_query):
  leads=[]

  formatted_query=search_query.replace(" ","+")
  target_url=f"https://www.google.com/maps/search/{formatted_query}"

  