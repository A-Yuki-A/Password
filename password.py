import streamlit as st
import string
import time
import itertools

# 使える文字（英大小文字 + 数字 + 記号）
custom_symbols = "!#$%&()/<=>?@"  # 制限された記号
available_chars = string.ascii_letters + string.digits + custom_symbols

# 利用可能な記号一覧を表示用に取得
symbols_list = custom_symbols


def simulate_brute_force(target_password):
    start_time = time.time()
    attempts = 0

    # 長さ1から順に全組み合わせを試す（盲目的な総当たり）
    for length in range(1, len(target_password) + 1):
        for combo in itertools.product(available_chars, repeat=length):
            attempts += 1
            guess = ''.join(combo)
            if guess == target_password:
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

    # 見つからなかった場合（理論上ありえない）
    end_time = time.time()
    elapsed_time = end_time - start_time
    return attempts, round(elapsed_time, 4), "解析失敗"

# アプリタイトル
st.title("Brute Blitz")

# ツール説明と使用可能文字の案内
st.write(f"""
このツールでは、パスワードが何か分からない状態で、
1文字から順に全組み合わせを試す「盲目的な総当たり」を体験できます。

**使える文字:**
- 英大文字: A–Z
- 英小文字: a–z
- 数字: 0–9
- 記号: {symbols_list}  
※記号は上記のもののみ利用可能です。
""" )

# パスワード入力 (1～15文字)
password = st.text_input(
    "パスワードを入力してください（1〜15文字、英数字・記号OK）",
    type="password"
)
run_attack = st.button("解析")

if run_attack:
    if not password:
        st.warning("パスワードを入力してください。")
    elif len(password) > 15:
        st.error("パスワードは15文字以内にしてください。")
    else:
        with st.spinner("解析中..."):
            attempts, elapsed, danger = simulate_brute_force(password)
        st.success("解析完了！")
        st.write(f"**試行回数：** {attempts:,} 回")
        st.write(f"**解析時間：** {elapsed} 秒")
        st.write(f"**危険度：** {danger}")

        st.markdown("---")
        st.info("パスワードがバレないまま、総当たり攻撃の威力を学びましょう。")
