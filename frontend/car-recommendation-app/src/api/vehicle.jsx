const API_BASE_URL = 'http://localhost:8080';

export const fetchVehicleOptions = async (query, limit = 10) => {
  const response = await fetch(
    `${API_BASE_URL}/vehicles/vehicle-options?q=${encodeURIComponent(query)}&limit=${limit}`
  );

  if (!response.ok) {
    throw new Error('Błąd wyszukiwania pojazdów');
  }

  return response.json();
};
