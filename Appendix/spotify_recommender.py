import tkinter as tk
from tkinter import ttk, messagebox
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from fuzzywuzzy import process
import pandas as pd
import requests

# Fetch data from API
url = "https://our-service-442302-c3.wl.r.appspot.com/get_data/spotify_songs"
response = requests.get(url)
data = response.json()
df = pd.DataFrame(data)

# Preprocess data
df = df.drop_duplicates().dropna()

# Normalize numerical features
scaler = MinMaxScaler()
numerical_features = ['TEMPO', 'LOUDNESS', 'TRACK_POPULARITY', 'DANCEABILITY', 'ENERGY', 'LIVENESS', 'INSTRUMENTALNESS']
df[numerical_features] = scaler.fit_transform(df[numerical_features])

# Compute feature vectors and similarity matrix
feature_vectors = df[numerical_features].values
similarity_matrix = cosine_similarity(feature_vectors)

# Get list of songs
all_songs = df['TRACK_NAME'].tolist()

# Function to get recommendations with artists
def get_recommendations(song_name, weights, n=10):
    try:
        idx = df[df['TRACK_NAME'].str.lower() == song_name.lower()].index[0]
    except IndexError:
        return f"Song '{song_name}' not found in the dataset."

    # Apply weights to the features
    weighted_vectors = feature_vectors * weights
    similarity_matrix = cosine_similarity(weighted_vectors)
    similarity_scores = list(enumerate(similarity_matrix[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    recommended_songs = []
    for i in similarity_scores:
        if (
            df.iloc[i[0]]['TRACK_NAME'] != song_name
            and (df.iloc[i[0]]['TRACK_NAME'], df.iloc[i[0]]['TRACK_ARTIST']) not in recommended_songs
        ):
            recommended_songs.append((df.iloc[i[0]]['TRACK_NAME'], df.iloc[i[0]]['TRACK_ARTIST']))
        if len(recommended_songs) >= n:
            break

    return recommended_songs

# Tkinter GUI
class SpotifyRecommenderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Spotify Song Recommender")
        self.geometry("600x800")
        self.configure(bg="#191414")  # Spotify's black background

        # Header
        header_label = tk.Label(self, text="Spotify Song Recommender", font=("Helvetica", 20, "bold"), bg="#191414", fg="#1DB954")
        header_label.pack(pady=20)

        # Input Section
        input_frame = tk.Frame(self, bg="#191414")
        input_frame.pack(pady=10, fill="x", padx=20)

        tk.Label(input_frame, text="Enter a Song Name:", font=("Helvetica", 12), bg="#191414", fg="white").grid(row=0, column=0, sticky="w", padx=5)
        self.song_entry = ttk.Entry(input_frame, width=40)
        self.song_entry.grid(row=0, column=1, padx=5, sticky="e")

        # Feature Sliders
        slider_frame = tk.Frame(self, bg="#191414")
        slider_frame.pack(pady=20, fill="x", padx=20)

        self.sliders = {}
        for idx, feature in enumerate(numerical_features):
            row = idx // 2
            col = idx % 2

            slider_container = tk.Frame(slider_frame, bg="#191414")
            slider_container.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

            tk.Label(slider_container, text=f"{feature} Weight:", font=("Helvetica", 12), bg="#191414", fg="white").pack(anchor="w")
            slider = tk.Scale(slider_container, from_=0, to=10, orient=tk.HORIZONTAL, length=250, bg="#191414", fg="white", troughcolor="#1DB954")
            slider.set(5)  # Default weight
            slider.pack(anchor="w")
            self.sliders[feature] = slider

        # Search Button
        search_button = tk.Button(self, text="Get Recommendations", font=("Helvetica", 12), bg="#1DB954", fg="white", command=self.show_recommendations)
        search_button.pack(pady=10)

        # Recommendations Section
        self.recommendations_label = tk.Label(self, text="", font=("Helvetica", 12), bg="#191414", fg="white", justify="left", anchor="w", wraplength=500)
        self.recommendations_label.pack(pady=20, fill="both", padx=20)

    def show_recommendations(self):
        song_name = self.song_entry.get()
        weights = [self.sliders[feature].get() for feature in numerical_features]

        # Check for a close match if the song is not found
        closest_match, similarity = process.extractOne(song_name, all_songs)
        if song_name.lower() != closest_match.lower():
            # Pop-up to suggest the correct song name
            response = messagebox.askyesno("Did you mean?", f"Did you mean '{closest_match}'?")
            if not response:
                return
            song_name = closest_match

        # Get recommendations with artists
        recommendations = get_recommendations(song_name, weights)

        # Display recommendations
        if isinstance(recommendations, str):  # Error message
            self.recommendations_label.config(text=recommendations, fg="red")
        else:
            recommendations_text = f"Recommendations for '{song_name}':\n" + "\n".join(
                [f"{idx+1}. {song} by {artist}" for idx, (song, artist) in enumerate(recommendations)]
            )
            self.recommendations_label.config(text=recommendations_text, fg="white")

# Run the app
if __name__ == "__main__":
    app = SpotifyRecommenderApp()
    app.mainloop()
