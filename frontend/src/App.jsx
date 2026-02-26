import { useState, useEffect, useRef } from 'react';
import ChatInput from './components/ChatInput';
import TrackCard from './components/TrackCard';
import { fetchRecommendations } from './api';
import './App.css';

function App() {
    const [recommendations, setRecommendations] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const resultsEndRef = useRef(null);
    const [errorMessage, setErrorMessage] = useState("");

    useEffect(() => {
        if (recommendations.length > 0 && resultsEndRef.current) {
            resultsEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [recommendations]);
    
    const handleSearch = async (userPrompt) => {
        setIsLoading(true);
        setRecommendations([]);
        setErrorMessage("");

        try {
            const result = await fetchRecommendations(userPrompt);
            setRecommendations(result);
        } catch (err) {
            console.error("Caught Error:", err);

    // Now 'err.status' exists because we attached it in api.js!
    if (err.status === 429) {
        setErrorMessage("Whoa there, DJ! You're searching too fast. Take a breath and try again in a minute.");
    } else {
        setErrorMessage(err.message || "The AI curator is currently unavailable.");
    }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <>
          {/* --- THE FULL-WIDTH NAVBAR --- */}
          <header className="header-container">
            <h1 className="title">Groove Dealer</h1>
            <img src="/favicon.png" alt="Groove Dealer Logo" className="app-logo" />
          </header>
      
          {/* --- THE CENTERED APP CONTENT --- */}
          <div className="app-container">
            <ChatInput onSubmit={handleSearch} isLoading={isLoading} />
      
            {errorMessage && (
              <div className="error-banner">
                ⚠️ {errorMessage}
              </div>
            )}
      
            {recommendations.length > 0 && (
              <div className="results-container">
                {recommendations.map((track, index) => (
                  <TrackCard 
                    key={index} 
                    track={track} 
                    index={100 - index} 
                  />
                ))}
                <div ref={resultsEndRef} />
              </div>
            )}
          </div>
        </>
      );
}

export default App;