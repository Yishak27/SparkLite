from dotenv import load_dotenv
import os
import openai

load_dotenv()
OPEN_API_KEY = os.getenv("OPEN_AI_KEY")
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_API_KEYS = [k.strip() for k in GROK_API_KEY.split(",") if k.strip()]

class AICodeGenarator:
    def __init__(self):
        # self.client = openai.OpenAI(api_key=OPEN_API_KEY)
        self.current_key_index = 0
        self.client = self._create_client(GROK_API_KEYS[self.current_key_index])

    def _create_client(self, key):
        return openai.OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=key
        )
        # self.client = openai.OpenAI(
        #     base_url="https://api.groq.com/openai/v1",
        #     api_key=GROK_API_KEY
        # )
        
        # if 'chat_messages' not in st.session_state:
        #     st.session_state.chat_messages = []

    def _rotate_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(GROK_API_KEYS)
        print(f"Switching to next API key (index {self.current_key_index})")
        self.client = self._create_client(GROK_API_KEYS[self.current_key_index])

    def safe_completion(self, **kwargs):
        attempts = len(GROK_API_KEYS)
        for _ in range(attempts):
            try:
                response = self.client.chat.completions.create(**kwargs)
                return response
            except Exception as e:
                print("Error:", e)
                print("Trying next key...")
                self._rotate_key()
        raise Exception("All Groq API keys failed")     