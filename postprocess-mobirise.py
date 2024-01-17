from typing import List
from pathlib import Path
from bs4 import BeautifulSoup
import os

script_path = Path(__file__)
exported_website_path = script_path.parent

def main():
  remove_mobirise_footers_from_pages()
  add_background_to_css()

def remove_mobirise_footers_from_pages():
  html_files = find_html_files_in_directory(exported_website_path)
  for file_path in html_files:
    remove_mobirise_footer(file_path)

def find_html_files_in_directory(directory : Path) -> List[Path]:
  html_files = []
  for root, directories, filenames in os.walk(str(directory)):
    for filename in filenames:
      if filename.endswith('.html'):
        html_files.append(Path(os.path.join(root, filename)))
  return html_files

def remove_mobirise_footer(file_path : Path) -> None:
  print(f'loading path {file_path}')
  with open(file_path, 'r') as file_handle:
    soup = BeautifulSoup(file_handle.read())

  sections = soup.find_all('section')
  for section in sections:
    print(f'section: {(section.attrs["class"])}')
    if 'display-7' in section.attrs["class"]:
      section.extract()
  #for element in tree.iter():
  #  if element.name == 'body':
  #    for body_element in element.iter():
  #      classes = body_element.get('class')
  #      if classes.contains('display-7'):
  #        element.remove(body_element)

  with open(file_path, 'w') as file_handle:
    file_handle.write(str(soup))

def add_background_to_css():
  pass

if __name__ == '__main__':
  main()
