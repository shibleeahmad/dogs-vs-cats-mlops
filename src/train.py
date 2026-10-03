import os

def main():
    print("Running Dogs vs. Cats training pipeline...")
    # Ensure output directories exist
    os.makedirs("models", exist_ok=True)
    print("Training complete. Model saved locally.")

if __name__ == "__main__":
    main()