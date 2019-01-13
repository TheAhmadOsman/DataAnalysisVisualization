# Ahmad M. Osman - DS320
import urllib
import ssl
from bs4 import BeautifulSoup

# Reading the front page HTML
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Read the HTML from the URL and pass on to BeautifulSoup
url = 'https://www.cia.gov/library/publications/the-world-factbook/'
print("Opening the file connection...")
uh = urllib.request.urlopen(url, context=ctx)
print("HTTP status", uh.getcode())
html = uh.read().decode()
print("Reading done. Total {} characters read.".format(len(html)))

soup = BeautifulSoup(html, 'html.parser')
country_codes = []
country_names = []

# Find the HTML tags named ‘option’
for tag in soup.find_all('option'):
    # The char 5 and 6 of the tag value represent the 2-character country code.
    country_codes.append(tag.get('value')[5:7])
    country_names.append(tag.text)
temp = country_codes.pop(0)  # To remove the first entry 'World'
temp = country_names.pop(0)  # To remove the first entry 'World'

# Download all the text data of all countries into a dictionary by scraping each page individually
# The key thing to identify is how the URL of each countries information page is structured

# Base URL
urlbase = 'https://www.cia.gov/library/publications/the-world-factbook/geos/'
# Empty data dictionary
text_data = dict()
# Iterate over every country
for i in range(1, len(country_names)-1):
    country_html = country_codes[i]+'.html'
    url_to_get = urlbase+country_html
    # Read the HTML from the URL and pass on to BeautifulSoup
    html = urllib.request.urlopen(url_to_get, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    txt = soup.get_text()
    text_data[country_names[i]] = txt
    print("Finished loading data for {}".format(country_names[i]))

print("\n**Finished downloading all text data!**")

# Converting string to float


def convert_float(string):
    if string.isnumeric():
        return float(string)
    if string[0].isdigit():
        if ',' not in string and '.' in string:
            return float(string)
        if ',' not in string and '.' not in string:
            idx = string.find(' ')
            result = string[:idx]
            return float(result)
        idx1 = string.find(',')
        idx2 = string.find(' ')
        result = string[:idx1]+string[idx1+1:idx2]
        return float(result)
    else:
        return (-1)


# Using regular expression to extract the GDP/capita data from the text dump
# 'b' to catch 'billions', 't' to catch 'trillions'
# Notice the multiple error-handling checks placed in the code.
import re

# Initialize dictionary for holding the data
GDP_PPP = {}
# Iterate over every country
for i in range(1, len(country_names)-1):
    country = country_names[i]
    txt = text_data[country]
    pos = txt.find('GDP - per capita (PPP):')
    if pos != -1:  # If the wording/phrase is not present
        pos = pos+len('GDP - per capita (PPP):')
        string = txt[pos+1:pos+11]
        start = re.search('\$', string)
        end = re.search('\S', string)
        if (start != None and end != None):  # If search fails somehow
            start = start.start()
            end = end.start()
            a = string[start+1:start+end-1]
            # print(a)
            a = convert_float(a)
            if (a != -1.0):  # If the float conversion fails somehow
                # print("GDP/capita (PPP) of {}: {} dollars".format(country, a))
                # Insert the data in the dictionary
                GDP_PPP[country] = a
            # else:
                # print("**Could not find GDP/capita data!**")
        # else:
            # print("**Could not find GDP/capita data!**")
    # else:
        #print("**Could not find GDP/capita data!**")
print("Finished finding all GDP/capita data")

# Using regular expression to extract the internet user percentage data from the text dump
# Initialize dictionary for holding the data
Internet_user = {}
# Iterate over every country
for i in range(1, len(country_names)-1):
    country = country_names[i]
    txt = text_data[country]
    pos = txt.find('Internet users:')
    if pos != -1:
        pos = pos+len('Internet users: ')
        string = txt[pos:pos+50]
        # print(string)
        start = re.search('percent of population: ', string)
        end = re.search('%', string)
        if (start != None and end != None):
            start = start.end()
            end = end.start()
            a = string[start:end]
            if a[-1].isdigit():
                a = float(a)
                #print("Internet users % of {}: {}".format(country, a))
                # Insert the data in the dictionary
                Internet_user[country] = a
            # else:
                #print("**Could not find Internet users data!**")
        # else:
           # print("**Could not find Internet users data!**")
    # else:
        #print("**Could not find Internet users data!**")

print("Finished finding all Internet users data")

# Saving into CSV
import csv

print("\nSaving data into CSV file")

with open('InternetUsers-GDPPerCapita.csv', mode='w') as csv_file:
    fieldnames = ['Country', 'Internet Users %', 'GDP/Capita']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for key, value in Internet_user.items():
        try:
            writer.writerow(
                {'Country': key.strip(), 'Internet Users %': value, 'GDP/Capita': GDP_PPP[key]})
        except:
            continue

print("Finished saving data into CSV file")
