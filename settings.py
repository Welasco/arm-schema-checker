import os


class Settings:
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
        self.Endpoint = os.getenv('GPT_OPENAI_ENDPOINT')
        self.api_key = os.getenv('GPT_OPENAI_KEY')
        self.model = os.getenv('GPT_OPENAI_MODEL_NAME')
        self.deployment = os.getenv('GPT_OPENAI_DEPLOYMENT_NAME')
        self.version = os.getenv('GPT_OPENAI_API_VERSION')


settings = None


def get_settings():
    global settings
    if settings is None:
        settings = Settings()
    return settings
