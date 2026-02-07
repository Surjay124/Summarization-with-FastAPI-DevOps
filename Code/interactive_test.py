import httpx
import json
import sys

# Constants
API_URL = "http://127.0.0.1:8000/api/v1/summarize"

def main():
    print("\n" + "="*50)
    print("   AI Summarizer Service - Interactive Client")
    print("="*50)
    print("Note: Provide a text with at least 2 sentences to see the summarization in action.\n")

    while True:
        print("\nEnter text to summarize (or type 'exit' to quit):")
        # Read multi-line input
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if not line and not lines:
                continue # ignore empty starting lines
            if line.strip() == "END": # keyword to end input if needed, but enter twice is standard
                break
            if not line: # empty line means end of input for this script's simplicity
                break
            lines.append(line)
        
        text = " ".join(lines).strip()
        
        if text.lower() == 'exit':
            print("Exiting...")
            break
            
        if not text:
            print("Error: Input text was empty.")
            continue

        try:
            num_sentences = input("Enter number of sentences for summary (default 3): ")
            num_sentences = int(num_sentences) if num_sentences.strip() else 3
        except ValueError:
            print("Invalid number. Using default 3.")
            num_sentences = 3

        payload = {
            "text": text,
            "num_sentences": num_sentences
        }

        print("\nSending request...")
        try:
            with httpx.Client() as client:
                response = client.post(API_URL, json=payload, timeout=30.0)
            
            if response.status_code == 200:
                data = response.json()
                print("\n" + "-"*20 + " SUMMARY " + "-"*20)
                print(data['summary'])
                print("-"*(49))
                print(f"[Original info: {data['original_length']} chars -> {data['summary_length']} chars]")
            else:
                print(f"\n❌ Error {response.status_code}: {response.text}")

        except httpx.RequestError as e:
            print(f"\n❌ Error: Could not connect to server. Is it running? Details: {e}")
            
        print("\n" + "="*50)

if __name__ == "__main__":
    main()
