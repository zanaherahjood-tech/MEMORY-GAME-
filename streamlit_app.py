import streamlit as st
import random
import string
import time

# إعداد الصفحة
st.set_page_config(page_title="لعبة اختبار الذاكرة 🧠", layout="centered")

# ثيم برتقالي/أسود/أبيض
st.markdown("""
    <style>
        .main {
            background-color: #fff;
        }
        div.stButton > button {
            background-color: orange;
            color: black;
            font-size: 20px;
            height: 3em;
            width: 100%;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# مؤثرات صوتية
def play_sound(sound_url):
    st.audio(sound_url)

exciting_sound = "https://www.soundjay.com/buttons/sounds/button-16.mp3"
tense_sound = "https://www.soundjay.com/misc/sounds/bell-ringing-01.mp3"

# بدء اللعبة
if "level" not in st.session_state:
    st.session_state.level = 1
    st.session_state.attempts = 5
    st.session_state.stage = "start"
    st.session_state.sequence = ""
    st.session_state.user_input = ""

# إعادة تعيين اللعبة
def reset_game():
    st.session_state.level = 1
    st.session_state.attempts = 5
    st.session_state.stage = "start"
    st.session_state.sequence = ""
    st.session_state.user_input = ""

# توليد تسلسل
def generate_sequence(length):
    return ''.join(random.choices(string.ascii_uppercase, k=length))

# ====== شاشة البدء ======
if st.session_state.stage == "start":
    st.title("🧠 لعبة اختبار الذاكرة")
    st.markdown("احفظ تسلسل الحروف الذي يظهر، ثم اكتبه بالترتيب.\n\n لديك 5 محاولات فقط. كل مستوى يصبح أصعب! 🚀")
    if st.button("ابدأ اللعبة ▶️"):
        st.session_state.stage = "show"
        st.experimental_rerun()

# ====== عرض التسلسل مع عداد ======
elif st.session_state.stage == "show":
    st.subheader(f"المستوى {st.session_state.level} | المحاولات المتبقية: {st.session_state.attempts}")

    seq_length = st.session_state.level + 2
    st.session_state.sequence = generate_sequence(seq_length)

    st.markdown("### ⚡ احفظ هذا التسلسل:")

    placeholder = st.empty()
    for i in range(3, 0, -1):
        with placeholder.container():
            st.markdown(f"## {' '.join(st.session_state.sequence)}")
            st.markdown(f"⏳ <b>{i}</b> ثانية", unsafe_allow_html=True)
        play_sound(exciting_sound)
        time.sleep(1)
    placeholder.empty()

    st.session_state.stage = "input"
    st.experimental_rerun()

# ====== مرحلة الإدخال ======
elif st.session_state.stage == "input":
    st.subheader(f"✍️ اكتب التسلسل الذي رأيته (بدون فراغات):")
    play_sound(tense_sound)
    st.text_input("تسلسل الحروف:", key="user_input")

    if st.button("تحقق ✅"):
        correct = st.session_state.user_input.upper().replace(" ", "")
        if correct == st.session_state.sequence:
            st.success("✅ إجابة صحيحة! ننتقل للمستوى التالي...")
            st.session_state.level += 1
        else:
            st.error(f"❌ خطأ! التسلسل الصحيح كان: {st.session_state.sequence}")
            st.session_state.attempts -= 1

        if st.session_state.attempts == 0:
            st.session_state.stage = "end"
        else:
            st.session_state.stage = "show"

        time.sleep(2)
        st.experimental_rerun()

# ====== نهاية اللعبة ======
elif st.session_state.stage == "end":
    st.markdown(f"## 💥 انتهت اللعبة!")
    st.markdown(f"وصلت إلى المستوى: **{st.session_state.level}**")
    if st.button("🔁 إعادة اللعب"):
        reset_game()
        st.experimental_rerun()
