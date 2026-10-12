import csv
import io
import math
from datetime import datetime
import streamlit as st

# ==============================================================================
# 1. PAGE CONFIGURATION & PREMIUM STYLING
# ==============================================================================

st.set_page_config(
    page_title="Rajan Calculator",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Theme State Initialization (Dark Mode by default)
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

is_dark = st.session_state.get("dark_mode", True)

# Custom CSS for Modern Dark Premium Calculator UI (Matching Reference Design)
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* Global Font & Reset */
html, body, [class*="css"] {
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
}

/* Hide Default Streamlit Chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Outer App Background - Premium Deep Navy & Midnight Blue Glow */
.stApp {
    background: 
        radial-gradient(circle at 15% 10%, rgba(99, 102, 241, 0.18) 0%, transparent 40%),
        radial-gradient(circle at 85% 85%, rgba(6, 182, 212, 0.16) 0%, transparent 45%),
        radial-gradient(circle at 50% 50%, rgba(139, 92, 246, 0.10) 0%, transparent 50%),
        #070b16 !important;
    color: #f1f5f9;
}

/* Central Calculator Dashboard Container */
.block-container {
    padding-top: 1.8rem !important;
    padding-bottom: 2.2rem !important;
    max-width: 530px !important;
}

/* Header Styling */
.header-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    padding: 0 4px;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.calc-icon-wrapper {
    width: 44px;
    height: 44px;
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(99, 102, 241, 0.25) 100%);
    border: 1px solid rgba(56, 189, 248, 0.35);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 16px rgba(6, 182, 212, 0.25);
}

.calc-icon {
    font-size: 1.6rem;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.4));
}

.calc-title-box {
    display: flex;
    flex-direction: column;
}

.calc-title-text {
    font-size: 1.65rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0;
    line-height: 1.15;
    letter-spacing: -0.5px;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
}

.calc-subtitle {
    font-size: 0.76rem;
    color: #94a3b8;
    margin: 0;
    font-weight: 500;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}

.badge-premium {
    background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 50%, #8b5cf6 100%);
    color: #ffffff;
    font-size: 0.70rem;
    font-weight: 700;
    padding: 5px 12px;
    border-radius: 20px;
    letter-spacing: 1px;
    text-transform: uppercase;
    box-shadow: 0 0 16px rgba(139, 92, 246, 0.45), inset 0 1px 1px rgba(255, 255, 255, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

/* Navigation Radio Tabs Styling (4 Modern Rounded Equal Tabs) */
div[data-testid="stRadio"] {
    margin-bottom: 18px;
}

div[data-testid="stRadio"] > label {
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
    margin-bottom: 8px !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}

div[data-testid="stRadio"] > div[role="radiogroup"] {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    gap: 6px;
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 18px;
    padding: 6px;
    box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.5), 0 4px 15px rgba(0, 0, 0, 0.3);
}

div[data-testid="stRadio"] > div[role="radiogroup"] > label {
    flex: 1;
    text-align: center;
    justify-content: center;
    border-radius: 13px;
    padding: 10px 8px;
    margin: 0;
    font-weight: 600;
    font-size: 0.92rem;
    color: #94a3b8;
    background: transparent;
    border: 1px solid transparent;
    transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
}

div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
    color: #38bdf8;
    background: rgba(56, 189, 248, 0.10);
}

/* Hide Radio Circle Indicator */
div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {
    display: none !important;
}

/* Active Tab Highlight - Blue and Purple Gradient with Glow */
div[data-testid="stRadio"] > div[role="radiogroup"] > label[aria-checked="true"],
div[data-testid="stRadio"] > div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    box-shadow: 0 4px 18px rgba(124, 58, 237, 0.45), inset 0 1px 1px rgba(255, 255, 255, 0.3) !important;
}

/* Main Calculator Card Panel - Glassmorphic Dark Container */
.calc-panel {
    background: rgba(17, 24, 39, 0.85);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(56, 189, 248, 0.22);
    border-radius: 26px;
    padding: 22px 24px;
    box-shadow: 
        0 25px 50px -12px rgba(0, 0, 0, 0.75),
        0 0 30px rgba(99, 102, 241, 0.12),
        inset 0 1px 1px rgba(255, 255, 255, 0.1);
    position: relative;
}

.card-title {
    color: #38bdf8;
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 8px;
    text-shadow: 0 0 12px rgba(56, 189, 248, 0.3);
}

/* Result / Screen Display Styling - OLED Deep Display */
.result-screen {
    background: linear-gradient(180deg, #070b14 0%, #0b1120 100%);
    border: 1px solid rgba(6, 182, 212, 0.3);
    border-radius: 20px;
    padding: 16px 20px;
    margin-bottom: 20px;
    box-shadow: 
        inset 0 2px 10px rgba(0, 0, 0, 0.9),
        0 0 20px rgba(6, 182, 212, 0.12),
        0 1px 1px rgba(255, 255, 255, 0.05);
    min-height: 108px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
}

.result-screen::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.5), transparent);
}

.display-label-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
}

.display-label {
    font-size: 0.68rem;
    font-weight: 700;
    color: #06b6d4;
    text-transform: uppercase;
    letter-spacing: 1.8px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.display-label.error {
    color: #f87171;
}

.display-status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #06b6d4;
    box-shadow: 0 0 8px #06b6d4;
    display: inline-block;
}

.display-status-dot.error {
    background: #ef4444;
    box-shadow: 0 0 8px #ef4444;
}

.display-expr {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.05rem;
    color: #94a3b8;
    text-align: right;
    word-break: break-all;
    min-height: 24px;
    line-height: 1.35;
    letter-spacing: 0.5px;
}

.display-result {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.35rem;
    font-weight: 700;
    color: #38bdf8;
    text-align: right;
    word-break: break-all;
    line-height: 1.15;
    text-shadow: 0 0 18px rgba(56, 189, 248, 0.5);
    letter-spacing: -0.5px;
}

.display-error {
    font-family: 'Outfit', sans-serif;
    font-size: 0.95rem;
    color: #fca5a5;
    text-align: right;
    font-weight: 600;
    word-break: break-word;
    background: rgba(239, 68, 68, 0.15);
    padding: 8px 14px;
    border-radius: 10px;
    border: 1px solid rgba(239, 68, 68, 0.35);
    box-shadow: 0 2px 10px rgba(239, 68, 68, 0.15);
}

/* ==============================================================================
   CALCULATOR BUTTONS STYLING
   ============================================================================== */

/* Base & Number Buttons - Dark Blue Gradient with Subtle Glow */
.stButton > button {
    width: 100%;
    border-radius: 16px !important;
    background: linear-gradient(145deg, #162035 0%, #0d1527 100%) !important;
    color: #f1f5f9 !important;
    font-weight: 600 !important;
    font-size: 1.18rem !important;
    padding: 13px 8px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
    transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.stButton > button:hover {
    background: linear-gradient(145deg, #1e2c47 0%, #131f38 100%) !important;
    color: #38bdf8 !important;
    border-color: rgba(56, 189, 248, 0.5) !important;
    box-shadow: 0 6px 18px rgba(56, 189, 248, 0.22), 0 0 12px rgba(56, 189, 248, 0.15) !important;
    transform: translateY(-2px) !important;
}

.stButton > button:active {
    transform: translateY(1px) scale(0.97) !important;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.4) !important;
}

/* Operator Buttons in Column 4 (÷, ×, −, +) - Purple Accents */
.calc-panel div[data-testid="stHorizontalBlock"] div[data-testid="column"]:nth-child(4) .stButton > button:not([kind="primary"]) {
    background: linear-gradient(145deg, #2e1a47 0%, #1e1333 100%) !important;
    color: #c084fc !important;
    border: 1px solid rgba(168, 85, 247, 0.35) !important;
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4), 0 0 10px rgba(168, 85, 247, 0.15) !important;
}

.calc-panel div[data-testid="stHorizontalBlock"] div[data-testid="column"]:nth-child(4) .stButton > button:not([kind="primary"]):hover {
    background: linear-gradient(145deg, #442268 0%, #2c194a 100%) !important;
    color: #f3e8ff !important;
    border-color: #c084fc !important;
    box-shadow: 0 6px 18px rgba(168, 85, 247, 0.35), 0 0 15px rgba(168, 85, 247, 0.3) !important;
    transform: translateY(-2px) !important;
}

/* Top Row Operator Buttons: ⌫ (col 2) and % (col 3) - Purple Accents */
.calc-panel div[data-testid="stHorizontalBlock"]:nth-of-type(1) div[data-testid="column"]:nth-child(2) .stButton > button,
.calc-panel div[data-testid="stHorizontalBlock"]:nth-of-type(1) div[data-testid="column"]:nth-child(3) .stButton > button {
    background: linear-gradient(145deg, #251b3e 0%, #19142b 100%) !important;
    color: #c084fc !important;
    border: 1px solid rgba(168, 85, 247, 0.3) !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4), 0 0 8px rgba(168, 85, 247, 0.1) !important;
}

.calc-panel div[data-testid="stHorizontalBlock"]:nth-of-type(1) div[data-testid="column"]:nth-child(2) .stButton > button:hover,
.calc-panel div[data-testid="stHorizontalBlock"]:nth-of-type(1) div[data-testid="column"]:nth-child(3) .stButton > button:hover {
    background: linear-gradient(145deg, #3c2660 0%, #261943 100%) !important;
    color: #f3e8ff !important;
    border-color: #c084fc !important;
    box-shadow: 0 6px 16px rgba(168, 85, 247, 0.3) !important;
    transform: translateY(-2px) !important;
}

/* AC Button (type="secondary") - Red Accent with Glow */
div[data-testid="stButton"] > button[kind="secondary"] {
    background: linear-gradient(145deg, rgba(239, 68, 68, 0.20) 0%, rgba(185, 28, 28, 0.28) 100%) !important;
    color: #fca5a5 !important;
    border: 1px solid rgba(239, 68, 68, 0.45) !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.18) !important;
}

div[data-testid="stButton"] > button[kind="secondary"]:hover {
    background: linear-gradient(145deg, rgba(239, 68, 68, 0.38) 0%, rgba(185, 28, 28, 0.50) 100%) !important;
    color: #ffffff !important;
    border-color: #ef4444 !important;
    box-shadow: 0 6px 20px rgba(239, 68, 68, 0.45) !important;
    transform: translateY(-2px) !important;
}

/* Primary Equals (=) & Action Buttons - Cyan-Blue-Purple Gradient */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 50%, #8b5cf6 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    box-shadow: 0 6px 22px rgba(6, 182, 212, 0.45), 0 0 15px rgba(139, 92, 246, 0.35) !important;
}

div[data-testid="stButton"] > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #0891b2 0%, #2563eb 50%, #7c3aed 100%) !important;
    box-shadow: 0 8px 28px rgba(6, 182, 212, 0.65), 0 0 22px rgba(139, 92, 246, 0.5) !important;
    transform: translateY(-2px) scale(1.02) !important;
}

/* Compact Preset Buttons in 5-Column Grid */
div[data-testid="stHorizontalBlock"]:has(div[data-testid="column"]:nth-child(5)) .stButton > button {
    padding: 8px 4px !important;
    font-size: 0.95rem !important;
    border-radius: 12px !important;
    background: linear-gradient(145deg, #131c2e 0%, #0c1220 100%) !important;
    border: 1px solid rgba(56, 189, 248, 0.25) !important;
    color: #38bdf8 !important;
}

div[data-testid="stHorizontalBlock"]:has(div[data-testid="column"]:nth-child(5)) .stButton > button:hover {
    background: linear-gradient(145deg, #1e2c47 0%, #101a2f 100%) !important;
    border-color: #38bdf8 !important;
    box-shadow: 0 0 12px rgba(56, 189, 248, 0.35) !important;
    transform: translateY(-2px) !important;
}

/* ==============================================================================
   INPUTS & CONTROLS STYLING
   ============================================================================== */

.stNumberInput, .stTextInput, .stSelectbox {
    margin-bottom: 14px;
}

.stNumberInput label, .stTextInput label, .stSelectbox label {
    font-weight: 600 !important;
    color: #94a3b8 !important;
    font-size: 0.84rem !important;
    letter-spacing: 0.4px !important;
}

.stNumberInput input, .stTextInput input {
    background: #090e1a !important;
    color: #f8fafc !important;
    border: 1px solid rgba(56, 189, 248, 0.25) !important;
    border-radius: 14px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.05rem !important;
    padding: 12px 14px !important;
    box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.6) !important;
    transition: all 0.2s ease !important;
}

.stNumberInput input:focus, .stTextInput input:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.25), inset 0 2px 6px rgba(0, 0, 0, 0.6) !important;
}

