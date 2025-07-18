import openai
import google.generativeai as genai

# ================================
# Explain Error Function
# ================================
def explain_error(response, right_answer, openai_key, gemini_key, instruction="", llm="OpenAI GPT-4o"):
    prompt = f"""{instruction}

Compare the student's response with the correct answer and explain the mistake:
- Response: {response}
- Right Answer: {right_answer}

Clearly describe the misunderstanding or mathematical error.
"""

    if llm == "OpenAI GPT-4o":
        openai.api_key = openai_key
        try:
            return openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            ).choices[0].message.content.strip()
        except Exception as e:
            return f"Error from OpenAI: {e}"

    elif llm == "Gemini Pro":
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error from Gemini: {e}"


# ================================
# Extract Error Summary
# ================================
def extract_summary(explanation, openai_key, gemini_key=None, llm="OpenAI GPT-4o"):
    prompt = f"""Extract and categorize the actual mathematical errors found in the explanation.

### Input:
{explanation}

### Output:
Comma-separated error types (e.g. omission error, conceptual misunderstanding)
"""
    if llm == "OpenAI GPT-4o":
        openai.api_key = openai_key
        try:
            return openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            ).choices[0].message.content.strip()
        except Exception as e:
            return f"Error from OpenAI: {e}"

    elif llm == "Gemini Pro":
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error from Gemini: {e}"


# ================================
# Categorize Using Newman
# ================================
def categorize_newman(explanation, openai_key, gemini_key=None, llm="OpenAI GPT-4o"):
    nea_background = """
**Newman’s Error Categories:**
1. **Reading Error**: Misreading or misinterpreting symbols or text of a problem (e.g., reading t as x).
2. **Comprehension Error**: Misunderstanding the meaning of the question despite correct reading, often due to conceptual confusion.
3. **Transformation Error**: Difficulty translating a problem into mathematical equations or procedures.
4. **Process Skills Error**: Incorrect use of algorithms or computational steps (e.g., applying the wrong derivative).
5. **Encoding Error**: Final answer is incorrect due to poor notation, sign errors, or misformatting, even if reasoning was correct.
"""

    prompt = f"""{nea_background}

Based on the explanation below, identify which Newman error categories apply:

### Explanation:
{explanation}

### Instructions:
- Only include relevant categories.
- Format output as a comma-separated list (e.g. comprehension error, encoding error)
- Do NOT include explanations or repeated items.
"""

    if llm == "OpenAI GPT-4o":
        openai.api_key = openai_key
        try:
            return openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            ).choices[0].message.content.strip()
        except Exception as e:
            return f"Error from OpenAI: {e}"

    elif llm == "Gemini Pro":
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error from Gemini: {e}"
