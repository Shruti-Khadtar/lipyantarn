# lipyantarn
A **Streamlit app** to convert **Marathi text ↔ shorthand images**. 
An interactive Marathi shorthand converter that translates between text and handwritten shorthand using phrase matching and image recognition.


---

## Features

- **Text → Shorthand:** Convert Marathi sentences into shorthand symbols.  
- **Shorthand → Text:** Upload shorthand images to get Marathi text.  
- Supports punctuation symbols: `. ? ! - ( )`  
- Visualizes shorthand symbols side by side.  

---

## Quick Start

1. **Clone & install:**
```bash
git clone https://github.com/Shruti-Khadtar/lipyantarn.git
cd marathi-shorthand-app
pip install -r requirements.txt
```
2.	**Run the app:**
```streamlit run app.py```

3.	**Update dataset path in app.py:**
```image_folder_path = "/path/to/ALL_IMAGES" ```
________________________________________

## Dataset
The dataset used in this project is available here:  
🔗 Google Drive: [View Dataset](https://drive.google.com/drive/folders/142zvE4nC_RLLcB3Ci7UF7QymODiAvpOf?usp=drive_link)

> Note: The dataset is hosted on Google Drive due to size limitations.

-	Shorthand images folder (ALL_IMAGES/) is required.
-	Image naming: words or symbols they represent (e.g., dot.jpg, अंदाजपत्रक.jpg)
________________________________________
## Folder Structure
```
marathi-shorthand-app/
│
├─ app.py
├─ requirements.txt
├─ ALL_IMAGES/       # Dataset folder
└─ README.md
```
________________________________________

License
MIT © Shruti Khadtar

GitHub: https://github.com/Shruti-Khadtar
