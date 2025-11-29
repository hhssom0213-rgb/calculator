import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import random
import pandas as pd

st.set_page_config(page_title="멀티 기능 웹앱", page_icon="🌍", layout="wide")


# ============================================================
#                   1) 계산기 기능
# ============================================================
def calculator_app():
    st.title("🧮 다기능 계산기")
    st.write("사칙연산, 지수, 로그, 다항함수 그래프 기능")

    # 기본 계산
    st.header("📌 계산 기능")

    num1 = st.number_input("첫 번째 숫자", value=0.0)
    num2 = st.number_input("두 번째 숫자", value=0.0)

    operation = st.selectbox(
        "연산 선택",
        ["덧셈 (+)", "뺄셈 (-)", "곱셈 (×)", "나눗셈 (÷)", "모듈러 (%)",
         "지수 (a^b)", "로그 (log_a(b))"]
    )

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
                st.error("0으로 나눌 수 없습니다.")
            else:
                st.success(f"결과: {num1 / num2}")
        elif operation == "모듈러 (%)":
            if num2 == 0:
                st.error("0으로 나눌 수 없습니다.")
            else:
                st.success(f"결과: {num1 % num2}")
        elif operation == "지수 (a^b)":
            st.success(f"{num1}^{num2} = {num1 ** num2}")
        elif operation == "로그 (log_a(b))":
            if num1 <= 0 or num1 == 1 or num2 <= 0:
                st.error("로그 조건을 만족해야 합니다.")
            else:
                st.success(math.log(num2, num1))
    except Exception as e:
        st.error(f"오류 발생: {e}")

    # 다항함수 그래프
    st.header("📊 다항함수 그래프 (Plotly)")
    poly_input = st.text_input("다항식 입력 (예: 2*x**3 - 3*x + 1)")
    x_min = st.number_input("x 최소값", value=-10.0)
    x_max = st.number_input("x 최대값", value=10.0)

    if st.button("그래프 그리기"):
        try:
            x = np.linspace(x_min, x_max, 500)
            y = eval(poly_input, {"x": x, "np": np, "math": math})
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, mode="lines"))
            fig.update_layout(
                title=f"y = {poly_input}",
                xaxis_title="x",
                yaxis_title="y",
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"그래프 오류: {e}")


# ============================================================
#               2) 확률 시뮬레이터 기능
# ============================================================
def probability_simulator():
    st.title("🎲 확률 시뮬레이터")

    sim_type = st.selectbox("종류 선택", ["동전", "주사위"])
    trials = st.number_input("시행 횟수", value=100, min_value=1)

    if st.button("시뮬레이션 실행"):
        results = []

        if sim_type == "동전":
            outcomes = ["앞면", "뒷면"]
            for _ in range(trials):
                results.append(random.choice(outcomes))

        elif sim_type == "주사위":
            outcomes = [1, 2, 3, 4, 5, 6]
            for _ in range(trials):
                results.append(random.choice(outcomes))

        counts = {o: results.count(o) for o in outcomes}

        fig = go.Figure()
        fig.add_trace(go.Bar(x=list(counts.keys()), y=list(counts.values())))
        fig.update_layout(
            title=f"{sim_type} 시뮬레이션 결과 ({trials}회)",
            xaxis_title="결과",
            yaxis_title="빈도",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.write("📝 결과:", counts)


# ============================================================
#           3) 연도별 세계인구 분석 기능
# ============================================================
def world_population_app():
    st.title("🌍 연도별 세계인구 분석")

    st.write("CSV 파일을 불러와 연도별 국가 인구를 세계 지도 위에 시각화합니다.")

    # 파일 업로드
    uploaded_file = st.file_uploader("world_population.csv 파일을 업로드하세요", type=["csv"])

    if uploaded_file is None:
        st.info("세계 인구 데이터 파일을 업로드해주세요.")
        return

    df = pd.read_csv(uploaded_file)

    # 연도 선택
    available_years = [1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022]
    selected_year = st.selectbox("연도 선택", available_years)

    # 선택한 연도 데이터 필터
    df_year = df[df["year"] == selected_year]

    # 지도 생성
    st.subheader(f"📌 세계 인구 지도 ({selected_year})")

    fig = px.choropleth(
        df_year,
        locations="iso_code",
        color="population",
        hover_name="country",
        color_continuous_scale="Viridis",
        title=f"{selected_year}년 세계 인구 분포",
    )
    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=False),
        coloraxis_colorbar=dict(title="Population")
    )

    st.plotly_chart(fig, use_container_width=True)


# ============================================================
#                     메인 메뉴
# ============================================================
st.sidebar.title("🔧 메뉴 선택")
app_mode = st.sidebar.radio(
    "원하는 기능을 선택하세요",
    ["계산기", "확률 시뮬레이터", "연도별 세계인구 분석"]
)

if app_mode == "계산기":
    calculator_app()
elif app_mode == "확률 시뮬레이터":
    probability_simulator()
elif app_mode == "연도별 세계인구 분석":
    world_population_app()
