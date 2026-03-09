import streamlit as st
from groq import Groq
import google.generativeai as genai
from datetime import datetime
import os
import json

# Page config
st.set_page_config(page_title="LLM Bridge - Instagram Marketing",
                   page_icon="🌉",
                   layout="wide")

# Custom CSS
st.markdown("""
<style>
    .llm-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .groq-output {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #2196F3;
        margin: 10px 0;
    }
    .gemini-output {
        background-color: #f3e5f5;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #9c27b0;
        margin: 10px 0;
    }
    .merged-output {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin: 10px 0;
    }
    .agreement {
        color: #4caf50;
        font-weight: bold;
    }
    .disagreement {
        color: #ff9800;
        font-weight: bold;
    }
</style>
""",
            unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'product_info' not in st.session_state:
    st.session_state.product_info = {}
if 'groq_analysis' not in st.session_state:
    st.session_state.groq_analysis = None
if 'gemini_analysis' not in st.session_state:
    st.session_state.gemini_analysis = None
if 'merged_campaign' not in st.session_state:
    st.session_state.merged_campaign = None

# Get API keys
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Initialize clients
try:
    groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-2.5-flash')
    else:
        gemini_model = None
except Exception as e:
    st.error(f"Error: {e}")
    groq_client = None
    gemini_model = None

# Title
st.title("🌉 LLM Bridge: Instagram Marketing AI")
st.markdown("**Multi-Model Intelligence for RareRegalia Campaigns**")

# Check API keys
if not GROQ_API_KEY or not GEMINI_API_KEY:
    st.warning("⚠️ Please add API keys to Replit Secrets")
    st.stop()

# Progress tracker
progress_cols = st.columns(4)
with progress_cols[0]:
    st.metric("Step 1", "Product Info",
              "✓" if st.session_state.step > 1 else "→")
with progress_cols[1]:
    st.metric("Step 2", "AI Analysis",
              "✓" if st.session_state.step > 2 else "→")
with progress_cols[2]:
    st.metric("Step 3", "LLM Bridge",
              "✓" if st.session_state.step > 3 else "→")
with progress_cols[3]:
    st.metric("Step 4", "Campaign", "✓" if st.session_state.step > 4 else "→")

st.markdown("---")

# STEP 1: Product Information
if st.session_state.step == 1:
    st.markdown("### 📸 Step 1: Tell Us About Your Product")

    col1, col2 = st.columns(2)

    with col1:
        product_name = st.text_input("Product Name", "Solitaire Diamond Ring")
        product_type = st.selectbox("Product Type", [
            "Engagement Ring", "Wedding Band", "Necklace", "Earrings",
            "Bracelet"
        ])
        price = st.number_input("Price (₹)",
                                min_value=1000,
                                max_value=10000000,
                                value=75000,
                                step=5000)

    with col2:
        campaign_goal = st.selectbox("Campaign Goal", [
            "Sales (Conversions)", "Website Traffic", "Brand Awareness",
            "Engagement"
        ])
        budget = st.number_input("Campaign Budget (₹)",
                                 min_value=500,
                                 max_value=1000000,
                                 value=15000,
                                 step=1000)
        duration = st.selectbox("Campaign Duration",
                                ["7 days", "14 days", "30 days"])

    product_description = st.text_area(
        "Product Description (Optional)",
        "Elegant 1-carat lab-grown diamond solitaire ring with platinum band. Ethically sourced, certified, perfect for engagements.",
        height=100)

    target_audience_notes = st.text_input(
        "Target Audience Notes (Optional)",
        "Engaged couples, 24-34, Mumbai/Delhi, conscious consumers")

    if st.button("🚀 Start AI Analysis",
                 type="primary",
                 use_container_width=True):
        st.session_state.product_info = {
            "name": product_name,
            "type": product_type,
            "price": price,
            "goal": campaign_goal,
            "budget": budget,
            "duration": duration,
            "description": product_description,
            "audience_notes": target_audience_notes
        }
        st.session_state.step = 2
        st.rerun()

# STEP 2: Parallel AI Analysis
elif st.session_state.step == 2:
    st.markdown("### 🤖 Step 2: AI Models Analyzing...")

    info = st.session_state.product_info

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### ⚡ Groq (Performance Brain)")
        with st.spinner("Groq analyzing..."):
            groq_prompt = f"""You are a performance marketing expert analyzing this Instagram ad campaign for RareRegalia (lab-grown diamond jewelry in India).

Product: {info['name']}
Type: {info['type']}
Price: ₹{info['price']:,}
Goal: {info['goal']}
Budget: ₹{info['budget']:,}
Duration: {info['duration']}
Description: {info['description']}

Provide a data-driven analysis with:
1. Target Audience (demographics, age, location, behavior)
2. Ad Copy Hooks (3 performance-focused options, punchy and direct)
3. Campaign Strategy (placement, budget allocation, timing)
4. Key Metrics to track

Be analytical, numbers-focused, and conversion-oriented. Keep it under 400 words."""

            try:
                groq_response = groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{
                        "role": "user",
                        "content": groq_prompt
                    }],
                    max_tokens=2000,
                    temperature=0.4)
                groq_analysis = groq_response.choices[0].message.content
                st.session_state.groq_analysis = groq_analysis
            except Exception as e:
                groq_analysis = f"Error: {str(e)}"
                st.session_state.groq_analysis = groq_analysis

        st.markdown('<div class="groq-output">', unsafe_allow_html=True)
        st.markdown(groq_analysis)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("#### 🌟 Gemini (Creative Brain)")
        with st.spinner("Gemini analyzing..."):
            gemini_prompt = f"""You are a creative brand strategist analyzing this Instagram campaign for RareRegalia (lab-grown diamond jewelry in India).

Product: {info['name']}
Type: {info['type']}
Price: ₹{info['price']:,}
Goal: {info['goal']}
Budget: ₹{info['budget']:,}
Duration: {info['duration']}
Description: {info['description']}

Provide a creative analysis with:
1. Brand Positioning (emotional angle, storytelling)
2. Ad Copy Hooks (3 creative, emotion-focused options)
3. Visual & Content Ideas (carousel, stories, reels)
4. Audience Psychographics (values, lifestyle, motivations)

Be creative, brand-focused, and emotionally resonant. Keep it under 400 words."""

            try:
                gemini_response = gemini_model.generate_content(
                    gemini_prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=2000,
                        temperature=0.7,
                    ))
                gemini_analysis = gemini_response.text
                st.session_state.gemini_analysis = gemini_analysis
            except Exception as e:
                gemini_analysis = f"Error: {str(e)}"
                st.session_state.gemini_analysis = gemini_analysis

        st.markdown('<div class="gemini-output">', unsafe_allow_html=True)
        st.markdown(gemini_analysis)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Product Info"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("🔗 Merge & Synthesize →",
                     type="primary",
                     use_container_width=True):
            st.session_state.step = 3
            st.rerun()

