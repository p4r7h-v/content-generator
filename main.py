import streamlit as st
import openai
import tenacity

# Cache to maintain state
@st.cache_data()
def load_state():
    return {"outline": ""}

# Function Descriptions
function_descriptions = [
    {
        "name": "write_file",
        "description": "Writes the provided content to the provided file path.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "The full file path to write the content to."},
                "content": {"type": "string", "description": "The content to write."},
            },
            "required": ["file_path", "content"],
        },
    }
]


@tenacity.retry(stop=tenacity.stop_after_attempt(5), wait=tenacity.wait_fixed(2))
def gpt_function_call(model, functions, function_call, messages, stream=False):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            stream=stream,
            functions=functions,
            function_call=function_call,
            max_tokens=150,
        )
        
        print(f"Debug: Type of response is {type(response)}")

        # Convert the OpenAIObject to a dictionary
        response_dict = response.to_dict()

        function_name = None
        function_argument_text = ''
        regular_response_text = ''
        
        if 'choices' in response_dict and len(response_dict['choices']) > 0:
            choice = response_dict['choices'][0]
            
            if 'message' in choice and 'content' in choice['message']:
                regular_response_text = choice['message']['content']

            if 'delta' in choice and 'function_call' in choice['delta']:
                function_call_data = choice['delta']['function_call']
                function_name = function_call_data.get('name', None)
                function_argument_text = function_call_data.get('arguments', '')

        return regular_response_text, function_name, function_argument_text

    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return None, None, None
    except Exception as e:
        print(f"An unknown error occurred: {e}")
        return None, None, None



# Main Function
def main():
    st.title("Automated Content Creation")
    
    state = load_state()

    # User Inputs
    content_type = st.text_input("Enter the Type of Content (e.g., outline, video script):")
    goal = st.text_input("Enter the Goal:")
    topic = st.text_input("Enter the Topic:")
    relevant_content = st.text_area("Enter Relevant Content:", height=200)
    audience = st.text_input("Enter the Intended Audience:")

    # Initialize your messages here
    messages = [{
        "role": "system",
        "content": "You are a helpful assistant that helps people write content. You have access to {functions} that can help you write content. Content type is {content_type}. Goal is {goal}. Topic is {topic}. Relevant content is {relevant_content}. Audience is {audience}."
    }]
    st.markdown("## Messages")
    st.markdown("### System")

    # Generate Content Button
    if st.button("Generate Content"):
        regular_response_text, function_name, function_argument_text = gpt_function_call(
            model="gpt-3.5-turbo",
            functions=function_descriptions,
            function_call="auto",
            messages=messages,
            stream=False  # Update this as per your needs
        )
        state["outline"] = regular_response_text
        st.markdown(regular_response_text)
        st.success(f"{content_type.capitalize()} Generated!")

    # Save Draft Button
    if st.button("Save Draft"):
        draft_path = f'drafts/{topic}_{content_type}.txt'
        write_result = write_file(draft_path, state.get("outline", ""))
        st.success(write_result)

if __name__ == "__main__":
    main()
