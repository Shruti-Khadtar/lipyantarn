import streamlit as st
from PIL import Image
import imagehash
import os
import matplotlib.pyplot as plt


# ========== CONFIG ==========
# Update this to your shorthand images folder
image_folder_path = 'C:/Users/admin/Desktop/MyProjects/Lipyantar/Steno/ALL_IMAGES'

# ========== UTILITY FUNCTIONS ==========

def fetch_all_files_from_drive(drive_path, file_extensions=(".jpg", ".png")):
    files_list = []
    for root, dirs, files in os.walk(drive_path):
        for file in files:
            if file.endswith(file_extensions):
                files_list.append(os.path.join(root, file))
    return files_list

def display_images_side_by_side(images):
    num_images = len(images)
    fig, axes = plt.subplots(1, num_images, figsize=(2 * num_images, 2))
    if num_images == 1:
        axes = [axes]
    for ax, image_path in zip(axes, images):
        image = Image.open(image_path)
        ax.imshow(image)
        ax.axis('off')
    st.pyplot(fig)

def find_similar_image(input_image, image_files):
    try:
        input_hash = imagehash.average_hash(input_image)
        for image_path in image_files:
            try:
                current_image = Image.open(image_path)
                current_hash = imagehash.average_hash(current_image)
                if input_hash - current_hash < 5:  # similarity threshold
                    return image_path
            except Exception as e:
                print(f"Error comparing image {image_path}: {e}")
    except Exception as e:
        print(f"Error processing input image: {e}")
    return None

# ========== MAIN APP ==========

st.set_page_config(page_title="Marathi Shorthand App", layout="centered")
st.title("लिप्यंतर")

mode = st.radio("Select Mode", ["Text to Shorthand", "Shorthand to Text"], horizontal=True)

image_files = fetch_all_files_from_drive(image_folder_path)

# ========== MODE 1 ==========
# Symbol to image name mapping
SYMBOL_MAPPING = {
    '.': 'dot',
    '?': 'question_mark',
    '!': 'exclamation',
    '-': 'dash',
    '(': 'left_paren',
    ')': 'right_paren'
}

if mode == "Text to Shorthand":
    st.subheader("📝 Text ➜ Shorthand")

    marathi_input = st.text_area("Enter Marathi sentence:", height=100)
    if marathi_input:
        matched_output = []
        cleaned_input = marathi_input.strip()

        # Get actual image base names (without extension)
        image_name_list = sorted(
            [os.path.splitext(os.path.basename(path))[0] for path in image_files],
            key=lambda x: -len(x)  # longer phrases first
        )

        remaining_text = cleaned_input

        while remaining_text:
            match_found = False

            # Check for symbol at start
            if remaining_text[0] in SYMBOL_MAPPING:
                symbol_name = SYMBOL_MAPPING[remaining_text[0]]
                matched_output.append((remaining_text[0], symbol_name))
                remaining_text = remaining_text[1:].strip()
                continue

            # Match phrases or words
            for phrase in image_name_list:
                if remaining_text.startswith(phrase):
                    matched_output.append((phrase, phrase))
                    remaining_text = remaining_text[len(phrase):].strip()
                    match_found = True
                    break

            if not match_found:
                # fallback to first word
                parts = remaining_text.split(maxsplit=1)
                word = parts[0]
                matched_output.append((word, word))
                remaining_text = parts[1] if len(parts) > 1 else ""
                remaining_text = remaining_text.strip()

        # Display matched phrases/words and their shorthand images
        for label, key in matched_output:
            st.markdown(f"**{label}**")
            matched_image = None

            for path in image_files:
                name = os.path.splitext(os.path.basename(path))[0]
                if name == key:
                    matched_image = path
                    break

            if matched_image:
                st.image(matched_image, width=150)
            else:
                st.warning(f"No image found for '{label}'")



# ========== MODE 2 ==========
elif mode == "Shorthand to Text":
    st.subheader("🖼️ Shorthand ➜ Text")

    uploaded_files = st.file_uploader("Upload shorthand image(s):", type=["jpg", "png"], accept_multiple_files=True)

    if uploaded_files:
        matched_paths = []
        decoded_texts = []

        for uploaded_file in uploaded_files:
            input_image = Image.open(uploaded_file)
            similar_image_path = find_similar_image(input_image, image_files)

            if similar_image_path:
                matched_paths.append(similar_image_path)
                decoded_texts.append(os.path.splitext(os.path.basename(similar_image_path))[0])
            else:
                st.warning(f"No match found for {uploaded_file.name}")

        if matched_paths:
            st.success("Matched Image(s):")
            display_images_side_by_side(matched_paths)

        if decoded_texts:
            st.info("Output Marathi Text:")
            st.markdown('"' + " ".join(decoded_texts) + '"')