.stSelectbox div[data-baseweb="select"] {
    background: #090e1a !important;
    border-radius: 14px !important;
    border: 1px solid rgba(56, 189, 248, 0.25) !important;
    box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.6) !important;
    transition: all 0.2s ease !important;
}

.stSelectbox div[data-baseweb="select"]:hover {
    border-color: rgba(56, 189, 248, 0.45) !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: transparent !important;
    color: #f8fafc !important;
}

/* Dropdown popover menu */
ul[data-baseweb="menu"] {
    background: #090e1a !important;
    border: 1px solid rgba(56, 189, 248, 0.25) !important;
    border-radius: 14px !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.85) !important;
}

li[data-baseweb="menu-item"] {
    color: #cbd5e1 !important;
}

li[data-baseweb="menu-item"]:hover, li[data-baseweb="menu-item"][aria-selected="true"] {
    background: rgba(56, 189, 248, 0.15) !important;
    color: #38bdf8 !important;
}

/* ==============================================================================
   GST BREAKDOWN CARDS
   ============================================================================== */

.gst-card-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-top: 12px;
}

.gst-metric-box {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 10px 14px;
    display: flex;
    flex-direction: column;
}

.gst-metric-box.highlight {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.12) 0%, rgba(59, 130, 246, 0.16) 100%);
    border-color: rgba(56, 189, 248, 0.35);
}

.gst-metric-title {
    font-size: 0.72rem;
    font-weight: 600;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.gst-metric-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.15rem;
    font-weight: 700;
    color: #a7f3d0;
    margin-top: 2px;
}

.gst-metric-val.accent {
    color: #38bdf8;
}

.gst-metric-val.total {
    color: #38bdf8;
    font-size: 1.35rem;
    text-shadow: 0 0 12px rgba(56, 189, 248, 0.35);
}

/* ==============================================================================
   HISTORY STYLING
   ============================================================================== */

.history-stat-card {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(20, 30, 50, 0.9) 100%);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 18px;
    padding: 14px 16px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.08);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.history-stat-card:hover {
    border-color: rgba(56, 189, 248, 0.5);
    transform: translateY(-2px);
}

.history-stat-title {
    font-size: 0.72rem;
    color: #94a3b8;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}

.history-stat-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.65rem;
    font-weight: 700;
    color: #38bdf8;
    margin-top: 4px;
    text-shadow: 0 0 12px rgba(56, 189, 248, 0.3);
}

.history-container {
    max-height: 380px;
    overflow-y: auto;
    padding-right: 6px;
    margin-bottom: 18px;
}

.history-container::-webkit-scrollbar {
    width: 6px;
}

.history-container::-webkit-scrollbar-track {
    background: rgba(15, 23, 42, 0.5);
    border-radius: 4px;
}

.history-container::-webkit-scrollbar-thumb {
    background: rgba(56, 189, 248, 0.35);
    border-radius: 4px;
}

.history-item-card {
    background: linear-gradient(135deg, #0e1726 0%, #111d30 100%);
    padding: 14px 18px;
    border-radius: 16px;
    margin-bottom: 12px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    transition: all 0.2s ease;
}

.history-item-card:hover {
    border-color: rgba(56, 189, 248, 0.35);
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35), 0 0 15px rgba(56, 189, 248, 0.1);
    transform: translateX(3px);
}

.history-item-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.75rem;
    color: #94a3b8;
    margin-bottom: 8px;
}

.history-badge {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
    color: #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.3);
    padding: 3px 10px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.72rem;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.history-item-math {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1rem;
    color: #f8fafc;
    display: flex;
    justify-content: space-between;
    align-items: center;
    word-break: break-all;
}

.history-idx {
    color: #06b6d4;
    margin-right: 6px;
}

.history-res {
    color: #38bdf8;
    font-size: 1.15rem;
    margin-left: 8px;
}

.history-details {
    font-size: 0.8rem;
    color: #94a3b8;
    margin-top: 6px;
    padding-top: 6px;
    border-top: 1px dashed rgba(255, 255, 255, 0.08);
}

/* Download Button Styling */
.stDownloadButton > button {
    background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    font-weight: 700 !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35) !important;
    padding: 12px 10px !important;
    transition: all 0.2s ease !important;
}

.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #0369a1 0%, #1d4ed8 100%) !important;
    box-shadow: 0 6px 20px rgba(2, 132, 199, 0.5) !important;
    transform: translateY(-2px) !important;
}

/* Footer Section */
.footer-box {
    text-align: center;
    margin-top: 26px;
    padding-top: 16px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.footer-line1 {
    font-size: 0.85rem;
    color: #64748b;
    margin: 0;
}

.footer-line2 {
    font-size: 0.82rem;
    color: #94a3b8;
    font-weight: 500;
    margin: 0;
}

.footer-highlight {
    color: #38bdf8;
    font-weight: 600;
}

.footer-author {
    color: #06b6d4;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-shadow: 0 0 10px rgba(6, 182, 212, 0.4);
}

/* Responsive Breakpoints */
@media (max-width: 640px) {
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1.2rem !important;
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
        max-width: 100% !important;
    }
    .calc-panel {
        padding: 16px !important;
        border-radius: 20px !important;
    }
    .calc-title-text {
        font-size: 1.4rem !important;
    }
    .display-result {
        font-size: 1.9rem !important;
    }
    .stButton > button {
        padding: 11px 4px !important;
        font-size: 1.05rem !important;
        border-radius: 12px !important;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label {
        padding: 8px 4px !important;
        font-size: 0.85rem !important;
    }
}

/* Theme Toggle Switcher */
div[data-testid="stToggle"] {
    display: flex;
    justify-content: flex-end;
    margin-top: -6px;
    margin-bottom: 14px;
}

div[data-testid="stToggle"] label {
    cursor: pointer;
}

div[data-testid="stToggle"] label p {
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
    letter-spacing: 0.3px !important;
}
</style>
"""

# Custom CSS for Modern Light Calculator UI
light_css = """
<style>
/* Outer App Background - Clean White / Soft Glow */
.stApp {
    background: 
        radial-gradient(circle at 15% 10%, rgba(99, 102, 241, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 85% 85%, rgba(6, 182, 212, 0.08) 0%, transparent 45%),
        radial-gradient(circle at 50% 50%, rgba(139, 92, 246, 0.05) 0%, transparent 50%),
        #ffffff !important;
    color: #0f172a !important;
}

/* Header Styling */
.calc-icon-wrapper {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(99, 102, 241, 0.18) 100%) !important;
    border: 1px solid rgba(14, 165, 233, 0.3) !important;
    box-shadow: 0 4px 12px rgba(6, 182, 212, 0.15) !important;
}

.calc-title-text {
    color: #0f172a !important;
    text-shadow: none !important;
}

.calc-subtitle {
    color: #64748b !important;
}

/* Theme Toggle Label in Light Mode */
div[data-testid="stToggle"] label p {
    color: #475569 !important;
}

/* Navigation Radio Tabs Styling */
div[data-testid="stRadio"] > label {
    color: #64748b !important;
}

div[data-testid="stRadio"] > div[role="radiogroup"] {
    background: #f1f5f9 !important;
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05), 0 2px 8px rgba(0, 0, 0, 0.03) !important;
}

