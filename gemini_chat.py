import google.generativeai as genai
from System.instruction import instructions
from System.Encryption import decoded

# Configure API key
genai.configure(api_key=decoded)

# -------------------------
# MODEL OPTIONS (choose one)
# -------------------------
# MODEL_ID = "gemini-3-flash-preview"      # Main JARVIS model (default)
# MODEL_ID = "gemini-2.5-flash-lite"       # Older, low-tier text model
# MODEL_ID = "gemini-2.5-flash-native-audio-dialog"  # Live API, unlimited (overkill for text)
# -------------------------

PRIMARY_MODEL_ID = "gemini-3-flash-preview"
FALLBACK_MODEL_ID = "gemini-2.5-flash-lite"

# Pre-initialize models
PRIMARY_MODEL = genai.GenerativeModel(
    model_name=PRIMARY_MODEL_ID,
    system_instruction=instructions
)

FALLBACK_MODEL = genai.GenerativeModel(
    model_name=FALLBACK_MODEL_ID,
    system_instruction=instructions
)

def chat(user_input, session_data):
    """
    Chat function with session-based history.
    Automatically falls back to Lite model if quota exceeded.
    """
    # Initialize history
    if "history" not in session_data:
        session_data["history"] = []

    history = session_data["history"]

    # Append user message
    history.append({"role": "user", "parts": [{"text": user_input}]})

    try:
        # Attempt primary model first
        response = PRIMARY_MODEL.generate_content(history)
        response_text = response.text or "[EMPTY RESPONSE]"
        history.append({"role": "model", "parts": [{"text": response_text}]})
        session_data["history"] = history
        return response_text

    except Exception as e:
        error_msg = str(e)
        print("--- JARVIS PRIMARY ERROR ---")
        print(error_msg)

        # Handle quota exceeded
        if "429" in error_msg:
            print("Quota hit. Switching to fallback model.")
            try:
                response = FALLBACK_MODEL.generate_content(history)
                response_text = response.text or "[EMPTY RESPONSE]"
                history.append({"role": "model", "parts": [{"text": response_text}]})
                session_data["history"] = history
                return f"[Safety Backup] {response_text}"
            except Exception as fe:
                print("--- FALLBACK MODEL ERROR ---")
                print(str(fe))
                return "[MOCK] All models unavailable. Please try later."

        # Handle model not found
        if "404" in error_msg:
            return f"Model ID Error: '{PRIMARY_MODEL_ID}' might be incorrect."

        # Other errors
        return f"System Error: {error_msg[:50]}..."
    
    finally:
        # Optional: keep only last 20 messages to prevent history overload
        if len(history) > 20:
            session_data["history"] = history[-20:]
        else:
            session_data["history"] = history