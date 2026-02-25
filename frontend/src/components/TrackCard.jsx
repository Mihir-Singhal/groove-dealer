export default function TrackCard({ track, index }) {
    // Redirects to Spotify in a new tab when the card is clicked
    const handlePlay = () => {
        if (track.spotify_url) {
            window.open(track.spotify_url, '_blank');
        }
    };

    return (
        <div 
            className="track-card" 
            onClick={handlePlay}
            style={{ zIndex: index }} // Ensures overlapping works correctly
        >
            <img 
            src={track.image_url || "https://placehold.co/150x150/2a1b42/ffffff?text=Cover"} 
                alt="Album Art" 
                className="album-art"
                 onError={(e) => {
            
                 e.target.onerror = null; 
                 e.target.src = "https://placehold.co/150x150/2a1b42/ffffff?text=Cover";
        }}
    />
            <div className="track-info">
               
                <h3 className="track-title">{track.title}</h3>
                <p className="track-artist">{track.artist}</p>
                <p className="track-album">{track.genre || "Electronic"}</p>
            </div>
        </div>
    );
}