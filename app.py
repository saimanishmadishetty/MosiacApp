import streamlit as st
from PIL import Image
import numpy as np
import io
import base64
from vipas import model
from vipas.exceptions import UnauthorizedException, NotFoundException

def predict_image(input_data):
    model_id = "mdl-cqta6o82a6n8u"
    vps_model_client = model.ModelClient()
    response = vps_model_client.predict(model_id=model_id, input_data=input_data)
    return response

# Set the title and description with new font style
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        html, body, [class*="css"] {
            font-family: 'Roboto', sans-serif;
        }
        .title {
            font-size: 2.5rem;
            color: #4CAF50;
            text-align: center;
        }
        .description {
            font-size: 1.25rem;
            color: #555;
            text-align: center;
            margin-bottom: 2rem;
        }
        .uploaded-image {
            border: 2px solid #4CAF50;
            border-radius: 8px;
        }
        .prediction-container {
            text-align: center;
            margin-top: 20px;
        }
        .prediction-title {
            font-size: 24px;
            color: #333;
        }
        .prediction-class {
            font-size: 20px;
            color: #4CAF50;
        }
        .confidence {
            font-size: 20px;
            color: #FF5733;
        }
        .stButton button {
            display: block;
            margin-left: auto;
            margin-right: auto;
            background-color: #4CAF50;
            color: white;
            padding: 10px 24px;
            font-size: 16px;
            cursor: pointer;
            border: none;
            border-radius: 8px;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Mosaic Art Generator App</div>', unsafe_allow_html=True)
st.markdown('<div class="description">Upload an image and let the model process it into a mosaic style. This model can transform your images into beautiful mosaics.</div>', unsafe_allow_html=True)

# Upload image file
uploaded_file = st.file_uploader("Choose an image...", type="jpg")
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    if st.button('Convert Image'):
        try:
            prediction_output = predict_image(img_str)
            output_base64 = prediction_output
            output_image_data = base64.b64decode(output_base64)
            result_image = Image.open(io.BytesIO(output_image_data))
            
            # Resize the result image to match the dimensions of the input image
            result_image = result_image.resize(image.size)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(image, caption='Uploaded Image', use_column_width=True)
            
            with col2:
                st.image(result_image, caption='Processed Image', use_column_width=True)
                
        except UnauthorizedException as e:
            st.error("Unauthorized exception: " + str(e))
        except NotFoundException as e:
            st.error("Not found exception: " + str(e))
        except Exception as e:
            st.error("Exception when calling model->predict: %s\n" % e)

# Add some styling with Streamlit's Markdown
st.markdown("""
    <style>
        .stApp {
            background-color: #f5f5f5;
            padding: 0;
        }
        .stApp > header {
            position: fixed;
            top: 0;
            width: 100%;
            z-index: 1;
            background: #ffffff;
            border-bottom: 1px solid #e0e0e0;
        }
        .stApp > main {
            margin-top: 4rem;
            padding: 2rem;
        }
        pre {
            background: #e0f7fa;
            padding: 15px;
            border-radius: 8px;
            white-space: pre-wrap;
            word-wrap: break-word;
            border: 1px solid #4CAF50;
        }
        .css-1cpxqw2.e1ewe7hr3 {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)
