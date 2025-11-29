import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="다기능 계산기", page_icon="🧮")

st.title("🧮 다기능 계산기 (Streamlit)")
st.write("사칙연산, 모듈러, 지수, 로그, **다항함수 그래프 Plotly 시각화** 기능이 포함된 계산기 웹앱입니다.")

# ---------------------------------------------
# 1) 기본 계산기 영역
# ---------------------------------------------
st.header("📌 계산 기능")

# 입력값
num1 = st.number_input("첫 번째 숫자", value=0.0, format="%.10f")
num2 = st.number_input("두 번째 숫자", value=0.0, format="%.10f")

# 연산 선택
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

# 결과 계산
st.subheader("🔎 결과")

try:
    if operation == "덧셈 (+)":
        st.success(f"결과: {num1 + num2}")

    elif operation == "뺄셈 (-)":
        st.success(f"결과: {num1 - num2}")

    elif operation == "곱셈 (×)":
        st.success(f"결과: {num1 * num2}")

    elif operation == "나눗셈 (÷)":
        if num2 == 0:
            st.error("❌ 0으로 나눌 수 없습니다.")
        else:
            st.success(f"결과: {num1 / num2}")

    elif operation == "모듈러 (%)":
        if num2 == 0:
            st.error("❌ 0으로 나눌 수 없습니다.")
        else:
            st.success(f"결과: {num1 % num2}")

    elif operation == "지수 (a^b)":
        st.success(f"{num1} ^ {num2} = {num1 ** num2}")

    elif operation == "로그 (log_a(b))":
        if num1 <= 0 or num1 == 1 or num2 <= 0:
            st.error("❌ 로그의 정의역에 맞지 않습니다.")
        else:
            st.success(f"log_{num1}({num2}) = {math.log(num2, num1)}")

except Exception as e:
    st.error(f"오류 발생: {e}")



# ---------------------------------------------
# 2) 다항함수 그래프 기능
# ---------------------------------------------
st.header("📊 다항함수 그래프 그리기 (Plotly)")

st.write("예: `2*x**3 - 3*x + 1`, `x**2`, `-0.5*x**4 + x` 등 형태로 입력")

poly_input = st.text_input("다항식을 입력하세요 (변수는 x 사용)")

x_min = st.number_input("x 최소값", value=-10.0)
x_max = st.number_input("x 최대값", value=10.0)

if x_min >= x_max:
    st.warning("⚠ x 최소값은 최대값보다 작아야 합니다.")

if st.button("그래프 그리기"):
    try:
        # x 범위 생성
        x = np.linspace(x_min, x_max, 500)

        # 문자열로 받은 함수 계산
        y = eval(poly_input, {"x": x, "np": np, "math": math})

        # Plotly 그래프 생성
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='다항함수'))
        fig.update_layout(
            title=f"다항함수 그래프:  y = {poly_input}",
            xaxis_title="x",
            yaxis_title="y",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"그래프를 그릴 수 없습니다: {e}")
