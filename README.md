# GPT-3 Content Generator (Text)

This application is designed to generate various types of content using OpenAI's GPT-3 model. It provides a simple and user-friendly interface to input content requirements and generate corresponding outputs, which can be downloaded as text files.

## Features

- **Content Type Specification**: Users can specify the type of content they want to generate, such as outlines, video scripts, etc.
- **Goal and Topic Input**: Users can input the goal of the content and the topic to guide the content generation.
- **Relevant Context Addition**: Users can add any relevant context that should be included in the generated content.
- **Audience Specification**: The intended audience can be specified to tailor the content accordingly.
- **API Key Customization**: Users have the option to use their own OpenAI API key or the default key set in the environment.
- **Content Generation**: With the press of a button, the application generates content based on the inputs provided.
- **Content Download**: Generated content can be downloaded as a `.txt` file.

## How to Run the Application

1. Ensure you have Python and Streamlit installed on your system.
2. Clone this repository to your local machine.
3. Navigate to the cloned directory.
4. Run the command: `streamlit run app.py` (replace `app.py` with the actual file name if different).
5. The application will start and open in your default web browser.

## Configuration

The application uses the `OPENAI_API_KEY` environment variable as the default API key. If you want to use a different key, you can enter it in the provided text input field within the application.

## Dependencies

- Python 3
- Streamlit
- OpenAI
- Tenacity
- Logging

Install all the required packages using the following command:

```bash
pip install -r requirements.txt
```

## Usage

1. Enter the type of content you want to generate, such as an outline or a video script, in the "Enter the Type of Content" input field.
2. Provide the goal of the content in the "Enter the Goal" input field. This helps tailor the content generation process to your specific objectives.
3. Specify the topic of your content in the "Enter the Topic" input field to give the AI a clear direction for content generation.
4. Add any relevant context or background information in the "Enter Relevant Context" text area. This can include details that you want the generated content to consider or encompass.
5. Define the intended audience in the "Enter the Intended Audience" input field. Knowing the audience helps in customizing the content to their interests and comprehension level.
6. Click the "Generate Content" button to instruct the AI to start generating content based on the provided information.
7. Review the generated content in the output area. If it meets your requirements, you can use the "Download Draft" button to save the content to your device as a `.txt` file.


## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

For any queries or suggestions, please reach out to the project maintainer at your-email@example.com.

## Acknowledgements

- [OpenAI](https://openai.com/)
- [Streamlit](https://streamlit.io/)
- [Explore my other work](https://parth.club)

