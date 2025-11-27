import streamlit as st
if c2.button("90° 회전", key=f"rot_{eq['id']}"):
eq['w'], eq['h'] = eq['h'], eq['w']
eq['rot'] = (eq['rot'] + 90) % 360


st.header("장비 배치 영역")
# Prepare items for component
items = []
for eq in st.session_state.equipments:
items.append({
"id": eq['id'],
"name": eq['name'],
"x": eq['x'],
"y": eq['y'],
"w": eq['w'],
"h": eq['h'],
})


# Call the custom component (returns updated items with new x,y)
updated = drag_component(items, width=AREA_W, height=AREA_H)


# Update session state positions from component result
if updated is not None:
id_map = {it['id']: it for it in updated}
for eq in st.session_state.equipments:
if eq['id'] in id_map:
eq['x'] = id_map[eq['id']]['x']
eq['y'] = id_map[eq['id']]['y']


# Show quick table
st.subheader("장비 테이블")
if len(st.session_state.equipments) == 0:
st.info("장비를 추가하세요.")
else:
import pandas as pd
df = pd.DataFrame(st.session_state.equipments)
st.dataframe(df)


# 하중 계산 및 히트맵
st.header("하중 분포 계산")
def compute_loadmap(equipments, area_w=AREA_W, area_h=AREA_H, res=50):
gx = area_w // res
gy = area_h // res
load = np.zeros((gy, gx))
for e in equipments:
x1 = max(0, int(e['x'] // res))
y1 = max(0, int(e['y'] // res))
x2 = min(gx, int((e['x'] + e['w']) // res))
y2 = min(gy, int((e['y'] + e['h']) // res))
if x2>x1 and y2>y1:
load[y1:y2, x1:x2] += e['weight']
from scipy.ndimage import gaussian_filter
return gaussian_filter(load, sigma=2)


if st.button("하중분포 그리기"):
lm = compute_loadmap(st.session_state.equipments)
fig, ax = plt.subplots(figsize=(10,6))
im = ax.imshow(lm, origin='lower', extent=[0, AREA_W, 0, AREA_H])
ax.set_title('하중 분포 (kg)')
fig.colorbar(im, ax=ax)
st.pyplot(fig)


# PNG download
buf = io.BytesIO()
fig.savefig(buf, format='png', dpi=200)
st.download_button('PNG 다운로드', data=buf.getvalue(), file_name='loadmap.png', mime='image/png')
