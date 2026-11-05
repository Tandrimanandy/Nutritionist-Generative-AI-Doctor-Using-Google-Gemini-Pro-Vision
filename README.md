# Nutritionist AI

An AI-powered nutrition assistant built with Streamlit and Google Gemini. Upload a photo of a meal, optionally add a question, and receive an itemised calorie estimate with a total.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-API-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-B8860B)](#license)

---

## Project Overview

Nutritionist AI is a single-page web application that analyses food images with a multimodal Gemini model. The application identifies the visible food items, estimates the calories for each item, and reports the total. The interface uses a custom yellow and brown theme with animated highlights.

Project documentation is organised into the expandable cards below. Select a card to view its contents.

---

<details>
<summary><b>Languages Used</b></summary>

<br>

| Language | Usage |
|---|---|
| Python 3.10 or later | Application logic, Gemini API integration, and Streamlit interface |
| CSS | Custom theme, hero banner, glitter animation, and component styling |
| HTML | Inline markup for layout elements rendered through `st.markdown` |

</details>

<details>
<summary><b>Libraries and Frameworks</b></summary>

<br>

| Package | Purpose |
|---|---|
| `streamlit` | Web interface, widgets, layout, and session handling |
| `google-genai` | Official Google GenAI SDK used to call the Gemini model |
| `python-dotenv` | Loads the API key from the `.env` file |
| `pillow` | Image support required by Streamlit for image handling |
| `random` (standard library) | Generates the fixed sparkle layout for the glitter effect |
| `os` (standard library) | Reads environment variables |
| `pathlib` (standard library) | Resolves the path of the `.env` file relative to `app.py` |

</details>

<details>
<summary><b>Functions and Components</b></summary>

<br>

**`sparkle_layer(count: int = 45) -> str`**
Builds the HTML for a fixed layer of twinkling gold sparkles. The layout uses a fixed random seed, so the sparkles appear in the same positions on every rerun.

**`get_client(api_key: str) -> genai.Client`**
Creates the Gemini client. The function is decorated with `@st.cache_resource`, so the client is created once and reused across user interactions.

**`analyse_food(client, user_prompt, image_bytes, mime_type) -> str`**
Sends the image and the user's question to the Gemini model together with the system prompt. It returns the response text. The temperature is set to `0.3` to keep the calorie estimates consistent.

**Page layout**

- Hero banner with the application title and animated shimmer effect
- Left column: image upload, optional question, and the calculate button
- Right column: preview of the uploaded image
- Results section: calorie breakdown inside a bordered card, followed by a disclaimer

**Configuration constants**

- `MODEL_NAME`: the Gemini model used for analysis (`gemini-flash-lite-latest`)
- `SYSTEM_PROMPT`: the instructions that define the nutritionist role and the output format
- `CSS`: the complete theme stylesheet

</details>

<details>
<summary><b>Project Structure</b></summary>

<br>

```
End_to_End_Nutritionist/
├── app.py               Main Streamlit application
├── requirements.txt     Python package dependencies
├── .env                 Environment variables (API key). Do not commit this file.
├── docs/
│   └── images/          Screenshots used in this README
│       ├── upload-and-preview.png
│       ├── nutrition-report.png
│       └── connection-error.png
└── .streamlit/          Optional folder for Streamlit settings
    └── config.toml      Optional theme configuration
```

</details>

<details>
<summary><b>Prerequisites</b></summary>

<br>

- Python 3.10 or later
- `pip` package manager
- A Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
- A web browser

</details>

<details>
<summary><b>Installation</b></summary>

<br>

**1. Open a terminal in the project folder**

```bash
cd End_to_End_Nutritionist
```

**2. Create and activate a virtual environment**

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS and Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install the dependencies**

```bash
pip install -r requirements.txt
```

</details>

<details>
<summary><b>Configuration</b></summary>

<br>

**1. Create the environment file**

Create a file named `.env` in the same folder as `app.py`:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your key. The application reads this value at startup. Do not share the key or commit the `.env` file to a public repository.

**2. Optional: theme configuration**

To apply the Streamlit theme settings, create a folder named `.streamlit` and add a file named `config.toml`:

```toml
[theme]
base = "light"
primaryColor = "#E6B800"
backgroundColor = "#FFF6D5"
secondaryBackgroundColor = "#FFF8E1"
textColor = "#5C3A21"
font = "serif"
```

**3. Optional: change the model**

To use a different Gemini model, edit `MODEL_NAME` near the top of `app.py`. For example:

```python
MODEL_NAME = "gemini-2.5-flash"
```

</details>

<details>
<summary><b>Running the Application</b></summary>

<br>

```bash
streamlit run app.py
```

Streamlit displays a local address, usually `http://localhost:8501`, and opens it in the default browser. To stop the application, press `Ctrl+C` in the terminal.

To run on a different port:

```bash
streamlit run app.py --server.port 8502
```

</details>

<details>
<summary><b>Usage</b></summary>

<br>

1. Select **Browse files** and upload a JPG, JPEG, or PNG image of food.
2. Confirm the image in the preview panel.
3. Optionally, enter a question, for example "Calculate the calories for this lunch".
4. Select **Calculate Total Calories**.
5. Review the itemised calorie breakdown and total in the Nutrition Report section.

The calorie values are estimates produced by an AI model. They are not medical advice.

</details>

<details>
<summary><b>Output</b></summary>

<br>

**Uploaded image and preview**

The uploaded photo is shown in the preview panel next to the optional question and the calculate button.
<img width="1920" height="1080" alt="Streamlit_2" src="https://github.com/user-attachments/assets/5f6c8028-47fd-4c3e-9ac9-05a5a04e88dc" />



**Nutrition report**

After calculation, the application lists each visible food item with its estimated calories, followed by the total and a note that the values are estimates.


<img width="1920" height="1080" alt="Streamlit_3" src="https://github.com/user-attachments/assets/82771ba2-bf7f-4680-b9a1-0967ac035b27" />


</details>

<details>
<summary><b>Dependencies File</b></summary>

<br>

The `requirements.txt` file should contain only the packages the application imports:

```text
streamlit>=1.40
google-genai>=1.0
python-dotenv>=1.0
pillow>=10.0
```

</details>

<details>
<summary><b>Troubleshooting</b></summary>

<br>

| Problem | Cause and solution |
|---|---|
| `GOOGLE_API_KEY is missing` | The `.env` file is missing or is not in the same folder as `app.py`. Create it there and restart the application. |
| `API key not valid` or HTTP 403 | The key is incorrect or contains extra spaces. Copy the key again from Google AI Studio. |
| HTTP 404 model not found | The model name is no longer available. Change `MODEL_NAME` in `app.py` to a current model. |
| `streamlit: command not found` | The virtual environment is not active. Activate it and run the installation step again. |
| Port already in use | Run the application with a different port, as shown in the Running the Application section. |
| Connection error in the browser | The Streamlit server is not running or the address is wrong. Start it with `streamlit run app.py` and open the address shown in the terminal. |
| Red underlines in the editor | The editor is using a Python interpreter without the packages installed. Select the interpreter inside the `venv` folder. |

</details>

<details>
<summary><b>Project Limitations</b></summary>

<br>

- Calorie estimates depend on how clearly the food is visible in the image. Portion sizes are estimated from the photo.
- The application does not store uploaded images or conversation history.
- The results are informational only and should not replace advice from a qualified healthcare professional or dietitian.

</details>

<details>
<summary><b>Future Improvements</b></summary>

<br>

- Daily calorie tracking with saved history
- Support for macronutrient breakdown (protein, carbohydrates, fat)
- Multiple food images in one request
- Export of the nutrition report as a PDF or CSV file

</details>

---

## License

This project is released under the MIT License. Replace this section with the license you choose.

## Acknowledgements

- [Google Gemini API](https://ai.google.dev/) for multimodal analysis
- [Streamlit](https://streamlit.io/) for the web framework
