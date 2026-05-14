import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchRecommendationsForUser } from "../api/recommendations";
import { logout } from "../api/auth";
import "./Recommendations.css";

const Recommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const wikiCache = new Map();

  useEffect(() => {
    const load = async () => {
      try {
        const data = await fetchRecommendationsForUser();
        const withRanking = data.map((vehicle, index) => ({
          ...vehicle,
          ranking: index + 1,
          matchPercentage: vehicle.match_percentage ?? (100 - index * 5)
        }));
        const withImages = await Promise.all(
          withRanking.map(async (v) => {
            if (v.image_url) return v;
            const img = await fetchWikipediaImage(v.vehicle_name);
            return { ...v, image_url: img || null };
          })
        );
        setRecommendations(withImages);
      } catch (err) {
        console.error(err);
        alert("Błąd pobierania rekomendacji");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const cleanVehicleNameForWiki = (name = "") => {
    return name
      .replace(/\b\d+(\.\d+)?\b/g, " ")
      .replace(/\b(km|kw|hp|v\d+|i|d|tdi|fsi|tsi|t)\b/gi, " ")
      .replace(/\b(19|20)\d{2}\s*-\s*(19|20)\d{2}\b/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  };

  const fetchWikipediaImage = async (rawName) => {
  const base = cleanVehicleNameForWiki(rawName);
  if (!base) return null;

  const cacheKey = `wiki:${base}`;
  if (wikiCache.has(cacheKey)) return wikiCache.get(cacheKey);

  const tryLang = async (lang) => {
    const searchUrl =
      `https://${lang}.wikipedia.org/w/api.php?origin=*` +
      `&action=query&list=search&format=json&srlimit=1&srsearch=${encodeURIComponent(base)}`;

    const sres = await fetch(searchUrl);
    if (!sres.ok) return null;
    const sdata = await sres.json();
    const title = sdata?.query?.search?.[0]?.title;
    if (!title) return null;

    const imgUrl =
      `https://${lang}.wikipedia.org/w/api.php?origin=*` +
      `&action=query&format=json&prop=pageimages&pithumbsize=800&titles=${encodeURIComponent(title)}`;

    const ires = await fetch(imgUrl);
    if (!ires.ok) return null;
    const idata = await ires.json();
    const pages = idata?.query?.pages;
    const page = pages ? pages[Object.keys(pages)[0]] : null;

    return page?.thumbnail?.source || null;
  };

  try {
    const imgEn = await tryLang("en");
    if (imgEn) {
      wikiCache.set(cacheKey, imgEn);
      return imgEn;
    }

    const imgPl = await tryLang("pl");
    wikiCache.set(cacheKey, imgPl);
    return imgPl;
  } catch {
    wikiCache.set(cacheKey, null);
    return null;
  }
};


  const getVehicleImage = (vehicle) => {
    return (
      vehicle.image_url ||
      "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800&q=80"
    );
  };

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <div className="recommendations-page">
      <div className="recommendations-container">
        <nav className="navbar">
          <div className="navbar-left">
            <span
  className="navbar-title logo-clickable"
  onClick={() => navigate("/home")}
>
              <span className="logo-light">Car</span>
              <span className="logo-bold">Fit</span>
            </span>
          </div>
          <div className="navbar-buttons">
            <button className="nav-btn" onClick={handleLogout}>
              Wyloguj
            </button>
          </div>
        </nav>

        <div className="recommendations-header">
          <button className="back-btn" onClick={() => navigate("/home")}>
            <span className="back-icon">←</span>
            <span>Powrót</span>
          </button>
          <h1 className="page-title">Top 10 Rekomendowanych Pojazdów</h1>
        </div>

        {loading ? (
          <div className="loading-container">
            <div className="spinner"></div>
            <p className="loading-text">Ładowanie rekomendacji...</p>
          </div>
        ) : (
          <div className="grid-container">
            {recommendations.map((vehicle) => (
              <div key={vehicle.vehicle_id} className="vehicle-card">
                <div className="ranking-badge">
                  #{vehicle.ranking}
                </div>

                <div className="vehicle-image-container">
                  <img
                    src={getVehicleImage(vehicle)}
                    alt={vehicle.vehicle_name}
                    className="vehicle-image"
                    onError={(e) => {
                      e.target.src = 'https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800&q=80';
                    }}
                  />
                </div>

                <div className="vehicle-content">
                  <div className="match-percentage">
                    <div className="match-bar-container">
                      <div
                        className="match-bar"
                        style={{ width: `${vehicle.matchPercentage}%` }}
                      />
                    </div>
                    <span className="match-text">
                      {vehicle.matchPercentage}% dopasowania
                    </span>
                  </div>

                  <h3 className="vehicle-name">
                    {vehicle.vehicle_name}
                  </h3>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Recommendations;