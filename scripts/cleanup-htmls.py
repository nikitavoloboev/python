import os
import shutil
from datetime import datetime
from bs4 import BeautifulSoup, Comment
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from markdown import markdown

class HTMLProcessor(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('output.html'):
            self.process_html(event.src_path)

    def process_html(self, file_path):
        # Read the content of output.html
        with open(file_path, 'r', encoding='utf-8') as file:
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
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        # Remove all <svg> tags
        for svg in soup.find_all('svg'):
            svg.decompose()

        # Remove all <button> tags
        for button in soup.find_all('button'):
            button.decompose()

        # Remove all <template> tags
        for template in soup.find_all('template'):
            template.decompose()

        # Remove all <path> tags
        for path in soup.find_all('path'):
            path.decompose()

        # Remove all <span> tags
        for span in soup.find_all('span'):
            span.unwrap()

        # Remove all <div> tags
        for div in soup.find_all('div'):
            div.unwrap()

        # Remove all <a> tags but keep the text content
        for a in soup.find_all('a'):
            a.unwrap()

        # Convert the cleaned HTML to Markdown
        markdown_content = markdown(str(soup))

        # Save the Markdown content to clean.md
        clean_file_path = os.path.join(os.path.dirname(file_path), 'clean.md')
        with open(clean_file_path, 'w', encoding='utf-8') as file:
            file.write(markdown_content)

        # Rename the processed output.html file
        current_date = datetime.now().strftime('%Y-%m-%d')
        new_file_name = f'processed-{current_date}.html'
        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
        shutil.move(file_path, new_file_path)

if __name__ == "__main__":
    path = os.path.expanduser('~/process')
    event_handler = HTMLProcessor()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
