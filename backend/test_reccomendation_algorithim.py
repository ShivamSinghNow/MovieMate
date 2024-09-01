import pytest
import pandas as pd
from reccomendation_algorithim import pearson_correlation, find_nearest_neighbor, predict_rating, reccomend_movies
from moviespreprocess import extractYear, cleanTitle


def test_pearson_correlation():
    # Assuming user1 and user2 are valid user IDs in your test dataset
    correlation = pearson_correlation(2, 5)
    assert isinstance(correlation, (float,int))
    if isinstance(correlation, float):
        assert -1.0 <= correlation <= 1.0
    else:
        assert correlation == 0

def test_pearson_identical_ratings(mocker):
    # Choose user IDs with identical ratings for their common movies
    correlation = pearson_correlation(1, 2)
    assert correlation == 1

def test_pearson_no_common_movies():
    # Choose user IDs that have no common movies rated
    correlation = pearson_correlation(2,3)
    assert correlation == 0

def test_pearson_one_common_movie():
    # Choose user IDs that have exactly one common movie rated
    correlation = pearson_correlation(3, 4)
    assert correlation == 0

def test_pearson_opposite_ratings():
    # Choose user IDs with opposite ratings for their common movies
    correlation = pearson_correlation(5, 6)
    assert correlation < 0

def test_find_nearest_neighbor():
    # Test with a valid user ID
    neighbors = find_nearest_neighbor(1, 5)
    assert isinstance(neighbors, list)
    assert len(neighbors) <= 5
    # Optionally, check the type of elements in neighbors, etc.

def test_find_nearest_neighbor_no_neighbors():
    neighbors = find_nearest_neighbor(8)
    assert len(neighbors) == 0 or all(neighbor[1] == 0 for neighbor in neighbors)

def test_neighbor_similarity_scores():
    neighbors = find_nearest_neighbor(3)
    assert all(-1 <= neighbor[1] <= 1 for neighbor in neighbors)

def test_predict_rating():
    rating = predict_rating(1, 2)  
    assert isinstance(rating, float) or rating is None
    if rating is not None:
        assert 0.0 <= rating <= 5.0  

def test_predict_rating_invalid_user():
    predicted_rating = predict_rating(9, 2)
    assert predicted_rating is None  

def test_predict_rating_different_neighbor_counts():
    for num_neighbors in [0, 1, 5, 10]:
        predicted_rating = predict_rating(3, 4, numNeighbors=num_neighbors)
        assert isinstance(predicted_rating, (float, type(None)))


def test_recommend_movies_valid_user():
    
    recommendations = reccomend_movies(1, 5)
    assert isinstance(recommendations, dict), "The output should be a dictionary."
    assert 1 in recommendations, "The dictionary should contain the user ID as a key."
    assert isinstance(recommendations[1], list), "The value should be a list of movie IDs."
    assert len(recommendations[1]) <= 5, "The list should not contain more than the requested number of recommendations."



def test_recommend_movies_different_counts():
    for count in [1, 3, 10]:
        recommendations = reccomend_movies(3, count)
        assert len(recommendations) <= count
    

def test_extract_year():
    assert extractYear("Jumanji (1995)") == 1995
    assert extractYear("Powder (1995)") == 1995

def test_cleanTitle():
    assert cleanTitle("Movie!@# Title (2021)") == "movie title"
    assert cleanTitle("Another Title(2010)") == "another title"