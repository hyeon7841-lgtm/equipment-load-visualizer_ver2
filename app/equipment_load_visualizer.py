import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from PIL import Image
import io
from streamlit_dragrect import st_dragrect

# -----------------------------
# 기본 설정
# -----------------------------
AREA_WIDTH = 3100  # mm
AREA_HEIGHT = 2050  # mm
GRID_RESOLUTION = 50  # 분포 해상도

st.set_page_config(layout="wide")
st.title("📦 장비 하중 분포 시각화 도구")

# -----------------------------
# 장비 목록 상태 저장
# -----------------------------
if "equipments" not in st.session_state:
    st.session_state.equipments = []

# -----------------------------
# 사이드바 - 장비 추가
# -----------------------------
st.sidebar.header("장비 추가")
name = st.sidebar.text_input("장비 이름", value=f"장비{len(st.session_state.equipments)+1}")
width = st.sidebar.number_input("가로(mm)", min_value=10, value=200)
height = st.sidebar.number_input("세로(mm)", min_value=10, value=200)
weight = st.sidebar.number_input("하중(kg)", min_value=1, value=100)

if st.sidebar.button("장비 추가"):
    st.session_state.equipments.append({
        "name": name,
        "width": width,
        "height": height,
        "weight": weight,
        "x": 100,
        "y": 100,
        "angle": 0   # 회전각
    })

# -----------------------------
# 메인 화면 UI
# -----------------------------
st.subheader("📍 장비 배치 (드래그 & 드롭)")

canvas = Image.new("RGB", (AREA_WIDTH // 10, AREA_HEIGHT // 10), "white")
fig, ax = plt.subplots(figsize=(8, 6))
ax.imshow(canvas)
ax.set_title("장비 배치 화면")
ax.axis("off")

# 드래그 가능한 장비 박스 생성
rects = []
for i, eq in enumerate(st.session_state.equipments):
    rects.append({
        "left": eq["x"]/10,
        "top": eq["y"]/10,
        "width": eq["width"]/10,
        "height": eq["height"]/10,
        "index": i
    })

drag_results = st_dragrect(rects)

# 드래그된 위치 업데이트
for result in drag_results:
    idx = result["index"]
    st.session_state.equipments[idx]["x"] = int(result["left"] * 10)
    st.session_state.equipments[idx]["y"] = int(result["top"] * 10)

# -----------------------------
# 자동 배치 기능
# -----------------------------
def auto_place():
    x_offset = 50
    y_offset = 50
    spacing = 80

    for i, eq in enumerate(st.session_state.equipments):
        eq["x"] = x_offset
        eq["y"] = y_offset + i * (eq["height"] + spacing)

if st.button("🔁 자동 배치"):
    auto_place()

# -----------------------------
# 90도 회전 기능
# -----------------------------
st.subheader("🔄 장비 회전")
for i, eq in enumerate(st.session_state.equipments):
    col1, col2, col3 = st.columns([2,2,2])
    col1.write(eq["name"])
    if col2.button(f"{eq['name']} 90° 회전"):
        w = eq["width"]
        h = eq["height"]
        eq["width"], eq["height"] = h, w  # swap
        eq["angle"] = (eq["angle"] + 90) % 360

# -----------------------------
# 하중 분포 계산
# -----------------------------
def compute_load_map():
    grid_x = AREA_WIDTH // GRID_RESOLUTION
    grid_y = AREA_HEIGHT // GRID_RESOLUTION
    load_map = np.zeros((grid_y, grid_x))

    for eq in st.session_state.equipments:
        x0 = eq["x"] // GRID_RESOLUTION
        y0 = eq["y"] // GRID_RESOLUTION
        w = eq["width"] // GRID_RESOLUTION
        h = eq["height"] // GRID_RESOLUTION

        load_map[y0:y0+h, x0:x0+w] += eq["weight"]

    return gaussian_filter(load_map, sigma=1.2)

# -----------------------------
# 하중 히트맵 출력
# -----------------------------
st.subheader("🔥 하중 분포 히트맵")

load_map = compute_load_map()

fig2, ax2 = plt.subplots(figsize=(10, 6))
heat = ax2.imshow(load_map, cmap="hot", origin="lower")
plt.colorbar(heat, ax=ax2)
ax2.set_title("하중 분포 (kg)")
st.pyplot(fig2)

# -----------------------------
# PNG 저장 기능
# -----------------------------
st.subheader("📸 PNG 저장")

if st.button("히트맵 PNG 저장"):
    buf = io.BytesIO()
    fig2.savefig(buf, format="png")
    st.download_button(label="다운로드", data=buf.getvalue(),
                       file_name="loadmap.png", mime="image/png")

st.success("완료되었습니다!")
