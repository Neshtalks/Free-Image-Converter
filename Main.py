import streamlit as st
from PIL import Image
from io import BytesIO
import zipfile

# Custom function to convert image format with high quality
def convert_img_format(image_bytes, output_format, quality=95):
    """
    Converts an image from its original format to the specified output format with high quality.
    
    Args:
        image_bytes (bytes): The image file as bytes.
        output_format (str): The desired output format (e.g., "png", "jpeg").
        quality (int): The quality of the output image (1-100).
    
    Returns:
        BytesIO: The converted image as bytes.
    """
    img = Image.open(BytesIO(image_bytes))
    buf = BytesIO()
    img.save(buf, format=output_format, quality=quality)
    buf.seek(0)
    return buf

# Define CSS styles for light and dark themes
light_theme = """
<style>
.stApp {
    background-color: white;
    color: black;
}
</style>
"""

dark_theme = """
<style>
.stApp {
    background-color: black;
    color: white;
}
</style>
"""

# Initialize session state if it doesn't exist
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# Function to toggle the theme based on the session state
def toggle_theme():
    if st.session_state.theme == "light":
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "light"

# Custom CSS for the floating theme toggle button in the top-right corner
st.markdown(
    """
    <style>
    .theme-toggle {
        position: fixed;
        top: 15px;
        right: 20px;
        z-index: 9999;
        background: rgba(0, 0, 0, 0.7);
        color: white;
        padding: 8px 12px;
        border-radius: 20px;
        cursor: pointer;
        font-size: 18px;
        display: flex;
        align-items: center;
        font-weight: bold;
        transition: background 0.3s ease-in-out;
    }
    .theme-toggle:hover {
        background: rgba(0, 0, 0, 0.9);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create a toggle button in the top-right corner
icon = "🌙" if st.session_state.theme == "light" else "🌞"
if st.button(icon, key="toggle_theme"):
    toggle_theme()

# Apply the selected theme
if st.session_state.theme == "dark":
    st.markdown(dark_theme, unsafe_allow_html=True)
else:
    st.markdown(light_theme, unsafe_allow_html=True)

# Setting up the webpage structure
st.title("🖼️ Image Convertor")
st.write("Convert all your images in one click! 🚀")

# About section
st.markdown(
    """
    <div class="about-section">
        <h2>About This Tool</h2>
        <p>
            This free image conversion tool allows you to quickly and easily convert images to various formats, 
            including PNG, JPEG, BMP, WebP, and more. Whether you're a designer, developer, or just someone 
            who needs to convert images, this tool is designed to be simple, fast, and hassle-free. 
            No sign-ups, no ads, just free image conversion!
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# File uploader for multiple files
uploaded_files = st.file_uploader(
    "📂 Upload Images",
    type=["png", "jpg", "jpeg", "jfif", "bmp", "webp", "avif"],
    accept_multiple_files=True
)

# Store uploaded files in session state
if uploaded_files:
    st.session_state.uploaded_files = uploaded_files

# Output format selection
format_options = ["PNG", "JPEG", "JFIF", "BMP", "WEBP", "AVIF"]
output_format = st.selectbox("🎨 Choose the output format", format_options)

# Quality slider for output images
quality = st.slider("🛠️ Set output quality (1-100)", min_value=1, max_value=100, value=95)

# If there are uploaded files, start the conversion process
if st.session_state.uploaded_files:
    if st.button("✨ Convert and Download All 📸"):
        # Create a ZIP file to store all converted images
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for uploaded_file in st.session_state.uploaded_files:
                try:
                    # Convert the image with the specified quality
                    uploaded_file_bytes = uploaded_file.getvalue()
                    converted_img = convert_img_format(uploaded_file_bytes, output_format.lower(), quality)
                    
                    # Add the converted image to the ZIP file
                    file_name = f"{uploaded_file.name.split('.')[0]}.{output_format.lower()}"
                    zip_file.writestr(file_name, converted_img.getvalue())
                except Exception as e:
                    st.error(f"❌ Error processing {uploaded_file.name}: {e}")

        # Provide the ZIP file for download
        zip_buffer.seek(0)
        st.download_button(
            label="📥 Download All Converted Images",
            data=zip_buffer,
            file_name=f"converted_images.zip",
            mime="application/zip"
        )

        # Clear the uploaded files from session state after download
        st.session_state.uploaded_files = []

else:
    st.write("📤 Please upload one or more images to convert.")

# Footer
st.markdown(
    """
    <div class="footer">
        <p>Made with ❤️ by Your Nesh</p>
    </div>
    """,
    unsafe_allow_html=True
)
