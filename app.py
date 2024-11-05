import os
import time
import tempfile
import streamlit as st
from pypdf import PdfReader
import fitz
import base64

def page_setup():
    st.header("Chat with different types of media/files!", anchor=False)

def get_typeofpdf():
    st.sidebar.header("Select type of Media")
    typepdf = st.sidebar.radio("Choose one:", ("PDF files", "Images", "Video, mp4 file", "Audio files"))
    return typepdf

def get_llminfo():
    st.sidebar.header("Options")
    temp = st.sidebar.slider("Temperature:", min_value=0.0, max_value=2.0, value=1.0, step=0.25)
    topp = st.sidebar.slider("Top P:", min_value=0.0, max_value=1.0, value=0.94, step=0.01)
    maxtokens = st.sidebar.slider("Maximum Tokens:", min_value=100, max_value=5000, value=2000, step=100)
    return model_name, temp, topp, maxtokens

def translate_response_to_bangla(model, response_text):
    translation_prompt = f"Translate the following text to Bangla: {response_text}"
    translation = model.generate_content([translation_prompt])
    return translation.text  

def delete_files_in_directory(directory_path):
    try:
        files = os.listdir(directory_path)
        for file in files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    except OSError:
        print("Error occurred while deleting files.")

def setup_documents(pdf_file_path, output_path):
    delete_files_in_directory(output_path)
    doc = fitz.open(pdf_file_path)
    os.chdir(output_path)
    for page in doc: 
        pix = page.get_pixmap(matrix=fitz.Identity, colorspace=fitz.csRGB) 
        pix.save(f"pdfimage-{page.number}.jpg")

def main():
    page_setup()
    typepdf = get_typeofpdf()
    model_name, temperature, top_p, max_tokens = get_llminfo()
    

      
    if typepdf == "PDF files":
        uploaded_files = st.file_uploader("Choose 1 or more PDF", type='pdf', accept_multiple_files=True)
        if uploaded_files:
            text = ""
            for pdf in uploaded_files:
                pdf_data = pdf.read()
                base64_pdf = base64.b64encode(pdf_data).decode("utf-8")
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="500" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
                pdf.seek(0)
                pdf_reader = PdfReader(pdf)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            question = st.text_input("Enter your question and hit return.")
            if question:
                response = model.generate_content([question, text])
                st.write("Response:", response.text)  

                if st.button("Translate Response to Bangla"):
                    translated_text = translate_response_to_bangla(model, response.text)
                    st.write("Translation in Bangla:", translated_text)

    elif typepdf == "Images":
        image_file_name = st.file_uploader("Upload your image file.", type=['jpg', 'jpeg', 'png'])
        if image_file_name:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                temp_file.write(image_file_name.read())
                st.image(image_file_name, caption="Uploaded Image Preview", use_column_width=True)
                temp_path = temp_file.name

            image_file = genai.upload_file(path=temp_path)
            
            while image_file.state.name == "PROCESSING":
                time.sleep(10)
                image_file = genai.get_file(image_file.name)
            
            if image_file.state.name == "FAILED":
                raise ValueError(image_file.state.name)
            
            prompt2 = st.text_input("Enter your prompt.") 
            if prompt2:
                response = model.generate_content([image_file, prompt2], request_options={"timeout": 600})
                st.markdown(response.text)  

                if st.button("Translate Response to Bangla"):
                    translated_text = translate_response_to_bangla(model, response.text)
                    st.write("Translation in Bangla:", translated_text)

            genai.delete_file(image_file.name)

    elif typepdf == "Video, mp4 file":
        video_file_name = st.file_uploader("Upload your video", type=['mp4'])
        if video_file_name:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                temp_file.write(video_file_name.read())
                st.video(video_file_name, format="video/mp4")
                temp_path = temp_file.name

            video_file = genai.upload_file(path=temp_path)
            
            while video_file.state.name == "PROCESSING":
                time.sleep(10)
                video_file = genai.get_file(video_file.name)
            
            if video_file.state.name == "FAILED":
                raise ValueError(video_file.state.name)
            
            prompt3 = st.text_input("Enter your prompt.") 
            if prompt3:
                response = model.generate_content([video_file, prompt3], request_options={"timeout": 600})
                st.markdown(response.text)  

                if st.button("Translate Response to Bangla"):
                    translated_text = translate_response_to_bangla(model, response.text)
                    st.write("Translation in Bangla:", translated_text)

            genai.delete_file(video_file.name)

    elif typepdf == "Audio files":
        audio_file_name = st.file_uploader("Upload your audio", type=['wav', 'mp3'])
        if audio_file_name:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_file.write(audio_file_name.read())
                st.audio(audio_file_name, format="audio/wav")
                temp_path = temp_file.name

            audio_file = genai.upload_file(path=temp_path)

            while audio_file.state.name == "PROCESSING":
                time.sleep(10)
                audio_file = genai.get_file(audio_file.name)
            
            if audio_file.state.name == "FAILED":
                raise ValueError(audio_file.state.name)
            
            prompt4 = st.text_input("Enter your prompt.") 
            if prompt4:
                response = model.generate_content([audio_file, prompt4], request_options={"timeout": 600})
                st.markdown(response.text)  

                if st.button("Translate Response to Bangla"):
                    translated_text = translate_response_to_bangla(model, response.text)
                    st.write("Translation in Bangla:", translated_text)

            genai.delete_file(audio_file.name)

if __name__ == '__main__':
    GOOGLE_API_KEY = ""
    genai.configure(api_key=GOOGLE_API_KEY)
    main()

