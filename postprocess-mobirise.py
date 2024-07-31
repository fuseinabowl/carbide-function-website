from typing import List
from pathlib import Path
from bs4 import BeautifulSoup
import os
import tempfile
import shutil

script_path = Path(__file__)
exported_website_path = script_path.parent
css_path = exported_website_path / r'assets/theme/css/style.css'

def main() -> None:
  remove_mobirise_footers_from_pages()
  add_background_to_css()

def remove_mobirise_footers_from_pages() -> None:
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
    soup = BeautifulSoup(file_handle.read(), features="html.parser")

  sections = soup.find_all('section')
  for section in sections:
    print(f'section: {(section.attrs["class"])}')
    if 'display-7' in section.attrs["class"]:
      section.extract()

  with open(file_path, 'w') as file_handle:
    file_handle.write(str(soup))

def add_background_to_css() -> None:
  found_body_tag = False
  with open(css_path, 'r') as source_file:
    (destination_file_os_handle, temp_path) = tempfile.mkstemp()
    with os.fdopen(destination_file_os_handle, 'w') as destination_file:
      for line in source_file:
        destination_file.write(line)
        if line.startswith('body {'):
          found_body_tag = True
          destination_file.write('  background-color: #385493;\n')
  assert found_body_tag, 'did not find body tag in CSS file'
  move_temp_file_to_css(temp_path, css_path)


def move_temp_file_to_css(temp_css_file : Path, css_path : Path) -> None:
  shutil.move(str(temp_css_file), str(css_path))

if __name__ == '__main__':
  main()
