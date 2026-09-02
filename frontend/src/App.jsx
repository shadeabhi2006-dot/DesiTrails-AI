import { useState } from "react";
import "./App.css";

const API_URL = "https://desitrails-ai.onrender.com";

const fallbackImage =
  "https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=900&q=80";

const defaultPlaces = [
  {
    name: "Bakkhali Beach",
    state: "West Bengal",
    description:
      "Peaceful, quiet, natural and less crowded coastal environment.",
    image: fallbackImage,
  },
  {
    name: "Jhargram",
    state: "West Bengal",
    description:
      "Forested, peaceful, rural and naturally beautiful.",
    image: fallbackImage,
  },
  {
    name: "Bangus Valley",
    state: "Jammu and Kashmir",
    description:
      "A pristine alpine valley with meadows, forests and mountain ranges.",
    image: fallbackImage,
  },
];

function App() {
  const [prompt, setPrompt] = useState("");
  const [places, setPlaces] = useState(defaultPlaces);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [searched, setSearched] = useState(false);

  const searchPlaces = async () => {
    if (!prompt.trim()) {
      setError("Please enter a travel preference.");
      return;
    }

    setLoading(true);
    setError("");
    setSearched(true);

    try {
      const response = await fetch(`${API_URL}/recommend-from-prompt`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt: prompt.trim() }),
      });

      if (!response.ok) {
        throw new Error("Backend request failed.");
      }

      const data = await response.json();

      if (!data.success) {
        setPlaces([]);
        setError(data.message || "No recommendations found.");
        return;
      }

      const recommendations = data.recommendations || [];

      if (recommendations.length === 0) {
        setPlaces([]);
        setError("No matching destinations found.");
        return;
      }

      setPlaces(
        recommendations.map((place) => ({
          ...place,
          image: place.image || fallbackImage,
          score: place.match_score,
          description:
            place.description ||
            "A beautiful lesser-known destination waiting to be explored.",
        }))
      );
    } catch (err) {
      console.error(err);
      setPlaces([]);
      setError(
        "Unable to connect to DesiTrails AI backend. Please check the backend deployment."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      searchPlaces();
    }
  };

  const useSuggestion = (value) => {
    setPrompt(value);
    setError("");
  };

  const openMap = (place) => {
    if (
      place.latitude !== undefined &&
      place.latitude !== null &&
      place.longitude !== undefined &&
      place.longitude !== null
    ) {
      const url =
        `https://www.google.com/maps/search/?api=1&query=` +
        `${place.latitude},${place.longitude}`;

      window.open(url, "_blank", "noopener,noreferrer");
      return;
    }

    const query = encodeURIComponent(
      `${place.name}, ${place.state}, India`
    );

    window.open(
      `https://www.google.com/maps/search/?api=1&query=${query}`,
      "_blank",
      "noopener,noreferrer"
    );
  };

  return (
    <div className="app">
      <header className="navbar">
        <div className="nav-container">
          <div className="logo">
            DesiTrails <span>AI</span>
          </div>

          <nav>
            <a href="#home" className="active">
              Home
            </a>
            <a href="#explore">Explore</a>
            <a href="#about">About</a>
          </nav>
        </div>
      </header>

      <main>
        <section className="hero" id="home">
          <div className="hero-container">
            <div className="hero-content">
              <h1>
                Find less popular places
                <br />
                in India using AI.
              </h1>

              <p className="hero-description">
                DesiTrails AI understands your travel preferences and
                recommends destinations from its curated dataset.
              </p>

              <div className="search-row">
                <div className="search-box">
                  <span className="location-icon">📍</span>

                  <input
                    type="text"
                    placeholder="e.g. cheap and peaceful place in Jammu and Kashmir"
                    value={prompt}
                    onChange={(event) => setPrompt(event.target.value)}
                    onKeyDown={handleKeyDown}
                  />
                </div>

                <button
                  className="search-button"
                  onClick={searchPlaces}
                  disabled={loading}
                >
                  {loading ? "Searching..." : "Search"}
                </button>
              </div>

              <div className="try-text">
                Try:{" "}
                <button
                  onClick={() =>
                    useSuggestion(
                      "I want a cheap and peaceful place in West Bengal"
                    )
                  }
                >
                  Cheap + peaceful in West Bengal
                </button>
                ,{" "}
                <button
                  onClick={() =>
                    useSuggestion(
                      "I want a nature-filled adventurous place in Jammu and Kashmir"
                    )
                  }
                >
                  Nature + adventure in J&K
                </button>
                ,{" "}
                <button
                  onClick={() =>
                    useSuggestion(
                      "I want a cool and peaceful place in Manipur"
                    )
                  }
                >
                  Cool + peaceful in Manipur
                </button>
              </div>
            </div>

            <div className="hero-image">
              <div className="landscape">
                <div className="cloud cloud-one"></div>
                <div className="cloud cloud-two"></div>
                <div className="mountain mountain-one"></div>
                <div className="mountain mountain-two"></div>
                <div className="mountain mountain-three"></div>
                <div className="tree tree-one">▲</div>
                <div className="tree tree-two">▲</div>
                <div className="tree tree-three">▲</div>
                <div className="ground"></div>
                <div className="path"></div>
              </div>
            </div>
          </div>
        </section>

        {error && <div className="error-message">{error}</div>}

        <section className="recommendations" id="explore">
          <div className="recommendation-container">
            <h2>
              {searched
                ? "Places you might like"
                : "Less known places you might like"}
            </h2>

            {loading ? (
              <div className="loading">
                Finding the best places for you...
              </div>
            ) : places.length === 0 ? (
              <div className="no-results">
                No matching destinations found.
              </div>
            ) : (
              <div className="cards">
                {places.map((place, index) => (
                  <div
                    className="place-card"
                    key={`${place.name}-${index}`}
                  >
                    <div className="card-image-wrapper">
                      <img
                        src={place.image || fallbackImage}
                        alt={place.name}
                        onError={(event) => {
                          event.currentTarget.src = fallbackImage;
                        }}
                      />

                      {place.score !== undefined &&
                        place.score !== null && (
                          <div className="score">
                            {Math.round(Number(place.score))}% match
                          </div>
                        )}
                    </div>

                    <div className="card-content">
                      <h3>{place.name}</h3>

                      <div className="state">
                        <span className="pin">📍</span>
                        {place.state}
                      </div>

                      <p>{place.description}</p>

                      <div className="card-details">
                        {place.budget !== undefined && (
                          <span>Budget: ₹{place.budget}</span>
                        )}
                        {place.best_season && (
                          <span>Best: {place.best_season}</span>
                        )}
                        {place.tourism_saturation && (
                          <span>Tourism: {place.tourism_saturation}</span>
                        )}
                      </div>

                      <button
                        className="map-button"
                        onClick={() => openMap(place)}
                      >
                        View on Map →
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}

            <a className="explore-more" href="#explore">
              Explore more places <span>→</span>
            </a>
          </div>
        </section>

        <section className="about" id="about">
          <div className="about-container">
            <h2>Discover India beyond the usual</h2>
            <p>
              DesiTrails AI understands travel preferences and ranks
              destinations from the dataset using only the preferences
              detected in the user's prompt.
            </p>
          </div>
        </section>
      </main>

      <footer>
        <div className="footer-container">
          <div>© 2026 DesiTrails AI</div>

          <div className="footer-links">
            <a href="#about">About</a>
            <a href="#privacy">Privacy</a>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
