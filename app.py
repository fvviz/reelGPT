import streamlit as st
import subprocess

def run_main_py(LINK, model):
    cmd = f"python main.py {LINK} --model {model}"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode == 0:
        st.success("Process completed successfully.")
    else:
        st.error(f"An error occurred: {err.decode()}")

def display_video(video_path):
    video_file = open(video_path, 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

def main():
    st.title("Reels-GPT")

    LINK = st.text_input("Enter YouTube video link")
    model = st.selectbox("Select Model", ("tiny", "small", "base", "large"))

    if st.button("Process Video"):
        run_main_py(LINK, model)
        video_path = "final_output.mp4"
        st.subheader("Processed Video")
        display_video(video_path)

if __name__ == "__main__":
    main()
