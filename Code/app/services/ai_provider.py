import nltk
from sentence_transformers import SentenceTransformer, util
from app.core.config import settings
import logging
import time

class AIProvider:
    def __init__(self):
        # Setup logging
        self.logger = logging.getLogger("AIProvider")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.FileHandler(settings.LOG_FILE_PATH)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self.logger.info("Initializing AIProvider...")

        # Suppress benign warnings from transformers (like "UNEXPECTED position_ids")
        logging.getLogger("transformers").setLevel(logging.ERROR)
        
        # Ensure NLTK data is downloaded
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("Downloading NLTK punkt tokenizer...")
            nltk.download('punkt')
            nltk.download('punkt_tab')

        # Load the model upon initialization
        print(f"Loading model: {settings.MODEL_NAME}...")
        self.model = SentenceTransformer(settings.MODEL_NAME)
        print("Model loaded successfully.")

    def summarize(self, text: str, num_sentences: int = 3) -> str:
        # --- Validation Logic ---
        if not text:
             raise ValueError("Text cannot be empty")
        
        # Remove whitespace for checks
        clean_text = text.replace(" ", "")
        
        if not clean_text:
             raise ValueError("Text cannot be empty")

        if clean_text.isdigit():
            raise ValueError("Text cannot consist only of numbers")

        if len(text.strip()) < 10:
             raise ValueError("Text is too short (min 10 chars)")
             
        if not any(c.isalnum() for c in text):
             raise ValueError("Text must contain letters or numbers")
        # ------------------------

        start_time = time.time()
        self.logger.info(f"Received summarization request. Text length: {len(text)} chars. Target sentences: {num_sentences}")
        self.logger.debug(f"Input text (first 100 chars): {text[:100]}...")
        # Use NLTK for robust sentence splitting
        sentences = nltk.sent_tokenize(text)
        print(f"DEBUG: Detected {len(sentences)} sentences.")
        
        if not sentences:
            return ""

        # FALLBACK: If we only found 1 sentence (but it's a long one), try to split by clauses
        if len(sentences) == 1:
            print("DEBUG: Single sentence detected. Attempting to split by clauses (';', ' - ').")
            # Try splitting by semicolon first
            clauses = text.split(';')
            if len(clauses) == 1:
                # Try splitting by " - " (dash used as separator)
                 clauses = text.split(' - ')
            
            # If we successfully split into multiple meaningful chunks, treat them as "sentences"
            if len(clauses) > 1:
                sentences = [c.strip() for c in clauses if c.strip()]
                print(f"DEBUG: Successfully split into {len(sentences)} clauses.")

        # If the text is *still* short enough, we can't really "summarize" it by extraction
        if len(sentences) <= num_sentences:
            print("DEBUG: Number of sentences <= requested. Returning original text.")
            return " ".join(sentences)

        # Compute embeddings
        # Encode the full document
        doc_embedding = self.model.encode(text, convert_to_tensor=True)
        # Encode individual sentences
        sentence_embeddings = self.model.encode(sentences, convert_to_tensor=True)

        # Calculate cosine similarity with the document
        scores = util.cos_sim(doc_embedding, sentence_embeddings)[0]

        # Pair scores with original index and sentence text
        scored_sentences = []
        for i, score in enumerate(scores):
            scored_sentences.append((score.item(), i, sentences[i]))

        # Sort by similarity score descending to find most relevant sentences
        scored_sentences.sort(key=lambda x: x[0], reverse=True)

        # Take top N
        top_sentences = scored_sentences[:num_sentences]

        # Sort by original index (i) to restore narrative flow
        top_sentences.sort(key=lambda x: x[1])

        # Join sentences
        final_summary = " ".join([item[2] for item in top_sentences])
        
        duration = time.time() - start_time
        self.logger.info(f"Summarization completed in {duration:.2f} seconds. Summary length: {len(final_summary)} chars.")
        self.logger.debug(f"Output summary: {final_summary}")
        
        return final_summary

# Global instance
ai_provider = AIProvider()
