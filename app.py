import streamlit as st
import openai

# 页面基础配置（解决移动端适配）
st.set_page_config(
    page_title="AI求职助手 V3.0",
    page_icon="✨",
    layout="wide",  # 自适应布局
    initial_sidebar_state="collapsed"  # 移动端默认收起侧边栏
)

# 从 Streamlit Secrets 安全读取 API Key
DOUBAN_API_KEY = st.secrets.get("DOUBAN_API_KEY", "")
DOUBAN_MODEL_ID = "doubao-seed-1-8-251228"

def call_ai(prompt):
    """通用 AI 调用函数，增加异常捕获和兼容性处理"""
    if not DOUBAN_API_KEY:
        st.error("未配置 API Key，请在 Streamlit Secrets 中设置 DOUBAN_API_KEY")
        return None
    
    try:
        # 兼容不同版本的 OpenAI 客户端
        client = openai.OpenAI(
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            api_key=DOUBAN_API_KEY
        )
        response = client.chat.completions.create(
            model=DOUBAN_MODEL_ID,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,  # 增加温度参数，避免移动端返回空值
            max_tokens=2000   # 增加最大令牌数
        )
        return response.choices[0].message.content.strip()
    except openai.APIError as e:
        st.error(f"AI 接口错误: {e.message}")
        return None
    except Exception as e:
        st.error(f"系统错误: {str(e)}")
        return None

# 页面标题（适配移动端显示）
st.markdown("<h1 style='text-align: center; font-size: 24px;'>✨ AI求职助手 V3.0</h1>", unsafe_allow_html=True)

# 替换侧边栏为移动端友好的选择框
function = st.selectbox(
    "🔧 选择功能", 
    ["简历优化", "求职信生成", "面试题预测"],
    key="function_selector",
    help="请选择需要使用的求职辅助功能"
)

# 简历优化功能
if function == "简历优化":
    st.markdown("<h2 style='font-size: 20px;'>📝 AI简历优化</h2>", unsafe_allow_html=True)
    
    # 移动端适配的输入框
    job_requirement = st.text_area(
        "岗位要求",
        placeholder="请输入目标岗位的任职要求...",
        height=150,
        key="job_req"
    )
    personal_experience = st.text_area(
        "个人经历",
        placeholder="请输入你的工作/实习经历...",
        height=150,
        key="personal_exp"
    )
    
    # 按钮样式优化
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        generate_btn = st.button("🚀 生成优化简历", use_container_width=True)
    
    if generate_btn:
        if job_requirement and personal_experience:
            with st.spinner("AI 正在优化简历..."):
                prompt = f"""
                你是专业的简历优化专家，请根据岗位要求和个人经历，生成一份优化后的简历。
                岗位要求：{job_requirement}
                个人经历：{personal_experience}
                要求：
                1. 语言专业、简洁，突出与岗位匹配的能力
                2. 格式清晰，分点展示
                3. 适配移动端阅读
                """
                optimized_resume = call_ai(prompt)
                if optimized_resume:
                    st.markdown("### 📄 优化后的简历：")
                    st.write(optimized_resume)
                    # 增加复制按钮（移动端可用）
                    st.code(optimized_resume, language="text")
        else:
            st.warning("⚠️ 请填写岗位要求和个人经历")

# 求职信生成功能
elif function == "求职信生成":
    st.markdown("<h2 style='font-size: 20px;'>✉️ AI求职信生成</h2>", unsafe_allow_html=True)
    
    company_info = st.text_area(
        "公司及岗位信息",
        placeholder="请输入公司名称、岗位名称及岗位职责...",
        height=150,
        key="company_info"
    )
    personal_intro = st.text_area(
        "个人介绍",
        placeholder="请输入你的个人优势、求职动机...",
        height=150,
        key="personal_intro"
    )
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        generate_btn = st.button("🚀 生成求职信", use_container_width=True)
    
    if generate_btn:
        if company_info and personal_intro:
            with st.spinner("AI 正在生成求职信..."):
                prompt = f"""
                你是专业的求职顾问，请根据公司信息和个人介绍，生成一封真诚、专业的求职信。
                公司及岗位信息：{company_info}
                个人介绍：{personal_intro}
                要求：
                1. 突出与岗位的匹配度
                2. 表达真诚的求职意愿
                3. 语言简洁，适配移动端阅读
                """
                cover_letter = call_ai(prompt)
                if cover_letter:
                    st.markdown("### 📄 生成的求职信：")
                    st.write(cover_letter)
                    st.code(cover_letter, language="text")
        else:
            st.warning("⚠️ 请填写公司信息和个人介绍")

# 面试题预测功能
elif function == "面试题预测":
    st.markdown("<h2 style='font-size: 20px;'>🎯 AI面试题预测</h2>", unsafe_allow_html=True)
    
    job_desc = st.text_area(
        "岗位描述",
        placeholder="请输入完整的岗位描述...",
        height=150,
        key="job_desc"
    )
    experience_level = st.selectbox(
        "经验等级", 
        ["应届生", "1-3年", "3-5年"],
        key="exp_level"
    )
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        generate_btn = st.button("🚀 生成面试题", use_container_width=True)
    
    if generate_btn:
        if job_desc:
            with st.spinner("AI 正在生成面试题..."):
                prompt = f"""
                你是资深面试官，请根据岗位描述和候选人经验，生成10道高频面试题及参考答案要点。
                岗位描述：{job_desc}
                候选人经验：{experience_level}
                要求：
                1. 题目分点清晰
                2. 答案要点简洁明了
                3. 适配移动端阅读
                """
                questions = call_ai(prompt)
                if questions:
                    st.markdown("### 📄 生成的面试题及参考答案：")
                    st.write(questions)
                    st.code(questions, language="text")
        else:
            st.warning("⚠️ 请填写岗位描述")
