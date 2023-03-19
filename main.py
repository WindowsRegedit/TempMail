import re
import uuid
import random
import requests
import pandas as pd
import numpy as np
import streamlit as st

proxy = "http://127.0.0.1:7890/"
proxies = {
    "http": proxy,
    "https": proxy
}
st.title("临时邮箱聚合系统")
st.text("本页面中所有临时邮箱均为YopMail提供")

@st.cache_data(ttl=640)
def get_table():
    global resp, res
    resp = requests.get("https://yopmail.com/zh/domain?d=all").text
    resp = re.findall("<div>(@.*?)</div>", resp)
    res = resp[:100]
    res = np.reshape(res, (-1, 5))

    df = pd.DataFrame(
        res,
        columns=["第 %d 列" % i for i in range(1, 6)])
    return df, resp, res


df, resp, res = get_table()
st.table(df)

mail = st.selectbox("选择邮箱后缀：", resp + ["随机后缀"], index=len(resp) - 1)
if mail == "随机后缀":
    mail = random.choice(resp)

name = st.text_input("输入邮箱名称：", value=str(uuid.uuid4())[:random.randint(18, 36)])
if st.button("生成临时邮箱"):
    st.write(f"邮箱：{name}{mail}")
    st.write(f"访问链接：https://yopmail.com/zh/?login={name}")
