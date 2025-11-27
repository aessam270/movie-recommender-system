import os
import urllib.request
import zipfile
import shutil

def download_data():
    """Download and extract MovieLens dataset"""
    print("Downloading MovieLens dataset...")
    url = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
    zip_path = "ml-latest-small.zip"
    
    try:
        # Download
        urllib.request.urlretrieve(url, zip_path)
        print("Download complete. Extracting...")
        
        # Extract
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
            
        # Move files to data directory
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Move specific files we need
        source_dir = "ml-latest-small"
        shutil.move(os.path.join(source_dir, "movies.csv"), "data/movies.csv")
        shutil.move(os.path.join(source_dir, "ratings.csv"), "data/ratings.csv")
        
        # Cleanup
        os.remove(zip_path)
        shutil.rmtree(source_dir)
        
        print("Data setup complete! Files saved in 'data/' directory.")
        
    except Exception as e:
        print(f"Error setting up data: {e}")

if __name__ == "__main__":
    download_data()
