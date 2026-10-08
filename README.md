# Movie Recommendation System

A content-based movie recommender built with Python and Streamlit. Pick a movie and the app suggests five similar ones, with posters fetched from the TMDB API.

**Live demo: https://movie-recommendation-system-jqbaemfpwils2gphmzqp4j.streamlit.app/

## Features

- Select any movie from a searchable dropdown
- See the selected movie's poster
- Get 5 similar movie recommendations with posters
- Poster lookups are cached for speed, with a placeholder when a poster is unavailable

## How It Works

1. **Data:** the [TMDB 5000 Movies and Credits](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) datasets are merged on movie title.
2. **Preprocessing:** for each movie, the overview, genres, keywords, top 3 cast members and director are combined into a single `tags` text field, then lowercased and stemmed with NLTK's Porter Stemmer.
3. **Vectorization:** `CountVectorizer` (5,000 features, English stop words removed) turns each movie's tags into a vector.
4. **Similarity:** cosine similarity between vectors measures how alike two movies are. The five most similar movies are recommended.
5. **Posters:** each movie's `movie_id` is its TMDB ID, which is used to fetch the poster from the TMDB API.

The data preparation lives in `Movie_Recommendation.ipynb`.

## Tech Stack

- Python 3.10+
- Streamlit
- pandas
- scikit-learn
- NLTK (in the notebook)
- requests
- TMDB API

## Project Structure

```
Movie-Recommendation-System/
├── app.py                         # Streamlit app
├── movies_dict.pkl                # Processed movie data (movie_id, title, tags)
├── Movie_Recommendation.ipynb     # Data preprocessing and model building
├── requirements.txt               # Dependencies
└── .streamlit/
    └── secrets.toml               # TMDB API key (not committed)
```

The similarity matrix is too large for GitHub (about 176 MB), so the app rebuilds it from `movies_dict.pkl` when it starts and caches it.

## Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/nakibahsan299-debug/Movie-Recommendation-System.git
   cd Movie-Recommendation-System
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # macOS / Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your TMDB API key**

   Get a free key at [themoviedb.org](https://www.themoviedb.org/) (Settings, then API). Create `.streamlit/secrets.toml`:
   ```toml
   API_KEY = "your_tmdb_api_key"
   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

   It opens at `http://localhost:8501`.

## Deploy on Streamlit Community Cloud

1. Push the project to GitHub, without `secrets.toml`.
2. Go to [share.streamlit.io](https://share.streamlit.io) and click **Create app**.
3. Select the repository, branch and `app.py`.
4. Under **Advanced settings, Secrets**, add:
   ```toml
   API_KEY = "your_tmdb_api_key"
   ```
5. Click **Deploy**.

## Requirements

```
streamlit
pandas
requests
scikit-learn
```

## Acknowledgements

- Movie data from the [TMDB 5000 dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
- Posters provided by [TMDB](https://www.themoviedb.org/). This product uses the TMDB API but is not endorsed or certified by TMDB.

## Author

Nakib Ahsan
