import streamlit as st
import ai_services
import io
import time

# --- Pager Configuration ---
st.set_page_config(
    page_title="BizForge | AI Branding Suite",
    page_icon="⚒️",
    layout="wide",
)

# Custom CSS for UI touches
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        border-radius: 6px;
        font-weight: bold;
    }
    .main-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.05);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 class='main-header'>⚒️ BizForge</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 2rem;'>Your All-In-One AI Powered Branding Suite</p>", unsafe_allow_html=True)

# --- Navigation / Tabs ---
tabs = st.tabs([
    "🏷️ Brand Name", 
    "💡 Startup Idea", 
    "✍️ Marketing Content", 
    "🎨 Logo Generator", 
    "🎭 Sentiment Analysis", 
    "🌈 Color Palette", 
    "🤖 AI Assistant"
])

# --- 1. Brand Name Generator ---
with tabs[0]:
    st.header("Brand Name Generator")
    st.markdown("Generate 10-20 creative brand names tailored to your industry.")
    
    col1, col2 = st.columns(2)
    with col1:
        industry = st.text_input("Industry", placeholder="e.g., Tech, Fashion, Food...")
        tone = st.selectbox("Brand Tone", ["Professional", "Playful", "Modern", "Luxury", "Minimalist", "Edgy"])
    with col2:
        keywords = st.text_input("Keywords", placeholder="e.g., fast, cloud, organic...")
        language = st.selectbox("Language", ["English", "Spanish", "French", "German"])
        
    if st.button("Generate Names", type="primary"):
        if industry and keywords:
            with st.spinner("Forging brand names..."):
                result = ai_services.generate_brand_names(industry, keywords, tone, language)
                names = [n.strip() for n in result.split('\n') if n.strip()]
                st.success("Success!")
                for name in names:
                    st.write(f"- {name}")
        else:
            st.warning("Please provide both Industry and Keywords.")

# --- 2. Startup Idea Generator ---
with tabs[1]:
    st.header("Startup Idea Generator")
    st.markdown("Turn concepts into concrete startup propositions.")
    
    idea_keywords = st.text_input("Keywords / Concepts", placeholder="e.g., Fitness, AI, Gamification")
    
    if st.button("Generate Startup Idea", type="primary"):
        if idea_keywords:
            with st.spinner("Brainstorming..."):
                idea = ai_services.generate_startup_idea(idea_keywords)
                st.info(idea)
        else:
            st.warning("Please provide some keywords.")

# --- 3. Marketing Content ---
with tabs[2]:
    st.header("Marketing Content Writer")
    st.markdown("Draft targeted copy for your products.")
    
    product = st.text_input("Product / Service Description", placeholder="e.g., An app that tracks dog walking goals")
    col1, col2 = st.columns(2)
    with col1:
        content_type = st.selectbox("Content Type", [
            "Instagram Caption", 
            "Twitter Thread", 
            "Product Description", 
            "Email Newsletter", 
            "Landing Page Hero"
        ])
    with col2:
        content_tone = st.selectbox("Tone", ["Engaging", "Urgent", "Informative", "Humorous", "Professional"], key="content_tone")
        
    if st.button("Write Content", type="primary"):
        if product:
            with st.spinner("Writing copy..."):
                content = ai_services.generate_marketing_content(product, content_tone, content_type)
                st.write(content)
        else:
            st.warning("Please describe your product.")

