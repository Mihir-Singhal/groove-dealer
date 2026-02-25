import axios from 'axios';

const API_BASE_URL = 'https://groove-dealer.onrender.com';

export const fetchRecommendations = async (prompt) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/api/recommend`, {
            user_prompt: prompt
        });
        return response.data.recommendations;
    } catch (error) {
        console.error("Error fetching recommendations:", error);
    
    // Create a new error object
    const customError = new Error(error.response?.data?.detail || "Failed to connect.");
    
    // Attach the status code so App.jsx can see it!
    customError.status = error.response?.status; 
    
    throw customError;
    }
};