import streamlit as st
import random

st.set_page_config(page_title="轻松一天生成器（上海版）", page_icon="🌿")

st.title("🌿 轻松一天生成器（上海版）")
st.write("不用想太多，帮你随便过一天～")

# 用户选择
mood = st.selectbox(
    "你现在的状态是：",
    ["一个人", "想放松", "不想花钱", "随便逛逛"]
)

# 方案库（文案升级版）
plans = {
    "一个人": [
        ["找个公园随便走走", "找家安静咖啡店坐一会", "吃点简单的晚餐"],
        ["去书店逛逛", "找个角落发发呆", "回家随便看看视频"],
        ["在街上随便走走", "买杯饮料坐着", "早点回去休息"],
        ["找个商场慢慢逛", "看看没见过的小店", "随便吃点东西"],
        ["去一个不常去的地方走走", "找地方坐一会", "慢慢回家"]
    ],
    "想放松": [
        ["找个绿地晒晒太阳", "喝杯咖啡放空", "慢慢吃顿饭"],
        ["去安静商场逛逛", "随便看看店", "吃点甜的"],
        ["城市walk随便走", "看到哪就停一下", "回家休息"],
        ["找个舒服的地方坐着", "刷会手机", "简单吃点"],
        ["下午随便晃一圈", "找地方歇会", "晚上早点回去"]
    ],
    "不想花钱": [
        ["去公园走走", "找个地方坐着", "回家"],
        ["随便在街上晃", "看看人来人往", "早点休息"],
        ["去图书馆待一会", "散步", "回家"],
        ["沿着一条路一直走", "找地方坐会", "结束一天"],
        ["随便换个区逛逛", "走累了就休息", "回家"]
    ],
    "随便逛逛": [
        ["随机坐一站地铁下车", "附近逛逛", "找点吃的"],
        ["去没去过的街区", "随便走走", "喝点东西"],
        ["打开地图随便选点", "走过去看看", "路上随便停"],
        ["选一个方向一直走", "看到有意思的就停", "慢慢结束"],
        ["找条没走过的路", "随便看看周围", "吃点东西"]
    ]
}

# 花费范围
cost_range = {
    "一个人": "约50-100元",
    "想放松": "约80-150元",
    "不想花钱": "0-30元",
    "随便逛逛": "约30-80元"
}

# 氛围文案
vibes = [
    "今天适合慢一点，不用着急。",
    "就这样随便走走，也挺好的。",
    "不用特别安排，轻松一点就好。",
    "给自己一点不被打扰的时间。",
    "今天不需要效率，只需要舒服。"
]

# 初始化 session（让按钮更丝滑）
if "results" not in st.session_state:
    st.session_state.results = []

# 生成函数
def generate_plan():
    results = []
    for _ in range(3):
        plan = random.choice(plans[mood])
        vibe = random.choice(vibes)
        results.append((plan, vibe))
    st.session_state.results = results

# 按钮区
col1, col2 = st.columns(2)

with col1:
    if st.button("✨ 生成今天安排"):
        generate_plan()

with col2:
    if st.button("🔄 再来一批"):
        generate_plan()

# 展示结果
if st.session_state.results:
    st.markdown("---")
    st.subheader("🌈 给你3种过法：")

    for i, (plan, vibe) in enumerate(st.session_state.results):
        st.markdown(f"### 方案 {i+1}")

        st.write(f"- 下午：{plan[0]}")
        st.write(f"- 傍晚：{plan[1]}")
        st.write(f"- 晚上：{plan[2]}")

        st.write(f"💰 预计花费：{cost_range[mood]}")
        st.write(f"🌿 感觉：{vibe}")

        st.markdown("---")