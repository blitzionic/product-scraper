from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

'''
active product: done
discontinued/out-of-stock product: 
no results found: 
'''

def scrape_home_depot(model_number, driver):
    model_url = f"https://www.homedepot.com/s/{model_number}"
    print("MODEL URL: ", model_url)

    try:
        product_data = {
          'Retailer': "Home Depot",
          'Link': model_url,
          'Brand': "",
          'Category': "",
          'Model Number': model_number,
          'SKU': "",
          'Description': "",
          'Status': "Active",
          'Listed Price': 0.0,
          'Original Price': 0.0,
          'Date': datetime.now().strftime('%Y-%m-%d')
        }

        driver.get(model_url)

        try:
          price_element = driver.find_element(By.CSS_SELECTOR, ".price-format__large.price-format__main-price")
          price_parts = price_element.find_elements(By.TAG_NAME, "span")
          product_data['Listed Price'] = ''.join([part.get_attribute('textContent').strip() for part in price_parts])
        except:
          # not working 
          price_element = driver.find_element(By.XPATH, "//div[contains(@class, 'price-format__main-price')]//span[contains(text(), '$')]")
          product_data['Listed Price'] = price_element.get_attribute('textContent').strip()
          product_data['Status'] = "Discontinued"
          
        # get original price
        #original_price_element = driver.find_element(By.CSS_SELECTOR, ".price-detailed__was-price .u__strike span")
        
        try:
            original_price_element = driver.find_element(By.CSS_SELECTOR, ".price-detailed__was-price .u__strike span")
            product_data['Original Price'] = original_price_element.get_attribute('textContent').strip()
        except:
            try:  # discontinued product format
                original_price_element = driver.find_element(By.CSS_SELECTOR, ".price__was-price .u__strike span")
                product_data['Original Price'] = original_price_element.get_attribute('textContent').strip()
            except:
                original_price_element = None

        if original_price_element is None:
            product_data['Original Price'] = product_data['Listed Price']

        brand = driver.find_element(By.CSS_SELECTOR, "h2.sui-font-regular.sui-text-base.sui-tracking-normal.sui-normal-case.sui-line-clamp-unset.sui-font-normal.sui-text-primary").text
        product_data['Brand'] = brand

        sku = driver.find_element(By.CSS_SELECTOR, ".sui-font-regular.sui-text-xs.sui-leading-normal.sui-tracking-normal.sui-normal-case.sui-line-clamp-unset.sui-font-normal.sui-text-primary.sui-text-left").text.split()[-1]
        product_data['SKU'] = sku

        breadcrumbs = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.breadcrumbs"))
        )

        breadcrumb_items = breadcrumbs.find_elements(By.CSS_SELECTOR, "a")

        category = breadcrumb_items[-2].text if len(breadcrumb_items) > 1 else breadcrumb_items[-1].text
        product_data['Category'] = category

        description = driver.find_element(By.CSS_SELECTOR, "title").get_attribute("textContent")
        description_parts = description.split()

        modified_description = ' '.join(description_parts[1:])
        ending_phrase = " - The Home Depot"

        if modified_description.endswith(ending_phrase):
            modified_description = modified_description[:-len(ending_phrase)].strip()

        product_data['Description'] = modified_description



        print(product_data)

        return product_data
    
    except TimeoutException:
        print("Timed out waiting for page to load")
        return None
    
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return None
