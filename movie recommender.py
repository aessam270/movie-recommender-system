import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def load_and_prepare_data():
    """Load data and create movie statistics"""
    # Load datasets
    movies = pd.read_csv("data/movies.csv")
    ratings = pd.read_csv("data/ratings.csv")
    df = pd.merge(ratings, movies, on='movieId')
    
    # Create movie stats
    movie_stats = df.groupby('title').agg({
        'rating': ['count', 'mean']
    }).round(2)
    movie_stats.columns = ['rating_count', 'average_rating']
    
    return df, movie_stats

def create_movie_matrix(df, max_users=5000, max_movies=1000):
    """Create user-movie rating matrix"""
    # Get top users and movies for performance
    top_users = df['userId'].value_counts().head(max_users).index
    top_movies = df['title'].value_counts().head(max_movies).index
    
    # Filter and create matrix
    df_subset = df[df['userId'].isin(top_users) & df['title'].isin(top_movies)]
    return df_subset.pivot_table(index='userId', columns='title', values='rating')

def get_recommendations(movie_matrix, movie_stats, movie_title, top_n=10):
    """Get movie recommendations based on correlation"""
    if movie_title not in movie_matrix.columns:
        return f"Movie '{movie_title}' not found!"
    
    # Calculate correlations and merge with stats
    correlations = movie_matrix.corrwith(movie_matrix[movie_title]).dropna()
    recommendations = pd.DataFrame({'correlation': correlations})
    recommendations = recommendations.join(movie_stats)
    
    # Filter and sort
    return recommendations[
        (recommendations['rating_count'] > 50) & 
        (recommendations.index != movie_title)
    ].sort_values('correlation', ascending=False).head(top_n)

def plot_top_movies(movie_stats, top_n=10):
    """Plot top rated movies"""
    top_movies = movie_stats[movie_stats['rating_count'] > 50].head(top_n)
    
    plt.figure(figsize=(10, 6))
    plt.barh(range(len(top_movies)), top_movies['average_rating'])
    plt.yticks(range(len(top_movies)), top_movies.index)
    plt.xlabel('Average Rating')
    plt.title(f'Top {top_n} Highest Rated Movies')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

# Main execution
if __name__ == "__main__":
    # Load data
    df, movie_stats = load_and_prepare_data()
    movie_matrix = create_movie_matrix(df)
    
    # Get recommendations
    movie_title = "Toy Story (1995)"
    recommendations = get_recommendations(movie_matrix, movie_stats, movie_title)
    
    print(f"Movies similar to '{movie_title}':")
    print(recommendations[['correlation', 'average_rating', 'rating_count']].head())
    
    # Plot top movies
    plot_top_movies(movie_stats)



# Streamlit app 
def streamlit_app():
    st.title("🎬 Movie Recommender")
    
    
    # Load data 
    df, movie_stats = load_and_prepare_data()
    movie_matrix = create_movie_matrix(df)
    
    movie_name = st.text_input("Enter a movie:")
    
    if movie_name:
        recommendations = get_recommendations(movie_matrix, movie_stats, movie_name)
        
        if isinstance(recommendations, str):  # Error message
            st.error(recommendations)
        else:
            st.write("**Similar Movies:**")
            for title, row in recommendations.iterrows():
                st.write(f"• {title} - Rating: {row['average_rating']:.1f} ⭐")

if __name__ == "__main__":
    import sys
    if 'streamlit' in sys.modules:
        streamlit_app()
    else:
        # Regular Python execution
        df, movie_stats = load_and_prepare_data()
        movie_matrix = create_movie_matrix(df)
        
        movie_title = "Toy Story (1995)"
        recommendations = get_recommendations(movie_matrix, movie_stats, movie_title)
        print(f"Movies similar to '{movie_title}':")
        print(recommendations[['correlation', 'average_rating', 'rating_count']].head())