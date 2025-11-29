import streamlit as st
import math

st.set_page_config(page_title="다기능 계산기", page_icon="🧮")

st.title("🧮 다기능 계산기 (Streamlit)")
st.write("사칙연산, 모듈러 연산, 지수, 로그 기능을 포함한 간단한 계산기 웹앱입니다.")

# --- 입력값 ---
st.subheader("📌 숫자 입력")
num1 = st.number_input("첫 번째 숫자", value=0.0, format="%.10f")
num2 = st.number_input("두 번째 숫자", value=0.0, format="%.10f")

# --- 기능 선택 ---
st.subheader("📌 실행할 연산 선택")
operation = st.selectbox(
    "원하는 연산을 선택하세요",
    [
        "덧셈 (+)",
        "뺄셈 (-)",
        "곱셈 (×)",
        "나눗셈 (÷)",
        "모듈러 (%)",
        "지수 (a^b)",
        "로그 (log_a(b))"
    ]
)

# --- 계산 실행 ---
st.subheader("📌 결과")

try:
    if operation == "덧셈 (+)":
        result = num1 + num2
        st.success(f"결과: {result}")

    elif operation == "뺄셈 (-)":
        result = num1 - num2
        st.success(f"결과: {result}")

    elif operation == "곱셈 (×)":
        result = num1 * num2
        st.success(f"결과: {result}")

    elif operation == "나눗셈 (÷)":
        if num2 == 0:
            st.error("❌ 0으로 나눌 수 없습니다.")
        else:
            result = num1 / num2
            st.success(f"결과: {result}")

    elif operation == "모듈러 (%)":
        if num2 == 0:
            st.error("❌ 0으로 나눌 수 없습니다.")
        else:
            result = num1 % num2
            st.success(f"결과: {result}")

    elif operation == "지수 (a^b)":
        result = num1 ** num2
        st.success(f"{num1} ^ {num2} = {result}")

    elif operation == "로그 (log_a(b))":
        if num1 <= 0 or num1 == 1 or num2 <= 0:
            st.error("❌ 로그는 밑이 양수(그리고 1이 아님), 진수가 양수여야 합니다.")
        else:
            result = math.log(num2, num1)
            st.success(f"log_{num1}({num2}) = {result}")

except Exception as e:
    st.error(f"오류 발생: {e}")
