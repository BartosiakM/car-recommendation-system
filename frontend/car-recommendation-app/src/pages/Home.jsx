import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from "react-router-dom";
import './Home.css';
import { fetchUserRatings, addOrUpdateRating, deleteRating } from '../api/ratings';
import { fetchRecommendationsForUser } from '../api/recommendations';
import { fetchVehicleOptions } from '../api/vehicle';
import { logout } from "../api/auth";
import StarRating from "../components/StarRating";

const Home = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [vehicleOptions, setVehicleOptions] = useState([]);
  const [selectedVehicle, setSelectedVehicle] = useState(null);
  const [userRatings, setUserRatings] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [loading, setLoading] = useState(false);
  const [searchLoading, setSearchLoading] = useState(false);
  const [toast, setToast] = useState(null);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  
  const navigate = useNavigate();
  const searchRef = useRef(null);
  const dropdownRef = useRef(null);
  const searchTimeoutRef = useRef(null);

  const [ratings, setRatings] = useState({ 
    performance: 3,
    size: 3,
    economy: 3,
    practicality: 3,
    exoticness: 3,
    engagement: 3
  });

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  };

  const fetchUserRatingsFn = async () => {
    try {
      setLoading(true);
      const data = await fetchUserRatings();
      setUserRatings(data);
    } catch (e) {
      console.error(e);
      showToast('Błąd pobierania ocen', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate("/"); 
  };

  useEffect(() => {
    fetchUserRatingsFn();
  }, []);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowDropdown(false);
        setSelectedIndex(-1);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSearchChange = async (e) => {
    const query = e.target.value;
    setSearchQuery(query);
    setSelectedIndex(-1);

    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }

    if (query.length >= 2) {
      setSearchLoading(true);
      
      searchTimeoutRef.current = setTimeout(async () => {
        try {
          const data = await fetchVehicleOptions(query, 10);
          setVehicleOptions(data);
          setShowDropdown(true);
        } catch (error) {
          console.error('Błąd wyszukiwania:', error);
          showToast('Błąd wyszukiwania', 'error');
        } finally {
          setSearchLoading(false);
        }
      }, 300);
    } else {
      setVehicleOptions([]);
      setShowDropdown(false);
      setSearchLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (!showDropdown || vehicleOptions.length === 0) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex(prev => 
          prev < vehicleOptions.length - 1 ? prev + 1 : prev
        );
        break;
      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex(prev => prev > 0 ? prev - 1 : -1);
        break;
      case 'Enter':
        e.preventDefault();
        if (selectedIndex >= 0) {
          handleSelectVehicle(vehicleOptions[selectedIndex]);
        }
        break;
      case 'Escape':
        setShowDropdown(false);
        setSelectedIndex(-1);
        break;
      default:
        break;
    }
  };

  useEffect(() => {
    if (selectedIndex >= 0 && dropdownRef.current) {
      const selectedElement = dropdownRef.current.children[selectedIndex];
      if (selectedElement) {
        selectedElement.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      }
    }
  }, [selectedIndex]);

  const handleSelectVehicle = (vehicle) => {
    setSelectedVehicle(vehicle);
    setSearchQuery(vehicle.vehicle_name);
    setShowDropdown(false);
    setSelectedIndex(-1);

    const existingRating = userRatings.find(r => r.vehicle_id === vehicle.vehicle_id);
    if (existingRating) {
      setRatings({
        performance: existingRating.performance || 3,
        size: existingRating.size || 3,
        economy: existingRating.economy || 3,
        practicality: existingRating.practicality || 3,
        exoticness: existingRating.exoticness || 3,
        engagement: existingRating.engagement || 3
      });
    } else {
      setRatings({
        performance: 3,
        size: 3,
        economy: 3,
        practicality: 3,
        exoticness: 3,
        engagement: 3
      });
    }
  };

  const handleAddRating = async () => {
    if (!selectedVehicle) {
      showToast('Wybierz pojazd!', 'error');
      return;
    }

    try {
      setLoading(true);
      await addOrUpdateRating({
        user_id: localStorage.getItem("id"),
        vehicle_id: selectedVehicle.vehicle_id,
        ...ratings,
      });

      showToast('Ocena została zapisana!');
      setSearchQuery('');
      setSelectedVehicle(null);
      setRatings({
        performance: 3,
        size: 3,
        economy: 3,
        practicality: 3,
        exoticness: 3,
        engagement: 3
      });
      await fetchUserRatingsFn();
    } catch (error) {
      console.error('Błąd:', error);
      showToast('Błąd zapisywania oceny', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteRating = async (vehicleId, vehicleName) => {
    if (!window.confirm(`Czy na pewno chcesz usunąć ocenę dla ${vehicleName}?`)) return;

    try {
      setLoading(true);
      await deleteRating(vehicleId);
      showToast('Ocena została usunięta!');
      await fetchUserRatingsFn();
    } catch (error) {
      console.error('Błąd:', error);
      showToast('Błąd usuwania oceny', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateRecommendations = () => {
    if (userRatings.length === 0) {
      showToast('Dodaj najpierw oceny pojazdów', 'error');
      return;
    }
    navigate("/recommendations");
  };

  const categoryLabels = {
    performance: 'Wydajność',
    size: 'Rozmiar',
    economy: 'Ekonomia',
    practicality: 'Praktyczność',
    exoticness: 'Egzotyczność',
    engagement: 'Zaangażowanie'
  };

  return (
    <div className="home-page">
      {toast && (
        <div className={`toast toast-${toast.type}`}>
          {toast.message}
        </div>
      )}

      <nav className="navbar">
        <div className="navbar-left">
          <span className="navbar-title">
            <span className="logo-light">Car</span>
            <span className="logo-bold">Fit</span>
          </span>
        </div>
        <div className="navbar-buttons">
          <button className="nav-btn nav-btn-primary" onClick={handleLogout}>
            Wyloguj
          </button>
        </div>
      </nav>

      <div className="home-container">
        <div className="left-column">
          <div className="card add-rating-card">
            <h2 className="card-title">Dodaj ocenę pojazdu</h2>
            
            <div className="search-container" ref={searchRef}>
              <input
                type="text"
                placeholder="Wyszukaj pojazd..."
                value={searchQuery}
                onChange={handleSearchChange}
                onKeyDown={handleKeyDown}
                onFocus={() => vehicleOptions.length > 0 && setShowDropdown(true)}
                className="search-input"
                aria-label="Wyszukaj pojazd"
                aria-autocomplete="list"
                aria-controls="vehicle-dropdown"
                aria-expanded={showDropdown}
              />
              
              {searchLoading && (
                <div className="search-spinner"></div>
              )}

              {showDropdown && vehicleOptions.length > 0 && (
                <div 
                  className="dropdown" 
                  id="vehicle-dropdown"
                  role="listbox"
                  ref={dropdownRef}
                >
                  {vehicleOptions.map((vehicle, index) => (
                    <div
                      key={vehicle.vehicle_id}
                      className={`dropdown-item ${index === selectedIndex ? 'dropdown-item-selected' : ''}`}
                      onClick={() => handleSelectVehicle(vehicle)}
                      role="option"
                      aria-selected={index === selectedIndex}
                    >
                      {vehicle.vehicle_name}
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="rating-form">
              {!selectedVehicle ? (
                <div className="empty-rating-state">
                  <svg className="empty-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2" />
                  </svg>
                  <p className="empty-subtitle">
                    Wybierz pojazd z listy, aby dodać ocenę
                  </p>
                </div>
              ) : (
                <>
                  <h3 className="selected-vehicle">
                    {selectedVehicle.vehicle_name}
                  </h3>

                  {Object.keys(ratings).map((key) => (
                    <div key={key} className="rating-row">
                      <label>{categoryLabels[key]}</label>
                      <StarRating
                        value={ratings[key]}
                        onChange={(val) =>
                          setRatings({ ...ratings, [key]: val })
                        }
                      />
                    </div>
                  ))}

                  <button
                    onClick={handleAddRating}
                    className="btn-rating btn-primary"
                    disabled={loading}
                  >
                    {loading ? 'Zapisywanie...' : 'Zapisz ocenę'}
                  </button>
                </>
              )}
            </div>
          </div>

          <button
            onClick={handleGenerateRecommendations}
            className="btn btn-generate"
            disabled={userRatings.length === 0 || loading}
          >
            Generuj rekomendacje {userRatings.length > 0 && `(${userRatings.length})`}
          </button>
        </div>

        <div className="right-column">
          <div className="card ratings-card">
            <h2 className="card-title">Dodane pojazdy ({userRatings.length})</h2>
            
            <div className="ratings-list">
              {loading && userRatings.length === 0 ? (
                <div className="loading-state">
                  <div className="spinner"></div>
                  <p>Ładowanie ocen...</p>
                </div>
              ) : userRatings.length === 0 ? (
                <div className="empty-message-container">
                  <svg className="empty-icon-large" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                  <p className="empty-message">Nie masz jeszcze żadnych ocen</p>
                  <p className="empty-hint">Użyj wyszukiwarki po lewej stronie, aby dodać pierwszy pojazd</p>
                </div>
              ) : (
                userRatings.map((rating) => (
                  <div key={rating.vehicle_id} className="rating-item">
                    <div className="rating-header">
                      <h4 className="rating-vehicle-name">{rating.vehicle_name}</h4>
                      <button 
                        onClick={() => handleDeleteRating(rating.vehicle_id, rating.vehicle_name)}
                        className="delete-btn"
                        aria-label={`Usuń ocenę dla ${rating.vehicle_name}`}
                        disabled={loading}
                      >
                        ×
                      </button>
                    </div>
                    <div className="rating-details">
                      <span className="rating-detail">Wydajność: <strong>{rating.performance}</strong></span>
                      <span className="rating-detail">Rozmiar: <strong>{rating.size}</strong></span>
                      <span className="rating-detail">Ekonomia: <strong>{rating.economy}</strong></span>
                      <span className="rating-detail">Praktyczność: <strong>{rating.practicality}</strong></span>
                      <span className="rating-detail">Egzotyczność: <strong>{rating.exoticness}</strong></span>
                      <span className="rating-detail">Zaangażowanie: <strong>{rating.engagement}</strong></span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;