import React, { useState } from "react";
import { Camera } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { register } from "../api/auth"; 
import "./auth.css"


function Register() {
  const [registerForm, setRegisterForm] = useState({
    username: "",
    password: "",
    confirmPassword: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleKeyPress = (e) => {
    if (e.key === "Enter") handleRegister();
  };

  const handleRegister = async () => {
    if (!registerForm.username || !registerForm.password) {
      setError("Podaj nazwę użytkownika i hasło");
      return;
    }

    if (registerForm.username.length < 3 || registerForm.username.length > 50) {
    setError("Nazwa użytkownika musi mieć od 3 do 50 znaków");
    return;
  }

  if (registerForm.password.length < 8) {
    setError("Hasło musi mieć co najmniej 8 znaków");
    return;
  }
  
    if (registerForm.password !== registerForm.confirmPassword) {
      setError("Hasła muszą być takie same");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const data = await register(
        registerForm.username,
        registerForm.password
      );
      console.log("Zarejestrowano, backend:", data);

      navigate("/login");
    } catch (err) {
      setError(err.message || "Wystąpił błąd podczas rejestracji");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="auth-card">
        <div className="auth-header">
          <Camera size={48} className="auth-icon" />
          <h1 className="auth-title">Rejestracja</h1>
          <p className="auth-subtitle">Utwórz nowe konto</p>
        </div>

        <div className="auth-form">
          <div className="form-group">
            <label className="label">Nazwa użytkownika</label>
            <input
              type="text"
              className="input"
              value={registerForm.username}
              onChange={(e) =>
                setRegisterForm({
                  ...registerForm,
                  username: e.target.value,
                })
              }
            />
          </div>

          <div className="form-group">
            <label className="label">Hasło</label>
            <input
              type="password"
              className="input"
              value={registerForm.password}
              onChange={(e) =>
                setRegisterForm({
                  ...registerForm,
                  password: e.target.value,
                })
              }
            />
          </div>

          <div className="form-group">
            <label className="label">Potwierdź hasło</label>
            <input
              type="password"
              className="input"
              value={registerForm.confirmPassword}
              onChange={(e) =>
                setRegisterForm({
                  ...registerForm,
                  confirmPassword: e.target.value,
                })
              }
              onKeyDown={handleKeyPress}
            />
          </div>

          {error && <p className="auth-error">{error}</p>}

          <button
            onClick={handleRegister}
            className="btn-primary auth-btn"
            disabled={loading}
          >
            {loading ? "Rejestrowanie..." : "Zarejestruj się"}
          </button>
        </div>

        <p className="auth-switch">
          Masz już konto?{" "}
          <button
            type="button"
            onClick={() => navigate("/login")}
            className="link-button"
          >
            Zaloguj się
          </button>
        </p>
      </div>
    </div>
  );
}

export default Register;
