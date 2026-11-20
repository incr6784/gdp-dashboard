import math

import streamlit as st


st.set_page_config(
    page_title="여러가지 원으로 자신의 작품을 만들어보아요",
    page_icon="🎨",
    layout="wide",
)

COLORS = {
    "🔴 빨강": "#ef476f",
    "🟠 주황": "#ff8c42",
    "🟡 노랑": "#ffd166",
    "🟢 초록": "#63b995",
    "🩵 민트": "#5bc0be",
    "🔵 파랑": "#4d96ff",
    "🟣 보라": "#9b72cf",
    "🩷 분홍": "#f284b6",
    "🟤 갈색": "#a47148",
    "⚫ 회색": "#687386",
}
SHAPES = {
    "원": "circle",
    "반원": "semicircle",
    "1/4원": "quarter",
}

if "artwork" not in st.session_state:
    st.session_state.artwork = []
if "awaiting_continue" not in st.session_state:
    st.session_state.awaiting_continue = False
if "finished" not in st.session_state:
    st.session_state.finished = False


def shape_measure(radius: int, shape: str, measure: str) -> float:
    """Return area or the full boundary length using pi = 3."""
    if measure == "넓이":
        fraction = {"circle": 1, "semicircle": 0.5, "quarter": 0.25}[shape]
        return 3 * radius**2 * fraction

    curved_edge = {"circle": 6, "semicircle": 3, "quarter": 1.5}[shape] * radius
    straight_edges = {"circle": 0, "semicircle": 2, "quarter": 2}[shape] * radius
    return curved_edge + straight_edges


def shape_formula(radius: int, shape: str, measure: str) -> str:
    if measure == "넓이":
        fraction = {"circle": "3", "semicircle": "3 ÷ 2", "quarter": "3 ÷ 4"}[shape]
        return f"{fraction} × {radius} × {radius}"
    formulas = {
        "circle": f"6 × {radius}",
        "semicircle": f"3 × {radius} + 2 × {radius}",
        "quarter": f"1.5 × {radius} + 2 × {radius}",
    }
    return formulas[shape]


def format_number(value: float) -> str:
    number = float(value)
    return str(int(number)) if number.is_integer() else f"{number:g}"


def drawing_svg(items: list[dict], framed: bool = False) -> str:
    width, height = 600, 360
    drawing = [
        f'<svg width="100%" viewBox="0 0 {width} {height}" role="img" '
        'aria-label="여러 가지 원으로 꾸민 그림판" xmlns="http://www.w3.org/2000/svg">',
        '<rect width="600" height="360" rx="20" fill="#fffdf8"/>',
        '<path d="M30 30H570M30 90H570M30 150H570M30 210H570M30 270H570M30 330H570 '
        'M30 30V330M90 30V330M150 30V330M210 30V330M270 30V330M330 30V330'
        'M390 30V330M450 30V330M510 30V330M570 30V330" '
        'stroke="#eee9df" stroke-width="1" stroke-dasharray="2 7"/>',
    ]
    for item in items:
        cx = item["x"] / 100 * width
        cy = item["y"] / 100 * height
        radius = item["radius"] * 7
        color = item["color"]
        shape = item["shape"]
        common = 'stroke="#ffffff" stroke-width="3" stroke-linejoin="round"'
        if shape == "circle":
            drawing.append(
                f'<circle cx="{cx:g}" cy="{cy:g}" r="{radius:g}" fill="{color}" '
                f'fill-opacity=".9" {common}/>'
            )
        elif shape == "semicircle":
            drawing.append(
                f'<path d="M {cx-radius:g} {cy:g} A {radius:g} {radius:g} 0 0 0 '
                f'{cx+radius:g} {cy:g} Z" fill="{color}" fill-opacity=".9" {common}/>'
            )
        else:
            drawing.append(
                f'<path d="M {cx:g} {cy:g} L {cx:g} {cy-radius:g} '
                f'A {radius:g} {radius:g} 0 0 1 {cx+radius:g} {cy:g} Z" '
                f'fill="{color}" fill-opacity=".9" {common}/>'
            )
    drawing.append("</svg>")
    artwork = "".join(drawing)
    if not framed:
        return (
            '<div style="padding:12px;background:white;border:3px solid #eadcc7;'
            f'border-radius:22px;box-shadow:0 6px 18px #72552a12">{artwork}</div>'
        )
    return (
        '<div style="background:linear-gradient(135deg,#f8e6c8,#fff8eb);'
        'padding:34px 7%;border-radius:18px;text-align:center">'
        '<div style="font-size:20px;color:#755c45;margin-bottom:14px">우리 반 작은 미술관</div>'
        '<div style="max-width:680px;margin:auto;padding:16px;background:#a66b3f;'
        'border:9px solid #d5a66f;border-radius:8px;box-shadow:0 12px 24px #65432140">'
        f'<div style="background:#fffdf8;padding:8px">{artwork}</div></div>'
        '<div style="font-size:16px;color:#755c45;margin-top:16px">멋진 작품이 완성되었어요!</div>'
        "</div>"
    )


def show_drawing(items: list[dict], framed: bool = False) -> None:
    content = drawing_svg(items, framed=framed)
    height = 540 if framed else 400
    st.iframe(
        f'<style>html,body{{margin:0;background:transparent}}</style>{content}',
        width="stretch",
        height=height,
        alt="완성 중인 원 그림판" if not framed else "액자에 걸린 완성 작품",
    )


