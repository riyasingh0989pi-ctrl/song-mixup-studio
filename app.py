import io
import streamlit as st
from pydub import AudioSegment

st.set_page_config(
    page_title="Song Mixup Studio",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 Song Mixup Studio")
st.write("Do tracks upload karein aur unka smooth mashup banayein.")

# File uploaders
col1, col2 = st.columns(2)

with col1:
    song_file_1 = st.file_uploader(
        "🎵 Pehla Track (MP3/WAV)",
        type=["mp3", "wav"]
    )

with col2:
    song_file_2 = st.file_uploader(
        "🎵 Dusra Track (MP3/WAV)",
        type=["mp3", "wav"]
    )

# Mix settings
st.subheader("🎚️ Mix Settings")

crossfade_sec = st.slider(
    "Crossfade Duration (seconds)",
    min_value=1,
    max_value=10,
    value=4
)

cut_duration = st.slider(
    "Har song ka duration mix me (seconds)",
    min_value=10,
    max_value=120,
    value=30
)

if song_file_1 and song_file_2:

    if st.button("🎧 Mix Songs"):

        with st.spinner("Audio process aur mix ho raha hai..."):

            try:
                # Load tracks
                track1 = AudioSegment.from_file(song_file_1)
                track2 = AudioSegment.from_file(song_file_2)

                duration_ms = cut_duration * 1000
                fade_ms = crossfade_sec * 1000

                # Trim tracks
                segment1 = track1[:duration_ms]
                segment2 = track2[:duration_ms]

                # Normalize volume safely
                if segment1.max_dBFS != float("-inf"):
                    segment1 = segment1.apply_gain(-segment1.max_dBFS)

                if segment2.max_dBFS != float("-inf"):
                    segment2 = segment2.apply_gain(-segment2.max_dBFS)

                # Make sure crossfade isn't longer than songs
                fade_ms = min(
                    fade_ms,
                    len(segment1),
                    len(segment2)
                )

                # Create mashup
                mixed_track = segment1.append(
                    segment2,
                    crossfade=fade_ms
                )

                # Export MP3
                output_buffer = io.BytesIO()

                mixed_track.export(
                    output_buffer,
                    format="mp3",
                    bitrate="192k"
                )

                mixed_audio_bytes = output_buffer.getvalue()

                st.success("🎉 Mixup ready hai!")

                st.audio(
                    mixed_audio_bytes,
                    format="audio/mp3"
                )

                st.download_button(
                    label="⬇️ Download Mashup (MP3)",
                    data=mixed_audio_bytes,
                    file_name="mashup_mix.mp3",
                    mime="audio/mp3"
                )

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

else:
    st.info("👆 Dono songs upload karke mashup banayein!")
