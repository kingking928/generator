import streamlit as st
import pandas as pd
import random
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

st.set_page_config(page_title="轻松一天生成器", page_icon="🌿", layout="centered")

# ===== UI样式 =====
st.markdown("""
    <style>
    .card {
        padding: 18px;
        border-radius: 15px;
        background-color: #f7f7f7;
        margin-bottom: 12px;
    }
    .title {
        font-size: 17px;
        font-weight: bold;
    }
    .meta {
        color: gray;
        font-size: 14px;
        margin-top: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# ===== 标题 =====
st.title("🌿 轻松一天生成器")
st.caption("不想计划的时候，就随便过一天")

# ===== 数据 =====
df = pd.read_csv("places.csv")

areas = ["不限"] + sorted(df["area"].dropna().unique().tolist())
# ===== 输入区 =====
col1, col2 = st.columns(2)

with col1:
    people = st.selectbox("👥 和谁", ["一个人", "情侣", "闺蜜", "朋友", "家人"])

with col2:
    weather = st.selectbox("🌦 天气", ["晴天", "雨天"])

vibe = st.selectbox(
    "🌿 想要什么感觉",
    ["都可以", "安静", "热闹", "放空", "出片"]
)
area_choice = st.selectbox("📍 想在哪个区", areas)

# ===== 匹配函数 =====
def match(value, target):
    return target in str(value) or "不限" in str(value) or "所有人" in str(value)

# ===== 生成逻辑 =====
def generate_plan():
    filtered = df[
        df["people"].apply(lambda x: match(x, people)) &
        df["weather"].apply(lambda x: match(x, weather))
    ]

    if area_choice != "不限":
        filtered = filtered[df["area"] == area_choice]

    if vibe != "都可以":
        filtered = filtered[filtered["vibe"] == vibe]

    if len(filtered) < 3:
        filtered = df

    # ===== 区域统一 =====
    if area_choice != "不限":
        area = area_choice
    else:
        area = random.choice(filtered["area"].unique())
    filtered = filtered[filtered["area"] == area]

    if len(filtered) < 3:
        filtered = df

    # ===== 去重控制 =====
    used_names = set()
    used_types = set()

    def pick_by_type(preferred_types):
        # 优先选指定类型
        candidates = filtered[filtered["type"].isin(preferred_types)]

        # 去掉已选地点 & 类型
        candidates = candidates[
            ~candidates["name"].isin(used_names) &
            ~candidates["type"].isin(used_types)
        ]

        # 如果没有 → 放宽“类型限制”（但不重复地点）
        if len(candidates) == 0:
            candidates = filtered[
                ~filtered["name"].isin(used_names)
            ]

        # 如果还是没有（极端情况）
        if len(candidates) == 0:
            candidates = filtered

        choice = candidates.sample(1).iloc[0]

        used_names.add(choice["name"])
        used_types.add(choice["type"])

        return choice

    # ===== 时间段选择 =====
    afternoon = pick_by_type(["coffee", "walk"])
    evening = pick_by_type(["walk", "food"])
    night = pick_by_type(["night"])

    plan = [
        (afternoon["name"], afternoon["desc"]),
        (evening["name"], evening["desc"]),
        (night["name"], night["desc"]),
    ]

    return plan, area

def generate_image(plan, area):
    from PIL import Image, ImageDraw, ImageFont
    from io import BytesIO

    # ===== 画布（更像小红书比例）=====
    img = Image.new('RGB', (700, 1000), color=(245, 245, 245))
    draw = ImageDraw.Draw(img)

    # ===== 字体 =====
    try:
        font_title = ImageFont.truetype("NotoSansSC-Regular.ttf", 48)
        font_sub = ImageFont.truetype("NotoSansSC-Regular.ttf", 26)
        font_text = ImageFont.truetype("NotoSansSC-Regular.ttf", 30)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_text = ImageFont.load_default()

    # ===== 标题 =====
    draw.text((50, 60), "今日份随便过一天", fill=(0, 0, 0), font=font_title)

    # ===== 副信息 =====
    draw.text((50, 130), f"{area} ｜ 不想计划也没关系", fill=(120, 120, 120), font=font_sub)

    # ===== 卡片背景 =====
    card_x1, card_y1 = 40, 180
    card_x2, card_y2 = 660, 780
    draw.rounded_rectangle(
        (card_x1, card_y1, card_x2, card_y2),
        radius=25,
        fill=(255, 255, 255)
    )

    # ===== 行程内容 =====
    y = 220
    time_labels = ["下午", "傍晚", "晚上"]

    for i in range(3):
        name, desc = plan[i]

        # 时间
        draw.text((70, y), time_labels[i], fill=(100, 100, 100), font=font_sub)

        # 地点
        draw.text((70, y + 40), name, fill=(0, 0, 0), font=font_text)

        # 描述
        draw.text((70, y + 80), desc, fill=(120, 120, 120), font=font_sub)

        y += 170

    # ===== 底部文案 =====
    draw.text(
        (50, 820),
        "不想计划的时候，就随便过一天\n反而更轻松一点",
        fill=(150, 150, 150),
        font=font_sub
    )

    # ===== 输出 =====
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer

# ===== 按钮 =====
if st.button("✨ 随便安排一下", use_container_width=True):
    plan, area = generate_plan()
    st.session_state.plan = plan
    st.session_state.area = area

# ===== 展示结果 =====
if "plan" in st.session_state:

    st.markdown("## 🌈 今天可以这样过")

    st.markdown(f"""
    <div class="meta">📍 {st.session_state.area}</div>
    """, unsafe_allow_html=True)

    time_labels = ["🌤 下午", "🌆 傍晚", "🌙 晚上"]

    for i in range(3):
        name, desc = st.session_state.plan[i]

        st.markdown(f"""
        <div class="card">
            <div class="title">{time_labels[i]} · {name}</div>
            <div class="meta">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

if "plan" in st.session_state:
    # 生成图片
    img_buffer = generate_image(st.session_state.plan, st.session_state.area)

    st.download_button(
        label="📸 下载分享图片",
        data=img_buffer,
        file_name="today_plan.png",
        mime="image/png"
    )