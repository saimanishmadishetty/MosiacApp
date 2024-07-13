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

st.title('Mosaic Image Processing App')

uploaded_file = st.file_uploader("Choose an image...", type="jpg")
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    if st.button('Process Image'):
        try:
            prediction_output = predict_image(img_str)
            output_base64 = prediction_output
            output_image_data = base64.b64decode(output_base64)
            result_image = Image.open(io.BytesIO(output_image_data))
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
        .stTitle, .stMarkdown, .stButton, .stImage {
            text-align: center;
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 24px;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border: none;
            border-radius: 8px;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        .stImage > img {
            border: 2px solid #4CAF50;
            border-radius: 8px;
        }
        .css-1cpxqw2.e1ewe7hr3 {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)
