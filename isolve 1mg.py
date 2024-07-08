import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.1mg.com/categories/health-conditions/derma-care-1183'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Log the response content for debugging
with open('response_content.html', 'w', encoding='utf-8') as f:
    f.write(soup.prettify())

products = soup.find_all('div', class_='sku-card-item style__slide-parent___3t2fC style__hover-effect___1MxM7')

if products:
    with open('ecommerce_product_list.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Image', 'MRP', 'Selling Price', 'Ratings', 'Number of Ratings'])

        for product in products:
            name_elem = product.find('div', class_='style__name___3YOZc style__large-font___2dBUf')
            name = name_elem.text.strip() if name_elem else 'No Name'
            
            # Debug: Print the product block to see the structure
            print("Product Block:", product.prettify())
            
            # Attempt to find the image URL
            image_elem = product.find('img', class_='style__image___Ny-Sa style__loaded___22epL')
            if not image_elem:
                # If not found, try a different approach or print the product block
                print("Image element not found in product block:", product.prettify())
                image = 'No Image'
            else:
                image = image_elem['src'] if 'src' in image_elem.attrs else 'No Image'

            ratings_elem = product.find('span', class_='CardRatingDetail__weight-700___27w9q')
            ratings = ratings_elem.text.strip() if ratings_elem else 'No Ratings'
            
            num_ratings_elem = product.find('span', class_='CardRatingDetail__ratings-header___2yyQW')
            num_ratings = num_ratings_elem.text.strip().split()[0] if num_ratings_elem else 'No Number of Ratings'
            
            mrp_elem = product.find('span', class_='style__strike-price___3Ag3J')
            mrp = mrp_elem.text.strip().replace('₹', '') if mrp_elem else 'No MRP'

            price_elem = product.find('div', class_='style__price___196ew')
            price = price_elem.text.strip().replace('₹', '') if price_elem else 'No Selling Price'

            writer.writerow([name, image, mrp, price, ratings, num_ratings])

    print('Data extraction and cleaning complete. File saved as ecommerce_product_list.csv')
else:
    print('No products found. Please check the CSS selector.')
