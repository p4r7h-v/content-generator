import streamlit as st
import openai
from tenacity import retry, stop_after_attempt, wait_fixed
import io
import os



# Separate OpenAI API interaction into its own class
class OpenAIAgent:
    def __init__(self, model, api_key=None):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
    def call(self, messages, stream=False):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                stream=stream,
            )
            return self._parse_response(response)
        except openai.error.OpenAIError as e:
            print(f"OpenAI API error: {e}")
            return ""
        except Exception as e:
            print(f"An unknown error occurred: {e}")
            return ""

    def _parse_response(self, response):
        response_dict = response.to_dict()
        if 'choices' in response_dict and response_dict['choices']:
            choice = response_dict['choices'][0]
            if 'message' in choice and 'content' in choice['message']:
                return choice['message']['content']
        return ""

# Cache to maintain state
@st.cache_data()
def load_state():
    return {"outline": ""}


# Main Function
def main():
    st.title("GPT-3 Content Generator (Text)")

    # Allow users to provide an API key
    user_api_key = st.text_input("Enter your OpenAI API Key (leave blank to use the default):")

    state = load_state()
    ai_agent = OpenAIAgent(model="gpt-3.5-turbo")

    content_type = st.text_input("Enter the Type of Content (e.g., outline, video script):")
    goal = st.text_input("Enter the Goal:")
    topic = st.text_input("Enter the Topic:")
    relevant_context = st.text_area("Enter Relevant Context:", height=200)
    audience = st.text_input("Enter the Intended Audience:")

    messages = [{
        "role": "system",
        "content": f"You are a helpful assistant that writes content. Requested content type is {content_type}. Goal is {goal}. Topic is {topic}. Relevant context is {relevant_context}. Audience is {audience}."
    }]

    if st.button("Generate Content"):
        regular_response_text = ai_agent.call(messages)
        state["outline"] = regular_response_text
        st.markdown("### Generated Content")
        st.markdown(regular_response_text)
        st.success(f"{content_type.capitalize()} Generated!")

    # Generate and download the draft
    if state["outline"]:
        draft_filename = f'{topic}_{content_type}.txt'
        # Convert the outline to bytes
        to_write = io.BytesIO(state["outline"].encode())
        st.download_button(
            label="Download Draft",
            data=to_write,
            file_name=draft_filename,
            mime="text/plain",
        )


if __name__ == "__main__":
    main()