# STEP 3: LLM Bridge - Merge & Debate
elif st.session_state.step == 3:
    st.markdown("### 🌉 Step 3: LLM Bridge - Synthesis & Consensus")

    info = st.session_state.product_info
    groq_analysis = st.session_state.groq_analysis
    gemini_analysis = st.session_state.gemini_analysis

    with st.spinner("Bridge synthesizing insights from both models..."):

        # Send to Gemini to synthesize (since it's better at reasoning)
        bridge_prompt = f"""You are the LLM Bridge Synthesizer. Two AI models have analyzed an Instagram campaign for RareRegalia. Your job is to merge their insights and create a superior strategy.

GROQ'S ANALYSIS (Performance-focused):
{groq_analysis}

GEMINI'S ANALYSIS (Creative-focused):
{gemini_analysis}

PRODUCT CONTEXT:
{info['name']} - ₹{info['price']:,}
Goal: {info['goal']}
Budget: ₹{info['budget']:,} for {info['duration']}

Create a MERGED CAMPAIGN STRATEGY that:
1. CONSENSUS AREAS (where both models agree)
2. COMPLEMENTARY INSIGHTS (combine Groq's data + Gemini's creativity)
3. CONFLICTS (where they disagree, and your recommendation)
4. FINAL UNIFIED STRATEGY with:
   - Target Audience (merge demographics + psychographics)
   - Top 3 Ad Hooks (best from both, or hybrid versions)
   - Campaign Setup (budget, placement, timing)
   - Success Metrics

Format clearly with sections. Be decisive and actionable. ~500 words."""

        try:
            bridge_response = gemini_model.generate_content(
                bridge_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2000,
                    temperature=0.6,
                ))
            merged_campaign = bridge_response.text
            st.session_state.merged_campaign = merged_campaign
        except Exception as e:
            merged_campaign = f"Error: {str(e)}"
            st.session_state.merged_campaign = merged_campaign

    st.markdown('<div class="merged-output">', unsafe_allow_html=True)
    st.markdown("#### 🎯 SYNTHESIZED CAMPAIGN STRATEGY")
    st.markdown(merged_campaign)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Show comparison
    with st.expander("📊 View Model Comparison"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**⚡ Groq's Approach**")
            st.markdown(groq_analysis)
        with col2:
            st.markdown("**🌟 Gemini's Approach**")
            st.markdown(gemini_analysis)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Analysis"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("📋 Generate Campaign Package →",
                     type="primary",
                     use_container_width=True):
            st.session_state.step = 4
            st.rerun()

