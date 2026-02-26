# 🎛️ Groove Dealer AI

![Live Deployment](https://img.shields.io/badge/Status-Live-success)
![React](https://img.shields.io/badge/Frontend-React%20%7C%20Vite-61DAFB?logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI%20%7C%20Python-009688?logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/AI_Engine-LangChain%20%7C%20Groq-purple)

**Groove Dealer** is a decoupled, AI-powered Full Stack web application designed to curate highly specific, non-commercial electronic music tracks (e.g., Progressive House, Minimal/Microhouse, Progressive Psytrance). 

By leveraging a custom LLM agent pipeline and the Spotify Web API, it bypasses standard algorithm drift to deliver precise, underground track recommendations.

🔗 **[View Live Application Here](https://groove-dealer.vercel.app/)**

---

## 🏗️ System Architecture

The application utilizes a strict Split-Host architecture, decoupling the client from the AI processing engine to ensure high performance and scalability.

* **Frontend (Vercel):** A responsive, glassmorphism UI built with React and Vite.
* **Backend (Render):** A stateless Python/FastAPI server handling rate-limiting, AI orchestration, and Spotify authentication.
* **AI Pipeline:** A multi-stage LangChain agent using Groq's high-speed LLM to translate user intent into structured Spotify queries.

---

## ✨ Key Features

* **Intelligent Curation:** Utilizes LangChain to interpret complex genre requests and filter out commercial/mainstream results.
* **Decoupled Architecture:** Independent frontend and backend deployments communicating via a secure, CORS-protected REST API.
* **API Security & Rate Limiting:** Implements `slowapi` on the backend to prevent abuse of the Groq and Spotify APIs.
* **Responsive Glassmorphism UI:** Custom CSS implementation ensuring flawless rendering across 4K monitors, tablets, and mobile devices.
* **Dynamic Audio Metadata:** Real-time integration with the Spotify API to fetch high-fidelity album art, artist details, and track IDs.

---

## 🛠️ Tech Stack

### Frontend
* **Framework:** React 18 (Vite)
* **Styling:** Custom CSS (Flexbox/Grid, CSS Variables, Media Queries)
* **Deployment:** Vercel

### Backend
* **Framework:** FastAPI (Python 3.10)
* **AI Orchestration:** LangChain & LangChain-Groq
* **External APIs:** Spotify Web API (`spotipy`), Groq API, LastFM API
* **Security:** `slowapi` (Rate Limiting), `python-dotenv`, CORS Middleware, Bouncer Firewall
* **Deployment:** Render
