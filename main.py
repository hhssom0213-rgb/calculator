import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------
# Load Data
# ------------------------------------------------------
@st.cache_data
def load_population_data():
    df = pd.read_csv("world_population.csv")
    return df

# ------------------------------------------------------
# Sidebar Navigation
# ------------------------------------------------------
st.sidebar.title("활동 선택")
page = st.sidebar.radio(
    "원하는 기능을 선택하세요",
    [
        "기본 계산기", 
        "확률 시뮬레이터", 
        "연도별 세계인구 분석",
    ]
)

# ------------------------------------------------------
# 1) Calculator App
# ------------------------------------------------------
def calculator_app():
    st.title("🧮 기본 계산기")
    num1 = st.number_input("첫 번째 숫자", value=0.0)
    num2 = st.number_input("두 번째 숫자", value=0.0)
    operation = st.selectbox("연산 선택", ["+", "-", "×", "÷"])

    if st.button("계산하기"):
        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "×":
            result = num1 * num2
        elif operation == "÷":
            result = "0으로 나눌 수 없습니다" if num2 == 0 else num1 / num2
        st.success(f"결과: {result}")

# ------------------------------------------------------
# 2) Probability Simulator
# ------------------------------------------------------
def probability_simulator():
    st.title("🎲 확률 시뮬레이터")

    import random

    trials = st.number_input("시행 횟수", min_value=1, value=100)
    if st.button("동전 던지기 시뮬레이션 실행"):
        results = [random.choice(["앞면", "뒷면"]) for _ in range(trials)]
        heads = results.count("앞면")
        tails = trials - heads
        st.write(f"앞면: {heads}")
        st.write(f"뒷면: {tails}")
        st.write(f"앞면 비율: {heads / trials:.2f}")

# ------------------------------------------------------
# 3) World Population Map App
# ------------------------------------------------------
def world_population_map():
    st.title("🌍 연도별 세계인구 분석")

    df = load_population_data()

    # 필요한 연도만 선택
    selected_years = [1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022]
    year = st.selectbox("연도 선택", selected_years)

    # 열 이름이 연도로 되어 있다고 가정
    if str(year) not in df.columns:
        st.error(f"데이터에 {year}년 인구 정보가 없습니다.")
        return

    # 지도 시각화
    st.subheader(f"{year}년 세계 인구 지도")

    fig = px.choropleth(
        df,
        locations="Country",  # 국가 이름
        locationmode="country names",
        color=str(year),
        hover_name="Country",
        color_continuous_scale="YlOrRd",
        title=f"{year}년 세계 인구 분포",
    )

    st.plotly_chart(fig, use_container_width=True)

    # 구간 색칠
    st.subheader("인구 구간별 색상 표시")
    bins = st.slider("구간 개수", min_value=3, max_value=12, value=6)

    df["Bins"] = pd.cut(df[str(year)], bins=bins)

    fig2 = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="Bins",
        hover_name="Country",
        title=f"{year}년 인구 구간별 색상 지도",
    )

    st.plotly_chart(fig2, use_container_width=True)

# ------------------------------------------------------
# Page Routing
# ------------------------------------------------------
if page == "기본 계산기":
    calculator_app()
elif page == "확률 시뮬레이터":
    probability_simulator()\elif page == "연도별 세계인구 분석":
    world_population_map()
