from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import time
import re

'''
active product: # 
discontinued/out-of-stock product: # 
no results found: # 
multi-active product: #  

# some models may have multiple listings, need to account for that
'''


def scrape_costco(model_number, driver):

  model_url = f"https://www.costco.com/CatalogSearch?dept=All&keyword={model_number}"
  print(model_url)

  try:
    
    product_data = {
      'Retailer': "Costco", # 
      'Link': model_url, # 
      'Brand': "", #
      'Category': "", #
      'Model Number': model_number, #
      'SKU': "", #
      'Description': "", #
      'Status': "Active", # 
      'Listed Price': 0.0, # 
      'Original Price': 0.0, # 
      'Date': datetime.now().strftime('%Y-%m-%d')
    }

    driver.get(model_url)
    time.sleep(20)
    
    no_results = bool(driver.find_elements(By.XPATH, "//h1[@automation-id='noResultsFound']"))
    bad_page = bool(driver.find_elements(By.CSS_SELECTOR, ".innerContainer .inner.bear"))

    if no_results or bad_page:
        print("No results found")
        product_data['Status'] = "Not Found"
        return product_data

    first_product = driver.find_elements(By.CSS_SELECTOR, ".product-tile-set a.product-image-url")
    if first_product: # go into first listing assume that is the correct one
        model_url = first_product.get_attribute('href')
        driver.get(model_url)
        time.sleep(3)

    print("PASSED")


    driver.save_screenshot(f"screenshots/screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

    description_element = driver.find_element(By.XPATH, "//div[contains(@class, 'product-h1-container-v2')]//h1[@itemprop='name']")
    
    '''
    max_retries = 5

    for attempt in range(max_retries):
      
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.value[automation-id='productPriceOutput']"))
        )
        price_text = price_element.text
        print("price_text", price_text)
        if price_text != "--" and price_text != "":
            print(f"Price detected: {price_text}")
            product_data['Listed Price'] = price_text
            break  
    '''

    # accounts for both when price is listed and when membership is needed
    script_element = driver.find_element(By.XPATH, "//script[contains(text(), 'adobeProductData')]")
    script_content = script_element.get_attribute('innerHTML')
    price_match = re.search(r'priceTotal:\s*initialize\((\d+\.\d+)\)', script_content)
    if price_match:
        price_text = price_match.group(1)
        product_data['Listed Price'] = (price_text)
    else:
        product_data['Listed Price'] = "Not found"


    # check for discounted price

    discounted_price_element = driver.find_element(By.CSS_SELECTOR, "span.value[automation-id='productPriceOutput']")
    discounted_price = (discounted_price_element.text)
    
    if discounted_price != "" and discounted_price != "--" and discounted_price != "Not found":
        product_data['Original Price'] = product_data['Listed Price']
        product_data['Listed Price'] = discounted_price
    else:
        product_data['Original Price'] = product_data['Listed Price']

    brand, *description_parts = description_element.text.split()
    product_data['Brand'] = brand
    product_data['Description'] = " ".join(description_parts)
 
    sku_element = driver.find_element(By.CSS_SELECTOR, "span[data-sku]")
    product_data['SKU'] = sku_element.get_attribute('data-sku')
        
    # breadcrumbs = driver.find_elements(By.CSS_SELECTOR, "ul.crumbs li")

    #product_data['Category'] = breadcrumbs[-1].text.strip()
    breadcrumbs = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.crumbs li")))
    product_data['Category'] = breadcrumbs[-2].text.strip().split('\n')[-1]
    
    # check stock status
    out_of_stock_button = driver.find_elements(By.CSS_SELECTOR, "input#add-to-cart-btn.out-of-stock")
    if out_of_stock_button:
        product_data['Status'] = "Out of Stock"
        print("Product is out of stock")


    
    print(product_data)

    return product_data
  
    # You can add more scraping logic here based on what data you need
    # make exception for no product found
  except TimeoutException:
        print("Timed out waiting for page to load")
        return None
    
  except Exception as e:
        print(f"Unexpected Error: {e}")
        return None
  
  #finally:
      # Step 6: Close the WebDriver
      # driver.quit()