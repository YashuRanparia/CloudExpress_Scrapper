import csv
import urllib.parse

import cssutils
import requests
from bs4 import BeautifulSoup


def extract_and_save_style_data(url, element_selectors, output_file):
  """Extracts style data for specified elements and saves it to a text file.

  Args:
    url: The URL of the webpage.
    element_selectors: A list of CSS selectors for the target elements.
    output_file: The path to the output text file.
  """

  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')

  all_elements = soup.find_all()

  with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['element_type', 'property', 'value']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for element in all_elements:
        inline_styles = element.attrs.get('style')
        external_stylesheets = [link['href'] for link in soup.find_all('link', rel='stylesheet')]
        external_styles = {}
        for css_url in external_stylesheets:
          base_url = urllib.parse.urljoin(url, css_url)
          css_content = requests.get(base_url).text
          sheet = cssutils.parseString(css_content)
          for rule in sheet:
            if isinstance(rule, cssutils.css.CSSStyleRule):
              if rule.selectorText == element:
                for property in rule.style.properties:
                    external_styles[property.name] = property.value

        merged_styles = {}
        if inline_styles:
          merged_styles = dict(tuple(style.split(':')) for style in inline_styles.split(';') if style)
        merged_styles.update(external_styles)

        style_properties = ['font-family', 'font-style', 'font-size', 'color']

        for property, value in merged_styles.items():
          if property in style_properties:
            writer.writerow({
              'element_type': element.name,  # Get element type (e.g., p, div)
              'property': property,
              'value': value,
            })