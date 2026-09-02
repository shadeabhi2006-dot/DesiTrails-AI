import { useEffect, useMemo, useState } from "react";
import "./App.css";

const API_URL = "https://desitrails-ai.onrender.com";
const fallbackImage = "https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=900&q=80";

const defaultPlaces = [
  { name: "Bakkhali Beach", state: "West Bengal", description: "Peaceful, quiet, natural and less crowded coastal environment.", image: fallbackImage },
  { name: "Jhargram", state: "West Bengal", description: "Forested, peaceful, rural and naturally beautiful.", image: fallbackImage },
  { name: "Bangus Valley", state: "Jammu and Kashmir", description: "A pristine alpine valley with meadows, forests and mountain ranges.", image: fallbackImage },
];

const DEFAULT_SLIDERS = { budget: 5, nature: 5, adventure: 5, culture: 5, crowd: 3, accessibility: 5 };

const num = (value, fallback = 0) => Number.isFinite(Number(value)) ? Number(value) : fallback;
const clamp = (value, min = 0, max = 100) => Math.max(min, Math.min(max, Number(value) || 0));

function normalizeTourism(value) {
  const text = String(value ?? "").trim().toLowerCase();
  if (text.includes("very low") || text === "low") return "Low";
  if (text.includes("high") || text.includes("very high")) return "High";
  if (text.includes("medium") || text.includes("moderate")) return "Medium";
  return text ? text.charAt(0).toUpperCase() + text.slice(1) : "Medium";
}

function similarity(destination, sliderValue, field) {
  const difference = Math.abs(num(destination[field], 0) - sliderValue);
  return clamp(100 - difference * 10);
}

