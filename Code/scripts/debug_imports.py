import sys
print("Python started")
sys.stdout.flush()

print("Importing nltk...")
import nltk
print("NLTK imported")
sys.stdout.flush()

print("Checking NLTK data...")
try:
    nltk.data.find('tokenizers/punkt')
    print("NLTK data found")
except LookupError:
    print("NLTK data missing")
sys.stdout.flush()

print("Importing sentence_transformers...")
from sentence_transformers import SentenceTransformer
print("SentenceTransformer imported")
sys.stdout.flush()

print("Done")
