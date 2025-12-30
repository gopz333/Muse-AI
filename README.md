 🪄 Muse.AI – Your AI Creative Writing Companion 
Muse.AI is a personal project I created using Python, Streamlit, and Google’s Gemma 2B model (via LM Studio). 
It takes the first few lines of a poem or essay, understands your tone, and continues it in your style — like a personal muse that co-writes with you. 🎨 

💡 What Muse.AI Can Do 
* Continue your poems or essays in your chosen tone 
* Generate a short, creative title automatically ✨ 
* Adjust creativity with a simple slider 
* Save each piece separately (Poems & Essays folders) 
* View your past creations right inside the app 

⚙️ Tech Stack 
* Python 
* Streamlit (for UI) 
* Gemma 2B (Local LLM via LM Studio) 
* REST API integration (requests + JSON) 
 
 🚀 How To Run 
 1️⃣ Install Requirements 
```bash 
pip install -r requirements.txt

2️⃣ Start Your Model in LM Studio
•	Load model: codegood/gemma-2b-it-Q4_K_M-GGUF
•	Start the local server
•	Note your endpoint (e.g. http://192.168.x.x:1234)

3️⃣ Launch Muse.AI
python -m streamlit run muse_gemma2b.py

📁 Folder Structure

Muse.AI/
 ├── muse_gemma2b.py
 ├── requirements.txt
 ├── README.md
 ├── .gitignore
 └── MuseCreations/
      ├── Poems/
      │    ├── Whispers_of_the_Moon_2025-12-29_19-45-31.txt
      └── Essays/
           ├── The_Future_of_AI_2025-12-29_20-10-22.txt

🌟 Example Output

Input:
The ocean hums a lullaby beneath the silver moon,

Muse.AI’s Continuation:
Each wave carries secrets untold,
Whispered softly into the heart of dawn.

Generated Title: Whispers of the Moon 🌙


