from flask import Flask, render_template, request
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

# Load dataset
df = pd.read_csv('spotify_songs_local.csv')  # Replace with your dataset or API integration

# Preprocess data
df = df.drop_duplicates()
df = df.dropna()

scaler = MinMaxScaler()
df[['TEMPO', 'LOUDNESS', 'TRACK_POPULARITY']] = scaler.fit_transform(
    df[['TEMPO', 'LOUDNESS', 'TRACK_POPULARITY']]
)

# Select features for recommendation
features = ['TEMPO', 'LOUDNESS', 'LIVENESS', 'TRACK_POPULARITY', 'DANCEABILITY', 'ENERGY', 'INSTRUMENTALNESS']

# Compute feature vectors and similarity matrix
feature_vectors = df[features].values
similarity_matrix = cosine_similarity(feature_vectors)

# Recommendation function
def get_recommendations(song_name, n=10):
    """Get top n similar songs."""
    try:
        idx = df[df['TRACK_NAME'] == song_name].index[0]
    except IndexError:
        return f"Song '{song_name}' not found in the dataset."

    similarity_scores = list(enumerate(similarity_matrix[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    recommended_songs = []
    for i in similarity_scores:
        if df.iloc[i[0]]['TRACK_NAME'] != song_name and df.iloc[i[0]]['TRACK_NAME'] not in recommended_songs:
            recommended_songs.append(df.iloc[i[0]]['TRACK_NAME'])
        if len(recommended_songs) >= n:
            break

    return recommended_songs

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        song_name = request.form['song_name']  # Get song name from user input
        recommendations = get_recommendations(song_name)
        return render_template('index.html', recommendations=recommendations, song_name=song_name)
    else:
        return render_template('index.html', recommendations=None)

if __name__ == '__main__':
    app.run(debug=True)
