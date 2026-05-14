import pytest
import numpy as np
from types import SimpleNamespace
from app.utils.recommender import _rating_center, _scale_rating, _vehicle_feature_vector, _build_XY_for_user, _score_candidates_ridge_multioutput

def test_rating_center_1_5():
    assert _rating_center("1_5") == 3.0

def test_scale_rating_neutral_is_zero():
    assert _scale_rating(3, 3.0) == 0.0

def test_vehicle_feature_vector_order_and_values():
    v = SimpleNamespace(
        performance_score=1.0,
        size_score=2.0,
        economy_score=3.0,
        practicality_score=4.0,
        exoticness_score=5.0,
        engagement_score=6.0,
    )
    vec = _vehicle_feature_vector(v)
    assert vec == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]

def test_build_xy_shapes_and_values():
    v1 = SimpleNamespace(performance_score=1, size_score=1, economy_score=1,
                         practicality_score=1, exoticness_score=1, engagement_score=1)
    v2 = SimpleNamespace(performance_score=2, size_score=2, economy_score=2,
                         practicality_score=2, exoticness_score=2, engagement_score=2)

    r1 = SimpleNamespace(performance=3, size=3, economy=3, practicality=3, exoticness=3, engagement=3)
    r2 = SimpleNamespace(performance=5, size=1, economy=3, practicality=3, exoticness=3, engagement=3)

    rows = [(r1, v1), (r2, v2)]
    X, Y = _build_XY_for_user(rows, "1_5")

    assert X.shape == (2, 6)
    assert Y.shape == (2, 6)

    assert np.allclose(Y[0], np.zeros(6))

    assert Y[1][0] == 1.0
    assert Y[1][1] == -1.0

def test_score_candidates_returns_score_for_each_candidate():
    X_rated = np.array([[1,2,3,4,5,6],
                        [2,3,4,5,6,7],
                        [3,4,5,6,7,8]], dtype=float)
    Y_rated = np.zeros((3, 6), dtype=float)
    X_candidates = np.random.RandomState(0).rand(5, 6)

    scores = _score_candidates_ridge_multioutput(X_rated, Y_rated, X_candidates, alpha=1.0)

    assert len(scores) == 5

def test_score_candidates_is_deterministic():
    rng = np.random.RandomState(0)
    X_rated = rng.rand(5, 6)
    Y_rated = rng.rand(5, 6)
    X_candidates = rng.rand(10, 6)

    s1 = _score_candidates_ridge_multioutput(X_rated, Y_rated, X_candidates, alpha=1.0)
    s2 = _score_candidates_ridge_multioutput(X_rated, Y_rated, X_candidates, alpha=1.0)

    assert np.allclose(s1, s2)