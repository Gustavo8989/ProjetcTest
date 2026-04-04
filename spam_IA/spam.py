# Identificação de spam no Email
import pandas as pd 
import kagglehub
import re

path = kagglehub.dataset_download("uciml/sms-spam-collection-dataset")
print("Path to dataset files:", path)
