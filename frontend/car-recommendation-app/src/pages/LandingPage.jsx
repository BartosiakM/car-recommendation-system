import { useNavigate } from "react-router-dom";
import heroImg from "../assets/hero7.jpg";
import "./LandingPage.css";
import { Brain, BarChart3, Star, Presentation } from "lucide-react";

export default function LandingPage() {
  const navigate = useNavigate();
  const scrollToFeatures = () => {
    const section = document.querySelector(".features-section");
    section?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="landing-page">
      <nav className="navbar">
        <div className="navbar-left">
           <span className="navbar-title">
    <span className="logo-light">Car</span>
    <span className="logo-bold">Fit</span>
  </span>
        </div>

        <div className="navbar-buttons">
          <button className="nav-btn" onClick={() => navigate("/login")}>
            Zaloguj
          </button>
          <button className="nav-btn nav-btn-primary" onClick={() => navigate("/register")}>
            Zarejestruj
          </button>
        </div>
      </nav>

      <section className="hero">
        <img src={heroImg} alt="Samochód" className="hero-img" />

        <div className="hero-overlay"></div>

        <div className="hero-content">
          <h1 className="hero-title">Znajdź swój idealny samochód</h1>
          <p className="hero-subtitle">
Precyzyjne rekomendacje pojazdów oparte na danych technicznych.
          </p>

          <div className="hero-buttons">
            <button className="hero-main-btn btn-primary" onClick={scrollToFeatures}>
              Dowiedz się więcej
            </button>
          </div>
        </div>
      </section>

      <section className="features-section">
        <div className="features-header">
          <h2>Jak działa CarFit?</h2>
          <p>
            Łączymy dane techniczne, uczenie maszynowe i Twoje doświadczenia,
            aby pomóc Ci wybrać samochód, który naprawdę do Ciebie pasuje.
          </p>
        </div>

        <div className="features-grid">
          <div className="feature-card">
            <Brain className="feature-icon brain"/>
            <h3>Rekomendacje oparte na ML</h3>
            <p>
              Model uczenia maszynowego analizuje Twoje pojazdy oraz ich oceny,
               aby zaproponowac najbardziej dopasowane pojazdy.
            </p>
          </div>

          <div className="feature-card">
            <BarChart3 className="feature-icon chart" />
            <h3>Dane techniczne pojazdów</h3>
            <p>
              Bierzemy pod uwagę moc, moment obrotowy, spalanie, rozmiar nadwozia i
              28 innych parametrów technicznych.
            </p>
          </div>

          <div className="feature-card">
            <Star className="feature-icon star" />
            <h3>Twoje oceny i doświadczenia</h3>
            <p>
              Oceniaj samochody, którymi jeździłeś – system uczy się Twojego
              stylu i priorytetów przy wyborze auta.
            </p>
          </div>

          <div className="feature-card">
            <Presentation className="feature-icon presentation" />
            <h3>Prezentacja wyników</h3>
            <p>
              W CarFit zobaczysz wyniki rekomendacji w prostej i przejrzystej formie
            </p>
          </div>
        </div>
      </section>

      <footer className="footer">
        <div className="footer-content">
          <div className="footer-brand">
            <h3>CarFit</h3>
            <p>Inteligentny system rekomendacji samochodów</p>
          </div>

          <div className="footer-links">
            <div className="footer-column">
              <h4>Produkt</h4>
              <a href="#features">Funkcje</a>
              <a href="#how-it-works">Jak działa</a>
              <a href="#pricing">Cennik</a>
            </div>

            <div className="footer-column">
              <h4>Firma</h4>
              <a href="#about">O nas</a>
              <a href="#contact">Kontakt</a>
              <a href="#careers">Kariera</a>
            </div>

            <div className="footer-column">
              <h4>Wsparcie</h4>
              <a href="#help">Pomoc</a>
              <a href="#privacy">Prywatność</a>
              <a href="#terms">Regulamin</a>
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          <p>&copy; 2025 CarFit. Wszystkie prawa zastrzeżone.</p>
        </div>
      </footer>
    </div>
  );
}
