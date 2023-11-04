import streamlit as st
import subprocess
import time

def run_main_py(LINK, model):
    cmd = ["python", "main.py", LINK, model]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()  # Wait for the process to finish

def display_video(video_path):
    video_file = open(video_path, 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

def main():
    st.title("Reels-GPT")

    LINK = st.text_input("Enter YouTube video link")
    model = st.selectbox("Select Model", ("tiny", "small", "base", "large"))
    process_button = st.button("Process Video")

    if process_button:
        process_button.text("Processing...")
        process_button.disabled = True

        with st.spinner("Processing..."):
            start_time = time.time()

            run_main_py(LINK, model)
            video_path = "out/final_output.mp4"
            st.subheader("Processed Video")
            display_video(video_path)

            end_time = time.time()
            st.text(f"Process completed in {round(end_time - start_time, 2)} seconds")

if __name__ == "__main__":
    main()
