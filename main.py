from selenium import webdriver
import csv
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from home_depot import scrape_home_depot
from lowes import scrape_lowes
from costco import scrape_costco



def save_to_csv(results, filename='products_data.csv'):
    if not results:
        print("No data to save")
        return
    
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='', encoding='utf-8') as output_file:
        keys = results[0].keys()
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        
        if not file_exists:
            dict_writer.writeheader()
        
        dict_writer.writerows(results)

def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("disable-blink-features=AutomationControlled")
    options.add_argument("--headless=new")
    options.add_argument("start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    return webdriver.Chrome(options=options)

def main():
    driver = initialize_driver()

    #model_number = "FGEH3047VF" # inactive
    # model_number = "GCFE3060BF" # discontinued
    #model_number = "MDB4949SKZ"
    #model_number = "XR77A80CL"
    # model_number = "WH1000XM5/B"
    # model_number = "WM5500HWA" # model with multiple listings
    model_number = "LRYKC2606"
    # model_number = "FGEH3047VF" # gibberish
    
    #res = scrape_home_depot(model_number, driver)
    res = scrape_costco(model_number, driver)

    
    #save_to_csv([res])

    # driver.quit()


if __name__ == "__main__":
    product_links = []
    main()