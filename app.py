import streamlit as st
import subprocess
import time

def run_main_py(LINK, model):
    cmd = ["python", "main.py", LINK, model]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while process.poll() is None:
        st.text("Processing...")
        time.sleep(0.1)  # Adjust this delay as needed
    if process.returncode == 0:
        st.text("Process completed successfully.")
    else:
        st.text(f"An error occurred.")

def display_video(video_path):
    video_file = open(video_path, 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

def main():
    st.title("Reels-GPT")

    LINK = st.text_input("Enter YouTube video link")
    model = st.selectbox("Select Model", ("tiny", "small", "base", "large"))

    if st.button("Process Video"):
        with st.spinner("Processing..."):
            progress_bar = st.progress(0)
            start_time = time.time()

            run_main_py(LINK, model)
            video_path = "out/final_output.mp4"
            st.subheader("Processed Video")
            display_video(video_path)

            progress_bar.progress(100)
            end_time = time.time()
            st.text(f"Process completed in {round(end_time - start_time, 2)} seconds")

if __name__ == "__main__":
    main()
