from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def scraping_start():
    driver.get("https://libgen.is")
    input_search= 'xray'
    open_page_and_input(input_search)
    parsing_and_store_data()



def open_page_and_input(search_text):
    #entering input in searchbar
    search_var= driver.find_element(By.ID, "searchform") #here the id and xpaths might not work in future if libgen's html got changed
    search_var.send_keys(Keys.CONTROL,'a')
    search_var.send_keys(Keys.CLEAR)
    search_var.send_keys(search_text)
    # finding detailed button 
    view_element= driver.find_element(By.XPATH, "//*[@value='simple']")
    view_element.send_keys(Keys.ARROW_RIGHT)
    # setting pages to 100
    res_per_page= driver.find_element(By.NAME, "res")
    for _ in range(3):
        res_per_page.send_keys(Keys.DOWN)
    
    # #making click on search button
    subclick= driver.find_element(By.XPATH,"//*[@value='Search!']" )
    subclick.send_keys(Keys.ENTER)
    return None

def parsing_and_store_data():
    resultSheet= driver.find_element(By.TAG_NAME, 'body')
    html=resultSheet.get_attribute("innerHTML")
    soup = BeautifulSoup(html, 'html.parser')

    parser_titles_and_authors(soup)


def parser_titles_and_authors(soup):
    
    # Find all tables in the HTML
    tables = soup.find_all('table', rules='cols')

    extracted_titles = []

    for table in tables:
        # Find all <td> elements within the table
        td_elements = table.find_all('td', colspan='2')
        
        for td in td_elements:
            # Find the <a> tag within the <td> element
            a_tag = td.find('a')
            
            if a_tag:
                # Extract the text from the <a> tag and append it to the list
                value = a_tag.get_text(strip=True)
                extracted_titles.append(value)

    # Store the extracted values in a file (values.txt)
    with open("book-titles.txt", "w", encoding="utf-8") as f:
        for value in extracted_titles:
            f.write(value + '\n')

    extracted_authors = []

    for table in tables:
        # Find all <td> elements having colspan=3 within the table
        td_elements = table.find_all('td', colspan='3')
        # print(td_elements)
        for td in td_elements:
            # Find the <a> tag within the <td> element
            a_tag = td.find_all('a')
            
            if a_tag:
                # Extract the text from the <a> tag and append it to the list
                concatenated_values=""
                for i in a_tag:
                    value =i.get_text(strip=True)
                    concatenated_values += value + " "
                extracted_authors.append(concatenated_values)


    # Store the extracted values in a file (values.txt)
    with open("authors.txt", "w", encoding="utf-8") as f:
        for value in extracted_authors:
            f.write(value + '\n')        
          
    
if __name__ == "__main__":

    driver = webdriver.Chrome()

    # driver.implicitly_wait(10)
    scraping_start()
    # driver.implicitly_wait(10)

    print("Successful")
    driver.close()
