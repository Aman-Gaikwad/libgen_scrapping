import requests


def get_book_cover_image(book_name):
    api_key = 'yourAPIkey'
    url = 'https://www.googleapis.com/books/v1/volumes?q={}&key={}'.format(book_name, api_key)
    response = requests.get(url)
    if response.status_code == 200:
        book_info = response.json()
        if 'items' in book_info:
            image_url = book_info['items'][0]['volumeInfo'].get('imageLinks', {}).get('thumbnail')
            return image_url
    return None

# Read book titles from book-titles.txt and fetch image URLs
book_info_list = []

with open("book-titles.txt", "r", encoding="utf-8") as title_file:
    book_titles = title_file.read().splitlines()

for title in book_titles:
    image_url = get_book_cover_image(title)
    if image_url:
        book_info_list.append(image_url + "\n")
    else:
        book_info_list.append("\n")

# Save the book information to image-url.txt
with open("image-url.txt", "w") as image_url_file:
    image_url_file.writelines(book_info_list)

print("Book titles and image URLs saved to image-url.txt.")