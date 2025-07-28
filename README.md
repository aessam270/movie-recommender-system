# 🎬 Movie Recommender System

A simple movie recommendation system built with Python that suggests movies based on user ratings and correlations.

## 🚀 Features

- **Correlation-based recommendations** - Find movies similar to your favorites
- **Interactive web interface** - Built with Streamlit
- **Data visualization** - See top-rated movies in charts
- **Fast performance** - Optimized for large datasets

## 📊 How it works

1. Loads movie and rating data from CSV files
2. Creates a user-movie rating matrix
3. Calculates correlations between movies
4. Recommends movies with high correlation scores
5. Filters results by minimum rating count for quality

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/aessam270/movie-recommender.git
cd movie-recommender

# Install required packages
pip install pandas matplotlib streamlit numpy


```

## 📁 Data Setup

Download the MovieLens dataset and place these files in a `data/` folder:
- `movies.csv` - Contains movieId, title, genres
- `ratings.csv` - Contains userId, movieId, rating, timestamp

You can get the data from: [MovieLens Dataset](https://grouplens.org/datasets/movielens/)

## 🏃‍♂️ Usage

### Run the Streamlit Web App
```bash
streamlit run movie-recommender.py
```

### Run as Python Script
```bash
python movie-recommender.py
```

## 📸 Screenshots


## 📈 Example Output

```
Movies similar to 'Toy Story (1995)':
                               correlation  average_rating  rating_count
Toy Story 2 (1999)                   0.87            4.1           156
A Bug's Life (1998)                  0.76            3.9           142
Monsters, Inc. (2001)                0.72            4.2           98
```

## 🔧 Technical Details

- **Language**: Python 3.7+
- **Libraries**: Pandas, NumPy, Matplotlib, Streamlit
- **Algorithm**: Pearson correlation coefficient
- **Dataset**: MovieLens (movies and ratings)

## 🎯 Future Improvements

- [ ] Add content-based filtering
- [ ] Implement collaborative filtering
- [ ] Add user authentication
- [ ] Include movie posters and descriptions
- [ ] Deploy to cloud platform

## 🤝 Contributing

Feel free to fork this project and submit pull requests! Some areas that need work:
- Better error handling
- More recommendation algorithms
- UI/UX improvements

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

Ahmed Essam - Aspiring Data Scientist
- GitHub: [@aessam270](https://github.com/aessam270)