# STEP 4: Final Campaign Package
elif st.session_state.step == 4:
    st.markdown("### 📦 Step 4: Your Complete Campaign Package")

    info = st.session_state.product_info
    merged_campaign = st.session_state.merged_campaign

    # Generate detailed campaign specs
    with st.spinner("Generating complete campaign specifications..."):

        specs_prompt = f"""Based on this merged campaign strategy, create a DETAILED INSTAGRAM ADS MANAGER SETUP GUIDE.

MERGED STRATEGY:
{merged_campaign}

PRODUCT: {info['name']} - ₹{info['price']:,}
BUDGET: ₹{info['budget']:,} for {info['duration']}

Provide:

**CAMPAIGN STRUCTURE:**
- Campaign Objective (exact Instagram option)
- Campaign Budget Optimization settings

**AD SET DETAILS (2-3 ad sets):**
For each ad set:
- Name
- Target Audience (detailed: age, gender, location, interests, behaviors)
- Placements (Feed/Stories/Reels)
- Budget allocation
- Schedule

**AD CREATIVE:**
- 3 Ad copy variations (Primary Text + Headline + CTA)
- Image/Video recommendations
- Story sequence ideas

**TRACKING:**
- Pixel events to track
- Success metrics
- Optimization tips

**BUDGET BREAKDOWN:**
Show exactly how ₹{info['budget']:,} should be split

Format as a step-by-step implementation guide. ~600 words."""

        try:
            specs_response = gemini_model.generate_content(
                specs_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=1200,
                    temperature=0.5,
                ))
            campaign_specs = specs_response.text
        except Exception as e:
            campaign_specs = f"Error: {str(e)}"

    # Display campaign package
    st.markdown("#### 🎯 Campaign Specifications")
    st.markdown(campaign_specs)

    st.markdown("---")

    # Export options
    st.markdown("#### 📥 Export Options")

    col1, col2, col3 = st.columns(3)

    with col1:
        full_export = f"""
RAREREGALIA INSTAGRAM CAMPAIGN
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Product: {info['name']}
Budget: ₹{info['budget']:,}
Duration: {info['duration']}

=== GROQ ANALYSIS ===
{st.session_state.groq_analysis}

=== GEMINI ANALYSIS ===
{st.session_state.gemini_analysis}

=== MERGED STRATEGY ===
{merged_campaign}

=== CAMPAIGN SPECIFICATIONS ===
{campaign_specs}
"""
        st.download_button(
            "📄 Download Full Report",
            full_export,
            file_name=
            f"rareregalia_campaign_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True)

    with col2:
        if st.button("🔄 Start New Campaign", use_container_width=True):
            st.session_state.step = 1
            st.session_state.product_info = {}
            st.session_state.groq_analysis = None
            st.session_state.gemini_analysis = None
            st.session_state.merged_campaign = None
            st.rerun()

    with col3:
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []

        if st.button("💬 Get AI Advice", use_container_width=True):
            st.session_state.show_chat = not st.session_state.get("show_chat", False)

    if st.session_state.get("show_chat", False):
        st.markdown("---")
        st.markdown("#### 💬 AI Campaign Assistant")
        
        # Display chat messages
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Chat input logic
        def handle_chat():
            user_input = st.session_state.chat_input
            if user_input:
                # Add user message
                st.session_state.chat_messages.append({"role": "user", "content": user_input})
                
                # Generate AI response
                try:
                    chat_prompt = f"""You are a helpful marketing assistant for RareRegalia. 
                    Based on the current campaign strategy: {st.session_state.merged_campaign}
                    Answer the user's question: {user_input}"""
                    
                    response = gemini_model.generate_content(chat_prompt)
                    st.session_state.chat_messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Chat error: {e}")
                
                # Clear input is handled by st.chat_input itself when used with session state key
                # but in older streamlit versions or specific setups, we might need a rerun
        
        if prompt := st.chat_input("Ask a question about your campaign...", key="chat_input", on_submit=handle_chat):
            # The message is already added in on_submit via handle_chat
            # Streamlit will clear the input automatically because it has a 'key'
            st.rerun()

    st.markdown("---")

    # Show the bridge value
    st.markdown("### 🌉 Why LLM Bridge is Better")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**⚡ Groq Contribution**")
        st.markdown("""
        - Fast analytical thinking
        - Performance metrics focus
        - Data-driven targeting
        - Conversion optimization
        """)

    with col2:
        st.markdown("**🌟 Gemini Contribution**")
        st.markdown("""
        - Creative storytelling
        - Brand positioning
        - Emotional resonance
        - Visual content ideas
        """)

    with col3:
        st.markdown("**🔗 Bridge Synthesis**")
        st.markdown("""
        - Best of both worlds
        - Cross-validation
        - Conflict resolution
        - Superior strategy
        """)

# Sidebar with tips
with st.sidebar:
    st.markdown("### 💡 Tips")
    st.markdown("""
    **How LLM Bridge Works:**

    1. **Parallel Analysis**: Both Groq and Gemini analyze your product simultaneously

    2. **Specialized Strengths**: 
       - Groq → Performance data
       - Gemini → Creative branding

    3. **Synthesis**: Bridge merges insights into superior strategy

    4. **Output**: Campaign better than any single AI could create

    ---

    **For Best Results:**
    - Provide detailed product description
    - Be specific about target audience
    - Set realistic budgets
    - Test multiple approaches
    """)

    st.markdown("---")
    st.markdown("**RareRegalia** 💎")
    st.markdown("Lab-Grown Diamond Jewelry")
    st.markdown("[Visit Website](https://rareregalia.com)")
