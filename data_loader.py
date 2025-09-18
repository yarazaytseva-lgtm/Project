import pandas as pd
import requests
from io import StringIO

FILE_ID = "10eufblSIFd0USk8-6YX2O5NyMI1RlaP-"
file_url = f"https://drive.google.com/uc?export=download&id={FILE_ID}"

response = requests.get(file_url)
raw_data = pd.read_csv(StringIO(response.text))
print(raw_data.head(10))

# https://drive.google.com/file/d/10eufblSIFd0USk8-6YX2O5NyMI1RlaP-/view?usp=drive_link