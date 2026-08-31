import { useState } from "react";
import "./App.css";


// ============================================================
// BACKEND URL
// ============================================================

const API_URL = "http://127.0.0.1:8000";


// ============================================================
// DEFAULT DESTINATIONS
// ============================================================

const defaultPlaces = [
  {
    name: "Tirthan Valley",
    state: "Himachal Pradesh",
    description:
      "A quiet valley with scenic trails, waterfalls and peaceful villages.",
    image:
      "https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=900&q=80"
  },

  {
    name: "Bhandardara",
    state: "Maharashtra",
    description:
      "Lakes, dams and mountains. Perfect for a calm weekend.",
    image:
      "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=900&q=80"
  },

  {
    name: "Kudle Beach",
    state: "Karnataka",
    description:
      "A clean and less crowded beach near Gokarna.",
    image:
      "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=900&q=80"
  },

  {
    name: "Ziro Valley",
    state: "Arunachal Pradesh",
    description:
      "Beautiful valley, rice fields and rich local culture.",
    image:
      "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80"
  }
];


// ============================================================
// IMAGE FALLBACK
// ============================================================

const fallbackImage =
  "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=900&q=80";


// ============================================================
// APP
// ============================================================

function App() {

  const [prompt, setPrompt] = useState("");

  const [places, setPlaces] =
    useState(defaultPlaces);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const [searched, setSearched] =
    useState(false);


  // ==========================================================
  // SEARCH
  // ==========================================================

  const searchPlaces = async () => {

    if (!prompt.trim()) {

      setError(
        "Please enter a travel preference."
      );

      return;
    }


    setLoading(true);
    setError("");
    setSearched(true);


    try {

      const response = await fetch(
        `${API_URL}/recommend-from-prompt`,
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json"
          },

          body: JSON.stringify({
            prompt: prompt
          })
        }
      );


      if (!response.ok) {

        throw new Error(
          "Backend request failed."
        );
      }


      const data =
        await response.json();


      // ======================================================
      // BACKEND ERROR
      // ======================================================

      if (!data.success) {

        setPlaces([]);

        setError(
          data.message ||
          "No recommendations found."
        );

        return;
      }


      // ======================================================
      // RECOMMENDATIONS
      // ======================================================

      const recommendations =
        data.recommendations || [];


      if (
        recommendations.length === 0
      ) {

        setPlaces([]);

        setError(
          "No matching destinations found."
        );

        return;
      }


      // ======================================================
      // PREPARE CARDS
      // ======================================================

      const formatted =
        recommendations.map(
          (place) => ({

            name:
              place.name ||
              "Unknown Place",

            state:
              place.state ||
              "India",

            description:
              place.description ||
              "A beautiful lesser-known destination waiting to be explored.",

            image:
              place.image ||
              fallbackImage,

            score:
              place.match_score,

            latitude:
              place.latitude,

            longitude:
              place.longitude,

            budget:
              place.budget,

            nature:
              place.nature_score,

            adventure:
              place.adventure_score,

            culture:
              place.culture_score,

            crowd:
              place.crowd_score,

            accessibility:
              place.accessibility_score,

            season:
              place.best_season
          })
        );


      setPlaces(formatted);

    }

    catch (err) {

      console.error(err);

      setPlaces([]);

      setError(
        "Unable to connect to DesiTrails AI backend. Make sure FastAPI is running."
      );
    }

    finally {

      setLoading(false);
    }
  };


  // ==========================================================
  // ENTER KEY
  // ==========================================================

  const handleKeyDown = (event) => {

    if (event.key === "Enter") {

      searchPlaces();
    }
  };


  // ==========================================================
  // SUGGESTION
  // ==========================================================

  const useSuggestion = (value) => {

    setPrompt(value);

    setError("");
  };


  // ==========================================================
  // MAP
  // ==========================================================

  const openMap = (place) => {

    if (
      place.latitude &&
      place.longitude
    ) {

      const url =
        `https://www.google.com/maps/search/?api=1&query=${place.latitude},${place.longitude}`;

      window.open(
        url,
        "_blank"
      );

      return;
    }


    const query =
      encodeURIComponent(
        `${place.name}, ${place.state}, India`
      );


    window.open(
      `https://www.google.com/maps/search/?api=1&query=${query}`,
      "_blank"
    );
  };


  // ==========================================================
  // RENDER
  // ==========================================================

  return (

    <div className="app">


      {/* ====================================================
          NAVBAR
      ==================================================== */}

      <header className="navbar">

        <div className="nav-container">

          <div className="logo">

            DesiTrails
            <span>AI</span>

          </div>


          <nav>

            <a
              href="#home"
              className="active"
            >
              Home
            </a>

            <a href="#explore">
              Explore
            </a>

            <a href="#about">
              About
            </a>

          </nav>

        </div>

      </header>


      {/* ====================================================
          HERO
      ==================================================== */}

      <main>

        <section
          className="hero"
          id="home"
        >

          <div className="hero-container">


            {/* LEFT */}

            <div className="hero-content">

              <h1>

                Find less popular places

                <br />

                in India using AI.

              </h1>


              <p className="hero-description">

                DesiTrails AI helps you discover hidden gems

                <br />

                off the beaten path.

              </p>


              {/* SEARCH */}

              <div className="search-row">

                <div className="search-box">

                  <span className="location-icon">
                    📍
                  </span>


                  <input
                    type="text"
                    placeholder="Where do you want to go?"
                    value={prompt}
                    onChange={(event) =>
                      setPrompt(
                        event.target.value
                      )
                    }
                    onKeyDown={
                      handleKeyDown
                    }
                  />

                </div>


                <button
                  className="search-button"
                  onClick={
                    searchPlaces
                  }
                  disabled={loading}
                >

                  {loading
                    ? "Searching..."
                    : "Search"}

                </button>

              </div>


              {/* SUGGESTIONS */}

              <div className="try-text">

                Try:

                <button
                  onClick={() =>
                    useSuggestion(
                      "Ziro Valley"
                    )
                  }
                >
                  Ziro Valley
                </button>

                ,

                <button
                  onClick={() =>
                    useSuggestion(
                      "Bhandardara"
                    )
                  }
                >
                  Bhandardara
                </button>

                ,

                <button
                  onClick={() =>
                    useSuggestion(
                      "Tirthan Valley"
                    )
                  }
                >
                  Tirthan Valley
                </button>

              </div>

            </div>


            {/* RIGHT ILLUSTRATION */}

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


        {/* ==================================================
            ERROR
        ================================================== */}

        {error && (

          <div className="error-message">

            {error}

          </div>

        )}


        {/* ==================================================
            RECOMMENDATIONS
        ================================================== */}

        <section
          className="recommendations"
          id="explore"
        >

          <div className="recommendation-container">


            <h2>

              {searched
                ? "Places you might like"
                : "Less known places you might like"}

            </h2>


            {loading ? (

              <div className="loading">

                Finding the best places
                for you...

              </div>

            ) : places.length === 0 ? (

              <div className="no-results">

                No matching destinations found.

              </div>

            ) : (

              <div className="cards">

                {places.map(
                  (place, index) => (

                    <div
                      className="place-card"
                      key={
                        `${place.name}-${index}`
                      }
                    >


                      {/* IMAGE */}

                      <div className="card-image-wrapper">

                        <img
                          src={
                            place.image ||
                            fallbackImage
                          }
                          alt={
                            place.name
                          }
                          onError={(
                            event
                          ) => {

                            event.currentTarget.src =
                              fallbackImage;

                          }}
                        />


                        {/* MATCH SCORE */}

                        {place.score !==
                          undefined &&
                          place.score !==
                          null && (

                            <div className="score">

                              {Math.round(
                                place.score
                              )}
                              % match

                            </div>

                          )}

                      </div>


                      {/* CONTENT */}

                      <div className="card-content">

                        <h3>

                          {place.name}

                        </h3>


                        <div className="state">

                          <span className="pin">
                            📍
                          </span>

                          {place.state}

                        </div>


                        <p>

                          {
                            place.description
                          }

                        </p>


                        {/* MAP BUTTON */}

                        <button
                          className="map-button"
                          onClick={() =>
                            openMap(
                              place
                            )
                          }
                        >

                          View on Map →

                        </button>

                      </div>

                    </div>

                  )
                )}

              </div>

            )}


            {/* EXPLORE MORE */}

            <a
              className="explore-more"
              href="#explore"
            >

              Explore more places

              <span>→</span>

            </a>

          </div>

        </section>


        {/* ==================================================
            ABOUT
        ================================================== */}

        <section
          className="about"
          id="about"
        >

          <div className="about-container">

            <h2>
              Discover India beyond the usual
            </h2>

            <p>

              DesiTrails AI understands your
              travel preferences and recommends
              lesser-known destinations based on
              budget, nature, adventure, culture,
              crowd levels and accessibility.

            </p>

          </div>

        </section>

      </main>


      {/* ====================================================
          FOOTER
      ==================================================== */}

      <footer>

        <div className="footer-container">

          <div>

            © 2026 DesiTrails AI

          </div>


          <div className="footer-links">

            <a href="#about">
              About
            </a>

            <a href="#privacy">
              Privacy
            </a>

          </div>

        </div>

      </footer>

    </div>
  );
}


export default App;