const API_BASE_URL = 'http://localhost:8080';

export const fetchUserRatings = async () => {
  const userId = localStorage.getItem("id");

  if (!userId) {
    throw new Error("Brak user_id w localStorage");
  }

  const response = await fetch(
    `${API_BASE_URL}/axes-ratings/user/${userId}`
  );

  if (!response.ok) {
    throw new Error("Błąd pobierania ocen użytkownika");
  }

  return response.json();
};


export const addOrUpdateRating = async (payload) => {
  const response = await fetch(`${API_BASE_URL}/axes-ratings/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error('Błąd zapisywania oceny');
  }

  return response.json().catch(() => true);
};

export const deleteRating = async (vehicleId) => {
  const userId = localStorage.getItem("id")
  
  if (!userId) {
    throw new Error("Brak user_id w localStorage");
  }
  const response = await fetch(
    `${API_BASE_URL}/axes-ratings/user/${userId}/vehicle/${vehicleId}`,
    { method: 'DELETE' }
  );

  if (!response.ok) {
    throw new Error('Błąd usuwania oceny');
  }

  return true;
};
