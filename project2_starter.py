# SI 201 Project 2
# Your name: Jake Verbick
# Your student id: 05350662
# Your email: jakeverb@umich.edu
# Who or what you worked with: I worked alone.
#  I used Gemini AI as a learning resource. I had the tool teach me (re-teach me) how to approach extracting from the files, as well as verifying the class tag i inspected was correct so that my project would run properly
# I as well sent my program + instructions after completiton to Gemini in order to verify the code was representative of the rubric.

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests

def load_listing_results(html_path):
   with open(html_path, 'r', encoding='utf-8-sig') as f:
       content = f.read()
   soup = BeautifulSoup(content, 'html.parser')
   listings = []
   title_tags = soup.find_all('div', class_='t1jojoys')
   for tag in title_tags:
       listing_title = tag.get_text(strip=True)
       tag_id_attr = tag.get('id', '')
       listing_id = tag_id_attr.replace("title_", "")
       if listing_id:
           listings.append((listing_title, listing_id))
   return listings[:18]

      
def get_listing_details(listing_id):
   filename = os.path.join("html_files", f"listing_{listing_id}.html")
   with open(filename, 'r', encoding='utf-8-sig') as f:
       content = f.read()
   soup = BeautifulSoup(content, 'html.parser')
  
   # Policy Number
   policy_number = "None"
   policy_tag = soup.find('li', class_='f19phm7j')
   if policy_tag:
       text = policy_tag.get_text()
       if "pending" in text.lower():
           policy_number = "Pending"
       elif "exempt" in text.lower():
           policy_number = "Exempt"
       elif ":" in text:
           policy_number = text.split(':')[-1].strip()


   #Host Type
   if "Superhost" in content:
       host_type = "Superhost" 
   else:
       host_type = "regular"


   #Host Name
   host_name = "None"
   for h2 in soup.find_all('h2'):
       if "Hosted by" in h2.get_text():
           host_name = h2.get_text().replace("Hosted by ", "").strip()
           break


   #Room Type
   subtitle_tag = soup.find('h2', class_='_14i3z6h')
   subtitle = subtitle_tag.get_text() if subtitle_tag else ""
  
   if "Private" in subtitle:
       room_type = "Private Room"
   elif "Shared" in subtitle:
       room_type = "Shared Room"
   else:
       room_type = "Entire Room"


   #Location Rating
   location_rating = 0.0
   rating_rows = soup.find_all('div', class_='_a3qxec')
   for row in rating_rows:
       if "Location" in row.get_text():
           rating_span = row.find('span', class_='_4oybiu')
           if rating_span:
               location_rating = float(rating_span.get_text().strip())
               break
              
   return {listing_id: {
       "policy_number": policy_number,
       "host_type": host_type,
       "host_name": host_name,
       "room_type": room_type,
       "location_rating": location_rating
   }}


def create_listing_database(html_path):
   listings = load_listing_results(html_path)
   database = []
  
   for listing_title, listing_id in listings:
      
       details_hidden = get_listing_details(listing_id)
       details = details_hidden[listing_id]
      
       listing_tuple = (
           listing_title,
           listing_id,
           details['policy_number'],
           details['host_type'],
           details['host_name'],
           details['room_type'],
           details['location_rating']
       )


       database.append(listing_tuple)
      
   return database

    

def output_csv(data, filename):
   data.sort(key=lambda x: x[6], reverse=True)


   header = [
       "Listing Title",
       "Listing ID",
       "Policy Number",
       "Host Type",
       "Host Name",
       "Room Type",
       "Location Rating"
   ]


   with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
       writer = csv.writer(f)
       writer.writerow(header)
       writer.writerows(data)

    

def avg_location_rating_by_room_type(data):
   room_sums = {}
   room_counts = {}


   for row in data:
      
       room_type = row[5]
       location_rating = row[6]


       if location_rating > 0.0:
          
           room_sums[room_type] = room_sums.get(room_type, 0.0) + location_rating
           room_counts[room_type] = room_counts.get(room_type, 0) + 1


   averages_dict = {}
   for r_type in room_sums:
      
       average = room_sums[r_type] / room_counts[r_type]
       averages_dict[r_type] = round(average, 1)


   return averages_dict


def validate_policy_numbers(data):
  
   valid_pattern = r'^(20\d{2}-00\d{4}STR|STR-000\d{4})$'
   invalid_listing_ids = []
  
   for row in data:
     
       listing_id = row[1]
       policy_number = row[2]
      
       if policy_number in ["Pending", "Exempt"]:
           continue
      
       if not re.match(valid_pattern, policy_number):
           invalid_listing_ids.append(listing_id)
          
   return invalid_listing_ids


def google_scholar_searcher(query):
   search_url = "https://scholar.google.com/scholar?q=" + query
  
   response = requests.get(search_url)
  
   soup = BeautifulSoup(response.text, 'html.parser')
  
   title_headers = soup.find_all('h3', class_='gs_rt')
  
   article_titles = []
   for header in title_headers:
      
       title_text = header.get_text()
       article_titles.append(title_text)
      
   return article_titles

    
class TestCases(unittest.TestCase):
   def setUp(self):
      
       self.base_dir = os.path.abspath(os.path.dirname(__file__))
       self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")


       self.listings = load_listing_results(self.search_results_path)
       self.detailed_data = create_listing_database(self.search_results_path)


   def test_load_listing_results(self):
      
       self.assertEqual(len(self.listings), 18)
       self.assertEqual(self.listings[0], ("Loft in Mission District", "1944564"))


   def test_get_listing_details(self):
       html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]


       results = []
       for l_id in html_list:
           results.append(get_listing_details(l_id))


     
       d467 = get_listing_details("467507")["467507"]
       self.assertEqual(d467["policy_number"], "STR-0005349")


      
       d194 = get_listing_details("1944564")["1944564"]
       self.assertEqual(d194["host_type"], "Superhost")
       self.assertEqual(d194["room_type"], "Entire Room")


       self.assertEqual(d194["location_rating"], 4.9)


   def test_create_listing_database(self):
     
       for row in self.detailed_data:
           self.assertEqual(len(row), 7)


       expected_last = ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8)
       self.assertEqual(self.detailed_data[-1], expected_last)


   def test_output_csv(self):
      
       out_path = os.path.join(self.base_dir, "test.csv")


       output_csv(self.detailed_data, out_path)
      
       rows = []
       with open(out_path, 'r', encoding='utf-8-sig') as f:
           reader = csv.reader(f)
           for row in reader:
               rows.append(row)


       expected_first_row = ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"]
       self.assertEqual(rows[1], expected_first_row)
       os.remove(out_path)


   def test_avg_location_rating_by_room_type(self):
       averages = avg_location_rating_by_room_type(self.detailed_data)
       self.assertEqual(averages.get("Private Room"), 4.9)


   def test_validate_policy_numbers(self):
       invalid_listings = validate_policy_numbers(self.detailed_data)
       self.assertEqual(invalid_listings, ["16204265"])


def main():
   detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
   output_csv(detailed_data, "airbnb_dataset.csv")



if __name__ == "__main__":
   main()
   unittest.main(verbosity=2)