st.markdown(
    """
    <style>
    .stApp { background: #fffaf1; }
    .block-container { max-width: 1050px; padding-top: 2rem; }
    .hero {
        padding: 1.6rem 2rem; border-radius: 22px;
        background: linear-gradient(120deg, #fff0cc, #ffe2dc);
        border: 1px solid #f4d8b8; margin-bottom: 1rem;
    }
    .hero h1 { color: #493c35; font-size: 2.1rem; margin: 0 0 .4rem; }
    .hero p { color: #705d50; font-size: 1.05rem; margin: 0; }
    .pi-note {
        background: #eff8eb; border-left: 5px solid #70ad67;
        border-radius: 8px; padding: 12px 16px; color: #385b35;
    }
    .board {
        padding: 12px; background: white; border: 3px solid #eadcc7;
        border-radius: 22px; box-shadow: 0 6px 18px #72552a12;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero"><h1>🎨 여러가지 원으로 자신의 작품을 만들어보아요</h1>'
    '<p>원의 넓이와 둘레를 맞히고, 알록달록한 도형으로 나만의 그림을 완성해요!</p></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="pi-note"><b>오늘의 약속!</b> 이 활동에서는 계산하기 쉽게 원주율(π)을 '
    '<b>3</b>으로 계산해요. 도형의 <b>넓이</b>와 <b>둘레</b> 중 원하는 것을 골라 맞혀 보세요.</div>',
    unsafe_allow_html=True,
)

if st.session_state.finished:
    st.subheader("작품이 액자에 걸렸어요! 🖼️")
    show_drawing(st.session_state.artwork, framed=True)
    if st.button("새 작품 만들기", type="primary"):
        st.session_state.artwork = []
        st.session_state.awaiting_continue = False
        st.session_state.finished = False
        st.rerun()
    st.stop()

stage = len(st.session_state.artwork) + 1

if not st.session_state.awaiting_continue:
    st.subheader(f"도전 {stage}: 도형을 골라 계산해 보세요")
    selection_cols = st.columns([1, 1, 1, 2])
    with selection_cols[0]:
        radius = st.selectbox("반지름", options=list(range(1, 11)), key=f"radius_{stage}")
    with selection_cols[1]:
        shape_label = st.selectbox("도형", options=list(SHAPES), key=f"shape_{stage}")
    with selection_cols[2]:
        measure = st.selectbox("무엇을 맞힐까요?", options=["둘레", "넓이"], key=f"measure_{stage}")
    shape = SHAPES[shape_label]
    unit = "cm" if measure == "둘레" else "cm²"
    with selection_cols[3]:
        st.markdown(
            f"#### 반지름이 **{radius}**인 {shape_label}의 **{measure}**는 얼마일까요?"
        )
        st.caption(
            "둘레는 곡선과 곧은 변을 모두 더해요. "
            + ("원 둘레의 일부와 지름/반지름 변을 더해요." if shape != "circle" else "원 둘레를 구해요.")
        )

    st.markdown("**그림에 사용할 색과 위치를 골라 보세요. 정답을 맞히면 그림판에 추가돼요!**")
    color_label = st.radio(
        "색깔 팔레트",
        options=list(COLORS),
        horizontal=True,
        key=f"palette_{stage}",
        label_visibility="collapsed",
    )

    with st.form(f"answer_form_{stage}_{radius}_{shape}_{measure}"):
        answer = st.number_input(
            f"정답을 입력하세요 ({unit})",
            min_value=0.0,
            step=0.5,
            format="%g",
            key=f"answer_{stage}_{radius}_{shape}_{measure}",
        )
        check_answer = st.form_submit_button("정답 확인하기 ✨", type="primary")

    if check_answer:
        correct_answer = shape_measure(radius, shape, measure)
        if math.isclose(answer, correct_answer, abs_tol=0.001):
            st.session_state.artwork.append(
                {
                    "radius": radius,
                    "shape": shape,
                    "measure": measure,
                    "color": COLORS[color_label],
                    "x": 30 + (stage * 13) % 40,
                    "y": 30 + (stage * 17) % 40,
                }
            )
            st.session_state.awaiting_continue = True
            st.success(
                f"정답이에요! {shape_formula(radius, shape, measure)} = "
                f"{format_number(correct_answer)} {unit} 🎉"
            )
        else:
            st.error("아쉬워요. 원주율은 3이에요. 식을 다시 생각하고 도전해 보세요!")
else:
    st.info("도형이 그림판에 추가되었어요. 계속 도전하거나 작품을 완성해 보세요!")

if st.session_state.awaiting_continue and st.session_state.artwork:
    last_index = len(st.session_state.artwork) - 1
    last_item = st.session_state.artwork[last_index]
    position_cols = st.columns(2)
    with position_cols[0]:
        x_position = st.slider(
            "가로 위치", 12, 88, last_item["x"], 2, key=f"position_x_{last_index}"
        )
    with position_cols[1]:
        y_position = st.slider(
            "세로 위치", 20, 80, last_item["y"], 2, key=f"position_y_{last_index}"
        )
    last_item["x"] = x_position
    last_item["y"] = y_position

show_drawing(st.session_state.artwork)

if st.session_state.awaiting_continue and st.session_state.artwork:
    action_cols = st.columns(2)
    with action_cols[0]:
        if st.button(
            "계속하기 ➜",
            type="primary",
            disabled=not st.session_state.awaiting_continue,
            use_container_width=True,
        ):
            st.session_state.awaiting_continue = False
            st.rerun()
    with action_cols[1]:
        if st.button("완성하기 🖼️", use_container_width=True):
            st.session_state.finished = True
            st.rerun()
