import { useState } from 'react';

export default function ChatInput({ onSubmit, isLoading }) {
    const [prompt, setPrompt] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (prompt.trim() && !isLoading) {
            onSubmit(prompt);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="search-container">
            <div className="search-input-wrapper">
                <input 
                    type="text" 
                    className="search-input"
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="Search for an artist or track..."
                    disabled={isLoading}
                />
            </div>
            <button 
                type="submit" 
                className={`curate-btn ${isLoading ? 'glowing' : ''}`}
                disabled={isLoading || !prompt.trim()}
            >
                {isLoading ? 'Curating...' : 'Curate'}
            </button>
        </form>
    );
}