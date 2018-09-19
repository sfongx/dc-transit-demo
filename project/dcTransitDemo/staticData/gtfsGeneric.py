import requests
import io
import zipfile
import csv

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
    
    def parseStops(self):
        # Open stops.txt as ZipExtFile
        stopsBytes = self.gtfsZip.open('stops.txt', 'r')

        # Read the ZipExtFile 
        stopsFile = stopsBytes.read()

        # Decode the file to CSV using StringIO
        stopsFileCSV = csv.StringIO(stopsFile.decode())

        # Now get the reader
        stopsReader = csv.DictReader(stopsFileCSV)
        
        # Initialize array to return
        out = []

        # Grab the stop name, stop ID, and coordinates
        for row in stopsReader:
            out.append({
                'stop_id': row['stop_id'],
                'stop_name': row['stop_name'],
                'lat': row['stop_lat'],
                'lon': row['stop_lon']
            })

        # Close the ZipExtFile
        stopsBytes.close()
        
        return out

    def parseRoutes(self, file):
        # Open stops.txt as ZipExtFile
        routesBytes = self.gtfsZip.open('routes.txt', 'r')

        # Read the ZipExtFile 
        routesFile = routesBytes.read()

        # Decode the file using the CSV library's StringIO
        routesFileCSV = csv.StringIO(routesFile.decode())
        
        # Now get the reader
        routesReader = csv.DictReader(routesFileCSV)
        
        # Initialize array to return
        out = []

        # Grab the internal agency ID, route ID, short/long names, and colors
        for row in routesReader:
            out.append({
                'internal_agency_id': row['agency_id'],
                'route_id': row['route_id'],
                'short_name': row['route_short_name'],
                'long_name': row['route_long_name'],
                'text_color': row['route_text_color'],
                'background_color': row['route_color']
            })

        # Close the ZipExtFile
        routesBytes.close()
        
        return out
