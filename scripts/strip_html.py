from bs4 import BeautifulSoup

# Read the content of output.html
with open('output.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Create a BeautifulSoup object and specify the parser
soup = BeautifulSoup(html_content, 'html.parser')

# Remove all <link> tags
for link in soup.find_all('link'):
    link.decompose()

# Remove all <script> tags
for script in soup.find_all('script'):
    script.decompose()

# Remove all <style> tags
for style in soup.find_all('style'):
    style.decompose()

# Remove all <meta> tags except the one with charset attribute
for meta in soup.find_all('meta'):
    if not meta.has_attr('charset'):
        meta.decompose()

# Remove the Content-Security-Policy meta tag
for meta in soup.find_all('meta', attrs={'http-equiv': 'Content-Security-Policy'}):
    meta.decompose()

# Remove all comments
for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
    comment.extract()

# Save the cleaned HTML to clean-output.html
with open('clean-output.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))