div[data-testid="stRadio"] > div[role="radiogroup"] > label {
    color: #64748b !important;
}

div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
    color: #0284c7 !important;
    background: rgba(255, 255, 255, 0.8) !important;
}

/* Main Calculator Card Panel - Light Container */
.calc-panel {
    background: #ffffff !important;
    border: 1px solid rgba(226, 232, 240, 0.9) !important;
    box-shadow: 
        0 20px 40px -12px rgba(0, 0, 0, 0.08),
        0 0 25px rgba(99, 102, 241, 0.05),
        inset 0 1px 1px rgba(255, 255, 255, 1) !important;
}

.card-title {
    color: #0284c7 !important;
    text-shadow: none !important;
}

/* Result / Screen Display Styling - Light Display */
.result-screen {
    background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%) !important;
    border: 1px solid rgba(14, 165, 233, 0.3) !important;
    box-shadow: 
        inset 0 2px 6px rgba(0, 0, 0, 0.04),
        0 4px 15px rgba(6, 182, 212, 0.08),
        0 1px 1px rgba(255, 255, 255, 0.9) !important;
}

.result-screen::before {
    background: linear-gradient(90deg, transparent, rgba(14, 165, 233, 0.4), transparent) !important;
}

.display-label {
    color: #0284c7 !important;
}

.display-status-dot {
    background: #0284c7 !important;
    box-shadow: 0 0 6px #0284c7 !important;
}

.display-expr {
    color: #64748b !important;
}

.display-result {
    color: #0284c7 !important;
    text-shadow: 0 0 12px rgba(2, 132, 199, 0.2) !important;
}

.display-error {
    color: #b91c1c !important;
    background: rgba(239, 68, 68, 0.12) !important;
    border: 1px solid rgba(239, 68, 68, 0.3) !important;
}

/* Calculator Buttons - Base & Number Buttons */
.stButton > button {
    background: linear-gradient(145deg, #ffffff 0%, #f1f5f9 100%) !important;
    color: #0f172a !important;
    border: 1px solid rgba(0, 0, 0, 0.09) !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05), inset 0 1px 0 rgba(255, 255, 255, 1) !important;
}

.stButton > button:hover {
    background: linear-gradient(145deg, #f8fafc 0%, #e2e8f0 100%) !important;
    color: #0284c7 !important;
    border-color: rgba(14, 165, 233, 0.4) !important;
    box-shadow: 0 4px 14px rgba(14, 165, 233, 0.16) !important;
}

/* Operator Buttons in Column 4 (÷, ×, −, +) */
.calc-panel div[data-testid="stHorizontalBlock"] div[data-testid="column"]:nth-child(4) .stButton > button:not([kind="primary"]) {
    background: linear-gradient(145deg, #f5f3ff 0%, #ede9fe 100%) !important;
    color: #7c3aed !important;
    border: 1px solid rgba(168, 85, 247, 0.3) !important;
    box-shadow: 0 2px 6px rgba(124, 58, 237, 0.1) !important;
}

.calc-panel div[data-testid="stHorizontalBlock"] div[data-testid="column"]:nth-child(4) .stButton > button:not([kind="primary"]):hover {
    background: linear-gradient(145deg, #ede9fe 0%, #ddd6fe 100%) !important;
    color: #6d28d9 !important;
    border-color: #a855f7 !important;
    box-shadow: 0 4px 12px rgba(168, 85, 247, 0.25) !important;
}

/* Top Row Operator Buttons: ⌫ (col 2) and % (col 3) */
.calc-panel div[data-testid="stHorizontalBlock"]:nth-of-type(1) div[data-testid="column"]:nth-child(2) .stButton > button,
.calc-panel div[data-testid="stHorizontalBlock"]:nth-of-type(1) div[data-testid="column"]:nth-child(3) .stButton > button {
    background: linear-gradient(145deg, #f5f3ff 0%, #ede9fe 100%) !important;
    color: #7c3aed !important;
    border: 1px solid rgba(168, 85, 247, 0.25) !important;
    box-shadow: 0 2px 6px rgba(124, 58, 237, 0.1) !important;
}

.calc-panel div[data-testid="stHorizontalBlock"]:nth-of-type(1) div[data-testid="column"]:nth-child(2) .stButton > button:hover,
.calc-panel div[data-testid="stHorizontalBlock"]:nth-of-type(1) div[data-testid="column"]:nth-child(3) .stButton > button:hover {
    background: linear-gradient(145deg, #ede9fe 0%, #ddd6fe 100%) !important;
    color: #6d28d9 !important;
    border-color: #a855f7 !important;
    box-shadow: 0 4px 12px rgba(168, 85, 247, 0.25) !important;
}

/* AC Button */
div[data-testid="stButton"] > button[kind="secondary"] {
    background: linear-gradient(145deg, #fee2e2 0%, #fecaca 100%) !important;
    color: #dc2626 !important;
    border: 1px solid rgba(239, 68, 68, 0.35) !important;
    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.12) !important;
}

div[data-testid="stButton"] > button[kind="secondary"]:hover {
    background: linear-gradient(145deg, #fecaca 0%, #fca5a5 100%) !important;
    color: #b91c1c !important;
    border-color: #ef4444 !important;
    box-shadow: 0 4px 14px rgba(239, 68, 68, 0.25) !important;
}

/* Compact Preset Buttons in 5-Column Grid */
div[data-testid="stHorizontalBlock"]:has(div[data-testid="column"]:nth-child(5)) .stButton > button {
    background: linear-gradient(145deg, #f0f9ff 0%, #e0f2fe 100%) !important;
    border: 1px solid rgba(14, 165, 233, 0.25) !important;
    color: #0284c7 !important;
}

div[data-testid="stHorizontalBlock"]:has(div[data-testid="column"]:nth-child(5)) .stButton > button:hover {
    background: linear-gradient(145deg, #e0f2fe 0%, #bae6fd 100%) !important;
    border-color: #0284c7 !important;
    box-shadow: 0 0 10px rgba(14, 165, 233, 0.25) !important;
}

/* Inputs & Controls (Light Input Fields) */
.stNumberInput label, .stTextInput label, .stSelectbox label {
    color: #475569 !important;
}

.stNumberInput input, .stTextInput input {
    background: #ffffff !important;
    color: #0f172a !important;
    border: 1px solid rgba(14, 165, 233, 0.3) !important;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05) !important;
}

.stNumberInput input:focus, .stTextInput input:focus {
    border-color: #0284c7 !important;
    box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.2), inset 0 1px 3px rgba(0, 0, 0, 0.05) !important;
}

.stSelectbox div[data-baseweb="select"] {
    background: #ffffff !important;
    border: 1px solid rgba(14, 165, 233, 0.3) !important;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05) !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: transparent !important;
    color: #0f172a !important;
}

ul[data-baseweb="menu"] {
    background: #ffffff !important;
    border: 1px solid rgba(14, 165, 233, 0.3) !important;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1) !important;
}

li[data-baseweb="menu-item"] {
    color: #1e293b !important;
}

li[data-baseweb="menu-item"]:hover, li[data-baseweb="menu-item"][aria-selected="true"] {
    background: rgba(14, 165, 233, 0.12) !important;
    color: #0284c7 !important;
}

/* GST Breakdown Cards */
.gst-metric-box {
    background: #f8fafc !important;
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
}

.gst-metric-box.highlight {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.10) 0%, rgba(59, 130, 246, 0.14) 100%) !important;
    border-color: rgba(14, 165, 233, 0.35) !important;
}

.gst-metric-title {
    color: #64748b !important;
}

.gst-metric-val {
    color: #059669 !important;
}

.gst-metric-val.accent {
    color: #0284c7 !important;
}

.gst-metric-val.total {
    color: #0284c7 !important;
    text-shadow: none !important;
}

/* History Cards */
.history-stat-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
    border: 1px solid rgba(14, 165, 233, 0.25) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04), inset 0 1px 0 rgba(255, 255, 255, 1) !important;
}

.history-stat-title {
    color: #64748b !important;
}

.history-stat-val {
    color: #0284c7 !important;
    text-shadow: none !important;
}

.history-container::-webkit-scrollbar-track {
    background: rgba(226, 232, 240, 0.6) !important;
}

.history-container::-webkit-scrollbar-thumb {
    background: rgba(14, 165, 233, 0.4) !important;
}

.history-item-card {
    background: #ffffff !important;
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
}

.history-item-card:hover {
    border-color: rgba(14, 165, 233, 0.4) !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06), 0 0 10px rgba(14, 165, 233, 0.1) !important;
}

.history-item-top {
    color: #64748b !important;
}

.history-badge {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.12) 0%, rgba(59, 130, 246, 0.12) 100%) !important;
    color: #0284c7 !important;
    border: 1px solid rgba(14, 165, 233, 0.3) !important;
}

.history-item-math {
    color: #0f172a !important;
}

.history-idx {
    color: #0284c7 !important;
}

