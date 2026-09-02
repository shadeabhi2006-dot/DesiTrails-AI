import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "YOUR_BACKEND_URL";

function App() {
  const [prompt, setPrompt] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [darkMode, setDarkMode] = useState(false);

  const [budget, setBudget] = useState(50);
  const [nature, setNature] = useState(50);
  const [adventure, setAdventure] = useState(50);
  const [culture, setCulture] = useState(50);
  const [crowd, setCrowd] = useState(50);
  const [accessibility, setAccessibility] = useState(50);
  const [state, setState] = useState("");

  useEffect(() => {
    const savedTheme = localStorage.getItem("desitrails-theme");

    if (savedTheme === "dark") {
      setDarkMode(true);
    }
  }, []);

  useEffect(() => {
    document.body.className = darkMode ? "dark" : "";

    localStorage.setItem(
      "desitrails-theme",
      darkMode ? "dark" : "light"
    );
  }, [darkMode]);

  const getRecommendations = async () => {
    if (!prompt.trim()) {
      setError("Tell us where or how you would like to travel.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/recommend?prompt=${encodeURIComponent(prompt)}`
      );

      if (!response.ok) {
        throw new Error("Unable to get recommendations.");
      }

      const data = await response.json();

      setRecommendations(
        data.recommendations ||
          data.destinations ||
          data ||
          []
      );
    } catch (err) {
      setError(
        "We couldn't load recommendations. Please try again."
      );
    }

    setLoading(false);
  };

  const getManualRecommendations = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/destinations`
      );

      if (!response.ok) {
        throw new Error("Unable to load destinations.");
      }

      const data = await response.json();

      let destinations =
        data.destinations ||
        data ||
        [];

      if (state) {
        destinations = destinations.filter(
          (place) =>
            place.state?.toLowerCase() ===
            state.toLowerCase()
        );
      }

      const calculateScore = (place) => {
        const values = [
          {
            user: nature,
            place: Number(place.nature_score || 0),
          },
          {
            user: adventure,
            place: Number(place.adventure_score || 0),
          },
          {
            user: culture,
            place: Number(place.culture_score || 0),
          },
          {
            user: 100 - crowd,
            place: Number(place.crowd_score || 0),
          },
          {
            user: accessibility,
            place: Number(
              place.accessibility_score || 0
            ),
          },
        ];

        const preferenceScore =
          values.reduce(
            (sum, item) =>
              sum +
              (100 -
                Math.abs(
                  item.user - item.place
                )),
            0
          ) / values.length;

        const budgetValue =
          Number(place.budget || 0);

        const budgetScore =
          100 -
          Math.min(
            100,
            Math.abs(
              budgetValue - budget
            )
          );

        return Math.round(
          preferenceScore * 0.75 +
            budgetScore * 0.25
        );
      };

      destinations = destinations
        .map((place) => ({
          ...place,
          match_score: Math.max(
            0,
            Math.min(
              100,
              calculateScore(place)
            )
          ),
        }))
        .sort(
          (a, b) =>
            b.match_score -
            a.match_score
        )
        .slice(0, 3);

      setRecommendations(destinations);
    } catch (err) {
      setError(
        "We couldn't load destinations. Please try again."
      );
    }

    setLoading(false);
  };

  const tourismClass = (tourism) => {
    if (!tourism) return "medium";

    const value =
      tourism.toLowerCase();

    if (value.includes("low")) {
      return "low";
    }

    if (value.includes("high")) {
      return "high";
    }

    return "medium";
  };

  return (
    <div className="app">

      {/* NAVBAR */}

      <header className="navbar">
        <div className="nav-inner">

          <div className="brand">

            <span className="brand-mark">
              D
            </span>

            <div>
              <div className="brand-name">
                DesiTrails
              </div>

              <div className="brand-subtitle">
                AI TRAVEL GUIDE
              </div>
            </div>

          </div>

          <button
            className="theme-button"
            onClick={() =>
              setDarkMode(!darkMode)
            }
            aria-label="Toggle dark mode"
          >
            {darkMode ? "☼" : "☾"}
          </button>

        </div>
      </header>


      <main>

        {/* HERO */}

        <section className="hero">

          <div className="hero-content">

            <p className="eyebrow">
              DISCOVER INDIA DIFFERENTLY
            </p>

            <h1>
              Travel beyond
              <span> the usual.</span>
            </h1>

            <p className="hero-description">
              Tell us what kind of journey you
              want. DesiTrails finds destinations
              across India that match your
              preferences.
            </p>


            {/* AI SEARCH */}

            <div className="search-box">

              <textarea
                value={prompt}
                onChange={(e) =>
                  setPrompt(e.target.value)
                }
                placeholder="Try: I want a peaceful, cheap place surrounded by nature in West Bengal..."
                rows="3"
              />

              <div className="search-footer">

                <span className="search-hint">
                  Describe your ideal trip naturally
                </span>

                <button
                  className="primary-button"
                  onClick={getRecommendations}
                  disabled={loading}
                >
                  {loading
                    ? "Finding..."
                    : "Find places"}

                  <span>→</span>
                </button>

              </div>

            </div>

          </div>

        </section>


        {/* MANUAL RECOMMENDATIONS */}

        <section className="manual-section">

          <div className="section-heading">

            <div>

              <p className="eyebrow">
                YOUR PREFERENCES
              </p>

              <h2>
                Or build your trip
                <br />
                <em>your way.</em>
              </h2>

            </div>

            <p className="section-description">
              Prefer more control? Adjust the
              sliders and let DesiTrails find
              the closest matches.
            </p>

          </div>


          <div className="manual-panel">

            <div className="state-control">

              <label>
                Preferred state
              </label>

              <select
                value={state}
                onChange={(e) =>
                  setState(e.target.value)
                }
              >

                <option value="">
                  Any state
                </option>

                <option value="West Bengal">
                  West Bengal
                </option>

                <option value="Jammu and Kashmir">
                  Jammu and Kashmir
                </option>

                <option value="Rajasthan">
                  Rajasthan
                </option>

                <option value="Kerala">
                  Kerala
                </option>

                <option value="Goa">
                  Goa
                </option>

                <option value="Sikkim">
                  Sikkim
                </option>

                <option value="Himachal Pradesh">
                  Himachal Pradesh
                </option>

                <option value="Uttarakhand">
                  Uttarakhand
                </option>

              </select>

            </div>


            <div className="slider-grid">

              <Slider
                label="Budget"
                value={budget}
                setValue={setBudget}
                left="Low"
                right="High"
              />

              <Slider
                label="Nature"
                value={nature}
                setValue={setNature}
                left="Less important"
                right="Very important"
              />

              <Slider
                label="Adventure"
                value={adventure}
                setValue={setAdventure}
                left="Relaxed"
                right="Adventurous"
              />

              <Slider
                label="Culture"
                value={culture}
                setValue={setCulture}
                left="Less important"
                right="Very important"
              />

              <Slider
                label="Crowd"
                value={crowd}
                setValue={setCrowd}
                left="Quiet"
                right="Lively"
              />

              <Slider
                label="Accessibility"
                value={accessibility}
                setValue={setAccessibility}
                left="Remote"
                right="Easy to reach"
              />

            </div>


            <button
              className="manual-button"
              onClick={
                getManualRecommendations
              }
              disabled={loading}
            >
              {loading
                ? "Finding destinations..."
                : "Show my matches →"}
            </button>

          </div>

        </section>


        {/* ERROR */}

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}


        {/* RESULTS */}

        {recommendations.length > 0 && (

          <section className="results-section">

            <div className="results-heading">

              <div>

                <p className="eyebrow">
                  RECOMMENDED FOR YOU
                </p>

                <h2>
                  Places worth discovering.
                </h2>

              </div>

              <span>
                {recommendations.length} matches
              </span>

            </div>


            <div className="recommendation-grid">

              {recommendations.map(
                (place, index) => (

                  <article
                    className="destination-card"
                    key={
                      place.name ||
                      index
                    }
                  >

                    <div className="card-number">
                      0{index + 1}
                    </div>


                    <div className="card-content">

                      <p className="card-location">
                        {place.state ||
                          "India"}
                      </p>

                      <h3>
                        {place.name}
                      </h3>


                      <div className="match">

                        <span>
                          Match
                        </span>

                        <strong>
                          {Math.round(
                            place.match_score ||
                              0
                          )}
                          %
                        </strong>

                      </div>


                      <div className="card-divider"></div>


                      <div className="card-details">

                        <div>

                          <span>
                            Budget
                          </span>

                          <strong>
                            {place.budget
                              ? `₹${place.budget}`
                              : "Varies"}
                          </strong>

                        </div>


                        <div>

                          <span>
                            Tourism
                          </span>

                          <strong
                            className={`tourism ${tourismClass(
                              place.tourism_saturation
                            )}`}
                          >
                            {place.tourism_saturation ||
                              "Medium"}
                          </strong>

                        </div>

                      </div>

                    </div>

                  </article>

                )
              )}

            </div>

          </section>

        )}

      </main>


      {/* FOOTER */}

      <footer>

        <div className="footer-inner">

          <div className="brand">

            <span className="brand-mark">
              D
            </span>

            <div>

              <div className="brand-name">
                DesiTrails
              </div>

              <div className="brand-subtitle">
                AI TRAVEL GUIDE
              </div>

            </div>

          </div>

          <p>
            Discover more. Travel differently.
          </p>

        </div>

      </footer>

    </div>
  );
}


function Slider({
  label,
  value,
  setValue,
  left,
  right
}) {

  return (

    <div className="slider-container">

      <div className="slider-top">

        <label>
          {label}
        </label>

        <span>
          {value}
        </span>

      </div>


      <input
        type="range"
        min="0"
        max="100"
        value={value}
        onChange={(e) =>
          setValue(
            Number(e.target.value)
          )
        }
      />


      <div className="slider-labels">

        <span>
          {left}
        </span>

        <span>
          {right}
        </span>

      </div>

    </div>

  );
}


export default App;