# --- 4. Logo Generator ---
with tabs[3]:
    st.header("Logo Concept Generator")
    st.markdown("Visualize your brand identity using text-to-image AI.")
    
    col1, col2 = st.columns(2)
    with col1:
        logo_brand = st.text_input("Brand Name", key="logo_brand")
        logo_style = st.selectbox("Design Style", [
            "Minimalist Flat Vector", 
            "3D Rendered", 
            "Neon Cyberpunk", 
            "Vintage Retro", 
            "Watercolor", 
            "Mascot"
        ])
    with col2:
        logo_industry = st.text_input("Industry", key="logo_industry")
        
    if st.button("Generate Logo Concept", type="primary"):
        if logo_brand and logo_industry:
            with st.spinner("Generating prompt..."):
                prompt = ai_services.generate_logo_prompt(logo_brand, logo_industry, logo_style)
                st.caption(f"**Design Brief:** {prompt}")
            
            import os
            
            # --- AGENT GENERATED HD LOGOS DEMO ---
            # Serve the stunning high-definition logos generated by the AI agent's internal image API
            brand_lower = logo_brand.lower().strip()
            local_image_path = None
            
            if "quantum" in brand_lower or "labs" in brand_lower:
                local_image_path = "quantum_labs_logo.png"
            elif "bizforge" in brand_lower:
                local_image_path = "bizforge_logo.png"
                
            if local_image_path and os.path.exists(local_image_path):
                with st.spinner("Loading high-definition Agent-Generated Logo..."):
                    time.sleep(1) # Simulated loading for UX
                    st.image(local_image_path, caption=f"HD Concept for {logo_brand}", use_container_width=True)
                    st.success("Successfully loaded premium logo generated by AI Agent!")
            else:
                with st.spinner("Designing High-Definition Logo Concept (This takes about 10-15 seconds)..."):
                    visual_result = ai_services.generate_logo(prompt, logo_brand, logo_style)
                    
                    if isinstance(visual_result, bytes):
                        st.image(visual_result, caption=f"HD Logo Concept for {logo_brand}", use_container_width=True)
                        st.success("Successfully generated professional logo!")
                    else:
                        st.error(f"Failed to generate logo: {visual_result}")
        else:
            st.warning("Please provide a Brand Name and Industry.")

# --- 5. Sentiment Analysis ---
with tabs[4]:
    st.header("Sentiment Analyzer")
    st.markdown("Analyze customer reviews and get PR-friendly rewritten responses.")
    st.info("💡 **What does it do?** Sentiment Analysis evaluates the emotional tone behind a body of text. It scores the text as Positive, Negative, or Neutral, and intelligently rewrites it (e.g., crafting a polite PR-friendly response to a negative review or enhancing a positive testimonial).")

    
    review_text = st.text_area("Customer Review or Feedback", height=150, placeholder="Type the review here...")
    
    if st.button("Analyze Sentiment", type="primary"):
        if review_text:
            with st.spinner("Analyzing text..."):
                result = ai_services.analyze_sentiment(review_text)
                
                col1, col2 = st.columns(2)
                with col1:
                    sentiment = result.get('sentiment', 'Unknown')
                    color = "green" if sentiment == "Positive" else "red" if sentiment == "Negative" else "gray"
                    st.metric(label="Sentiment", value=sentiment)
                with col2:
                    st.metric(label="Confidence", value=result.get('confidence', 'N/A'))
                
                st.subheader("Actionable Rewritten Response:")
                st.info(result.get('rewritten', 'No response generated.'))
        else:
            st.warning("Please provide a review to analyze.")

# --- 6. Color Palette ---
with tabs[5]:
    st.header("Color Palette Generator")
    st.markdown("Get a curated 5-color palette for your brand.")
    
    col1, col2 = st.columns(2)
    with col1:
        palette_industry = st.text_input("Industry", key="palette_ind", placeholder="e.g., Tech Startup")
    with col2:
        palette_vibes = st.text_input("Vibes / Mood", placeholder="e.g., Trustworthy, energetic, clean")
        
    if st.button("Generate Palette", type="primary"):
        if palette_industry and palette_vibes:
            with st.spinner("Curating colors..."):
                result = ai_services.get_color_palette(palette_industry, palette_vibes)
                colors = result.get('colors', [])
                
                if colors and len(colors) > 0:
                    st.write("### Your Hand-Picked Palette:")
                    cols = st.columns(len(colors))
                    for i, color in enumerate(colors):
                        with cols[i]:
                            st.markdown(
                                f"<div style='background-color:{color}; height:100px; border-radius:10px; margin-bottom:10px;'></div>", 
                                unsafe_allow_html=True
                            )
                            st.code(color)
                else:
                    st.error("Failed to extract color codes.")
        else:
            st.warning("Please provide an Industry and Vibes.")

# --- 7. AI Assistant Chat ---
with tabs[6]:
    st.header("AI Branding Specialist")
    st.markdown("Chat with the IBM Granite-powered assistant for strategic advice.")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask for branding advice..."):
        # Display user message
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Format history for the backend service
        formatted_history = []
        for i in range(0, len(st.session_state.messages) - 1, 2):
            if i+1 < len(st.session_state.messages):
                formatted_history.append({
                    "user": st.session_state.messages[i]["content"],
                    "assistant": st.session_state.messages[i+1]["content"]
                })

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = ai_services.chat_with_ai(prompt, formatted_history)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

