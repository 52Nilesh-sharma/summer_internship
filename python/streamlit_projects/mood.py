import streamlit as st
from streamlit_player import st_player

# Mood-based music data
music_data = {
    "Happy": {
        "image": "https://images.unsplash.com/photo-1443916568596-df5a58c445e9?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjF8fGhhcHB5fGVufDB8fDB8fHww",
        "songs": [
            {"title": "Jhoome Jo Pathaan", "url": "https://www.youtube.com/watch?v=ZbZSe6N_BXs", "thumbnail": "https://i.ytimg.com/vi/ZbZSe6N_BXs/hqdefault.jpg"},
            {"title": "Kala Chashma", "url": "https://www.youtube.com/watch?v=KQ6zr6kCPj8", "thumbnail": "https://i.ytimg.com/vi/KQ6zr6kCPj8/hqdefault.jpg"},
            {"title": "Leja Re", "url": "https://www.youtube.com/watch?v=ru0K8uYEZWw", "thumbnail": "https://i.ytimg.com/vi/ru0K8uYEZWw/hqdefault.jpg"}
        ]
    },
    "Sad": {
        "image": "https://images.unsplash.com/photo-1503264116251-35a269479413",
        "songs": [
            {"title": "Phir Bhi Tumko Chaahunga", "url": "https://www.youtube.com/watch?v=ru0K8uYEZWw", "thumbnail": "https://i.ytimg.com/vi/ru0K8uYEZWw/hqdefault.jpg"},
            {"title": "Tum Hi Aana", "url": "https://www.youtube.com/watch?v=ru0K8uYEZWw", "thumbnail": "https://i.ytimg.com/vi/ru0K8uYEZWw/hqdefault.jpg"},
            {"title": "Dil Diyan Gallan", "url": "https://www.youtube.com/watch?v=ru0K8uYEZWw", "thumbnail": "https://i.ytimg.com/vi/ru0K8uYEZWw/hqdefault.jpg"}
        ]
    },
    "Party": {
        "image": "https://images.unsplash.com/photo-1515169067865-5387ec356754",
        "songs": [
            {"title": "Badshah – Genda Phool", "url": "https://www.youtube.com/watch?v=HMqgVXSvwGo", "thumbnail": "https://i.ytimg.com/vi/HMqgVXSvwGo/hqdefault.jpg"},
            {"title": "Galti Se Mistake", "url": "https://www.youtube.com/watch?v=KQ6zr6kCPj8", "thumbnail": "https://i.ytimg.com/vi/KQ6zr6kCPj8/hqdefault.jpg"},
            {"title": "Nashe Si Chadh Gayi", "url": "https://www.youtube.com/watch?v=ru0K8uYEZWw", "thumbnail": "https://i.ytimg.com/vi/ru0K8uYEZWw/hqdefault.jpg"}
        ]
    }
}

# App config
st.set_page_config(page_title="🎵 Indian Mood Music", layout="wide")

# CSS Styling
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #ff9a9e, #fad0c4, #fad0c4);
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3 {
    color: #fff;
}
.stApp {
    background: linear-gradient(120deg, #f6d365 0%, #fda085 100%);
}
.song-card {
    background-color: rgba(255, 255, 255, 0.85);
    border-radius: 12px;
    padding: 10px;
    margin: 10px 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
.center-thumb {
    display: flex;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

# App title
st.markdown("<h1 style='text-align: center;'>🎧 Indian Mood Music Recommender</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Feel your mood. Hear the vibe. 🎶</h3>", unsafe_allow_html=True)
st.markdown("---")

# Mood selection
mood = st.selectbox("🎭 Choose your mood:", list(music_data.keys()))

# Display mood image (reduced size)
st.image(music_data[mood]["image"], width=500, caption=f"{mood} Mood Vibes 🌈")

# Song list with centered, larger thumbnails
st.markdown(f"### 🎼 Songs for your {mood} mood:")
for song in music_data[mood]["songs"]:
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            with st.container():
                st.markdown('<div class="center-thumb">', unsafe_allow_html=True)
                st.image(song["thumbnail"], width=200)
                st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f"#### {song['title']}")
            st_player(song["url"], height=80)
