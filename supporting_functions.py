import csv
import re

import pandas as pd


def dataPreprocessing(csv_file):
  df = pd.read_csv(csv_file)

  #Background related data
  bgProps = df[['url', 'tagName', 'backgroundColor',
       'backgroundImage', 'backgroundPosition', 'backgroundRepeat',
       'backgroundSize']]
  
  #Font related data
  fontProps = df[['url', 'tagName', 'value', 'no_of_chars', 'fontSize', 'color', 'fontFamily', 'fontWeight', 'fontVariant', 
                       'lineHeight','letterSpacing', 'wordSpacing', 'textAlign', 
                       'textDecoration','textTransform','projectedTag']]
  
  fontColors = fontProps[['color']]
  bgColors = bgProps[['backgroundColor']]
  
  #Removing the duplicate entries
  bgProps.drop_duplicates(inplace=True)
  fontProps.drop_duplicates(inplace=True)

  bgColors = color_to_rgb(bgColors,'backgroundColor')   #It converts the color to tuple (r,g,b) field name: rgb_format
  bgColors.drop_duplicates(subset=['rgb_format'], inplace=True)

  fontColors = color_to_rgb(fontColors,'color')   #It converts the color to tuple (r,g,b) field name: rgb_format
  fontColors.drop_duplicates(subset=['rgb_format'], inplace=True)

  #Saving all data to csv files
  bgProps.to_csv('./scrapped_data/bgProps.csv',index=False)
  print('bgProps saved!')
  fontProps.to_csv('./scrapped_data/fontProps.csv',index=False)
  print('fontProps saved!')
  fontColors.to_csv('./scrapped_data/fontColors.csv',index=False)
  print('fontColors saved!')
  bgColors.to_csv('./scrapped_data/bgColors.csv',index=False)
  print('bgColors saved!')

  pass

def color_to_rgb(df,color_field):
   df['rgb_format'] = df[color_field].apply(extract_rgb_values)
   return df

def extract_rgb_values(color_string):
  """Extracts the r, g, and b values from a color string.

  Args:
    color_string: The color string to extract values from.

  Returns:
    A tuple containing the r, g, and b values, or None if the string is invalid.
  """

  # Regular expression to match different color formats
  pattern = r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)" \
            r"|rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+\.\d+)\s*\)" \
            r"|color\s*\(\s*srgb\s*(\d+)\s*(\d+)\s*(\d+)\s*\/\s*(\d+\.\d+)\s*\)"

  match = re.match(pattern, color_string)

  if match:
    # Extract values based on the matched groups
    if match.group(1):
      return int(match.group(1)), int(match.group(2)), int(match.group(3))
    elif match.group(4):
      return int(match.group(4)), int(match.group(5)), int(match.group(6))
    elif match.group(7):
      return int(match.group(7)), int(match.group(8)), int(match.group(9))
    else:
      return 0, 0, 0
  else:
    return 0, 0, 0

def classify_size(size):
    """Classifies the given size into a projected size category."""
    if size >= 30:
        return "H1"
    elif 25 <= size <= 29:
        return "H2"
    elif 21 <= size <= 24:
        return "H3"
    elif 19 <= size <= 20:
        return "H4"
    elif 17 <= size <= 18:
        return "H5"
    else:
        return "H6"

def add_projected_size_column(csv_file_path):
    """Adds a new column 'projected_size' to the specified CSV file."""

    df = pd.read_csv(csv_file_path)
    df['font_size_float'] = df['font_size'].str.replace('px', '', regex=False).astype(float)
    df['projectedTag'] = df['font_size_float'].apply(classify_size)
    pass

async def getTop6(file):
    df = pd.read_csv(file)

    unique_urls = df['url'].unique()

    finaldf = pd.DataFrame(columns=df.columns)

    for url in unique_urls:
        toadd = df[df['url'] == url].sort_values('value',ascending = False)
        toadd = toadd.head(6)
        finaldf = pd.concat([finaldf, toadd], ignore_index=True)
        pass

    finaldf.to_csv('scrapped_data/top6Fonts.csv',index=False)
    # finaldf.to_csv('scrapped_data/final.csv', index=False, mode='a')
    pass

if __name__ == "__main__":
  # color_strings = ["rgba(255, 255, 255, 0.6)", "rgb(41, 40, 40)"]
  # for color_string in color_strings:
  #   r, g, b = extract_rgb_values(color_string)
  #   print(f"r: {r}, g: {g}, b: {b}")
  dataPreprocessing('updated_data.csv')
  pass