function App() {
  const [prompt, setPrompt] = useState("");
  const [places, setPlaces] = useState(defaultPlaces);
  const [loading, setLoading] = useState(false);
  const [manualLoading, setManualLoading] = useState(false);
  const [error, setError] = useState("");
  const [searched, setSearched] = useState(false);
  const [manualOpen, setManualOpen] = useState(false);
  const [allDestinations, setAllDestinations] = useState([]);
  const [selectedState, setSelectedState] = useState("All India");
  const [sliders, setSliders] = useState(DEFAULT_SLIDERS);
  const [darkMode, setDarkMode] = useState(() => localStorage.getItem("desitrails-dark-mode") === "true");

  useEffect(() => {
    document.body.classList.toggle("dark-mode", darkMode);
    localStorage.setItem("desitrails-dark-mode", String(darkMode));
  }, [darkMode]);

  useEffect(() => {
    fetch(`${API_URL}/destinations`)
      .then((response) => {
        if (!response.ok) throw new Error("Could not load destinations.");
        return response.json();
      })
      .then((data) => setAllDestinations(data.destinations || []))
      .catch((err) => console.error("Manual recommendation data error:", err));
  }, []);

  const states = useMemo(() => [
    "All India",
    ...Array.from(new Set(allDestinations.map((d) => String(d.state || "").trim()).filter(Boolean))).sort(),
  ], [allDestinations]);

  const budgetRange = useMemo(() => {
    const budgets = allDestinations.map((d) => num(d.budget, NaN)).filter(Number.isFinite);
    if (!budgets.length) return { min: 500, max: 10000 };
    return { min: Math.min(...budgets), max: Math.max(...budgets) };
  }, [allDestinations]);

  const selectedBudget = Math.round(budgetRange.min + ((budgetRange.max - budgetRange.min) * sliders.budget) / 10);

  const updateSlider = (name, value) => setSliders((current) => ({ ...current, [name]: Number(value) }));

  const searchPlaces = async () => {
    if (!prompt.trim()) { setError("Please enter a travel preference."); return; }
    setLoading(true); setError(""); setSearched(true);
    try {
      const response = await fetch(`${API_URL}/recommend-from-prompt`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt.trim() }),
      });
      if (!response.ok) throw new Error("Backend request failed.");
      const data = await response.json();
      if (!data.success) { setPlaces([]); setError(data.message || "No recommendations found."); return; }
      const recommendations = data.recommendations || [];
      if (!recommendations.length) { setPlaces([]); setError("No matching destinations found."); return; }
      setPlaces(recommendations.map((place) => ({
        ...place,
        image: place.image || fallbackImage,
        score: place.match_score,
        description: place.description || place.environment || place.geography || "A beautiful lesser-known destination waiting to be explored.",
      })));
    } catch (err) {
      console.error(err); setPlaces([]);
      setError("Unable to connect to DesiTrails AI. Please check the backend deployment.");
    } finally { setLoading(false); }
  };

  const manualRecommend = () => {
    if (!allDestinations.length) { setError("Manual recommendations are still loading. Please try again."); return; }
    setManualLoading(true); setError(""); setSearched(true);
    try {
      let candidates = allDestinations;
      if (selectedState !== "All India") {
        candidates = candidates.filter((d) => String(d.state || "").trim().toLowerCase() === selectedState.toLowerCase());
      }
      if (!candidates.length) { setPlaces([]); setError("No destinations found for the selected state."); return; }

      const scored = candidates.map((destination) => {
        const budget = num(destination.budget, budgetRange.min);
        const budgetScore = budgetRange.max === budgetRange.min
          ? 100
          : clamp(100 - (Math.abs(budget - selectedBudget) / (budgetRange.max - budgetRange.min)) * 100);
        const scores = [
          budgetScore,
          similarity(destination, sliders.nature, "nature_score"),
          similarity(destination, sliders.adventure, "adventure_score"),
          similarity(destination, sliders.culture, "culture_score"),
          similarity(destination, sliders.crowd, "crowd_score"),
          similarity(destination, sliders.accessibility, "accessibility_score"),
        ];
        return {
          ...destination,
          image: destination.image || fallbackImage,
          description: destination.description || destination.environment || destination.geography || "A beautiful lesser-known destination waiting to be explored.",
          score: clamp(scores.reduce((sum, score) => sum + score, 0) / scores.length),
        };
      });
      scored.sort((a, b) => Number(b.score) - Number(a.score) || num(b.nature_score) - num(a.nature_score));
      setPlaces(scored.slice(0, 3));
    } finally { setManualLoading(false); }
  };

  const resetManual = () => { setSelectedState("All India"); setSliders(DEFAULT_SLIDERS); setError(""); };
  const handleKeyDown = (event) => { if (event.key === "Enter") searchPlaces(); };
  const useSuggestion = (value) => { setPrompt(value); setError(""); };

  const openMap = (place) => {
    if (place.latitude !== undefined && place.latitude !== null && place.longitude !== undefined && place.longitude !== null) {
      window.open(`https://www.google.com/maps/search/?api=1&query=${place.latitude},${place.longitude}`, "_blank", "noopener,noreferrer");
      return;
    }
    const query = encodeURIComponent(`${place.name}, ${place.state}, India`);
    window.open(`https://www.google.com/maps/search/?api=1&query=${query}`, "_blank", "noopener,noreferrer");
  };

  const renderSlider = (label, key, leftLabel, rightLabel) => (
    <div className="slider-item">
      <div className="slider-header"><span>{label}</span><strong>{sliders[key]}/10</strong></div>
      <input className="preference-slider" type="range" min="0" max="10" step="1" value={sliders[key]} onChange={(event) => updateSlider(key, event.target.value)} />
      <div className="slider-labels"><span>{leftLabel}</span><span>{rightLabel}</span></div>
    </div>
  );

  return (
    <div className={`app ${darkMode ? "dark" : ""}`}>
      <header className="navbar">
        <div className="nav-container">
          <div className="logo">DesiTrails <span>AI</span></div>
          <nav><a href="#home" className="active">Home</a><a href="#explore">Explore</a><a href="#about">About</a></nav>
          <button className="theme-button" onClick={() => setDarkMode((current) => !current)}>{darkMode ? "☀️ Light" : "🌙 Dark"}</button>
        </div>
      </header>

      <main>
        <section className="hero" id="home">
          <div className="hero-container">
            <div className="hero-content">
              <div className="eyebrow">AI-POWERED TRAVEL DISCOVERY</div>
              <h1>Find less popular places<br />in India using AI.</h1>
              <p className="hero-description">Tell DesiTrails what kind of trip you want, and discover destinations from our curated dataset.</p>
              <div className="search-row">
                <div className="search-box"><span className="location-icon">📍</span><input type="text" placeholder="e.g. cheap and peaceful place in Jammu and Kashmir" value={prompt} onChange={(event) => setPrompt(event.target.value)} onKeyDown={handleKeyDown} /></div>
                <button className="search-button" onClick={searchPlaces} disabled={loading}>{loading ? "Searching..." : "Search"}</button>
              </div>
              <div className="try-text">Try: <button onClick={() => useSuggestion("I want a cheap and peaceful place in West Bengal")}>Cheap + peaceful in West Bengal</button>, <button onClick={() => useSuggestion("I want a nature-filled adventurous place in Jammu and Kashmir")}>Nature + adventure in J&K</button>, <button onClick={() => useSuggestion("I want a cool and peaceful place in Manipur")}>Cool + peaceful in Manipur</button></div>
            </div>
            <div className="hero-image"><div className="landscape"><div className="cloud cloud-one"></div><div className="cloud cloud-two"></div><div className="mountain mountain-one"></div><div className="mountain mountain-two"></div><div className="mountain mountain-three"></div><div className="tree tree-one">▲</div><div className="tree tree-two">▲</div><div className="tree tree-three">▲</div><div className="ground"></div><div className="path"></div></div></div>
          </div>
        </section>

        {error && <div className="error-message">{error}</div>}

        <section className="manual-section" id="manual">
          <div className="manual-container">
            <button className="manual-toggle" onClick={() => setManualOpen((current) => !current)}>
              <span><small>OPTIONAL</small><strong>Prefer sliders instead?</strong></span><span className="toggle-arrow">{manualOpen ? "−" : "+"}</span>
            </button>
            {manualOpen && <div className="manual-panel">
              <div className="manual-heading">
                <div><h2>Manual Recommendation</h2><p>Choose your preferences and let DesiTrails rank the closest matches.</p></div>
                <select value={selectedState} onChange={(event) => setSelectedState(event.target.value)} className="state-select">
                  {states.map((state) => <option key={state} value={state}>{state}</option>)}
                </select>
              </div>
              <div className="slider-grid">
                {renderSlider("Budget", "budget", `₹${Math.round(budgetRange.min)}`, `₹${Math.round(budgetRange.max)}`)}
                {renderSlider("Nature", "nature", "Low", "High")}
                {renderSlider("Adventure", "adventure", "Low", "High")}
                {renderSlider("Culture", "culture", "Low", "High")}
                {renderSlider("Crowd level", "crowd", "Less crowded", "More crowded")}
                {renderSlider("Accessibility", "accessibility", "Remote", "Easy to reach")}
              </div>
              <div className="manual-actions">
                <span className="budget-preview">Desired budget: <strong>₹{selectedBudget}</strong></span>
                <div><button className="reset-button" onClick={resetManual}>Reset</button><button className="manual-button" onClick={manualRecommend} disabled={manualLoading}>{manualLoading ? "Finding..." : "Recommend"}</button></div>
              </div>
            </div>}
          </div>
        </section>

        <section className="recommendations" id="explore">
          <div className="recommendation-container">
            <h2>{searched ? "Places you might like" : "Less known places you might like"}</h2>
            {loading || manualLoading ? <div className="loading">Finding the best places for you...</div> : places.length === 0 ? <div className="no-results">No matching destinations found.</div> : <div className="cards">
              {places.map((place, index) => <div className="place-card" key={`${place.name}-${index}`}>
                <div className="card-image-wrapper"><img src={place.image || fallbackImage} alt={place.name} onError={(event) => { event.currentTarget.src = fallbackImage; }} />{place.score !== undefined && place.score !== null && <div className="score">{Math.round(Number(place.score))}% match</div>}</div>
                <div className="card-content"><h3>{place.name}</h3><div className="state"><span className="pin">📍</span>{place.state}</div><p>{place.description}</p>
                  <div className="card-details"><span>Budget: ₹{num(place.budget).toLocaleString("en-IN")}</span><span>Tourism: {normalizeTourism(place.tourism_saturation)}</span></div>
                  <button className="map-button" onClick={() => openMap(place)}>View on Map →</button>
                </div>
              </div>)}
            </div>}
            <a className="explore-more" href="#explore">Explore more places <span>→</span></a>
          </div>
        </section>

        <section className="about" id="about"><div className="about-container"><h2>Discover India beyond the usual</h2><p>DesiTrails AI combines natural-language recommendations with an optional manual preference system, so users can choose either the AI prompt experience or slider-based recommendations.</p></div></section>
      </main>

      <footer><div className="footer-container"><div>© 2026 DesiTrails AI</div><div className="footer-links"><a href="#about">About</a></div></div></footer>
    </div>
  );
}

export default App;
