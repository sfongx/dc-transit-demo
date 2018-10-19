import requests
import io
import zipfile
import csv
import datetime

class GtfsGeneric():
    def __init__(self, url):
        # Attempt to download the zip and get it into memory
        try:
            # Get the zip response from the URL
            response = requests.get(url)

            # Save the zip as a class member
            self.gtfsZip = zipfile.ZipFile(io.BytesIO(response.content))
        
        except zipfile.BadZipFile:
            raise Exception("Error: bad zip file.")
        
        except zipfile.LargeZipFile:
            raise Exception("Error: zip file too large.")

        except:
            raise Exception("Uh-oh: Non-zip error happened.")

    def closeZip(self):
        # Close out the zipfile when done
        self.gtfsZip.close()

    def getCsvReader(self, filename):
        # Helper function to grab a specific file (stops, routes, etc.)
        
        # Open as ZipExtFile
        bytesFile = self.gtfsZip.open(filename, 'r')

        # Read the ZipExtFile 
        readFile = bytesFile.read()

        # Decode the ZipExtFile to CSV format using StringIO
        csvFile = csv.StringIO(readFile.decode())

        # Close the file
        bytesFile.close()

        # Return a dict reader for the CSV
        return csv.DictReader(csvFile)
    
    def parseStops(self):
        # Get the CSV dict reader for the stops file
        stopsReader = self.getCsvReader('stops.txt')

        # Just return reader out to the migration
        return stopsReader

    def parseRoutes(self):
        # Get the CSV dict reader for the stops file
        routesReader = self.getCsvReader('routes.txt')
        
        # Initialize array to return
        out = []

        # Grab the internal agency ID, route ID, short/long names, and colors
        for row in routesReader:
            # First deal with empty values for short and long names
            # Assumes at least one of them is non-empty
            if row['route_short_name'] == False:
                short_name = "-"
            else:
                short_name = row['route_short_name']

            if row['route_long_name'] == False:
                long_name = "-"
            else:
                long_name = row['route_long_name']

            # Put it together afterwards
            out.append({
                'internal_agency_id': row['agency_id'],
                'route_id': row['route_id'],
                'short_name': short_name,
                'long_name': long_name,
                'text_color': row['route_text_color'],
                'background_color': row['route_color']
            })
        
        return out

    def parseTrips(self):
        # Get the CSV dict reader for the stops file
        tripsReader = self.getCsvReader('trips.txt')

        # Just return the reader out to the migration
        return tripsReader

    def parseCalendar(self):
        # Get the CSV dict reader for the calendar file
        calendarReader = self.getCsvReader('calendar.txt')

        # Just return the reader out to the migration
        return calendarReader


    def parseStopTimes(self):
        # Get the CSV dict reader for the stops file
        stopTimesReader = self.getCsvReader('stop_times.txt')
        
        # Initialize array to return
        out = []

        # Grab the trip ID, stop ID, and arrival/departure times
        for stopTime in stopTimesReader:
            # Separate arrival time into its components so a datetime.time object can be created
            # Mod the hour by 24 to deal with early morning times (24 = midnight, 25 = 1 AM, etc)
            arrComps = stopTime['arrival_time'].split(":")
            arrHour = int(arrComps[0]) % 24
            arrMin = int(arrComps[1])
            arrSec = int(arrComps[2])
            
            # Separate departure time into its components so a datetime.time object can be created
            # Mod the hour by 24 to deal with early morning times (24 = midnight, 25 = 1 AM, etc)
            depComps = stopTime['departure_time'].split(":")
            depHour = int(depComps[0]) % 24
            depMin = int(depComps[1])
            depSec = int(depComps[2])

            # Now put it together. datime.time object will be created in the migration file
            out.append({
                'trip_id': stopTime['trip_id'],
                'stop_id': stopTime['stop_id'],
                'arr_hour': arrHour,
                'arr_min': arrMin,
                'arr_sec': arrSec,
                'dep_hour': depHour,
                'dep_min': depMin,
                'dep_sec': depSec,
            })

        return out

