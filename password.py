import streamlit as st
import string
import time

# 使える文字（英大小文字 + 数字 + 記号）
available_chars = string.ascii_letters + string.digits + string.punctuation

def simulate_brute_force(password):
    start_time = time.time()
    attempts = 0
    guessed_password = ''

    for char in password:
        for guess in available_chars:
            attempts += 1
            if guess == char:
                guessed_password += guess
                break

    end_time = time.time()
    elapsed_time = end_time - start_time

    # 危険度判定
    if elapsed_time < 0.01:
        danger = "非常に危険（瞬時に解読）"
    elif elapsed_time < 0.05:
        danger = "危険（簡単に解読）"
    elif elapsed_time < 0.1:
        danger = "注意（数秒で解読）"
    elif elapsed_time < 0.5:
        danger = "やや安全（ある程度時間がかかる）"
    else:
        danger = "比較的安全（時間がかかる）"

    return attempts, round(elapsed_time, 4), danger

st.title("Crack Me If You Can - Brute Force Simulator")
st.write("""
このツールでは、入力されたパスワードに対して、
ブルートフォース攻撃（総当たり）による解読を模擬体験できます。
""")

password = st.text_input("パスワードを入力してください（1〜10文字、英数字・記号OK）", type="password")
run_attack = st.button("解析")

if run_attack:
    if not password:
        st.warning("パスワードを入力してください。")
    elif len(password) > 10:
        st.error("パスワードは10文字以内にしてください。")
    else:
        with st.spinner("解析中..."):
            attempts, elapsed, danger = simulate_brute_force(password)
        st.success("解析完了！")
        st.write(f"**入力されたパスワード：** {password}")
        st.write(f"**試行回数：** {attempts:,} 回")
        st.write(f"**解析時間：** {elapsed} 秒")
        st.write(f"**危険度：** {danger}")

        st.markdown("---")
        st.info("長くて複雑なパスワードほど、総当たり攻撃に強くなります。")
