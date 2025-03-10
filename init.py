import requests
import json



def query_ollama(prompt):
    url = "http://127.0.0.1:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {"model": "deepseek-r1", "prompt": prompt}

    response = requests.post(url, headers=headers, json=data, stream=True)
    
    # Concatenating all response chunks
    final_text = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            final_text += data.get("response", "")

    return final_text.strip()

# Example usage
clean_answer = query_ollama("Explain diabetes.")
print("\nGenerated Answer:\n", clean_answer)