.history-res {
    color: #0284c7 !important;
}

.history-details {
    color: #64748b !important;
    border-top: 1px dashed rgba(0, 0, 0, 0.1) !important;
}

/* Footer Section */
.footer-box {
    border-top: 1px solid rgba(0, 0, 0, 0.08) !important;
}

.footer-line1 {
    color: #64748b !important;
}

.footer-line2 {
    color: #475569 !important;
}

.footer-highlight, .footer-author {
    color: #0284c7 !important;
    text-shadow: none !important;
}
</style>
"""

active_css = custom_css if is_dark else custom_css + light_css
st.markdown(active_css, unsafe_allow_html=True)


# ==============================================================================
# 2. HELPER FUNCTIONS & LOGIC
# ==============================================================================

def format_number(value: float) -> str:
    """Formats float numbers to clean strings without trailing .0 for integers."""
    if value is None:
        return ""
    try:
        if float(value).is_integer():
            return f"{int(value)}"
        else:
            formatted = f"{value:.8f}".rstrip('0').rstrip('.')
            return formatted
    except (ValueError, TypeError):
        return str(value)


def calculate(num1: float, num2: float, operator: str):
    """
    Performs mathematical calculations based on the selected operator.
    Handles division by zero, invalid roots, powers, and numerical overflows.

    Returns:
        tuple: (result_value, expression_string, error_message)
    """
    try:
        n1_str = format_number(num1)
        n2_str = format_number(num2)

        # 1. Addition (+)
        if "Addition" in operator or operator in ["+", "➕ Addition (+)"]:
            res = num1 + num2
            expr = f"{n1_str} + {n2_str}"
            return res, expr, None

        # 2. Subtraction (-)
        elif "Subtraction" in operator or operator in ["-", "−", "➖ Subtraction (-)"]:
            res = num1 - num2
            expr = f"{n1_str} − {n2_str}"
            return res, expr, None

        # 3. Multiplication (×)
        elif "Multiplication" in operator or operator in ["*", "×", "✖️ Multiplication (×)"]:
            res = num1 * num2
            expr = f"{n1_str} × {n2_str}"
            return res, expr, None

        # 4. Division (÷)
        elif "Division" in operator or operator in ["/", "÷", "➗ Division (÷)"]:
            if num2 == 0:
                return None, f"{n1_str} ÷ 0", "⚠️ Cannot divide by zero"
            res = num1 / num2
            expr = f"{n1_str} ÷ {n2_str}"
            return res, expr, None

        # 5. Modulus (%)
        elif "Modulus" in operator or operator in ["%", "% Modulus (%)"]:
            if num2 == 0:
                return None, f"{n1_str} % 0", "⚠️ Modulus by zero is undefined"
            res = num1 % num2
            expr = f"{n1_str} % {n2_str}"
            return res, expr, None

        # 6. Power (xʸ)
        elif "Power" in operator or operator in ["^", "xʸ", "xʸ Power (^)"]:
            if num1 == 0 and num2 < 0:
                return None, f"{n1_str} ^ ({n2_str})", "⚠️ Zero raised to negative power is undefined"
            if num1 < 0 and not float(num2).is_integer():
                return None, f"{n1_str} ^ ({n2_str})", "⚠️ Negative base with fractional exponent is undefined"
            res = math.pow(num1, num2)
            expr = f"{n1_str} ^ {n2_str}"
            return res, expr, None

        # 7. Percentage (%)
        elif "Percentage" in operator:
            res = (num1 * num2) / 100
            expr = f"{n1_str}% of {n2_str}"
            return res, expr, None

        # 8. Square (x²)
        elif "Square" in operator and "Root" not in operator:
            res = num1 ** 2
            expr = f"({n1_str})²"
            return res, expr, None

        # 9. Square Root (√x)
        elif "Square Root" in operator:
            if num1 < 0:
                return None, f"√({n1_str})", "⚠️ Cannot calculate square root of a negative number"
            res = math.sqrt(num1)
            expr = f"√({n1_str})"
            return res, expr, None

        else:
            return None, "", "⚠️ Unknown operation"

    except OverflowError:
        return None, "Error", "⚠️ Result is too large (Overflow)"
    except Exception as e:
        return None, "Error", f"⚠️ Calculation Error: {str(e)}"


# Helper function to save successful calculations to history with Date & Time
def add_to_history(expr: str, result_str: str, calc_type: str = "Basic", details_str: str = ""):
    """Saves the calculation expression, result, date, time, and type to history (max 20 items)."""
    if "history" not in st.session_state:
        st.session_state.history = []

    now = datetime.now()
    entry = {
        "timestamp": now.strftime("%d %b %Y | %I:%M %p"),
        "date": now.strftime("%d %b %Y"),
        "time": now.strftime("%I:%M %p"),
        "calc_type": calc_type,
        "expr": expr,
        "result": result_str,
        "details": details_str
    }
    st.session_state.history.insert(0, entry)
    st.session_state.history = st.session_state.history[:20]


# Helper function to generate CSV for History export
def generate_history_csv():
    """Generates a CSV string for all currently stored calculation history items."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Time", "Calculation Type", "Expression", "Result", "GST Details"])

    for item in st.session_state.history:
        if isinstance(item, dict):
            writer.writerow([
                item.get("date", "N/A"),
                item.get("time", "N/A"),
                item.get("calc_type", "General"),
                item.get("expr", ""),
                item.get("result", ""),
                item.get("details", "")
            ])
        else:
            # Handle legacy string history format
            str_item = str(item)
            parts = str_item.split("=")
            expr_part = parts[0].strip() if len(parts) > 0 else str_item
            res_part = parts[1].strip() if len(parts) > 1 else str_item
            writer.writerow(["Date unavailable", "N/A", "General", expr_part, res_part, ""])

    return output.getvalue()


