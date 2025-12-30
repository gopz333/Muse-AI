import streamlit as st
import requests
import json
import os
from datetime import datetime

# --- App Title ---
st.title("Muse AI🪄 ")

# --- User Interface ---
mode = st.radio("Choose your Muse:", ["Poem", "Essay"])
user_input = st.text_area("Write the beginning of your piece:")

# --- Creativity Slider ---
temperature = st.slider("Creativity Level 🎨", 0.3, 1.3, 0.8)

# --- When Button Clicked ---
if st.button("Continue Writing"):
    if not user_input.strip():
        st.warning("Please write something first!")
    else:
        # --- Build Prompt for Main Content ---
        if mode == "Poem":
            prompt = f"Continue this poem creatively and emotionally:\n{user_input}\n"
        else:
            prompt = f"Continue this essay in a formal and coherent way:\n{user_input}\n"

        # --- Prepare payload for Gemma 2B ---
        payload = {
            "model": "gemma-2b",
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": 200
        }

        try:
            # --- Send request to Gemma 2B ---
            response = requests.post(
                "http://192.168.27.163:1234/v1/completions",  # Your Gemma 2B endpoint
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload)
            )

            if response.status_code == 200:
                result = response.json()
                completion = result["choices"][0]["text"].strip()

                # --- Generate a Title for the Output ---
                title_prompt = f"Give a short and meaningful title for this {mode.lower()}:\n{user_input}\n{completion}\nTitle:"
                title_payload = {
                    "model": "gemma-2b",
                    "prompt": title_prompt,
                    "temperature": 0.7,
                    "max_tokens": 20
                }

                title_response = requests.post(
                    "http://192.168.27.163:1234/v1/completions",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(title_payload)
                )

                if title_response.status_code == 200:
                    title_result = title_response.json()
                    ai_title = title_result["choices"][0]["text"].strip().replace("\n", "")
                else:
                    ai_title = "Untitled Creation"

                # --- Display the Title and AI Continuation ---
                st.subheader(f"✨ Title: {ai_title}")
                st.write(completion)

                # --- Create Folder Structure ---
                base_folder = "MuseGemmaCreations"
                os.makedirs(base_folder, exist_ok=True)

                sub_folder = os.path.join(base_folder, f"{mode}s")  # Poems or Essays
                os.makedirs(sub_folder, exist_ok=True)

                # --- Clean title for file naming ---
                safe_title = "".join(c for c in ai_title if c.isalnum() or c in (" ", "-", "_")).rstrip()
                if not safe_title:
                    safe_title = "Untitled"

                # --- File name with timestamp ---
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"{safe_title}_{timestamp}.txt"
                file_path = os.path.join(sub_folder, filename)

                # --- Save Everything to File ---
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"--- MuseGemma Creation ---\n")
                    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Mode: {mode}\n")
                    f.write(f"Title: {ai_title}\n\n")
                    f.write("🖋️ User Input:\n")
                    f.write(user_input.strip() + "\n\n")
                    f.write("✨ AI Continuation:\n")
                    f.write(completion.strip() + "\n")

                st.success(f"Saved as '{filename}' ✅")
                st.info(f"File location: {file_path}")

            else:
                st.error(f"Error {response.status_code}: {response.text}")

        except Exception as e:
            st.error(f"Connection error: {e}")

# --- View Saved Creations ---
if st.button("📖 View My Creations"):
    base_folder = "MuseGemmaCreations"
    if not os.path.exists(base_folder):
        st.info("No saved creations yet. Generate one to start!")
    else:
        all_files = []
        for folder in ["Poems", "Essays"]:
            sub_path = os.path.join(base_folder, folder)
            if os.path.exists(sub_path):
                files = [f"{folder}/{file}" for file in os.listdir(sub_path)]
                all_files.extend(files)

        if not all_files:
            st.info("No saved creations yet. Generate one to start!")
        else:
            selected_file = st.selectbox("Select a creation to view:", all_files)
            folder_name, file_name = selected_file.split("/")
            file_path = os.path.join(base_folder, folder_name, file_name)

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                st.text_area("🖋️ Your Creation:", content, height=300)
