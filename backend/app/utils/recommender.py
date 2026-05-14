from __future__ import annotations

from typing import Any, Dict, List, Tuple, Literal, Optional

import numpy as np
from sqlalchemy.orm import Session
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

from app.errors.recommendation import ColdStartError
from app.models.user_vehicle_rating import UserVehicleRating
from app.models.vehicle import Vehicle



AXES = [
    ("performance", "performance_score"),
    ("size", "size_score"),
    ("economy", "economy_score"),
    ("practicality", "practicality_score"),
    ("exoticness", "exoticness_score"),
    ("engagement", "engagement_score"),
]
N_AXES = len(AXES)


def _rating_center(rating_scale: str) -> float:
    if rating_scale == "1_5":
        return 3.0
    if rating_scale == "-2_2":
        return 0.0
    raise ValueError(f"Unsupported rating scale: {rating_scale}")


def _scale_rating(val: float, center: float) -> float:
    return (float(val) - center) / 2.0


def _safe_float(x) -> float:
    if x is None:
        raise ValueError("Encountered None where float was expected")
    v = float(x)
    if np.isnan(v) or np.isinf(v):
        raise ValueError("Encountered NaN/Inf where finite float was expected")
    return v


def _vehicle_feature_vector(v: Vehicle) -> List[float]:
    return [_safe_float(getattr(v, feat)) for _, feat in AXES]


def _fetch_user_rows(db: Session, user_id: int) -> List[Tuple[UserVehicleRating, Vehicle]]:
    return (
        db.query(UserVehicleRating, Vehicle)
        .join(Vehicle, Vehicle.vehicle_id == UserVehicleRating.vehicle_id)
        .filter(UserVehicleRating.user_id == user_id)
        .all()
    )


def _score_to_percentage(score: float, min_score: float, max_score: float) -> int:
    if max_score <= min_score:
        return 100
    pct = (score - min_score) / (max_score - min_score) * 100.0
    return int(np.clip(pct, 0, 100))


def _build_XY_for_user(
    rows: List[Tuple[UserVehicleRating, Vehicle]],
    rating_scale: str,
) -> Tuple[np.ndarray, np.ndarray]:

    center = _rating_center(rating_scale)

    X = np.asarray([_vehicle_feature_vector(v) for _, v in rows], dtype=float)

    Y = np.zeros((len(rows), N_AXES), dtype=float)
    for i, (rating, _) in enumerate(rows):
        for j, (axis, _) in enumerate(AXES):
            Y[i, j] = _scale_rating(_safe_float(getattr(rating, axis)), center)

    return X, Y


def _format_result(
    v: Vehicle,
    score: float,
    match_pct: int,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "vehicle_id": v.vehicle_id,
        "vehicle_name": v.vehicle_name,
        "performance_score": float(v.performance_score),
        "size_score": float(v.size_score),
        "economy_score": float(v.economy_score),
        "practicality_score": float(v.practicality_score),
        "exoticness_score": float(v.exoticness_score),
        "engagement_score": float(v.engagement_score),
        "match_percentage": int(match_pct),
        "score": float(score),
        "image_url": getattr(v, "image_url", None),
    }
    if extra:
        out.update(extra)
    return out




def _score_candidates_ridge_multioutput(
    X_rated: np.ndarray,
    Y_rated: np.ndarray,
    X_candidates: np.ndarray,
    alpha: float,
) -> Tuple[np.ndarray, Dict[str, Any]]:

    scaler = StandardScaler()
    Xs = scaler.fit_transform(X_rated)
    Xc = scaler.transform(X_candidates)

    model = Ridge(alpha=float(alpha), random_state=0)
    model.fit(Xs, Y_rated)

    Yhat = model.predict(Xc)
    scores = np.sum(Yhat, axis=1)


    return scores





def recommend(
    db: Session,
    user_id: int,
    k: int = 10,
    rating_scale: str = "1_5",
    min_samples: int = 3,
    *,
    ridge_alpha: float = 1.0,
) -> List[Dict[str, Any]]:

    rows = _fetch_user_rows(db, user_id)
    if len(rows) < min_samples:
        raise ColdStartError(min_samples)

    rated_ids = [rating.vehicle_id for rating, _ in rows]

    candidates: List[Vehicle] = (
        db.query(Vehicle)
        .filter(~Vehicle.vehicle_id.in_(rated_ids))
        .all()
    )
    if not candidates:
        return []

    X_rated, Y_rated = _build_XY_for_user(rows, rating_scale=rating_scale)
    X_candidates = np.asarray([_vehicle_feature_vector(v) for v in candidates], dtype=float)


    scores= _score_candidates_ridge_multioutput(
        X_rated=X_rated,
        Y_rated=Y_rated,
        X_candidates=X_candidates,
        alpha=ridge_alpha,
    )

    scored = list(zip(scores.tolist(), candidates))
    scored.sort(key=lambda t: t[0], reverse=True)

    all_scores = [s for s, _ in scored]
    min_score = float(min(all_scores))
    max_score = float(max(all_scores))

    results: List[Dict[str, Any]] = []
    for score, v in scored[:k]:
        results.append(
            _format_result(
                v=v,
                score=float(score),
                match_pct=_score_to_percentage(float(score), min_score, max_score),
                extra=None,
            )
        )

    return results
