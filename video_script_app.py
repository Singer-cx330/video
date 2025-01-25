import streamlit as st
from openai import OpenAI
import json
from datetime import datetime

# 设置页面配置（必须是第一个 Streamlit 命令）
st.set_page_config(
    page_title="视频脚本生成器",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 更新CSS样式，减少白色背景，优化文字显示
st.markdown("""
<style>
    /* 主题颜色 */
    :root {
        --primary-color: #FF4B4B;
        --text-light: #ffffff;
        --text-dark: #1a1a1a;
        --background-dark: #1E1E1E;
        --background-darker: #141414;
        --accent-color: #FF6B6B;
    }
    
    /* 整体背景 */
    .stApp {
        background-color: var(--background-dark);
    }
    
    /* 标题容器 */
    .title-container {
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--accent-color) 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .title-container h1,
    .title-container p {
        color: var(--text-light);
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        font-weight: 600;
    }
    
    /* 侧边栏样式优化 */
    .css-1d391kg {  /* 侧边栏类名 */
        background-color: var(--background-darker);
        padding: 1rem;
    }
    
    /* 侧边栏容器样式 */
    .sidebar-content {
        background-color: var(--background-darker);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* 设置面板样式 */
    .stSelectbox,
    .stSlider,
    .stMultiSelect,
    .stTextInput {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .stSelectbox:hover,
    .stSlider:hover,
    .stMultiSelect:hover,
    .stTextInput:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    /* 输入框样式优化 */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox select {
        background-color: var(--background-darker) !important;
        color: var(--text-light) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        padding: 0.8rem !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stSelectbox select:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 2px rgba(255, 75, 75, 0.2) !important;
    }
    
    /* 标签样式优化 */
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stSlider label {
        color: var(--text-light) !important;
        font-weight: 500 !important;
        margin-bottom: 0.5rem !important;
        font-size: 0.9rem !important;
    }
    
    /* 分组标题样式 */
    .sidebar .stMarkdown h1,
    .sidebar .stMarkdown h2,
    .sidebar .stMarkdown h3 {
        color: var(--text-light) !important;
        font-size: 1.2rem !important;
        margin-bottom: 1rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid rgba(255, 75, 75, 0.3);
    }
    
    /* 展开面板样式 */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .streamlit-expanderContent {
        background-color: var(--background-darker) !important;
        border-radius: 0 0 10px 10px !important;
        padding: 1rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-top: none !important;
    }
    
    /* 滑块容器样式优化 */
    .slider-wrapper {
        margin: 1rem 0;
        padding: 0.5rem 0;
    }
    
    /* 移除滑块的背景框 */
    .stSlider {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    
    /* 滑块轨道样式 */
    .stSlider div[data-baseweb="slider"] div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        height: 4px !important;
    }
    
    /* 滑块手柄样式 */
    .stSlider div[data-baseweb="slider"] div[role="slider"] {
        background-color: var(--primary-color) !important;
        border: 2px solid white !important;
        height: 16px !important;
        width: 16px !important;
        border-radius: 50% !important;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* 数字输入框样式 */
    .custom-number-input {
        width: 80px !important;
        background-color: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 5px !important;
        color: var(--text-light) !important;
        padding: 0.3rem !important;
        text-align: center !important;
    }
    
    /* 滑块标签样式 */
    .slider-label {
        color: var(--text-light);
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* 当前值显示样式 */
    .current-value {
        color: var(--primary-color);
        font-weight: 500;
    }
    
    /* 语气风格滑块的标记样式 */
    .tone-marker {
        position: absolute;
        color: var(--text-light);
        font-size: 0.8rem;
        opacity: 0.7;
    }
    
    /* 当前选择的语气提示 */
    .tone-indicator {
        color: var(--text-light);
        text-align: center;
        margin-top: 0.5rem;
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    /* 多选框样式 */
    .stMultiSelect div[role="listbox"] {
        background-color: var(--background-darker) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    .stMultiSelect div[role="option"] {
        color: var(--text-light) !important;
        padding: 0.5rem 1rem !important;
    }
    
    .stMultiSelect div[role="option"]:hover {
        background-color: rgba(255, 75, 75, 0.1) !important;
    }
    
    /* 帮助文本图标样式 */
    .stTooltipIcon {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    /* 选项卡样式优化 */
    .stTabs {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 1rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0 !important;
        padding: 0.8rem 1.5rem !important;
        margin-right: 0.5rem !important;
    }
    
    /* 输入框样式 */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox select {
        background-color: var(--background-darker) !important;
        color: var(--text-light) !important;
        border: 1px solid #333 !important;
    }
    
    /* 标签文字 */
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stSlider label {
        color: var(--text-light) !important;
        font-weight: 500 !important;
    }
    
    /* 按钮样式 */
    .stButton>button {
        background-color: var(--primary-color) !important;
        color: var(--text-light) !important;
        border: none !important;
        font-weight: 600;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    /* 标签页 */
    .stTabs [data-baseweb="tab"] {
        background-color: var(--background-darker);
        color: var(--text-light) !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--primary-color);
    }
    
    /* 内容区域 */
    .content-container {
        background-color: var(--background-darker);
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #333;
    }
    
    /* 文本颜色 */
    p, h1, h2, h3, h4, h5, h6, span, div {
        color: var(--text-light) !important;
    }
    
    /* 帮助文本 */
    .stMarkdown div {
        color: #999 !important;
    }
    
    /* 选择框 */
    .stSelectbox>div>div {
        background-color: var(--background-darker) !important;
    }
    
    /* 滑块 */
    .stSlider>div>div {
        background-color: var(--background-darker) !important;
    }
    
    /* 复选框 */
    .stCheckbox label {
        color: var(--text-light) !important;
    }
    
    /* 分割线 */
    hr {
        border-color: #333;
    }
    
    /* 错误信息 */
    .stAlert {
        background-color: var(--background-darker) !important;
        color: var(--primary-color) !important;
        border: 1px solid var(--primary-color) !important;
    }
    
    /* 历史记录项 */
    .history-item {
        background-color: var(--background-darker);
        border: 1px solid #333;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    /* 空状态 */
    .empty-state {
        background-color: var(--background-darker);
        border: 1px solid #333;
        text-align: center;
        padding: 2rem;
    }
    
    /* 滚动条 */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--background-darker);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 4px;
    }
    
    /* 链接 */
    a {
        color: var(--primary-color) !important;
    }
    
    /* JSON 显示 */
    .stJson {
        background-color: var(--background-darker) !important;
        color: var(--text-light) !important;
    }
    
    /* 统一下拉框样式 */
    .stSelectbox > div[data-baseweb="select"] {
        background-color: var(--background-darker) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
    }
    
    .stSelectbox > div[data-baseweb="select"]:hover {
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    
    .stSelectbox > div[data-baseweb="select"] > div {
        background-color: transparent !important;
        color: var(--text-light) !important;
    }
    
    /* 下拉选项样式 */
    div[data-baseweb="popover"] div[data-baseweb="menu"] {
        background-color: var(--background-darker) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
    }
    
    div[data-baseweb="popover"] div[role="option"] {
        color: var(--text-light) !important;
        background-color: transparent !important;
    }
    
    div[data-baseweb="popover"] div[role="option"]:hover {
        background-color: rgba(255, 75, 75, 0.1) !important;
    }
    
    /* 选中项样式 */
    div[data-baseweb="popover"] div[aria-selected="true"] {
        background-color: rgba(255, 75, 75, 0.2) !important;
    }
    
    /* 标签样式统一 */
    .stSelectbox label {
        color: var(--text-light) !important;
        font-weight: 500 !important;
        margin-bottom: 0.5rem !important;
        font-size: 0.9rem !important;
    }
    
    /* 选项组容器样式 */
    .stSelectbox, .stMultiSelect {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* 悬停效果 */
    .stSelectbox:hover, .stMultiSelect:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# 在 Session State 中初始化所有状态
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''
if 'history' not in st.session_state:
    st.session_state.history = []
if 'template' not in st.session_state:
    st.session_state.template = None
if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False
if 'current_script' not in st.session_state:
    st.session_state.current_script = None

# 使用HTML创建更美观的标题
st.markdown("""
<div class="title-container">
    <h1>🎬 智能视频脚本生成器</h1>
    <p>专业的视频脚本一键生成工具</p>
</div>
""", unsafe_allow_html=True)

# 侧边栏美化
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0;">
        <h2 style="color: #FF4B4B;">⚙️ 设置面板</h2>
    </div>
    """, unsafe_allow_html=True)
    
    tabs = st.tabs(["基本设置", "高级设置", "模板"])
    
    with tabs[0]:
        st.header("基本设置")
        # API密钥输入
        api_key = st.text_input(
            "DeepSeek API 密钥",
            type="password",
            value=st.session_state.api_key,
            help="请输入您的 DeepSeek API 密钥"
        )
        
        if api_key:
            st.session_state.api_key = api_key
        
        # 高级设置折叠面板
        with st.expander("高级设置"):
            temperature = st.slider(
                "创意程度",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                help="较低的值会产生更保守的结果，较高的值会产生更有创意的结果"
            )
            max_tokens = st.slider(
                "最大生成长度",
                min_value=500,
                max_value=4000,
                value=2000,
                help="控制生成文本的最大长度"
            )
        
        st.header("脚本设置")
        video_type = st.selectbox(
            "选择视频类型",
            ["教育视频", "产品介绍", "故事叙述", "新闻报道", 
             "Vlog", "纪录片", "广告", "短视频", "直播脚本"]
        )
        
        target_audience = st.multiselect(
            "目标受众",
            ["儿童", "青少年", "年轻人", "中年人", "老年人", "专业人士", "普通大众"],
            default=["普通大众"]
        )
        
        # 修改视频时长为自定义输入
        st.markdown('<div class="slider-wrapper">', unsafe_allow_html=True)
        col_dur1, col_dur2 = st.columns([4, 1])
        with col_dur1:
            duration = st.slider(
                "视频时长（分钟）",
                min_value=1,
                max_value=60,
                value=5,
                help="拖动选择视频时长"
            )
        with col_dur2:
            duration = st.number_input(
                "",
                min_value=1,
                max_value=60,
                value=duration,
                key="duration_input"
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 先定义一个函数来获取语气风格
        def get_tone_from_value(value):
            if value < 20:
                return "严肃"
            elif value < 40:
                return "正式"
            elif value < 60:
                return "中性"
            elif value < 80:
                return "轻松"
            else:
                return "幽默"

        # 在语气风格滑块之前初始化默认值
        tone_value = st.session_state.get('tone_value', 50)
        tone = get_tone_from_value(tone_value)

        # 修改语气风格为滑块
        st.markdown('<div class="slider-wrapper">', unsafe_allow_html=True)
        st.markdown(
            '<div class="slider-label">语气风格 '
            f'<span class="current-value">{tone}</span></div>',
            unsafe_allow_html=True
        )
        tone_value = st.slider(
            "",
            min_value=0,
            max_value=100,
            value=tone_value,
            key="tone_slider",
            help="左侧更正式，右侧更轻松"
        )

        # 更新语气风格
        tone = get_tone_from_value(tone_value)
        st.session_state.tone_value = tone_value
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[1]:
        st.header("高级设置")
        
        # 添加新的高级设置
        language = st.selectbox(
            "脚本语言",
            ["中文", "英文", "日文", "韩文"],
            help="选择生成脚本的语言"
        )
        
        include_timestamps = st.checkbox(
            "包含时间戳",
            value=True,
            help="在脚本中添加预估的时间戳"
        )
        
        include_camera_directions = st.checkbox(
            "包含镜头指导",
            value=True,
            help="添加具体的镜头角度和运动建议"
        )
    
    with tabs[2]:
        st.header("模板管理")
        
        # 模板选择
        template_options = {
            "无": None,
            "产品发布会": {
                "structure": "1. 产品亮点展示\n2. 技术细节解析\n3. 价格与上市信息",
                "tone": "正式",
                "duration": 15
            },
            "教学视频": {
                "structure": "1. 学习目标\n2. 概念讲解\n3. 实例演示\n4. 练习建议",
                "tone": "中性",
                "duration": 10
            },
            "品牌故事": {
                "structure": "1. 创始背景\n2. 发展历程\n3. 价值主张\n4. 未来愿景",
                "tone": "温情",
                "duration": 5
            }
        }
        
        selected_template = st.selectbox(
            "选择模板",
            options=list(template_options.keys()),
            help="选择预设的脚本模板"
        )
        
        if selected_template != "无":
            st.session_state.template = template_options[selected_template]
            st.info(f"已加载 {selected_template} 模板")

# 主要内容区域美化
st.markdown("""
<div class="animate-fade-in">
    <h2 style="color: #FF4B4B; margin-bottom: 1rem;">📝 脚本工作台</h2>
</div>
""", unsafe_allow_html=True)

# 使用新的标签页样式
tabs = st.tabs(["✏️ 编辑器", "📚 历史记录"])

with tabs[0]:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        st.subheader("📝 创建新脚本")
        topic = st.text_area(
            "视频主题描述",
            height=150,
            help="详细描述您想要生成的视频主题和关键点"
        )
        
        with st.expander("✨ 更多选项", expanded=True):
            st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
            keywords = st.text_input(
                "🏷️ 关键词",
                help="用逗号分隔的关键词列表"
            )
            
            reference_links = st.text_area(
                "📚 参考资料",
                height=100,
                help="添加参考链接或资料"
            )
            
            special_requirements = st.text_area(
                "⚡ 特殊要求",
                height=100,
                help="添加任何特殊要求或注意事项"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            generate_button = st.button(
                "🚀 开始生成" if not st.session_state.is_generating else "⏳ 生成中...",
                type="primary",
                disabled=st.session_state.is_generating
            )
        with col_btn2:
            if st.session_state.is_generating:
                if st.button("⏹️ 终止生成", type="secondary"):
                    st.session_state.is_generating = False
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if st.session_state.current_script:
            st.markdown('<div class="content-container">', unsafe_allow_html=True)
            st.subheader("✏️ 编辑区域")
            edited_script = st.text_area(
                "当前脚本",
                value=st.session_state.current_script,
                height=400
            )
            
            col_edit1, col_edit2 = st.columns([1, 1])
            with col_edit1:
                if st.button("💾 保存修改"):
                    st.session_state.current_script = edited_script
                    if st.session_state.history:
                        st.session_state.history[-1]["script"] = edited_script
                        st.session_state.history[-1]["edited"] = True
                        st.success("✅ 修改已保存")
            
            with col_edit2:
                if st.button("🔄 重新生成"):
                    st.session_state.current_script = None
                    generate_button = True
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-state">
                <img src="https://img.icons8.com/clouds/100/000000/edit.png">
                <h3>准备开始创作</h3>
                <p style="color: #666;">在左侧输入主题并点击生成按钮，开始创作您的视频脚本</p>
            </div>
            """, unsafe_allow_html=True)

with tabs[1]:
    if st.session_state.history:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        col_hist1, col_hist2 = st.columns([1, 2])
        
        with col_hist1:
            st.subheader("历史记录列表")
            for idx, item in enumerate(reversed(st.session_state.history)):
                with st.container():
                    st.markdown(f"### {idx + 1}. {item['topic'][:30]}...")
                    st.caption(f"类型: {item['type']} | 时间: {item['timestamp']}")
                    col_act1, col_act2 = st.columns([1, 1])
                    with col_act1:
                        if st.button(f"加载 #{idx + 1}", key=f"load_{idx}"):
                            st.session_state.current_script = item['script']
                            st.rerun()
                    with col_act2:
                        if st.button(f"删除 #{idx + 1}", key=f"delete_{idx}"):
                            st.session_state.history.pop(-(idx + 1))
                            st.rerun()
                    st.markdown("---")
        
        with col_hist2:
            st.subheader("预览")
            selected_idx = st.number_input(
                "选择要预览的脚本编号",
                min_value=1,
                max_value=len(st.session_state.history),
                value=1
            )
            if selected_idx:
                item = st.session_state.history[-(selected_idx)]
                st.markdown("### 脚本内容")
                st.markdown(item['script'])
                st.markdown("### 详细信息")
                st.json({
                    "主题": item['topic'],
                    "类型": item['type'],
                    "生成时间": item['timestamp'],
                    "是否编辑过": item.get('edited', False)
                })
        
        # 导出功能
        st.markdown("---")
        col_exp1, col_exp2 = st.columns([1, 1])
        with col_exp1:
            if st.button("导出所有历史记录"):
                history_data = json.dumps(
                    st.session_state.history,
                    ensure_ascii=False,
                    indent=2
                )
                st.download_button(
                    label="下载JSON格式",
                    data=history_data,
                    file_name=f"script_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        with col_exp2:
            if st.button("清除所有历史记录"):
                if st.session_state.history:
                    st.session_state.history = []
                    st.session_state.current_script = None
                    st.success("历史记录已清除")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="stCard" style="text-align: center; padding: 3rem;">
            <img src="https://img.icons8.com/clouds/100/000000/empty-box.png" style="width: 100px; margin-bottom: 1rem;">
            <h3>暂无历史记录</h3>
            <p style="color: #666;">生成您的第一个脚本，开始创作之旅吧！</p>
        </div>
        """, unsafe_allow_html=True)

# 修改生成脚本的部分
if generate_button and not st.session_state.is_generating:
    if not st.session_state.api_key:
        st.error("请先在侧边栏输入您的 DeepSeek API 密钥")
    elif not topic:
        st.error("请输入视频主题")
    else:
        try:
            st.session_state.is_generating = True
            client = OpenAI(
                api_key=st.session_state.api_key,
                base_url="https://api.deepseek.com"
            )
            
            message_placeholder = st.empty()
            full_response = ""
            
            # 优化 prompt
            prompt = f"""
            请为以下视频创作专业脚本：
            
            基本信息：
            - 视频类型：{video_type}
            - 时长：{duration}分钟
            - 目标受众：{', '.join(target_audience)}
            - 语气风格：{tone}
            - 语言：{language}
            
            主题：{topic}
            关键词：{keywords}
            参考资料：{reference_links if reference_links else '无'}
            特殊要求：{special_requirements if special_requirements else '无'}
            
            {f'模板结构：{st.session_state.template["structure"]}' if st.session_state.template else ''}
            
            请按照以下结构编写脚本：
            1. 开场白（吸引观众注意力）
            2. 主要内容（分段呈现，使用转场）
            3. 结束语（包含行动号召）
            4. 建议的背景音乐风格
            5. 视觉效果建议
            6. 拍摄建议和注意事项
            {f'7. 时间戳标注' if include_timestamps else ''}
            {f'8. 镜头指导' if include_camera_directions else ''}
            """
            
            # 使用流式输出
            with st.spinner("正在生成脚本..."):
                stream = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是一位专业的视频脚本编剧，擅长创作引人入胜的视频内容"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True
                )
                
                # 实时显示生成的内容
                for chunk in stream:
                    if not st.session_state.is_generating:
                        break
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
                if st.session_state.is_generating:  # 只有在未终止的情况下才保存
                    st.session_state.current_script = full_response
                    st.session_state.history.append({
                        "topic": topic,
                        "type": video_type,
                        "script": full_response,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "edited": False
                    })
                
                st.session_state.is_generating = False
                
        except Exception as e:
            st.error(f"生成脚本时出现错误：{str(e)}")
            st.session_state.is_generating = False

# 美化页脚
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #666;">
    <hr>
    <p>由 DeepSeek API 提供支持 | 🎯 生成专业的视频脚本</p>
    <p style="font-size: 0.8rem;">© 2024 视频脚本生成器 - 让创作更简单</p>
</div>
""", unsafe_allow_html=True) 