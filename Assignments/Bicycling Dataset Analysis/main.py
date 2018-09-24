"""
Ahmad M. Osman

"For your homework please turn in your Python program with a comment at the top of the program which provides a description of what you found in looking at the data and what your results were. I will need some description of what you were looking for and what you found and how to interpret what you did to know how to grade your homework."

I plotted a graph between the AltitudeMeters and the HeartRateBpm variables. I, instinctively, decided on visualizing those two variables as they were standing out very clearly to make a correlation. I expected to see that the increase in AltitudeMeters would increase the HeartRateBpm, however, the data was not consistent at all with that. There was no correlation found between the two variables, but rather, a wide variety of values on the x-axis corresponded was a wide variety of values on the y-axis. This led me to think of the possible reasons why the correlation wasn't clearly found. One of them was that maybe the variable of DistanceMeters corresponds more with the HeartRateBpm as the amount of time an activity is done over, where time and distance are directly proportional, is a more important factor that would effect the HeartRateBpm and be of a correlation with. By looking through the data with eyes, I found out that the increase in the DistanceMeters variables is correlated with the increase of the HeartRateBpm. This is something that can be more explored if we can have two plotted variables with the HeartRateBpm, and with that in mind, I decided to add another sequence to plot which was the DistanceMeters with the HeartRateBpm. By looking at the plotted graph of the DistanceMeters, AltitudeMeters, and HeartRateBpm, I came to conclude that, in general, there is a better trend of DistanceMeters with the HeartRateBpm, but this trend still does not necessarily show a correlation as a variety of values on the x-axis corresponded was a wide variety of values on the y-axis. It simply can be that the DistanceMeters counted was not necessarily correctly taken on the bike, or maybe it was taken over a long day where the data kept being recorded not just while biking but also throughout the day, and thus the average HeartRateBpm got smaller and smaller that way. There are other ways to look at this data, starting with looking at the correlation value would be interesting, and from there we can discuss where the failure might be, and if not failure, maybe we can just conclude that that there is no correlation at all. Maybe a bigger dataset with minimal outliers, or maybe figuring out the cause of the outliers and justifying the elimination of those outliers to be able to show a correlation, among other ideas, can be used when visualizing and analyzing this dataset. Or simply, one can say that his understanding of this dataset is invalid, and go back to the variable descriptors to make more sense of what they are. All of these scenarios are possible.

All files attached, including the AltitudeHrtRate and the AltitudeDistanceHrtRate plot data.
"""

from xml.dom.minidom import parse

def main():
    xmldoc = parse("biking3-15-2012.tcx.xml")

    activities_element = xmldoc.getElementsByTagName("Activities")[0]
    activity_element = activities_element.getElementsByTagName("Activity")[0]
    trackpoints_element = activity_element.getElementsByTagName("Trackpoint")
    
    file = open("AltitudeDistanceHrtRate.xml", "w")
    file.write('<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n')
    file.write('<Plot title="Heart Rate and Altitude Meters/Distance Meters Relationship">\n')

    altitude_lst = []
    hrtrate_lst = []
    distance_lst = []

    for trackpoint_element in trackpoints_element:
        try:
            altitude_meters_element = trackpoint_element.getElementsByTagName("AltitudeMeters")[0]
            altitude = altitude_meters_element.firstChild.data
            
            altitude_lst.append(float(altitude))

            heart_rate_element = trackpoint_element.getElementsByTagName("HeartRateBpm")[0]
            heart_rate_value_element = heart_rate_element.getElementsByTagName("Value")[0]
            heartrate = heart_rate_value_element.firstChild.data
            
            hrtrate_lst.append(int(heartrate))

            distance_meters_element = trackpoint_element.getElementsByTagName("DistanceMeters")[0]
            distance = distance_meters_element.firstChild.data
            
            distance_lst.append(float(distance))
            
        except Exception as e:
            continue

    file.write('  <Axes>\n')
    file.write('    <XAxis min="'+str(min(hrtrate_lst))+'" max="'+str(max(hrtrate_lst))+'">Heart Rate BPM</XAxis>\n')
    file.write('    <YAxis min="'+str(min(altitude_lst))+'" max="'+str(max(distance_lst))+'">Altitude Meters - Distance Meters</YAxis>\n')
    file.write('  </Axes>\n')
    
    file.write('  <Sequence title="Heart Rate BMP vs Altitude Meters" color="red">\n') 
    for i in range(len(hrtrate_lst)):
        file.write('    <DataPoint x="'+str(hrtrate_lst[i])+'" y="'+str(altitude_lst[i])+'"/>\n')
    file.write('  </Sequence>\n')

    file.write('  <Sequence title="Heart Rate BMP vs Distance Meters" color="blue">\n')
    for i in range(len(hrtrate_lst)):
        file.write('    <DataPoint x="'+str(hrtrate_lst[i])+'" y="'+str(distance_lst[i])+'"/>\n')
    file.write('  </Sequence>\n')

    file.write('</Plot>\n')
    file.close()  

if __name__ == "__main__":
    main()
