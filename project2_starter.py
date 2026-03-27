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
    

    
def create_listing_database(html_path):
    

def output_csv(data, filename):
    

def avg_location_rating_by_room_type(data):
    


def validate_policy_numbers(data):
    
    

def google_scholar_searcher(query):
    

class TestCases(unittest.TestCase):
    def setUp(self):
        
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        
       

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        

    def test_create_listing_database(self):
       
       

    def test_output_csv(self):
        
        out_path = os.path.join(self.base_dir, "test.csv")

        
        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        

    def test_validate_policy_numbers(self):
        

def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)