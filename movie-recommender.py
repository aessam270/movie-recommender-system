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

def streamlit_app():
    st.title("🎬 Movie Recommender")
    
    try:
        # Load data 
        with st.spinner('Loading data...'):
            df, movie_stats = load_and_prepare_data()
            movie_matrix = create_movie_matrix(df)
        
        st.success("Data loaded successfully!")
        
        # Sidebar for stats
        st.sidebar.header("Dataset Stats")
        st.sidebar.write(f"Total Movies: {len(movie_stats)}")
        st.sidebar.write(f"Total Ratings: {len(df)}")
        
        # Main content
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Get Recommendations")
            movie_name = st.selectbox(
                "Select a movie:",
                options=movie_stats.index.sort_values(),
                index=None,
                placeholder="Type to search..."
            )
            
            if movie_name:
                recommendations = get_recommendations(movie_matrix, movie_stats, movie_name)
                
                if isinstance(recommendations, str):
                    st.error(recommendations)
                else:
                    st.write("### Similar Movies")
                    for title, row in recommendations.iterrows():
                        with st.expander(f"{title} (Rating: {row['average_rating']:.1f}⭐)"):
                            st.write(f"Correlation: {row['correlation']:.2f}")
                            st.write(f"Number of Ratings: {int(row['rating_count'])}")
                            
        with col2:
            st.subheader("Top Rated Movies")
            # Use st.pyplot for the plot
            top_movies = movie_stats[movie_stats['rating_count'] > 50].head(10)
            fig, ax = plt.subplots(figsize=(6, 8))
            ax.barh(range(len(top_movies)), top_movies['average_rating'])
            ax.set_yticks(range(len(top_movies)))
            ax.set_yticklabels(top_movies.index)
            ax.set_xlabel('Average Rating')
            ax.invert_yaxis()
            st.pyplot(fig)

    except FileNotFoundError:
        st.error("Data files not found! Please run setup_data.py first.")
    except Exception as e:
        st.error(f"An error occurred: {e}")


# Main execution
if __name__ == "__main__":
    import sys
    
    # Check if running with Streamlit
    if 'streamlit' in sys.modules:
        streamlit_app()
    else:
        # Regular Python execution
        try:
            df, movie_stats = load_and_prepare_data()
            movie_matrix = create_movie_matrix(df)
            
            movie_title = "Toy Story (1995)"
            recommendations = get_recommendations(movie_matrix, movie_stats, movie_title)
            
            print(f"Movies similar to '{movie_title}':")
            if isinstance(recommendations, str):
                print(recommendations)
            else:
                print(recommendations[['correlation', 'average_rating', 'rating_count']].head())
            
            # Plot top movies
            plot_top_movies(movie_stats)
            
        except FileNotFoundError:
            print("Error: Data files not found!")
            print("Please run 'python setup_data.py' first to download the dataset.")
        except Exception as e:
            print(f"An error occurred: {e}")
