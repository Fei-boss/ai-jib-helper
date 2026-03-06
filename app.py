import streamlit as st
import openai

# 从 Streamlit Secrets 安全读取 API Key（不会泄露到代码里）
DOUBAN_API_KEY = st.secrets.get("DOUBAN_API_KEY", "")
DOUBAN_MODEL_ID = "doubao-seed-1-8-251228"

def call_ai(prompt):
    """通用 AI 调用函数，英文命名更兼容"""
    if not DOUBAN_API_KEY:
        st.error("未配置 API Key，请在 Streamlit Secrets 中设置 DOUBAN_API_KEY")
        return None
    
    try:
        client = openai.OpenAI(
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            api_key=DOUBAN_API_KEY
        )
        response = client.chat.completions.create(
            model=DOUBAN_MODEL_ID,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"调用 AI 出错了: {e}")
        return None

# 页面标题
st.title("✨ AI求职助手 V3.0 (网页版)")

# 侧边栏功能选择
function = st.sidebar.selectbox("选择功能", ["简历优化", "求职信生成", "面试题预测"])

if function == "简历优化":
    st.subheader("📝 AI简历优化")
    job_requirement = st.text_area("岗位要求")
    personal_experience = st.text_area("个人经历")
    
    if st.button("生成优化简历"):
        if job_requirement and personal_experience:
            with st.spinner("AI 正在优化简历..."):
                prompt = f"""
                你是专业的简历优化专家，请根据岗位要求和个人经历，生成一份优化后的简历。
                岗位要求：{job_requirement}
                个人经历：{personal_experience}
                请用专业、简洁的语言，突出与岗位匹配的能力和经验。
                """
                optimized_resume = call_ai(prompt)
                if optimized_resume:
                    st.markdown("### 优化后的简历：")
                    st.write(optimized_resume)
        else:
            st.warning("请填写岗位要求和个人经历")

elif function == "求职信生成":
    st.subheader("✉️ AI求职信生成")
    company_info = st.text_area("公司及岗位信息")
    personal_intro = st.text_area("个人介绍")
    
    if st.button("生成求职信"):
        if company_info and personal_intro:
            with st.spinner("AI 正在生成求职信..."):
                prompt = f"""
                你是专业的求职顾问，请根据公司信息和个人介绍，生成一封真诚、专业的求职信。
                公司及岗位信息：{company_info}
                个人介绍：{personal_intro}
                请突出与岗位的匹配度和求职意愿。
                """
                cover_letter = call_ai(prompt)
                if cover_letter:
                    st.markdown("### 生成的求职信：")
                    st.write(cover_letter)
        else:
            st.warning("请填写公司信息和个人介绍")

elif function == "面试题预测":
    st.subheader("🎯 AI面试题预测")
    job_desc = st.text_area("岗位描述")
    experience_level = st.selectbox("经验等级", ["应届生", "1-3年", "3-5年"])
    
    if st.button("生成面试题"):
        if job_desc:
            with st.spinner("AI 正在生成面试题..."):
                prompt = f"""
                你是资深面试官，请根据岗位描述和候选人经验，生成10道高频面试题及参考答案要点。
                岗位描述：{job_desc}
                候选人经验：{experience_level}
                """
                questions = call_ai(prompt)
                if questions:
                    st.markdown("### 生成的面试题及参考答案：")
                    st.write(questions)
        else:
            st.warning("请填写岗位描述")