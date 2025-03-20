import requests

# Ollama API endpoint (default is localhost:11434)
OLLAMA_API_URL = "http://localhost:11434/api/generate"

def test_ollama(prompt: str, model: str = "llama3"):
    """
    Send a prompt to Ollama using the specified model and print the response.
    """
    try:
        # Prepare the request payload
        payload = {
            "model": model,  # Specify the model (e.g., llama3)
            "prompt": prompt,  # The input prompt
            "stream": False  # Disable streaming for simplicity
        }

        # Send the request to Ollama
        response = requests.post(OLLAMA_API_URL, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response JSON
            response_data = response.json()
            print("✅ Response from Ollama:")
            print(response_data.get("response", "No response found"))
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    # Test prompt
    test_prompt = "Explain the concept of artificial intelligence in one sentence."

    # Call the function to test Ollama
    print(f"🧪 Testing Ollama with model 'llama3' and prompt: '{test_prompt}'")
    test_ollama(test_prompt)