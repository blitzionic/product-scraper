from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime


'''
active product: done
discontinued/out-of-stock product: 
no results found: done
'''

def scrape_lowes(model_number, driver):
  
  model_url = f"https://www.lowes.com/search?searchTerm={model_number}"
  print(model_url)

  try:
    
    product_data = {
      'Retailer': "Lowes", # 
      'Link': model_url, # 
      'Brand': "", # 
      'Category': "", # 
      'Model Number': model_number, # 
      'SKU': "", # 
      'Description': "", # 
      'Status': "Active", 
      'Listed Price': 0.0, # 
      'Original Price': 0.0, # 
      'Date': datetime.now().strftime('%Y-%m-%d') # 
    }

    driver.get(model_url)

    


    try:  # complete this
      no_results_message = driver.find_element(By.XPATH, "//h1[contains(@class, 'styles__H1-sc-11vpuyu-0') and contains(text(), 'No Results Found')]")
      if no_results_message:
        print(product_data)

        return product_data
    except:
      print("Results found, proceed with scraping.")  

    
    price_element = driver.find_element(By.CSS_SELECTOR, "span.item-price-dollar")
    product_data['Listed Price'] = price_element.text

    original_price_element = driver.find_element(By.CSS_SELECTOR, "span.was-price-inline")
    product_data['Original Price'] = original_price_element.text

    title_element = driver.find_element(By.CSS_SELECTOR, "title")
    title_text = title_element.get_attribute("textContent")
    
    brand = title_text.split()[0] 
    product_data['Brand'] = brand

    product_data['Description'] = title_text.split(brand)[1]

    breadcrumbs = driver.find_elements(By.CSS_SELECTOR, "nav.BreadcrumbDesktopBase-sc-e8flgh-0 ol li a")
    if len(breadcrumbs) >= 2:
        product_data['Category'] = breadcrumbs[-2].text.strip()
    else:
      product_data['Category'] = "Unknown"

    try:
      sku_element = driver.find_element(By.CSS_SELECTOR, "p.styles__ParagraphRegular-sc-1ljw3tp-0")
      sku_text = sku_element.text
      product_data['SKU'] = sku_text.split("Item #")[-1].split("|")[0].strip()
    except:
      product_data['SKU'] = "N/A"


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
  
  finally:
      # Step 6: Close the WebDriver
      driver.quit()