# Helper function for scientific calculations (34 total functions)
def calculate_scientific(num: float, operation: str, num2: float = 0.0):
    """
    Performs scientific calculations using Python's math module.
    Handles single-input and multi-input scientific functions with full validation.

    Returns:
        tuple: (result_value, expression_string, error_message)
    """
    try:
        n_str = format_number(num)
        n2_str = format_number(num2)
        op_lower = operation.lower()

        # 1. Inverse Trigonometric Functions (asin, acos, atan) - Checked BEFORE sin, cos, tan
        if "asin" in op_lower:
            if num < -1 or num > 1:
                return None, f"asin({n_str})", "⚠️ Input for asin must be between -1 and 1"
            rad = math.asin(num)
            res = round(math.degrees(rad), 10)
            expr = f"asin({n_str})"
            return res, expr, None

        elif "acos" in op_lower:
            if num < -1 or num > 1:
                return None, f"acos({n_str})", "⚠️ Input for acos must be between -1 and 1"
            rad = math.acos(num)
            res = round(math.degrees(rad), 10)
            expr = f"acos({n_str})"
            return res, expr, None

        elif "atan" in op_lower:
            rad = math.atan(num)
            res = round(math.degrees(rad), 10)
            expr = f"atan({n_str})"
            return res, expr, None

        # 2. Hyperbolic Trigonometric Functions (sinh, cosh, tanh) - Checked BEFORE sin, cos, tan
        elif "sinh" in op_lower:
            res = round(math.sinh(num), 10)
            expr = f"sinh({n_str})"
            return res, expr, None

        elif "cosh" in op_lower:
            res = round(math.cosh(num), 10)
            expr = f"cosh({n_str})"
            return res, expr, None

        elif "tanh" in op_lower:
            res = round(math.tanh(num), 10)
            expr = f"tanh({n_str})"
            return res, expr, None

        # 3. Reciprocal Trigonometric Functions (cot, sec, cosec)
        elif "cosec" in op_lower:
            if abs(num % 180) < 1e-9 or abs(math.sin(math.radians(num))) < 1e-12:
                return None, f"cosec({n_str}°)", "⚠️ Cosecant is undefined for this angle"
            rad = math.radians(num)
            res = round(1 / math.sin(rad), 10)
            expr = f"cosec({n_str}°)"
            return res, expr, None

        elif "sec" in op_lower:
            if abs(num % 180 - 90) < 1e-9 or abs(math.cos(math.radians(num))) < 1e-12:
                return None, f"sec({n_str}°)", "⚠️ Secant is undefined for this angle"
            rad = math.radians(num)
            res = round(1 / math.cos(rad), 10)
            expr = f"sec({n_str}°)"
            return res, expr, None

        elif "cot" in op_lower:
            if abs(num % 180) < 1e-9 or abs(math.sin(math.radians(num))) < 1e-12:
                return None, f"cot({n_str}°)", "⚠️ Cotangent is undefined for this angle"
            rad = math.radians(num)
            res = round(1 / math.tan(rad), 10)
            expr = f"cot({n_str}°)"
            return res, expr, None

        # 4. Standard Trigonometric Functions (sin, cos, tan)
        elif "sin" in op_lower:
            rad = math.radians(num)
            res = round(math.sin(rad), 10)
            expr = f"sin({n_str}°)"
            return res, expr, None

        elif "cos" in op_lower:
            rad = math.radians(num)
            res = round(math.cos(rad), 10)
            expr = f"cos({n_str}°)"
            return res, expr, None

        elif "tan" in op_lower:
            if abs(num % 180 - 90) < 1e-9 or abs(math.cos(math.radians(num))) < 1e-12:
                return None, f"tan({n_str}°)", "⚠️ Tangent is undefined for this angle"
            rad = math.radians(num)
            res = round(math.tan(rad), 10)
            expr = f"tan({n_str}°)"
            return res, expr, None

        # 5. Logarithmic Functions (log10, log2, ln)
        elif "log10" in op_lower:
            if num <= 0:
                return None, f"log10({n_str})", "⚠️ Logarithm requires a positive number (x > 0)"
            res = math.log10(num)
            expr = f"log10({n_str})"
            return res, expr, None

        elif "log2" in op_lower:
            if num <= 0:
                return None, f"log2({n_str})", "⚠️ Logarithm requires a positive number (x > 0)"
            res = math.log2(num)
            expr = f"log2({n_str})"
            return res, expr, None

        elif "ln" in op_lower:
            if num <= 0:
                return None, f"ln({n_str})", "⚠️ Natural log requires a positive number (x > 0)"
            res = math.log(num)
            expr = f"ln({n_str})"
            return res, expr, None

        # 6. Powers & Exponentials (exp, 10^x, power)
        elif "exp" in op_lower:
            res = math.exp(num)
            expr = f"e^({n_str})"
            return res, expr, None

        elif "10^x" in op_lower:
            res = math.pow(10, num)
            expr = f"10^({n_str})"
            return res, expr, None

        elif "power" in op_lower or "xʸ" in operation:
            if num == 0 and num2 < 0:
                return None, f"{n_str} ^ ({n2_str})", "⚠️ Zero raised to negative power is undefined"
            if num < 0 and not float(num2).is_integer():
                return None, f"{n_str} ^ ({n2_str})", "⚠️ Negative base with fractional exponent is undefined"
            res = math.pow(num, num2)
            expr = f"{n_str} ^ {n2_str}"
            return res, expr, None

        # 7. Roots (cube root, square root, nth root)
        elif "cube root" in op_lower or "∛" in operation:
            if hasattr(math, 'cbrt'):
                res = math.cbrt(num)
            else:
                res = math.pow(abs(num), 1/3) * (-1 if num < 0 else 1)
            expr = f"∛({n_str})"
            return res, expr, None

        elif "square root" in op_lower or "√x" in operation:
            if num < 0:
                return None, f"√({n_str})", "⚠️ Cannot calculate square root of a negative number"
            res = math.sqrt(num)
            expr = f"√({n_str})"
            return res, expr, None

        elif "nth root" in op_lower or "ⁿ√" in operation:
            if num2 == 0:
                return None, f"{n2_str}√({n_str})", "⚠️ Root degree cannot be zero"
            if num < 0:
                if float(num2).is_integer() and int(num2) % 2 != 0:
                    res = - (abs(num) ** (1.0 / num2))
                else:
                    return None, f"{n2_str}√({n_str})", "⚠️ Even root of negative number is undefined"
            else:
                res = num ** (1.0 / num2)
            expr = f"{n2_str}√({n_str})"
            return res, expr, None

        # 8. Factorial, Permutation & Combination (factorial, npr, ncr)
        elif "factorial" in op_lower:
            if num < 0 or not float(num).is_integer():
                return None, f"factorial({n_str})", "⚠️ Factorial requires a non-negative whole number"
            if num > 1000:
                return None, f"factorial({n_str})", "⚠️ Input too large for factorial"
            res = math.factorial(int(num))
            expr = f"{n_str}!"
            return res, expr, None

        elif "npr" in op_lower:
            if num < 0 or num2 < 0 or not float(num).is_integer() or not float(num2).is_integer():
                return None, f"{n_str}P{n2_str}", "⚠️ nPr requires non-negative whole numbers"
            if num2 > num:
                return None, f"{n_str}P{n2_str}", "⚠️ r cannot be greater than n (r ≤ n)"
            res = math.perm(int(num), int(num2))
            expr = f"{n_str}P{n2_str}"
            return res, expr, None

        elif "ncr" in op_lower:
            if num < 0 or num2 < 0 or not float(num).is_integer() or not float(num2).is_integer():
                return None, f"{n_str}C{n2_str}", "⚠️ nCr requires non-negative whole numbers"
            if num2 > num:
                return None, f"{n_str}C{n2_str}", "⚠️ r cannot be greater than n (r ≤ n)"
            res = math.comb(int(num), int(num2))
            expr = f"{n_str}C{n2_str}"
            return res, expr, None

        # 9. Number Theory (gcd, lcm)
        elif "gcd" in op_lower:
            if num < 0 or num2 < 0 or not float(num).is_integer() or not float(num2).is_integer():
                return None, f"gcd({n_str}, {n2_str})", "⚠️ GCD requires non-negative whole numbers"
            res = math.gcd(int(num), int(num2))
            expr = f"gcd({n_str}, {n2_str})"
            return res, expr, None

        elif "lcm" in op_lower:
            if num < 0 or num2 < 0 or not float(num).is_integer() or not float(num2).is_integer():
                return None, f"lcm({n_str}, {n2_str})", "⚠️ LCM requires non-negative whole numbers"
            if hasattr(math, 'lcm'):
                res = math.lcm(int(num), int(num2))
            else:
                res = abs(int(num) * int(num2)) // math.gcd(int(num), int(num2)) if (int(num) and int(num2)) else 0
            expr = f"lcm({n_str}, {n2_str})"
            return res, expr, None

        # 10. Cube & Square (cube, square)
        elif "cube" in op_lower:
            res = num ** 3
            expr = f"({n_str})³"
            return res, expr, None

        elif "square" in op_lower:
            res = num ** 2
            expr = f"({n_str})²"
            return res, expr, None

        # 11. Rounding & Parts (floor, ceil, round, frac, absolute, reciprocal)
        elif "floor" in op_lower:
            res = math.floor(num)
            expr = f"floor({n_str})"
            return res, expr, None

        elif "ceil" in op_lower:
            res = math.ceil(num)
            expr = f"ceil({n_str})"
            return res, expr, None

        elif "round" in op_lower:
            res = round(num)
            expr = f"round({n_str})"
            return res, expr, None

        elif "frac" in op_lower:
            res = round(num - math.floor(num), 10)
            expr = f"frac({n_str})"
            return res, expr, None

        elif "absolute" in op_lower or "|x|" in op_lower:
            res = abs(num)
            expr = f"|{n_str}|"
            return res, expr, None

        elif "reciprocal" in op_lower or "1/x" in op_lower:
            if num == 0:
                return None, f"1 / {n_str}", "⚠️ Cannot divide by zero"
            res = 1 / num
            expr = f"1 / {n_str}"
            return res, expr, None

        else:
            return None, "", "⚠️ Unknown scientific operation"

    except OverflowError:
        return None, "Error", "⚠️ Result is too large (Overflow)"
    except Exception as e:
        return None, "Error", f"⚠️ Calculation Error: {str(e)}"


# Helper function for GST calculations (Add GST, Remove GST, CGST + SGST, IGST, Discount + GST)
def calculate_gst(amount: float, rate: float, mode: str, discount: float = 0.0):
    """
    Performs GST calculation based on the selected mode.
    Modes supported:
        - Add GST
        - Remove GST
        - CGST + SGST
        - IGST
        - Discount + GST

    Returns:
        tuple: (final_or_original_amount, main_gst_amount, expression_string, error_message, details_dict)
    """
    try:
        if amount < 0:
            return None, None, "", "⚠️ Amount cannot be negative", None
        if rate < 0:
            return None, None, "", "⚠️ GST Rate cannot be negative", None

        amt_str = format_number(amount)
        rate_str = format_number(rate)

        # 1. Add GST
        if mode == "Add GST":
            gst_amt = (amount * rate) / 100
            final_amt = amount + gst_amt
            expr = f"{amt_str} + {rate_str}% GST"
            details = {"final": final_amt, "gst": gst_amt, "taxable": amount}
            return final_amt, gst_amt, expr, None, details

        # 2. Remove GST
        elif mode == "Remove GST":
            denom = 1 + (rate / 100)
            if denom == 0:
                return None, None, f"{amt_str} - {rate_str}% GST", "⚠️ Invalid GST rate (-100%)", None
            orig_amt = amount / denom
            gst_amt = amount - orig_amt
            expr = f"{amt_str} - {rate_str}% GST (Inclusive)"
            details = {"final": orig_amt, "gst": gst_amt, "taxable": orig_amt}
            return orig_amt, gst_amt, expr, None, details

        # 3. CGST + SGST
        elif mode == "CGST + SGST":
            total_gst = (amount * rate) / 100
            cgst_amt = total_gst / 2
            sgst_amt = total_gst / 2
            final_amt = amount + total_gst
            expr = f"{amt_str} + {rate_str}% GST (CGST + SGST)"
            details = {
                "final": final_amt,
                "gst": total_gst,
                "cgst": cgst_amt,
                "sgst": sgst_amt,
                "taxable": amount
            }
            return final_amt, total_gst, expr, None, details

        # 4. IGST
        elif mode == "IGST":
            igst_amt = (amount * rate) / 100
            final_amt = amount + igst_amt
            expr = f"{amt_str} + {rate_str}% IGST"
            details = {
                "final": final_amt,
                "gst": igst_amt,
                "igst": igst_amt,
                "taxable": amount
            }
            return final_amt, igst_amt, expr, None, details

        # 5. Discount + GST
        elif mode == "Discount + GST":
            if discount < 0 or discount > 100:
                return None, None, "", "⚠️ Discount percentage must be between 0% and 100%", None
            disc_amt = (amount * discount) / 100
            taxable_amt = amount - disc_amt
            gst_amt = (taxable_amt * rate) / 100
            final_amt = taxable_amt + gst_amt
            disc_str = format_number(discount)
            expr = f"{amt_str} - {disc_str}% Disc + {rate_str}% GST"
            details = {
                "final": final_amt,
                "gst": gst_amt,
                "discount_amt": disc_amt,
                "taxable": taxable_amt,
                "original": amount
            }
            return final_amt, gst_amt, expr, None, details

        else:
            return None, None, "", "⚠️ Invalid GST mode", None

    except Exception as e:
        return None, None, "Error", f"⚠️ Calculation Error: {str(e)}", None


