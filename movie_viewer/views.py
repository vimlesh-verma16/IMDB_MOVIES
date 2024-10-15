import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Movie
from .forms import CSVUploadForm 
from django.core.paginator import Paginator
from datetime import datetime

def home(request):
    return render(request, 'home.html')

def upload_csv(request):
    cnt = 0
    if request.method == 'POST':
        if 'upload' in request.POST: 
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['file']
                if not csv_file.name.endswith('.csv'):
                    messages.error(request, "This is not a CSV file")
                    return redirect('upload-csv')

                try:
                    decoded_file = csv_file.read().decode('utf-8').splitlines()
                    reader = csv.DictReader(decoded_file)
                    for row in reader:
                        movie_data = {
                            "title": row['title'],
                            "original_title": row.get('original_title', None),
                            "release_date": row['release_date'],
                            "overview": row.get('overview', None),
                            "original_language": row['original_language'],
                            "language": row['languages'],
                            "runtime": row.get('runtime', None),
                            "status": row['status'],
                            "budget": row.get('budget', None),
                            "revenue": row.get('revenue', None),
                            "vote_average": row.get('vote_average', None),
                            "vote_count": row.get('vote_count', None),
                            "homepage": row.get('homepage', None),
                            "production_company_id": row.get('production_company_id', None),
                            "genre_id": row.get('genre_id', None),
                        }
                    
                        # Handle budget
                        try:
                            movie_data['budget'] = int(float(movie_data['budget'])) if movie_data['budget'] else None
                        except (ValueError, TypeError) as e:
                            messages.warning(request, f"Invalid budget value for '{row['title']}': {e}")
                            movie_data['budget'] = None

                        # Handle revenue
                        try:
                            movie_data['revenue'] = int(float(movie_data['revenue'])) if movie_data['revenue'] else None
                        except (ValueError, TypeError) as e:
                            messages.warning(request, f"Invalid revenue value for '{row['title']}': {e}")
                            movie_data['revenue'] = None

                        # Handle runtime
                        try:
                            movie_data['runtime'] = int(float(movie_data['runtime'])) if movie_data['runtime'] else None
                        except (ValueError, TypeError) as e:
                            messages.warning(request, f"Invalid runtime value for '{row['title']}': {e}")
                            movie_data['runtime'] = None

                        # Handle vote_average
                        try:
                            movie_data['vote_average'] = float(movie_data['vote_average']) if movie_data['vote_average'] else None
                        except (ValueError, TypeError) as e:
                            messages.warning(request, f"Invalid vote average for '{row['title']}': {e}")
                            movie_data['vote_average'] = None

                        # Handle vote_count
                        try:
                            movie_data['vote_count'] = int(float(movie_data['vote_count'])) if movie_data['vote_count'] else None
                        except (ValueError, TypeError) as e:
                            messages.warning(request, f"Invalid vote count for '{row['title']}': {e}")
                            movie_data['vote_count'] = None

                        # Handle release_date
                        try:
                            movie_data['release_date'] = datetime.strptime(row['release_date'], '%Y-%m-%d').date() if row['release_date'] else None
                        except ValueError as e:
                            messages.warning(request, f"Invalid release date for '{row['title']}': {e}")
                            movie_data['release_date'] = None  # Set to None if the date is invalid

                        # Handle production_company_id
                        try:
                            movie_data['production_company_id'] = int(float(movie_data['production_company_id'])) if movie_data['production_company_id'] else None
                        except (ValueError, TypeError) as e:
                            messages.warning(request, f"Invalid production company ID for '{row['title']}': {e}")
                            movie_data['production_company_id'] = None

                        # Handle genre_id
                        try:
                            movie_data['genre_id'] = int(movie_data['genre_id']) if movie_data['genre_id'] else None
                        except (ValueError, TypeError) as e:
                            messages.warning(request, f"Invalid genre ID for '{row['title']}': {e}")
                            movie_data['genre_id'] = None
                        
                        cnt+=1
                        if cnt == 20:
                            break
                            print("break the loop")
                        Movie.objects.create(**movie_data)

                    messages.success(request, "CSV uploaded successfully")
                    print("CSV uploaded successfully")
                    return redirect('upload-csv')
                except Exception as e:
                    messages.error(request, f"An error occurred: {str(e)}")
                    return redirect('upload-csv')
        elif 'clear' in request.POST:  # Handle database clearing
            Movie.objects.all().delete()  # Clear all movies from the Movie model
            messages.success(request, 'All movies have been deleted successfully.')
            return redirect('upload-csv')  # Redirect to the same page after deletion
    else:
        form = CSVUploadForm()

    return render(request, 'upload_csv.html', {'form': form})


def movie_list(request):
    movies = Movie.objects.all()

    # Filtering
    year_of_release = request.GET.get('year_of_release')
    language = request.GET.get('language')
    if year_of_release:
        try:
            year_of_release = int(year_of_release)  # Convert to integer
            movies = movies.filter(release_date__year=year_of_release)
        except ValueError:
            pass  # Ignore invalid year inputs

    if language:
        movies = movies.filter(language__contains=language)

    sort_by = request.GET.get('sort_by', 'release_date')  # Default to 'release_date'

    if sort_by in ['release_date', 'ratings']:
        movies = movies.order_by(sort_by)

    # Pagination
    paginator = Paginator(movies, 20)  # 10 movies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'movie_list.html', {'page_obj': page_obj})


