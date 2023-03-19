import re
import os
import uuid
import random
import requests
import streamlit as st

proxy = None
proxies = {
    "http": proxy,
    "https": proxy
}
st.title("临时邮箱聚合系统")
st.text("本页面中所有临时邮箱均为YopMail提供")
@st.cache_data(ttl=640)
def get_resp():
    resp = requests.get("https://yopmail.com/zh/domain?d=all").text
    resp = re.findall("<div>(@.*?)</div>", resp)
    return resp

resp = get_resp()

n = st.slider("输入生成数量", 1, 1000000, 10000)
if st.button("开始生成"):
    fn = str(uuid.uuid4()) + ".txt"
    with st.spinner("请稍等……"), open("..\\" + fn, "a+", encoding="utf-8") as f:
        for i in range(n):
            mail = random.choice(resp)
            name = str(uuid.uuid4())[:random.randint(18, 36)]
            f.write(f"邮箱：{name}{mail}\n")
            f.write(f"链接：https://yopmail.com/zh/?login={name}\n\n")

    if st.download_button("下载临时邮箱", open("..\\" + fn, "r", encoding="utf-8"), file_name="临时邮箱.txt"):
        os.remove("..\\" + fn)