# ==============================================================================
# 3. SESSION STATE INITIALIZATION
# ==============================================================================

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Basic"

if "calc_input" not in st.session_state:
    st.session_state.calc_input = "0"

if "pending_num1" not in st.session_state:
    st.session_state.pending_num1 = None

if "pending_op" not in st.session_state:
    st.session_state.pending_op = None

if "new_input" not in st.session_state:
    st.session_state.new_input = False

if "num1" not in st.session_state:
    st.session_state.num1 = 0.0

if "num2" not in st.session_state:
    st.session_state.num2 = 0.0

if "operator" not in st.session_state:
    st.session_state.operator = "➕ Addition (+)"

if "expr" not in st.session_state:
    st.session_state.expr = ""

if "result" not in st.session_state:
    st.session_state.result = "0"

if "error" not in st.session_state:
    st.session_state.error = None

if "history" not in st.session_state:
    st.session_state.history = []

if "sci_num" not in st.session_state:
    st.session_state.sci_num = 0.0

if "sci_num2" not in st.session_state:
    st.session_state.sci_num2 = 0.0

if "sci_op" not in st.session_state:
    st.session_state.sci_op = "sin (Sine)"

if "sci_result" not in st.session_state:
    st.session_state.sci_result = None

if "sci_expr" not in st.session_state:
    st.session_state.sci_expr = ""

if "sci_error" not in st.session_state:
    st.session_state.sci_error = None

if "gst_amount" not in st.session_state:
    st.session_state.gst_amount = 0.0

if "gst_rate" not in st.session_state:
    st.session_state.gst_rate = 18.0

if "gst_discount" not in st.session_state:
    st.session_state.gst_discount = 0.0

if "gst_mode" not in st.session_state:
    st.session_state.gst_mode = "Add GST"

if "gst_result" not in st.session_state:
    st.session_state.gst_result = None

if "gst_amt_res" not in st.session_state:
    st.session_state.gst_amt_res = None

if "gst_details" not in st.session_state:
    st.session_state.gst_details = None

if "gst_expr" not in st.session_state:
    st.session_state.gst_expr = ""

if "gst_error" not in st.session_state:
    st.session_state.gst_error = None


# Callback function for Quick Operator Buttons
def set_operator(op_name):
    st.session_state.operator = op_name


# Callback function for GST Rate Presets
def set_gst_preset(rate_val: float):
    st.session_state.gst_rate = float(rate_val)


# Callback function to clear state
def clear_all():
    st.session_state.calc_input = "0"
    st.session_state.pending_num1 = None
    st.session_state.pending_op = None
    st.session_state.new_input = False
    st.session_state.num1 = 0.0
    st.session_state.num2 = 0.0
    st.session_state.operator = "➕ Addition (+)"
    st.session_state.expr = ""
    st.session_state.result = "0"
    st.session_state.error = None


# Callback function to clear calculation history
def clear_history():
    st.session_state.history = []


# Keypad Action Callback Handlers
def handle_keypad_digit(digit: str):
    """Appends a digit to current calculation input."""
    if st.session_state.new_input or st.session_state.calc_input == "0":
        st.session_state.calc_input = str(digit)
        st.session_state.new_input = False
    else:
        st.session_state.calc_input += str(digit)
    st.session_state.result = st.session_state.calc_input
    st.session_state.error = None


def handle_keypad_dot():
    """Appends a decimal point if not already present."""
    if st.session_state.new_input:
        st.session_state.calc_input = "0."
        st.session_state.new_input = False
    elif "." not in st.session_state.calc_input:
        st.session_state.calc_input += "."
    st.session_state.result = st.session_state.calc_input


def handle_keypad_toggle_sign():
    """Toggles sign (positive/negative) of the current number."""
    val = st.session_state.calc_input
    if val.startswith("-"):
        st.session_state.calc_input = val[1:]
    elif val != "0":
        st.session_state.calc_input = "-" + val
    st.session_state.result = st.session_state.calc_input


def handle_keypad_backspace():
    """Removes last entered character."""
    val = st.session_state.calc_input
    if len(val) > 1:
        st.session_state.calc_input = val[:-1]
        if st.session_state.calc_input == "-":
            st.session_state.calc_input = "0"
    else:
        st.session_state.calc_input = "0"
    st.session_state.result = st.session_state.calc_input


def handle_keypad_op(op_symbol: str):
    """Handles operator selection (+, −, ×, ÷, %)."""
    try:
        current_val = float(st.session_state.calc_input)
    except ValueError:
        current_val = 0.0

    if st.session_state.pending_num1 is not None and st.session_state.pending_op is not None and not st.session_state.new_input:
        res_val, expr_str, error_msg = calculate(st.session_state.pending_num1, current_val, st.session_state.pending_op)
        if error_msg:
            st.session_state.error = error_msg
            st.session_state.result = ""
            st.session_state.pending_num1 = None
            st.session_state.pending_op = None
            return
        else:
            st.session_state.pending_num1 = res_val
            st.session_state.calc_input = format_number(res_val)
            st.session_state.result = st.session_state.calc_input
    else:
        st.session_state.pending_num1 = current_val

    st.session_state.pending_op = op_symbol
    st.session_state.new_input = True
    st.session_state.expr = f"{format_number(st.session_state.pending_num1)} {op_symbol}"
    st.session_state.error = None


def handle_keypad_equals():
    """Evaluates the mathematical expression and updates history."""
    if st.session_state.pending_num1 is None or st.session_state.pending_op is None:
        return

    try:
        num2_val = float(st.session_state.calc_input)
    except ValueError:
        num2_val = 0.0

    num1_val = st.session_state.pending_num1
    op_val = st.session_state.pending_op

    res_val, expr_str, error_msg = calculate(num1_val, num2_val, op_val)

    if error_msg:
        st.session_state.error = error_msg
        st.session_state.result = ""
    else:
        res_formatted = format_number(res_val)
        st.session_state.result = res_formatted
        st.session_state.calc_input = res_formatted
        st.session_state.expr = expr_str
        st.session_state.error = None
        add_to_history(expr_str, res_formatted, calc_type="Basic")

    st.session_state.pending_num1 = None
    st.session_state.pending_op = None
    st.session_state.new_input = True


# ==============================================================================
# 4. USER INTERFACE (PREMIUM DASHBOARD WITH KEYPAD)
# ==============================================================================

# Header Section (Title, Icon & Premium Badge)
st.markdown("""
<div class="header-container">
    <div class="header-left">
        <div class="calc-icon-wrapper">
            <span class="calc-icon">🧮</span>
        </div>
        <div class="calc-title-box">
            <h1 class="calc-title-text">Rajan Calculator</h1>
            <p class="calc-subtitle">Smart • Fast • Accurate</p>
        </div>
    </div>
    <span class="badge-premium">✨ Premium UI</span>
</div>
""", unsafe_allow_html=True)

# Theme Toggle Switcher (Dark Mode / Light Mode only)
st.toggle(
    "🌙 Dark Mode" if st.session_state.get("dark_mode", True) else "☀️ Light Mode",
    key="dark_mode"
)

# 4 Horizontal Equal-Width Navigation Tabs
nav_options = ["Basic", "Scientific", "GST", "History"]

selected_tab = st.radio(
    "Navigation Mode",
    options=nav_options,
    key="active_tab",
    horizontal=True,
    label_visibility="collapsed"
)


# ==============================================================================
# CONDITIONAL RENDERING BASED ON ACTIVE TAB
# ==============================================================================

