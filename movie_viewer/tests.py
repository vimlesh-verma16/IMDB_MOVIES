from django.test import TestCase

import json
import csv
import os
from io import StringIO
from django.urls import reverse
from django.test import TestCase
from .models import Movie
from .forms import CSVUploadForm

class MovieAPITests(TestCase):
    
    def setUp(self):
        self.upload_url = reverse('upload-csv')
        self.movie_list_url = reverse('movie-list')
        self.csv_file_path = 'test_movies.csv'
        
        # Sample CSV content
        csv_content = """title,original_title,release_date,overview,original_language,languages,runtime,status,budget,revenue,vote_average,vote_count,homepage,production_company_id,genre_id
Movie 1,Original Movie 1,2023-01-01,A great movie,English,English,120,Released,1000000,500000,8.5,100,https://example.com/1,1,1
Movie 2,Original Movie 2,2023-02-01,A fantastic sequel,Hindi,English,130,Released,2000000,1500000,7.5,200,https://example.com/2,1,2
Movie 3,Original Movie 3,2024-02-01,A fantastic sequel,Hindi,French,130,Released,2000000,1500000,7.1,200,https://example.com/2,1,2
"""
        # Write the sample CSV content to a temporary file
        with open(self.csv_file_path, 'w') as f:
            f.write(csv_content)

    def tearDown(self):
        # Remove the test CSV file after tests
        if os.path.exists(self.csv_file_path):
            os.remove(self.csv_file_path)

    def test_upload_csv(self):
        with open(self.csv_file_path, 'r') as csv_file:
            response = self.client.post(self.upload_url, {'file': csv_file}, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "CSV uploaded successfully")
            self.assertEqual(Movie.objects.count(), 3)  # Check if two movies are created


    def test_movie_list_filtering(self):
        # Upload a CSV file to have data for filtering
        with open(self.csv_file_path, 'r') as csv_file:
            self.client.post(self.upload_url, {'file': csv_file})

        # Test filtering by year
        response = self.client.get(self.movie_list_url, {'year_of_release': '2023'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Movie 1")
        self.assertContains(response, "Movie 2")

        response = self.client.get(self.movie_list_url, {'year_of_release': '2024'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Movie 3")

        # Test filtering by language
        response = self.client.get(self.movie_list_url, {'language': 'English'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Movie 1")
        self.assertContains(response, "Movie 2")

        response = self.client.get(self.movie_list_url, {'language': 'French'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Movie 3")

    def test_movie_list_sorting(self):
        # Upload a CSV file to have data for sorting
        with open(self.csv_file_path, 'r') as csv_file:
            self.client.post(self.upload_url, {'file': csv_file})

        # Test sorting by release_date
        response = self.client.get(self.movie_list_url, {'sort_by': 'release_date'})
        self.assertEqual(response.status_code, 200)
        movies = response.context['page_obj']
        self.assertEqual(movies.object_list[0].title, "Movie 1")  # Ensure correct order

        # Test sorting by ratings
        response = self.client.get(self.movie_list_url, {'sort_by': 'vote_average'})
        self.assertEqual(response.status_code, 200)
        movies = response.context['page_obj']
        self.assertEqual(movies.object_list[0].title, "Movie 3")  # Ensure correct order based on ratings


