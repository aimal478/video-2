import streamlit as st
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
import tempfile
import os

st.title("🎬 Video Editor with Animation and Music")

# Upload video file
video_file = st.file_uploader("Upload your video (.mp4)", type=["mp4"])
audio_file = st.file_uploader("Optional: Upload background music (.mp3)", type=["mp3"])

text = st.text_input("Enter animated text:", "Hello from Streamlit!")
text_size = st.slider("Text size", 20, 100, 60)
text_color = st.color_picker("Pick text color", "#ffffff")

if video_file:
    # Save video to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_vid:
        tmp_vid.write(video_file.read())
        video_path = tmp_vid.name

    # Load video
    clip = VideoFileClip(video_path)
    
    # Create animated text
    animated_text = (TextClip(text, fontsize=text_size, color=text_color.replace("#", ""))
                     .set_position(lambda t: (t * 100 % clip.w, 50))  # moving text
                     .set_duration(clip.duration))

    # Combine video and text
    final_clip = CompositeVideoClip([clip, animated_text])

    # Add audio if provided
    if audio_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
            tmp_audio.write(audio_file.read())
            audio_path = tmp_audio.name

        audio = AudioFileClip(audio_path).subclip(0, clip.duration)
        final_clip = final_clip.set_audio(audio)

    # Export edited video
    output_path = os.path.join(tempfile.gettempdir(), "edited_video.mp4")
    final_clip.write_videofile(output_path, fps=24)

    # Download link
    with open(output_path, "rb") as f:
        st.success("✅ Done! Download your edited video below:")
        st.download_button("Download Edited Video", f, file_name="edited_video.mp4")

