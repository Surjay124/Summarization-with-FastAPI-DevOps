from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_summary():
    text = (
        "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints. "
        "The key features are: Fast: Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic). "
        "Fast to code: Increase the speed to develop features by about 200% to 300%. "
        "Fewer bugs: Reduce about 40% of human (developer) induced errors. "
        "Intuitive: Great editor support. Completion everywhere. Less time debugging. "
        "Easy: Designed to be easy to use and learn. Less time reading docs. "
        "Short: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs. "
        "Robust: Get production-ready code. With automatic interactive documentation. "
        "Standards-based: Based on (and fully compatible with) the open standards for APIs: OpenAPI (previously known as Swagger) and JSON Schema."
    )
    
    print("Sending request...")
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/summarize",
            json={"text": text, "num_sentences": 2} # Ask for 2 sentences
        )
    
    if response.status_code == 200:
        data = response.json()
        print("\n--- RESPONSE ---")
        print(f"Original Length: {data['original_length']}")
        print(f"Summary Length: {data['summary_length']}")
        print("\n--- SUMMARY CONTENT ---")
        print(data['summary'])
        print("\n✅ Verification Successful!")
    else:
        print(f"\n❌ Request Failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_summary()
