import requests
from lxml import html
import json
import csv

def main():
    # Using XPath and JSON to extract a dictionary of all top 500 IMDB movies IDs 
    imdb = requests.get("https://www.imdb.com/list/ls003073623/")
    tree = (html.fromstring(imdb.content))
    movies = tree.xpath('//html/head/script[@type="application/ld+json"]/text()')[0]
    
    # We have our dictionary now
    jsonDict = json.loads(movies)

    # Lets get the urls that contain the ids
    jsonDict = jsonDict['about']['itemListElement']
    # Now we will have a list of IDs
    imdbIDs = [id['url'].split('/')[2] for id in jsonDict]

    # Preparing CSV file for storage
    headers_written = False
    filename = "osmanTop500MoviesInflationAdjusted.csv"

    # A context window to write each movie to the CSV file
    with open (filename, 'a') as csvfile:
        # Looping through the movies IDs, getting the info we want, doing data cleaning and finding the adjusted box office value, and then we save to the CSV file
        for imdbID in imdbIDs:
            # Now we use OMDB to get all the information we want
            movie = requests.get("http://www.omdbapi.com/?apikey=47734a01&i=" + imdbID)
            movie = json.loads(movie.content)
            
            # We clean the data - and get adjusted box office value            
            try:
                movie["imdbVotes"] = str(movie["imdbVotes"]).replace(',', '')
                movie["Released"] = str(movie["Released"]).replace(' ', '-')
                movie["Month"] = str(movie["Released"].split('-')[1])
                movie["DVD"] = str(movie["DVD"]).replace(' ', '-')
            except:
                pass

            # Preparing for inflation value factor
            # https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1&year1=199905&year2=201808
            months = { 'Jan' : '01', 'Feb' : '02', 'Mar' : '03', 'Apr' : '04', 'May' : '05', 'Jun' : '06', 'Jul' : '07', 'Aug' : '08', 'Sep' : '09', 'Oct' : '10', 'Nov' : '11', 'Dec' : '12' }
            
            try:
                # Cleaning BoxOffice values and Calculating the Adjusted Box Office Value
                movie["BoxOffice"] = str(movie["BoxOffice"]).replace(',', '')
                movie["BoxOffice"] = str(movie["BoxOffice"]).replace('$', '')

                # Getting adjusted value factor and calculating the adjusted box office value
                cpiStr = "https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1&year1=" + str(movie["Year"]) + str(months[movie["Month"]]) + "&year2=201808"
                cpiPage = requests.get(cpiStr)
                cpiTree = html.fromstring(cpiPage.content)
                factor = float(cpiTree.xpath('//span[@id="answer"]/text()')[0][1:].replace(',',''))
                movie["AdjustedForInflationBoxOffice"] = float(movie["BoxOffice"]) * factor
            except:
                movie["AdjustedForInflationBoxOffice"] = 0

            # Deleing the Ratings data - we do not need it
            del movie["Ratings"]

            # Starting to write to CSV file for this loop entry
            headers = movie.keys()
            writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n',fieldnames=headers)

            # Writing CSV file header once - at the first iteration of the loop
            if not headers_written:
                writer.writeheader()
                headers_written = True

            # Writing movie data to the CSV file
            writer.writerow(movie)


if __name__ == "__main__":
    main()
