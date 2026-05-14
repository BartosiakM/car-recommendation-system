import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import { validateToken } from "../api/auth";

export default function ProtectedRoute({ children }) {
  const [isValid, setIsValid] = useState(null); 

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      setIsValid(false);
      return;
    }

    validateToken()
      .then(() => setIsValid(true))
      .catch(() => {
        setIsValid(false);
        localStorage.removeItem("token");
      });
  }, []); 

  if (isValid === null) return <p>Sprawdzanie sesji...</p>;

  return isValid ? children : <Navigate to="/login" replace />;
}