# ------------------------------------------------------------------------------
# TAB 1: BASIC CALCULATOR (4-COLUMN KEYPAD)
# ------------------------------------------------------------------------------
if st.session_state.active_tab == "Basic":
    st.markdown('<div class="calc-panel">', unsafe_allow_html=True)

    # Result Display Screen
    if st.session_state.error:
        st.markdown(f"""
        <div class="result-screen">
            <div class="display-label-bar">
                <span class="display-label error"><span class="display-status-dot error"></span> ERROR</span>
                <span class="display-expr">{st.session_state.expr}</span>
            </div>
            <div class="display-error">{st.session_state.error}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-screen">
            <div class="display-label-bar">
                <span class="display-label"><span class="display-status-dot"></span> RESULT</span>
                <span class="display-expr">{st.session_state.expr}</span>
            </div>
            <div class="display-result">{st.session_state.result}</div>
        </div>
        """, unsafe_allow_html=True)

    # 4-Column Physical Keypad Grid
    # Row 1: AC | ⌫ | % | ÷
    r1c1, r1c2, r1c3, r1c4 = st.columns(4)
    with r1c1:
        st.button("AC", key="kp_ac", type="secondary", on_click=clear_all, use_container_width=True)
    with r1c2:
        st.button("⌫", key="kp_back", on_click=handle_keypad_backspace, use_container_width=True)
    with r1c3:
        st.button("%", key="kp_pct", on_click=handle_keypad_op, args=("%",), use_container_width=True)
    with r1c4:
        st.button("÷", key="kp_div", on_click=handle_keypad_op, args=("÷",), use_container_width=True)

    # Row 2: 7 | 8 | 9 | ×
    r2c1, r2c2, r2c3, r2c4 = st.columns(4)
    with r2c1:
        st.button("7", key="kp_7", on_click=handle_keypad_digit, args=("7",), use_container_width=True)
    with r2c2:
        st.button("8", key="kp_8", on_click=handle_keypad_digit, args=("8",), use_container_width=True)
    with r2c3:
        st.button("9", key="kp_9", on_click=handle_keypad_digit, args=("9",), use_container_width=True)
    with r2c4:
        st.button("×", key="kp_mul", on_click=handle_keypad_op, args=("×",), use_container_width=True)

    # Row 3: 4 | 5 | 6 | −
    r3c1, r3c2, r3c3, r3c4 = st.columns(4)
    with r3c1:
        st.button("4", key="kp_4", on_click=handle_keypad_digit, args=("4",), use_container_width=True)
    with r3c2:
        st.button("5", key="kp_5", on_click=handle_keypad_digit, args=("5",), use_container_width=True)
    with r3c3:
        st.button("6", key="kp_6", on_click=handle_keypad_digit, args=("6",), use_container_width=True)
    with r3c4:
        st.button("−", key="kp_sub", on_click=handle_keypad_op, args=("−",), use_container_width=True)

    # Row 4: 1 | 2 | 3 | +
    r4c1, r4c2, r4c3, r4c4 = st.columns(4)
    with r4c1:
        st.button("1", key="kp_1", on_click=handle_keypad_digit, args=("1",), use_container_width=True)
    with r4c2:
        st.button("2", key="kp_2", on_click=handle_keypad_digit, args=("2",), use_container_width=True)
    with r4c3:
        st.button("3", key="kp_3", on_click=handle_keypad_digit, args=("3",), use_container_width=True)
    with r4c4:
        st.button("+", key="kp_add", on_click=handle_keypad_op, args=("+",), use_container_width=True)

    # Row 5: ± | 0 | . | =
    r5c1, r5c2, r5c3, r5c4 = st.columns(4)
    with r5c1:
        st.button("±", key="kp_sign", on_click=handle_keypad_toggle_sign, use_container_width=True)
    with r5c2:
        st.button("0", key="kp_0", on_click=handle_keypad_digit, args=("0",), use_container_width=True)
    with r5c3:
        st.button(".", key="kp_dot", on_click=handle_keypad_dot, use_container_width=True)
    with r5c4:
        st.button("=", key="kp_eq", type="primary", on_click=handle_keypad_equals, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# TAB 2: SCIENTIFIC CALCULATOR (34 FUNCTIONS TOTAL)
# ------------------------------------------------------------------------------
elif st.session_state.active_tab == "Scientific":
    st.markdown('<div class="calc-panel">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🔬 Scientific Calculator</div>', unsafe_allow_html=True)

    # Multi-input detection map for second input requirement
    multi_input_keys = {
        "power": "Exponent (y)",
        "nth root": "Root Degree (n)",
        "gcd": "Second Integer",
        "lcm": "Second Integer",
        "npr": "r (Items to choose)",
        "ncr": "r (Items to choose)"
    }

    selected_op_lower = st.session_state.sci_op.lower()
    second_input_label = None
    for key, label in multi_input_keys.items():
        if key in selected_op_lower:
            second_input_label = label
            break

    sci_col1, sci_col2 = st.columns([1, 1])
    with sci_col1:
        st.number_input(
            "Scientific Input Number (x / n)" if second_input_label else "Scientific Input Number",
            key="sci_num",
            step=1.0,
            format="%.6g",
            help="Enter decimal or negative numbers"
        )

    with sci_col2:
        sci_op_options = [
            "sin (Sine)",
            "cos (Cosine)",
            "tan (Tangent)",
            "log10 (Log Base 10)",
            "ln (Natural Log)",
            "factorial (n!)",
            "cube (x³)",
            "cube root (∛x)",
            "absolute (|x|)",
            "reciprocal (1/x)",
            "square (x²)",
            "square root (√x)",
            "power (xʸ)",
            "nth root (ⁿ√x)",
            "asin (Inverse Sine)",
            "acos (Inverse Cosine)",
            "atan (Inverse Tangent)",
            "cot (Cotangent)",
            "sec (Secant)",
            "cosec (Cosecant)",
            "sinh (Hyperbolic Sine)",
            "cosh (Hyperbolic Cosine)",
            "tanh (Hyperbolic Tangent)",
            "log2 (Log Base 2)",
            "exp (eˣ)",
            "10^x (Power of 10)",
            "floor (Floor)",
            "ceil (Ceiling)",
            "round (Round)",
            "frac (Fractional Part)",
            "gcd (GCD)",
            "lcm (LCM)",
            "nPr (Permutation)",
            "nCr (Combination)"
        ]
        st.selectbox(
            "Select Scientific Operation",
            options=sci_op_options,
            key="sci_op"
        )

    # Show Second Input field if the selected operation requires two inputs
    if second_input_label:
        st.number_input(
            second_input_label,
            key="sci_num2",
            step=1.0,
            format="%.6g",
            help="Enter second input value"
        )

    sci_calc_clicked = st.button("🧪 Calculate Scientific", key="btn_calc_sci", type="primary", use_container_width=True)

    if sci_calc_clicked:
        num_val = st.session_state.sci_num
        num2_val = st.session_state.sci_num2 if second_input_label else 0.0
        op_val = st.session_state.sci_op
        res_val, expr_str, error_msg = calculate_scientific(num_val, op_val, num2_val)

        st.session_state.sci_expr = expr_str
        if error_msg:
            st.session_state.sci_error = error_msg
            st.session_state.sci_result = None
        else:
            st.session_state.sci_error = None
            res_formatted = format_number(res_val)
            st.session_state.sci_result = res_formatted
            add_to_history(expr_str, res_formatted, calc_type="Scientific")

    if st.session_state.sci_error:
        st.markdown(f"""
        <div class="result-screen" style="margin-top: 18px;">
            <div class="display-label-bar">
                <span class="display-label error"><span class="display-status-dot error"></span> ERROR</span>
                <span class="display-expr">{st.session_state.sci_expr}</span>
            </div>
            <div class="display-error">{st.session_state.sci_error}</div>
        </div>
        """, unsafe_allow_html=True)
    elif st.session_state.sci_result is not None:
        st.markdown(f"""
        <div class="result-screen" style="margin-top: 18px;">
            <div class="display-label-bar">
                <span class="display-label"><span class="display-status-dot"></span> SCIENTIFIC RESULT</span>
                <span class="display-expr">{st.session_state.sci_expr}</span>
            </div>
            <div class="display-result">= {st.session_state.sci_result}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# TAB 3: GST CALCULATOR (ADD, REMOVE, CGST+SGST, IGST, DISCOUNT+GST, PRESETS)
# ------------------------------------------------------------------------------
elif st.session_state.active_tab == "GST":
    st.markdown('<div class="calc-panel">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">💰 GST Calculator</div>', unsafe_allow_html=True)

    # 1. Mode Radio Options (5 Modes)
    gst_mode_options = ["Add GST", "Remove GST", "CGST + SGST", "IGST", "Discount + GST"]
    st.radio(
        "GST Calculation Mode",
        options=gst_mode_options,
        key="gst_mode",
        horizontal=True
    )

    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

    # 2. Dynamic Input Fields Based On Selected GST Mode
    if st.session_state.gst_mode == "Discount + GST":
        gst_col1, gst_col2, gst_col3 = st.columns([1, 1, 1])
        with gst_col1:
            st.number_input(
                "Original Amount",
                key="gst_amount",
                step=10.0,
                format="%.6g",
                help="Enter original item price"
            )
        with gst_col2:
            st.number_input(
                "Discount (%)",
                key="gst_discount",
                step=1.0,
                format="%.6g",
                help="Enter discount percentage (0 - 100%)"
            )
        with gst_col3:
            st.number_input(
                "GST Rate (%)",
                key="gst_rate",
                step=1.0,
                format="%.6g",
                help="Enter GST percentage rate"
            )
    else:
        gst_col1, gst_col2 = st.columns([1, 1])
        with gst_col1:
            st.number_input(
                "Taxable Amount" if st.session_state.gst_mode in ["CGST + SGST", "IGST"] else "Amount",
                key="gst_amount",
                step=10.0,
                format="%.6g",
                help="Enter base or total amount"
            )
        with gst_col2:
            st.number_input(
                "GST Rate (%)",
                key="gst_rate",
                step=1.0,
                format="%.6g",
                help="Enter GST percentage rate"
            )

    # 3. GST Rate Presets (Quick Preset Buttons)
    st.caption("⚡ **Quick GST Rate Presets**")
    p1, p2, p3, p4, p5 = st.columns(5)
    with p1:
        st.button("0%", key="preset_0", on_click=set_gst_preset, args=(0.0,), use_container_width=True)
    with p2:
        st.button("5%", key="preset_5", on_click=set_gst_preset, args=(5.0,), use_container_width=True)
    with p3:
        st.button("12%", key="preset_12", on_click=set_gst_preset, args=(12.0,), use_container_width=True)
    with p4:
        st.button("18%", key="preset_18", on_click=set_gst_preset, args=(18.0,), use_container_width=True)
    with p5:
        st.button("28%", key="preset_28", on_click=set_gst_preset, args=(28.0,), use_container_width=True)

    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

    gst_calc_clicked = st.button("🧾 Calculate GST", key="btn_calc_gst", type="primary", use_container_width=True)

    if gst_calc_clicked:
        amt_val = st.session_state.gst_amount
        rate_val = st.session_state.gst_rate
        mode_val = st.session_state.gst_mode
        disc_val = st.session_state.gst_discount if mode_val == "Discount + GST" else 0.0

        final_amt, gst_amt, expr_str, error_msg, details = calculate_gst(amt_val, rate_val, mode_val, disc_val)

        st.session_state.gst_expr = expr_str
        if error_msg:
            st.session_state.gst_error = error_msg
            st.session_state.gst_result = None
            st.session_state.gst_amt_res = None
            st.session_state.gst_details = None
        else:
            st.session_state.gst_error = None
            final_formatted = format_number(final_amt)
            gst_formatted = format_number(gst_amt)
            st.session_state.gst_result = final_formatted
            st.session_state.gst_amt_res = gst_formatted
            st.session_state.gst_details = details

            # Add calculation result to history with detailed breakdown string
            if mode_val == "CGST + SGST":
                cgst_str = format_number(details.get("cgst"))
                sgst_str = format_number(details.get("sgst"))
                hist_res = f"{final_formatted} (CGST: {cgst_str}, SGST: {sgst_str})"
            elif mode_val == "IGST":
                igst_str = format_number(details.get("igst"))
                hist_res = f"{final_formatted} (IGST: {igst_str})"
            elif mode_val == "Discount + GST":
                disc_str = format_number(details.get("discount_amt"))
                hist_res = f"{final_formatted} (Disc: {disc_str}, GST: {gst_formatted})"
            else:
                hist_res = f"{final_formatted} (GST: {gst_formatted})"

            add_to_history(expr_str, final_formatted, calc_type="GST", details_str=hist_res)

    # Result Display Box for GST
    if st.session_state.gst_error:
        st.markdown(f"""
        <div class="result-screen" style="margin-top: 18px;">
            <div class="display-label-bar">
                <span class="display-label error"><span class="display-status-dot error"></span> ERROR</span>
                <span class="display-expr">{st.session_state.gst_expr}</span>
            </div>
            <div class="display-error">{st.session_state.gst_error}</div>
        </div>
        """, unsafe_allow_html=True)
    elif st.session_state.gst_result is not None:
        details = st.session_state.gst_details or {}
        mode = st.session_state.gst_mode

        if mode == "CGST + SGST":
            cgst_str = format_number(details.get("cgst", 0))
            sgst_str = format_number(details.get("sgst", 0))
            gst_str = format_number(details.get("gst", 0))
            st.markdown(f"""
            <div class="result-screen" style="margin-top: 18px;">
                <div class="display-label-bar">
                    <span class="display-label"><span class="display-status-dot"></span> TAX BREAKDOWN</span>
                    <span class="display-expr">{st.session_state.gst_expr}</span>
                </div>
                <div class="gst-card-grid">
                    <div class="gst-metric-box">
                        <span class="gst-metric-title">CGST (50%)</span>
                        <span class="gst-metric-val">₹{cgst_str}</span>
                    </div>
                    <div class="gst-metric-box">
                        <span class="gst-metric-title">SGST (50%)</span>
                        <span class="gst-metric-val">₹{sgst_str}</span>
                    </div>
                    <div class="gst-metric-box">
                        <span class="gst-metric-title">TOTAL GST</span>
                        <span class="gst-metric-val accent">₹{gst_str}</span>
                    </div>
                    <div class="gst-metric-box highlight">
                        <span class="gst-metric-title">FINAL TOTAL</span>
                        <span class="gst-metric-val total">₹{st.session_state.gst_result}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        elif mode == "IGST":
            igst_str = format_number(details.get("igst", 0))
            st.markdown(f"""
            <div class="result-screen" style="margin-top: 18px;">
                <div class="display-label-bar">
                    <span class="display-label"><span class="display-status-dot"></span> IGST BREAKDOWN</span>
                    <span class="display-expr">{st.session_state.gst_expr}</span>
                </div>
                <div class="gst-card-grid">
                    <div class="gst-metric-box">
                        <span class="gst-metric-title">IGST AMOUNT</span>
                        <span class="gst-metric-val">₹{igst_str}</span>
                    </div>
                    <div class="gst-metric-box highlight">
                        <span class="gst-metric-title">FINAL AMOUNT (INCL. IGST)</span>
                        <span class="gst-metric-val total">₹{st.session_state.gst_result}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        elif mode == "Discount + GST":
            disc_str = format_number(details.get("discount_amt", 0))
            taxable_str = format_number(details.get("taxable", 0))
            gst_str = format_number(details.get("gst", 0))
            st.markdown(f"""
            <div class="result-screen" style="margin-top: 18px;">
                <div class="display-label-bar">
                    <span class="display-label"><span class="display-status-dot"></span> DISCOUNT & TAX BREAKDOWN</span>
                    <span class="display-expr">{st.session_state.gst_expr}</span>
                </div>
                <div class="gst-card-grid">
                    <div class="gst-metric-box">
                        <span class="gst-metric-title">DISCOUNT</span>
                        <span class="gst-metric-val" style="color: #fca5a5;">- ₹{disc_str}</span>
                    </div>
                    <div class="gst-metric-box">
                        <span class="gst-metric-title">TAXABLE VALUE</span>
                        <span class="gst-metric-val">₹{taxable_str}</span>
                    </div>
                    <div class="gst-metric-box">
                        <span class="gst-metric-title">GST AMOUNT</span>
                        <span class="gst-metric-val accent">+ ₹{gst_str}</span>
                    </div>
                    <div class="gst-metric-box highlight">
                        <span class="gst-metric-title">FINAL PAYABLE</span>
                        <span class="gst-metric-val total">₹{st.session_state.gst_result}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:  # Add GST / Remove GST
            label_text = "FINAL AMOUNT (INCL. GST)" if mode == "Add GST" else "ORIGINAL AMOUNT (EXCL. GST)"
            st.markdown(f"""
            <div class="result-screen" style="margin-top: 18px;">
                <div class="display-label-bar">
                    <span class="display-label"><span class="display-status-dot"></span> TAX BREAKDOWN</span>
                    <span class="display-expr">{st.session_state.gst_expr}</span>
                </div>
                <div class="gst-card-grid">
                    <div class="gst-metric-box">
                        <span class="gst-metric-title">GST AMOUNT</span>
                        <span class="gst-metric-val">₹{st.session_state.gst_amt_res}</span>
                    </div>
                    <div class="gst-metric-box highlight">
                        <span class="gst-metric-title">{label_text}</span>
                        <span class="gst-metric-val total">₹{st.session_state.gst_result}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# TAB 4: CALCULATION HISTORY (SUMMARY CARDS, DATE & TIME, CSV DOWNLOAD)
# ------------------------------------------------------------------------------
elif st.session_state.active_tab == "History":
    st.markdown('<div class="calc-panel">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🕘 Calculation History</div>', unsafe_allow_html=True)

    # 1. Summary Cards (Total Calculations & Last Result)
    if not st.session_state.history:
        total_count = 0
        last_result_str = "—"
    else:
        total_count = len(st.session_state.history)
        latest = st.session_state.history[0]
        if isinstance(latest, dict):
            last_result_str = latest.get("result", "—")
        else:
            str_item = str(latest)
            last_result_str = str_item.split("=")[1].strip() if "=" in str_item else str_item

    sum_col1, sum_col2 = st.columns(2)
    with sum_col1:
        st.markdown(f"""
        <div class="history-stat-card">
            <div class="history-stat-title">TOTAL CALCULATIONS</div>
            <div class="history-stat-val">{total_count} / 20</div>
        </div>
        """, unsafe_allow_html=True)

    with sum_col2:
        st.markdown(f"""
        <div class="history-stat-card">
            <div class="history-stat-title">LAST RESULT</div>
            <div class="history-stat-val" style="color: #a7f3d0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{last_result_str}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)

    # 2. History List View
    if not st.session_state.history:
        st.info("No calculation history available yet.")
    else:
        st.markdown('<div class="history-container">', unsafe_allow_html=True)
        for idx, item in enumerate(st.session_state.history, start=1):
            if isinstance(item, dict):
                timestamp = item.get("timestamp", "Date unavailable")
                calc_type = item.get("calc_type", "Calculation")
                expr = item.get("expr", "")
                result = item.get("result", "")
                details = item.get("details", "")

                st.markdown(
                    f"""
                    <div class="history-item-card">
                        <div class="history-item-top">
                            <span>🕒 {timestamp}</span>
                            <span class="history-badge">{calc_type}</span>
                        </div>
                        <div class="history-item-math">
                            <span><strong class="history-idx">{idx}.</strong> {expr}</span>
                            <strong class="history-res">= {result}</strong>
                        </div>
                        {f'<div class="history-details">{details}</div>' if details else ''}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                str_item = str(item)
                st.markdown(
                    f"""
                    <div class="history-item-card">
                        <div class="history-item-top">
                            <span>🕒 Date unavailable</span>
                            <span class="history-badge">Calculation</span>
                        </div>
                        <div class="history-item-math">
                            <span><strong class="history-idx">{idx}.</strong> {str_item}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        st.markdown('</div>', unsafe_allow_html=True)

        # 3. Action Buttons Row (Download CSV & Clear History)
        btn_col1, btn_col2 = st.columns([1, 1])
        with btn_col1:
            csv_data = generate_history_csv()
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name="calculation_history.csv",
                mime="text/csv",
                key="btn_download_csv",
                use_container_width=True
            )
        with btn_col2:
            st.button("🗑️ Clear History", key="btn_clear_hist", on_click=clear_history, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# 5. FOOTER
# ==============================================================================
st.markdown("""
<div class="footer-box">
    <p class="footer-line1">Built with <span class="footer-highlight">Python</span> & <span class="footer-highlight">Streamlit</span></p>
    <p class="footer-line2">By <span class="footer-author">Rajan</span></p>
</div>
""", unsafe_allow_html=True)
