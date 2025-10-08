from langchain.chat_models import init_chat_model
from dotenv import load_dotenv


load_dotenv()

def get_google_genai():
    model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
    return model
    


def get_google_genai_alt(model_name="gemini-2.5-flash", temperature=0.3):
    """
    Alternative using init_chat_model with explicit configuration.
    """
    from langchain.chat_models import init_chat_model
    
    model = init_chat_model(
        model_name,
        model_provider="google_genai",
        temperature=temperature,
        configurable_fields=["model", "temperature"],
        # Add Gemini-specific config
        model_kwargs={"convert_system_message_to_human": True}
    )
    return model
