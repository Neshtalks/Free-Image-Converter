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

# Custom CSS for a modern color scheme and layout
st.markdown(
    """
    <style>
    /* Background and overall theme */
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
        font-family: 'Arial', sans-serif;
    }
    /* Title styling */
    h1 {
        color: #ffffff;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 20px;
    }
    /* File uploader styling */
    .stFileUploader > div {
        background-color: #2d2d2d;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    /* Button styling */
    .stButton > button {
        background-color: #4CAF50;
        color: #ffffff;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 1rem;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    /* About section styling */
    .about-section {
        background-color: #2d2d2d;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .about-section h2 {
        color: #ffffff;
        font-size: 1.5rem;
        margin-bottom: 10px;
    }
    .about-section p {
        color: #cccccc;
        font-size: 1rem;
        line-height: 1.5;
    }
    /* Footer styling */
    .footer {
        text-align: center;
        margin-top: 40px;
        color: #777777;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add Font Awesome for icons
st.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">',
    unsafe_allow_html=True
)

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

# Output format selection
format_options = ["PNG", "JPEG", "JFIF", "BMP", "WEBP", "AVIF"]
output_format = st.selectbox("🎨 Choose the output format", format_options)

# Quality slider for output images
quality = st.slider("🛠️ Set output quality (1-100)", min_value=1, max_value=100, value=95)

if uploaded_files:
    if st.button("✨ Convert and Download All 📸"):
        # Create a ZIP file to store all converted images
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for uploaded_file in uploaded_files:
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
