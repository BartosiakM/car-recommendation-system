const API_BASE_URL = 'http://localhost:8080';

export const fetchRecommendationsForUser = async () => {
  const userId = localStorage.getItem("id")
  const response = await fetch(`${API_BASE_URL}/recommendations/user/${userId}`);
  if (!response.ok) {
    throw new Error('Błąd generowania rekomendacji');
  }
  return response.json();
};
