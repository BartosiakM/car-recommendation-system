import React, { useState } from "react";
import { Camera } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { login } from "../api/auth"; 
import "./auth.css"

function Login() {
  const [loginForm, setLoginForm] = useState({
    username: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleKeyPress = (e) => {
    if (e.key === "Enter") handleLogin();
  };

  const handleLogin = async () => {
  if (!loginForm.username || !loginForm.password) {
    setError("Podaj nazwę użytkownika i hasło");
    return;
  }

  try {
    setLoading(true);
    setError("");

    const data = await login(loginForm.username, loginForm.password);
    console.log("Zalogowano, backend:", data);

   if (data?.access_token) {
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("id", data.user_id);
    } else {
      console.error("Brak access_token w odpowiedzi backendu:", data);
    }

    navigate("/home");
  } catch (err) {
    setError(err.message || "Wystąpił błąd podczas logowania");
  } finally {
    setLoading(false);
  }
};


  return (
    <div className="page-container">
      <div className="auth-card">
        <div className="auth-header">
          <Camera size={48} className="auth-icon" />
          <h1 className="auth-title">Rekomendacje Pojazdów</h1>
          <p className="auth-subtitle">Zaloguj się do swojego konta</p>
        </div>

        <div className="auth-form">
          <div className="form-group">
            <label className="label">Nazwa użytkownika</label>
            <input
              type="text"
              className="input"
              value={loginForm.username}
              onChange={(e) =>
                setLoginForm({ ...loginForm, username: e.target.value })
              }
              onKeyDown={handleKeyPress}
            />
          </div>

          <div className="form-group">
            <label className="label">Hasło</label>
            <input
              type="password"
              className="input"
              value={loginForm.password}
              onChange={(e) =>
                setLoginForm({ ...loginForm, password: e.target.value })
              }
              onKeyDown={handleKeyPress}
            />
          </div>

          {error && <p className="auth-error">{error}</p>}

          <button
            onClick={handleLogin}
            className="btn-primary auth-btn"
            disabled={loading}
          >
            {loading ? "Logowanie..." : "Zaloguj się"}
          </button>
        </div>

        <p className="auth-switch">
          Nie masz konta?{" "}
          <button
            type="button"
            onClick={() => navigate("/register")}
            className="link-button"
          >
            Zarejestruj się
          </button>
        </p>
      </div>
    </div>
  );
}

export default Login;
