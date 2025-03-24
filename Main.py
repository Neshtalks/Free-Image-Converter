import streamlit as st
from PIL import Image
from io import BytesIO
import zipfile

def convert_img_format(image_bytes, output_format, quality=95):
    """Convert image to specified format with quality setting"""
    img = Image.open(BytesIO(image_bytes))
    buf = BytesIO()
    img.save(buf, format=output_format, quality=quality)
    buf.seek(0)
    return buf

# Initialize session state
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'zip_buffer' not in st.session_state:
    st.session_state.zip_buffer = None
if 'clear_flag' not in st.session_state:
    st.session_state.clear_flag = False

# App title and description
st.title("🖼️ Image Converter")
st.write("Convert multiple images in one click! 🚀")

# Handle clearing files
if st.session_state.clear_flag:
    st.session_state.uploaded_files = []
    st.session_state.zip_buffer = None
    st.session_state.clear_flag = False
    st.rerun()

# File uploader with dynamic key
uploader_key = "uploader_" + str(len(st.session_state.uploaded_files))
uploaded_files = st.file_uploader(
    "📂 Upload Images",
    type=["png", "jpg", "jpeg", "bmp", "webp"],
    accept_multiple_files=True,
    key=uploader_key
)

# Update session state
if uploaded_files and uploaded_files != st.session_state.uploaded_files:
    st.session_state.uploaded_files = uploaded_files

# Conversion options
output_format = st.selectbox("🎨 Output format", ["PNG", "JPEG", "BMP", "WEBP"])
quality = st.slider("🛠️ Quality (1-100)", 1, 100, 95, disabled=output_format=="BMP")

# Main conversion button with spinner
if st.session_state.uploaded_files and st.button("✨ Convert & Download"):
    with st.spinner('Converting images...'):
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for uploaded_file in st.session_state.uploaded_files:
                try:
                    converted = convert_img_format(
                        uploaded_file.getvalue(),
                        output_format.lower(),
                        quality
                    )
                    new_name = f"{uploaded_file.name.split('.')[0]}.{output_format.lower()}"
                    zipf.writestr(new_name, converted.getvalue())
                except Exception as e:
                    st.error(f"Error converting {uploaded_file.name}: {str(e)}")
        
        st.session_state.zip_buffer = zip_buffer
        st.success("Conversion complete! Click below to download.")

# Download button
if st.session_state.zip_buffer:
    st.download_button(
        "💾 Download All",
        data=st.session_state.zip_buffer,
        file_name="converted_images.zip",
        mime="application/zip"
    )

# Clear button - now working perfectly
if st.button("🗑️ Clear All Files"):
    st.session_state.clear_flag = True
    st.rerun()

if not st.session_state.uploaded_files:
    st.info("📤 Please upload images to convert")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by nesh")