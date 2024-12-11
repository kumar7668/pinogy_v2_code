import googlemaps

from typing import List, Dict, Optional, Union
from django.core.cache import cache
from django.db.models.query import QuerySet
from django.utils import timezone
from django.conf import settings

from .models import GoogleReviews, GooglePlace

MINIMUM_DAYS_TO_FETCH_REVIEW = 30

def get_google_place_id(location_name:str) -> Optional[GooglePlace]:
    """
        Fetch google place id from google if its not available in DB
        return object of GooglePlace or None
    """

    if place := GooglePlace.objects.filter(place_name=location_name):
        return place[0]
    
    try:
        gmaps = googlemaps.Client(key=settings.GOOGLE_REVIEWS_KEY)
        geocode_result = gmaps.geocode(location_name)
        place_id = geocode_result[0]['place_id'] if geocode_result else None
        
        if place_id:
            place = GooglePlace.objects.create(place_name=location_name, google_place_id=place_id)
            return place

        return None
    
    except Exception as e:
        return None

def get_google_reviews(google_place_id:str):
    """
    Fetch google review from google and store and pass to 
    """
    
    try:
        # get place data with reviews using place_id
        gmaps = googlemaps.Client(key=settings.GOOGLE_REVIEWS_KEY)
        gplace = gmaps.place(place_id=google_place_id)
        return gplace['result']['reviews']
    
    except Exception as e:
        return []

def store_reviews_in_db(place: GooglePlace, reviews_data: List[Dict[str, Union[str, int]]]) -> None:
    """
        Check if each object already exists in the database
        if not than save in DB
    """
    
    for review in reviews_data:

        review_obj, created = GoogleReviews.objects.get_or_create(
            place = place,
            author_name = review['author_name'],
            author_url = review['author_url'],
            profile_photo_url = review['profile_photo_url'],
            rating = review['rating'],
            text = review['text'],
        )

        if not created:
            review_obj.updated_at = timezone.now()
            review_obj.save()

def fetch_latest_google_reviews(location_name:str) -> None:
    """
        Driver function to fetch google reviews data and store in DB
    """
    place = get_google_place_id(location_name)
    reviews_data = get_google_reviews(place.google_place_id) if place else []
    if place and reviews_data:
        store_reviews_in_db(place, reviews_data)

def check_need_to_fetch_reviews() -> bool:
    """
        check that do we need to fetch new reviews from google or not based on last review
    """

    if last_review := GoogleReviews.objects.last():
        days_difference = (timezone.now().date() - last_review.created_at).days

        if days_difference < MINIMUM_DAYS_TO_FETCH_REVIEW:
            return False

    return True

def disabled_unused_place(active_location: list) -> None:
    GooglePlace.objects.exclude(place_name__in=active_location).update(is_active=False)

def get_google_reviews_list(first_location: str, minimum_rating: int, second_location: Optional[str] = None) -> QuerySet:
    """
        Fetch Reviews from google if check_need_to_fetch_reviews return True
        else return local google reviews from DB
    """

    cache_key = f"pinogy_testimonials:get_google_reviews_list:{first_location}:{second_location}:{minimum_rating}"

    if result:= cache.get(cache_key) :
        return result

    if check_need_to_fetch_reviews():
        fetch_latest_google_reviews(first_location)

        if second_location:
            fetch_latest_google_reviews(second_location)
        
        disabled_unused_place([first_location, second_location])
    
    google_reviews = GoogleReviews.objects.filter(place__is_active=True, is_published=True, rating__gte=minimum_rating)
    cache.set(cache_key, google_reviews, 60*60*24*7)

    return google_reviews