"""
Campus Equipment Predictive Maintenance Telemetry & Monitoring SCADA Dashboard
Topic: Predictive Maintenance Indicator for Campus Equipment
Engineered & Developed by: Habin Das

Ultra-Kinetic Animated Edition:
- Interactive HTML5 Glowing Particle Mesh & Constellation Background in Splash Intro
- Futuristic Laser Scanlines & Tech Crosshair HUD
- "Made by Habin Das" Holographic Gold Badge with Glowing Micro-animations
- Physics-Driven Animated Turbine Impeller (RPM rotation + blade motion blur)
- Animated Fluid Piping Circulation (Dash-offset fluid flow)
- Thermal Infrared Runaway Waveform & Mechanical Chassis Shudder FX
- Concentric Ripple Rings on Hazard Beacons
- 3D Interactive Equipment State Space Manifold (WebGL)
- 14-Day Forward Degradation Forecast Curve
- Batch CSV Telemetry Inspector with Downloadable Reports
- Multi-Model Algorithm Benchmark Arena & ROC Curves (No School Rubrics)
"""

import os
import io
import time
import joblib
import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Page Setup
st.set_page_config(
    page_title="Campus SCADA Predictive Maintenance Engine • Habin Das",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="auto"
)

# Session state initialization for Intro Splash
if "view" in st.query_params and st.query_params["view"] in ["dashboard", "blueprint", "app"]:
    st.session_state.intro_dismissed = True

if "intro_dismissed" not in st.session_state:
    st.session_state.intro_dismissed = False

# High-Grade Animated Industrial SCADA Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Outfit:wght@300;400;600;700;800;900&family=Orbitron:wght@600;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    code, pre, .mono {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Ambient Industrial Dark Background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #0d1527 0%, #050811 95%);
        color: #f1f5f9;
    }

    /* ========================================= */
    /* ULTRA-ANIMATED CINEMATIC INTRO SCREEN     */
    /* ========================================= */
    .intro-wrapper {
        position: relative;
        border: 2px solid rgba(56, 189, 248, 0.4);
        border-radius: 24px;
        background: radial-gradient(circle at center, #0e1c3e 0%, #060913 100%);
        box-shadow: 0 0 70px rgba(56, 189, 248, 0.3), inset 0 0 50px rgba(0, 0, 0, 0.85);
        padding: 50px 30px;
        text-align: center;
        margin: 15px auto 35px auto;
        overflow: hidden;
        animation: introPop 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes introPop {
        from { opacity: 0; transform: scale(0.95) translateY(30px); }
        to { opacity: 1; transform: scale(1) translateY(0); }
    }

    /* Animated Canvas Container */
    #particle-canvas {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
    }

    .intro-content {
        position: relative;
        z-index: 2;
    }

    /* Holographic Laser Sweep */
    .laser-scanner {
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, transparent, #38bdf8, #818cf8, #c084fc, transparent);
        box-shadow: 0 0 20px #38bdf8, 0 0 40px #818cf8;
        animation: laserSweep 3s ease-in-out infinite alternate;
        z-index: 3;
    }
    @keyframes laserSweep {
        0% { left: -70%; }
        100% { left: 70%; }
    }

    .intro-tag-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 24px;
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.5);
        border-radius: 40px;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.85rem;
        letter-spacing: 0.22em;
        color: #38bdf8;
        text-transform: uppercase;
        margin-bottom: 24px;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.35);
        animation: tagPulse 2s infinite alternate;
    }
    @keyframes tagPulse {
        0% { transform: scale(0.98); box-shadow: 0 0 15px rgba(56, 189, 248, 0.2); }
        100% { transform: scale(1.02); box-shadow: 0 0 35px rgba(56, 189, 248, 0.5); }
    }

    .intro-main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        line-height: 1.15;
        letter-spacing: -0.01em;
        background: linear-gradient(135deg, #ffffff 0%, #38bdf8 45%, #a855f7 90%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 14px;
        text-shadow: 0 0 40px rgba(56, 189, 248, 0.5);
    }

    .intro-sub-text {
        font-size: 1.25rem;
        color: #94a3b8;
        max-width: 840px;
        margin: 0 auto 30px auto;
        letter-spacing: 0.04em;
        line-height: 1.5;
    }

    /* Habin Das Holographic Frame */
    .habin-frame {
        display: inline-flex;
        flex-direction: column;
        align-items: center;
        background: rgba(15, 23, 42, 0.85);
        border: 2px solid #f59e0b;
        border-radius: 16px;
        padding: 16px 36px;
        margin-bottom: 25px;
        box-shadow: 0 0 35px rgba(245, 158, 11, 0.35), inset 0 0 20px rgba(245, 158, 11, 0.15);
        position: relative;
        animation: frameGlow 2.5s ease-in-out infinite alternate;
    }
    @keyframes frameGlow {
        0% { border-color: rgba(245, 158, 11, 0.6); box-shadow: 0 0 20px rgba(245, 158, 11, 0.2); }
        100% { border-color: #fbbf24; box-shadow: 0 0 45px rgba(245, 158, 11, 0.6); }
    }
    .habin-role {
        font-size: 0.8rem;
        letter-spacing: 0.25em;
        color: #f59e0b;
        text-transform: uppercase;
        font-weight: 800;
        font-family: 'Orbitron', sans-serif;
        margin-bottom: 4px;
    }
    .habin-name {
        font-size: 2.1rem;
        font-weight: 900;
        font-family: 'Outfit', sans-serif;
        letter-spacing: 0.08em;
        background: linear-gradient(90deg, #f59e0b, #fde047, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Progress bar animation */
    .intro-progress-bar-wrap {
        width: 320px;
        height: 6px;
        background: rgba(30, 41, 59, 0.8);
        border-radius: 6px;
        margin: 20px auto 10px auto;
        overflow: hidden;
        border: 1px solid rgba(56, 189, 248, 0.3);
    }
    .intro-progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #a855f7);
        border-radius: 6px;
        animation: progressFill 1.6s cubic-bezier(0.65, 0, 0.35, 1) forwards;
    }
    @keyframes progressFill {
        0% { width: 0%; }
        100% { width: 100%; }
    }

    /* ========================================= */
    /* DASHBOARD CARD & SCADA STYLING            */
    /* ========================================= */
    .scada-card {
        background: rgba(18, 26, 43, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .scada-card:hover {
        border-color: rgba(56, 189, 248, 0.55);
        box-shadow: 0 12px 36px rgba(56, 189, 248, 0.2);
        transform: translateY(-2px);
    }

    .brand-logo-badge {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 52px;
        height: 52px;
        border-radius: 14px;
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.22), rgba(168, 85, 247, 0.22));
        border: 1.5px solid rgba(56, 189, 248, 0.65);
        box-shadow: 0 0 22px rgba(56, 189, 248, 0.45);
        flex-shrink: 0;
        animation: logoGlow 2.5s infinite alternate;
        transition: transform 0.3s ease;
    }
    .brand-logo-badge:hover {
        transform: scale(1.05);
        border-color: #38bdf8;
    }
    @keyframes logoGlow {
        0% { box-shadow: 0 0 12px rgba(56, 189, 248, 0.3); border-color: rgba(56, 189, 248, 0.5); }
        100% { box-shadow: 0 0 28px rgba(56, 189, 248, 0.7); border-color: rgba(56, 189, 248, 0.95); }
    }
    .architect-badge {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.92), rgba(30, 41, 59, 0.88));
        border: 1.5px solid rgba(245, 158, 11, 0.45);
        border-radius: 12px;
        padding: 8px 16px;
        text-align: right;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4), 0 0 16px rgba(245, 158, 11, 0.2);
        transition: all 0.3s ease;
    }
    .architect-badge:hover {
        border-color: #f59e0b;
        box-shadow: 0 6px 24px rgba(245, 158, 11, 0.35);
    }

    .scada-header-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.85));
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 14px;
        padding: 18px 24px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
        position: relative;
        overflow: hidden;
    }
    .scada-header-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #38bdf8, transparent);
        animation: scanLine 3s linear infinite;
    }
    @keyframes scanLine {
        0% { left: -100%; }
        100% { left: 100%; }
    }

    .scada-title {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
        margin: 0;
    }

    .metric-title {
        font-size: 0.82rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        margin-bottom: 6px;
    }

    .metric-value-huge {
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Radar Beacon Sweep with Concentric Rings */
    .radar-wrapper {
        display: inline-flex;
        align-items: center;
        gap: 12px;
    }
    .radar-dish {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        border: 2px solid rgba(56, 189, 248, 0.6);
        position: relative;
        background: conic-gradient(from 0deg, rgba(56, 189, 248, 0.9) 0deg, transparent 90deg, transparent 360deg);
        animation: radarSweep 2s linear infinite;
    }
    @keyframes radarSweep {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-family: 'JetBrains Mono', monospace;
        transition: all 0.3s ease;
    }
    .badge-normal {
        background: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        border: 1px solid rgba(74, 222, 128, 0.4);
        box-shadow: 0 0 14px rgba(74, 222, 128, 0.25);
    }
    .badge-caution {
        background: rgba(234, 179, 8, 0.2);
        color: #facc15;
        border: 1px solid rgba(250, 204, 21, 0.5);
        box-shadow: 0 0 18px rgba(250, 204, 21, 0.3);
    }
    .badge-critical {
        background: rgba(239, 68, 68, 0.25);
        color: #f87171;
        border: 1px solid rgba(248, 113, 113, 0.6);
        box-shadow: 0 0 28px rgba(248, 113, 113, 0.5);
        animation: criticalBlink 0.9s infinite alternate;
    }
    @keyframes criticalBlink {
        0% { transform: scale(0.97); opacity: 0.75; }
        100% { transform: scale(1.03); opacity: 1; }
    }

    /* ANIMATED SVG BLUEPRINT STYLING */
    .blueprint-svg {
        background: #090e17;
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 16px;
        width: 100%;
        overflow: hidden;
    }

    /* Dynamic fluid pipe flow */
    .fluid-flow {
        stroke-dasharray: 8 6;
        animation: fluidFlow 0.75s linear infinite;
    }
    @keyframes fluidFlow {
        from { stroke-dashoffset: 28; }
        to { stroke-dashoffset: 0; }
    }

    /* Vibration Mechanical Shake */
    .motor-shake {
        animation: mechanicalShake 0.1s linear infinite;
        transform-origin: center;
    }
    @keyframes mechanicalShake {
        0% { transform: translate(0, 0); }
        25% { transform: translate(-2px, 2px); }
        50% { transform: translate(2px, -2px); }
        75% { transform: translate(-1.5px, -1.5px); }
        100% { transform: translate(0, 0); }
    }

    /* Rotating Impeller Turbine */
    .rotating-rotor {
        transform-origin: 370px 140px;
        animation: rotorSpin 1s linear infinite;
    }
    .rotating-rotor-fast {
        transform-origin: 370px 140px;
        animation: rotorSpin 0.35s linear infinite;
    }
    .rotating-rotor-erratic {
        transform-origin: 370px 140px;
        animation: rotorWobble 0.25s cubic-bezier(.36,.07,.19,.97) infinite;
    }
    @keyframes rotorSpin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    @keyframes rotorWobble {
        0% { transform: rotate(0deg) scale(0.97); }
        50% { transform: rotate(180deg) scale(1.03) skewX(3deg); }
        100% { transform: rotate(360deg) scale(0.97); }
    }

    /* Thermal Heat Shimmer */
    .thermal-glow {
        animation: heatGlow 1.5s ease-in-out infinite alternate;
    }
    @keyframes heatGlow {
        0% { filter: drop-shadow(0 0 5px rgba(239, 68, 68, 0.4)); opacity: 0.65; }
        100% { filter: drop-shadow(0 0 22px rgba(239, 68, 68, 1)); opacity: 1; }
    }

    /* Work Order Print Design */
    .work-order-ticket {
        background: #0f172a;
        border: 2px solid #334155;
        border-left: 6px solid #38bdf8;
        border-radius: 8px;
        padding: 24px;
        font-family: 'JetBrains Mono', monospace;
        color: #e2e8f0;
    }
    .barcode-line {
        letter-spacing: 4px;
        font-size: 1.1rem;
        color: #64748b;
    }

    /* ========================================= */
    /* MOBILE & TABLET RESPONSIVE MEDIA QUERIES  */
    /* ========================================= */
    @media (max-width: 768px) {
        .scada-header-card {
            flex-direction: column !important;
            align-items: flex-start !important;
            padding: 14px 16px !important;
            gap: 12px !important;
        }
        .scada-title {
            font-size: 1.35rem !important;
            line-height: 1.2 !important;
        }
        .metric-value-huge {
            font-size: 1.75rem !important;
        }
        .scada-card {
            padding: 14px 16px !important;
            margin-bottom: 12px !important;
        }
        .work-order-ticket {
            padding: 16px 14px !important;
        }
        .work-order-ticket > div:nth-child(2) {
            grid-template-columns: 1fr !important;
            gap: 8px !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            overflow-x: auto !important;
            flex-wrap: nowrap !important;
            padding-bottom: 6px !important;
            gap: 6px !important;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 8px 12px !important;
            font-size: 0.85rem !important;
            white-space: nowrap !important;
        }
    }

    @media (max-width: 480px) {
        .scada-title {
            font-size: 1.15rem !important;
        }
        .metric-value-huge {
            font-size: 1.5rem !important;
        }
        .status-badge {
            font-size: 0.75rem !important;
            padding: 4px 12px !important;
        }
    }

    /* Android Specific Resolution & WebView Port Optimization (360px - 430px) */
    @media screen and (max-width: 430px) {
        body, .stApp {
            overflow-x: hidden !important;
            width: 100vw !important;
        }
        .main .block-container {
            padding-left: 10px !important;
            padding-right: 10px !important;
            padding-top: 15px !important;
            padding-bottom: 25px !important;
            max-width: 100% !important;
        }
        .scada-header-card {
            padding: 12px 14px !important;
            border-radius: 12px !important;
        }
        .scada-title {
            font-size: 1.15rem !important;
            letter-spacing: -0.01em !important;
        }
        .metric-value-huge {
            font-size: 1.55rem !important;
        }
        .scada-card {
            padding: 12px 14px !important;
            border-radius: 12px !important;
        }
        .status-badge {
            font-size: 0.72rem !important;
            padding: 4px 10px !important;
        }
        /* Touch action optimizations for Android port */
        button, [role="button"], input[type="range"] {
            min-height: 44px !important;
            touch-action: manipulation !important;
        }
        .stSlider {
            padding: 6px 0 !important;
        }
        .stSelectbox, .stButton {
            width: 100% !important;
        }
        .stAlert {
            padding: 10px 14px !important;
            font-size: 0.85rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# CINEMATIC INTRO SPLASH OVERLAY (IFRAME)
# ==========================================
if not st.session_state.intro_dismissed:
    intro_html_doc = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Outfit:wght@300;400;600;700;800;900&family=Orbitron:wght@600;800;900&display=swap');

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Outfit', sans-serif;
        }

        body {
            background: transparent;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 10px;
            overflow: hidden;
        }

        .intro-wrapper {
            position: relative;
            width: 100%;
            max-width: 1050px;
            border: 2px solid rgba(56, 189, 248, 0.45);
            border-radius: 24px;
            background: radial-gradient(circle at center, #0e1c3e 0%, #060913 100%);
            box-shadow: 0 0 70px rgba(56, 189, 248, 0.35), inset 0 0 50px rgba(0, 0, 0, 0.85);
            padding: 40px 25px;
            text-align: center;
            overflow: hidden;
        }

        #particle-canvas {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
        }

        .intro-content {
            position: relative;
            z-index: 2;
        }

        .laser-scanner {
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, transparent, #38bdf8, #818cf8, #c084fc, transparent);
            box-shadow: 0 0 20px #38bdf8, 0 0 40px #818cf8;
            animation: laserSweep 3s ease-in-out infinite alternate;
            z-index: 3;
        }
        @keyframes laserSweep {
            0% { left: -70%; }
            100% { left: 70%; }
        }

        .intro-tag-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 24px;
            background: rgba(56, 189, 248, 0.15);
            border: 1px solid rgba(56, 189, 248, 0.5);
            border-radius: 40px;
            font-family: 'Orbitron', sans-serif;
            font-size: 0.82rem;
            letter-spacing: 0.22em;
            color: #38bdf8;
            text-transform: uppercase;
            margin-bottom: 18px;
            box-shadow: 0 0 25px rgba(56, 189, 248, 0.35);
        }

        .intro-main-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem;
            font-weight: 900;
            line-height: 1.15;
            letter-spacing: -0.01em;
            background: linear-gradient(135deg, #ffffff 0%, #38bdf8 45%, #a855f7 90%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 12px;
            text-shadow: 0 0 40px rgba(56, 189, 248, 0.5);
        }

        .intro-sub-text {
            font-size: 1.1rem;
            color: #94a3b8;
            max-width: 800px;
            margin: 0 auto 22px auto;
            letter-spacing: 0.04em;
            line-height: 1.5;
        }

        .habin-frame {
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            background: rgba(15, 23, 42, 0.9);
            border: 2px solid #f59e0b;
            border-radius: 16px;
            padding: 12px 38px;
            margin-bottom: 18px;
            box-shadow: 0 0 35px rgba(245, 158, 11, 0.35), inset 0 0 20px rgba(245, 158, 11, 0.15);
            animation: frameGlow 2.5s ease-in-out infinite alternate;
        }
        @keyframes frameGlow {
            0% { border-color: rgba(245, 158, 11, 0.6); box-shadow: 0 0 20px rgba(245, 158, 11, 0.2); }
            100% { border-color: #fbbf24; box-shadow: 0 0 45px rgba(245, 158, 11, 0.6); }
        }

        .habin-role {
            font-size: 0.78rem;
            letter-spacing: 0.25em;
            color: #f59e0b;
            text-transform: uppercase;
            font-weight: 800;
            font-family: 'Orbitron', sans-serif;
            margin-bottom: 4px;
        }

        .habin-name {
            font-size: 2.1rem;
            font-weight: 900;
            font-family: 'Outfit', sans-serif;
            letter-spacing: 0.08em;
            background: linear-gradient(90deg, #f59e0b, #fde047, #ffffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .intro-progress-bar-wrap {
            width: 340px;
            height: 6px;
            background: rgba(30, 41, 59, 0.8);
            border-radius: 6px;
            margin: 14px auto 8px auto;
            overflow: hidden;
            border: 1px solid rgba(56, 189, 248, 0.3);
        }

        .intro-progress-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #38bdf8, #818cf8, #a855f7);
            border-radius: 6px;
            animation: progressFill 1.8s cubic-bezier(0.65, 0, 0.35, 1) forwards;
        }
        @keyframes progressFill {
            0% { width: 0%; }
            100% { width: 100%; }
        }

        .kernel-status {
            font-size: 0.78rem;
            color: #64748b;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 0.1em;
        }

        /* Responsive Mobile Styles for Intro */
        @media (max-width: 768px) {
            .intro-wrapper {
                padding: 24px 14px !important;
                border-radius: 18px !important;
            }
            .intro-tag-pill {
                padding: 6px 14px !important;
                font-size: 0.7rem !important;
                letter-spacing: 0.14em !important;
                margin-bottom: 14px !important;
            }
            .intro-main-title {
                font-size: 1.55rem !important;
                line-height: 1.25 !important;
                margin-bottom: 10px !important;
            }
            .intro-sub-text {
                font-size: 0.9rem !important;
                line-height: 1.4 !important;
                margin-bottom: 16px !important;
            }
            .habin-frame {
                padding: 10px 22px !important;
                margin-bottom: 14px !important;
            }
            .habin-role {
                font-size: 0.68rem !important;
                letter-spacing: 0.18em !important;
            }
            .habin-name {
                font-size: 1.55rem !important;
            }
            .intro-progress-bar-wrap {
                width: 220px !important;
                margin: 12px auto 6px auto !important;
            }
            .kernel-status {
                font-size: 0.7rem !important;
            }
        }
    </style>
    </head>
    <body>
    <div class="intro-wrapper">
        <div class="laser-scanner"></div>
        <canvas id="particle-canvas"></canvas>

        <div class="intro-content">
            <div style="display: flex; justify-content: center; margin-bottom: 18px;">
                <div class="brand-logo-badge" style="width: 64px; height: 64px; border-radius: 18px;">
                    <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
                    </svg>
                </div>
            </div>
            <div class="intro-tag-pill">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
                </svg>
                <span>AUTONOMOUS SCADA AI ARCHITECTURE</span>
            </div>
            
            <h1 class="intro-main-title">
                PREDICTIVE MAINTENANCE INDICATOR<br>
                FOR CAMPUS EQUIPMENT
            </h1>
            
            <p class="intro-sub-text">
                Physics-Informed Anomaly Detection • Continuous Telemetry Stream Analysis • Remaining Useful Life (RUL) Regression Engine
            </p>
            
            <div class="habin-frame">
                <span class="habin-role">[ LEAD SYSTEM ARCHITECT ]</span>
                <span class="habin-name">HABIN DAS H</span>
                <span style="font-size: 0.72rem; color: #38bdf8; font-family: 'JetBrains Mono', monospace; letter-spacing: 0.12em; margin-top: 3px;">BCA 2ND YEAR • ARTIFICIAL INTELLIGENCE</span>
            </div>

            <div class="intro-progress-bar-wrap">
                <div class="intro-progress-bar-fill"></div>
            </div>
            <div class="kernel-status">
                INITIALIZING SCADA TELEMETRY KERNEL [100% READY]
            </div>
        </div>
    </div>

    <script>
    (function() {
        var canvas = document.getElementById('particle-canvas');
        if (!canvas) return;
        var ctx = canvas.getContext('2d');
        var width, height;
        var particles = [];

        function resize() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        }
        resize();
        window.addEventListener('resize', resize);

        for (var i = 0; i < 55; i++) {
            particles.push({
                x: Math.random() * (width || 800),
                y: Math.random() * (height || 500),
                vx: (Math.random() - 0.5) * 1.2,
                vy: (Math.random() - 0.5) * 1.2,
                radius: Math.random() * 2 + 1.2
            });
        }

        function draw() {
            if (!width || !height) resize();
            ctx.clearRect(0, 0, width, height);
            ctx.fillStyle = 'rgba(56, 189, 248, 0.8)';
            ctx.strokeStyle = 'rgba(56, 189, 248, 0.18)';
            ctx.lineWidth = 1;

            for (var i = 0; i < particles.length; i++) {
                var p = particles[i];
                p.x += p.vx;
                p.y += p.vy;

                if (p.x < 0 || p.x > width) p.vx *= -1;
                if (p.y < 0 || p.y > height) p.vy *= -1;

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                ctx.fill();

                for (var j = i + 1; j < particles.length; j++) {
                    var p2 = particles[j];
                    var dist = Math.hypot(p.x - p2.x, p.y - p2.y);
                    if (dist < 115) {
                        ctx.beginPath();
                        ctx.moveTo(p.x, p.y);
                        ctx.lineTo(p2.x, p2.y);
                        ctx.stroke();
                    }
                }
            }
            requestAnimationFrame(draw);
        }
        draw();
    })();
    </script>
    </body>
    </html>
    """

    components.html(intro_html_doc, height=520)

    c_center1, c_center2, c_center3 = st.columns([1, 1.4, 1])
    with c_center2:
        if st.button("🚀 ENTER ACTIVE SCADA COMMAND CONSOLE", use_container_width=True):
            st.session_state.intro_dismissed = True
            st.rerun()

        pdf_path = os.path.join(os.path.dirname(__file__), "Predictive_Maintenance_Project_Report.pdf")
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f_pdf:
                st.download_button(
                    label="📄 DOWNLOAD TECHNICAL PROJECT REPORT (PDF)",
                    data=f_pdf.read(),
                    file_name="Predictive_Maintenance_Project_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

    st.stop()


# Machine Profiles
EQUIPMENT_PROFILES = {
    "Chiller-Central-01": {
        "name": "Central Library Industrial Chiller 01",
        "type": "HVAC Chiller",
        "location": "Central Utility Plant • Sub-Basement B2",
        "diagram_icon": "❄️",
        "temp_base": 58.0,
        "vib_base": 1.1,
        "pressure_base": 52.0,
        "power_base": 42.0,
        "sound_base": 62.0,
        "critical_parts": ["Evaporator Expansion Valve", "Trane Centrifugal Bearing Set", "R-134a Seal Gasket"],
        "downtime_cost_per_hr": 1450,
        "campus_impact": "Loss of cooling to Main Library & 4 Lecture Halls (≈ 1,800 students)"
    },
    "AHU-Library-North": {
        "name": "Rooftop Air Handling Unit North",
        "type": "Air Handling Unit",
        "location": "Science Quad • Building 4 Roof",
        "diagram_icon": "💨",
        "temp_base": 42.0,
        "vib_base": 0.8,
        "pressure_base": 30.0,
        "power_base": 18.0,
        "sound_base": 55.0,
        "critical_parts": ["Supply Blower Belt", "MERV 14 Filter Pack", "Variable Frequency Drive Module"],
        "downtime_cost_per_hr": 680,
        "campus_impact": "Stagnant airflow & lab fume hood negative pressure disruption (≈ 450 researchers)"
    },
    "Pump-MainLoop-03": {
        "name": "Primary Campus Hydronic Circulation Pump",
        "type": "Water Circulation Pump",
        "location": "Tunnel Junction J-12 • Steam/Water Main",
        "diagram_icon": "🔄",
        "temp_base": 50.0,
        "vib_base": 1.4,
        "pressure_base": 65.0,
        "power_base": 28.0,
        "sound_base": 68.0,
        "critical_parts": ["Silicon Carbide Mechanical Shaft Seal", "Bronze Closed Impeller", "SKF 6309 Deep Groove Bearing"],
        "downtime_cost_per_hr": 2100,
        "campus_impact": "Total heating loop shutdown across Residential Quad (≈ 3,200 residents)"
    },
    "GenSet-Emergency-A": {
        "name": "Emergency Standby Diesel Generator 1200kVA",
        "type": "Diesel Generator",
        "location": "Auxiliary Power Vault • North Gate",
        "diagram_icon": "⚡",
        "temp_base": 82.0,
        "vib_base": 2.2,
        "pressure_base": 45.0,
        "power_base": 85.0,
        "sound_base": 78.0,
        "critical_parts": ["Bosch Common Rail Fuel Injector", "Turbocharger Impeller Bearing", "Dual Starter Solenoid"],
        "downtime_cost_per_hr": 4800,
        "campus_impact": "Failure of backup power to Data Center & Medical Research Freezers"
    }
}


@st.cache_resource
def load_trained_model():
    """Loads or trains the predictive model bundle."""
    model_path = "predictive_maintenance_model.joblib"
    if not os.path.exists(model_path):
        from train_model import train_predictive_maintenance_pipeline
        return train_predictive_maintenance_pipeline()
    return joblib.load(model_path)


model_bundle = load_trained_model()
clf = model_bundle["classifier"]
reg = model_bundle["regressor"]
metrics = model_bundle.get("metrics", {})
feat_imp = model_bundle.get("feature_importances", [])
benchmark_data = model_bundle.get("benchmark", [])
cm_data = model_bundle.get("confusion_matrix", [[1376, 5], [5, 114]])
roc_data = model_bundle.get("roc_curves", {})


# ==========================================
# SIDEBAR CONTROLS
# ==========================================
st.sidebar.markdown("""
<div style="text-align: center; padding: 16px 12px; background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.88)); border-radius: 14px; border: 1.5px solid rgba(245, 158, 11, 0.55); margin-bottom: 16px; box-shadow: 0 4px 24px rgba(0, 0, 0, 0.5), 0 0 18px rgba(245, 158, 11, 0.25);">
    <div style="display: inline-flex; align-items: center; justify-content: center; width: 48px; height: 48px; border-radius: 14px; background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(234, 179, 8, 0.1)); border: 1.5px solid #f59e0b; margin-bottom: 10px; box-shadow: 0 0 16px rgba(245, 158, 11, 0.4);">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
            <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
        </svg>
    </div>
    <div style="font-size: 0.68rem; color: #f59e0b; letter-spacing: 0.18em; font-weight: 800; font-family: 'Orbitron', sans-serif;">LEAD SYSTEM ARCHITECT</div>
    <div style="font-size: 1.35rem; font-weight: 900; color: #ffffff; letter-spacing: 0.04em; margin-top: 3px;">HABIN DAS H</div>
    <div style="font-size: 0.72rem; color: #38bdf8; font-family: 'JetBrains Mono', monospace; margin-top: 4px; letter-spacing: 0.08em;">BCA 2ND YEAR • ARTIFICIAL INTELLIGENCE</div>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("🎬 Replay Cinematic Intro", use_container_width=True):
    st.session_state.intro_dismissed = False
    st.rerun()

pdf_report_path = os.path.join(os.path.dirname(__file__), "Predictive_Maintenance_Project_Report.pdf")
if os.path.exists(pdf_report_path):
    with open(pdf_report_path, "rb") as f_pdf:
        st.sidebar.download_button(
            label="📄 Download Project Report (PDF)",
            data=f_pdf.read(),
            file_name="Predictive_Maintenance_Project_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.sidebar.markdown("### 🏢 Campus Machinery Fleet")
selected_key = st.sidebar.selectbox(
    "Monitored Asset:",
    options=list(EQUIPMENT_PROFILES.keys()),
    format_func=lambda k: f"{EQUIPMENT_PROFILES[k]['diagram_icon']} {k}"
)
profile = EQUIPMENT_PROFILES[selected_key]

st.sidebar.markdown(f"**Asset:** `{profile['name']}`  \n**Location:** `{profile['location']}`")
st.sidebar.divider()

# Live Telemetry Auto-Stream Simulator Toggle
st.sidebar.markdown("### ⚡ Live Replay & Simulation")
auto_stream = st.sidebar.toggle("▶️ Live Telemetry Auto-Stream (Animated Replay)", value=False)
if auto_stream:
    stream_step = int((time.time() * 2) % 100)
    sim_noise_temp = np.sin(stream_step * 0.2) * 4.0
    sim_noise_vib = np.cos(stream_step * 0.25) * 0.25
else:
    sim_noise_temp = 0.0
    sim_noise_vib = 0.0

# Quick Presets
st.sidebar.markdown("### 🧪 Telemetry Scenario Injector")
scenario = st.sidebar.selectbox(
    "Instant Test Scenario:",
    [
        "🟢 Nominal Operation (Safe & Steady)",
        "🟡 Early Bearing Wear (Vibration Harmonic Spike)",
        "🔴 Thermal Runaway (Cooling Failure)",
        "🔴 Hydraulic Cavitation (Loop Pressure Collapse)",
        "⚠️ Catastrophic Multi-Fault Imminent"
    ]
)

if scenario.startswith("🟢"):
    d_hours, d_temp, d_vib, d_press, d_kw, d_sound = 2450.0, profile["temp_base"] + 1.2, profile["vib_base"] + 0.1, profile["pressure_base"] - 0.5, profile["power_base"] + 1.0, profile["sound_base"] + 0.8
elif scenario.startswith("🟡"):
    d_hours, d_temp, d_vib, d_press, d_kw, d_sound = 5400.0, profile["temp_base"] + 9.0, profile["vib_base"] + 1.6, profile["pressure_base"] - 3.5, profile["power_base"] + 6.5, profile["sound_base"] + 10.0
elif "Thermal" in scenario:
    d_hours, d_temp, d_vib, d_press, d_kw, d_sound = 4900.0, profile["temp_base"] + 34.0, profile["vib_base"] + 0.9, profile["pressure_base"] - 4.5, profile["power_base"] + 22.0, profile["sound_base"] + 6.5
elif "Hydraulic" in scenario:
    d_hours, d_temp, d_vib, d_press, d_kw, d_sound = 6100.0, profile["temp_base"] + 8.5, profile["vib_base"] + 2.2, max(5.0, profile["pressure_base"] - 29.0), profile["power_base"] + 15.0, profile["sound_base"] + 13.0
else: # Catastrophic
    d_hours, d_temp, d_vib, d_press, d_kw, d_sound = 8600.0, profile["temp_base"] + 42.0, profile["vib_base"] + 4.5, max(5.0, profile["pressure_base"] - 28.0), profile["power_base"] + 28.0, profile["sound_base"] + 24.0

st.sidebar.markdown("### 🎛️ Live Sensor Telemetry Sliders")
inp_hours = st.sidebar.slider("Operating Hours (hrs)", 100.0, 10000.0, float(d_hours), step=50.0)
inp_temp = st.sidebar.slider("Temperature (°C)", 20.0, 135.0, float(d_temp + sim_noise_temp), step=0.5)
inp_vib = st.sidebar.slider("Vibration RMS (mm/s)", 0.2, 9.0, float(max(0.1, d_vib + sim_noise_vib)), step=0.05)
inp_press = st.sidebar.slider("Hydraulic Pressure (psi)", 5.0, 105.0, float(d_press), step=0.5)
inp_kw = st.sidebar.slider("Power Consumption (kW)", 5.0, 150.0, float(d_kw), step=1.0)
inp_sound = st.sidebar.slider("Acoustic Sound Level (dB)", 35.0, 120.0, float(d_sound), step=0.5)

st.sidebar.divider()
enable_audio = st.sidebar.checkbox("🔊 Audio Alarm Synth on Critical Risk", value=True)


# ==========================================
# REAL-TIME INFERENCE ENGINE
# ==========================================
temp_base = profile["temp_base"]
vib_base = profile["vib_base"]
press_base = profile["pressure_base"]

temp_delta = inp_temp - temp_base
thermal_strain_index = (inp_temp / temp_base) * (inp_kw / 25.0)
vib_delta = inp_vib - vib_base
vibration_acoustic_coupling = inp_vib * (inp_sound / 50.0)
pressure_drop_pct = (press_base - inp_press) / press_base
mech_thermal_synergy = max(0.0, temp_delta) * max(0.0, vib_delta)
wear_fatigue_factor = (inp_hours / 5000.0) ** 1.5

feat_dict = {
    "operating_hours": [inp_hours],
    "temperature_c": [inp_temp],
    "vibration_rms": [inp_vib],
    "pressure_psi": [inp_press],
    "power_consumption_kw": [inp_kw],
    "sound_level_db": [inp_sound],
    "temp_delta": [temp_delta],
    "thermal_strain_index": [thermal_strain_index],
    "vib_delta": [vib_delta],
    "vibration_acoustic_coupling": [vibration_acoustic_coupling],
    "pressure_drop_pct": [pressure_drop_pct],
    "mech_thermal_synergy": [mech_thermal_synergy],
    "wear_fatigue_factor": [wear_fatigue_factor]
}

X_current = pd.DataFrame(feat_dict)
risk_proba = float(clf.predict_proba(X_current)[0, 1])
risk_pct = round(risk_proba * 100.0, 1)
pred_rul_hours = max(1.0, float(reg.predict(X_current)[0]))
pred_rul_days = round(pred_rul_hours / 24.0, 1)

# Status & Animation Classes
if risk_pct < 28.0:
    status_label = "NOMINAL • HEALTHY"
    badge_class = "badge-normal"
    badge_color = "#22c55e"
    action_window = "Next Routine Service in 30 Days"
    action_urgency = "LOW"
    action_recommendation = "Continue nominal operation. Lubricant and thermal dissipation envelopes are within safety margins."
    component_color_bearing = "#22c55e"
    component_color_thermal = "#38bdf8"
    component_color_pressure = "#22c55e"
    rotor_animation_class = "rotating-rotor"
    chassis_shake_class = ""
    thermal_glow_class = ""
elif risk_pct < 68.0:
    status_label = "ELEVATED WEAR • WARNING"
    badge_class = "badge-caution"
    badge_color = "#eab308"
    action_window = "Schedule Maintenance Inspection Within 7–14 Days"
    action_urgency = "ELEVATED"
    action_recommendation = "Plan an off-peak maintenance window. Inspect motor bearing clearances, balance rotor, and check filter differentials."
    component_color_bearing = "#eab308" if vib_delta > 0.8 else "#22c55e"
    component_color_thermal = "#f59e0b" if temp_delta > 10 else "#38bdf8"
    component_color_pressure = "#eab308" if pressure_drop_pct > 0.15 else "#22c55e"
    rotor_animation_class = "rotating-rotor-fast"
    chassis_shake_class = "motor-shake" if vib_delta > 1.0 else ""
    thermal_glow_class = "thermal-glow" if temp_delta > 15 else ""
else:
    status_label = "CRITICAL • BREAKDOWN IMMINENT"
    badge_class = "badge-critical"
    badge_color = "#ef4444"
    action_window = "EMERGENCY SHUTDOWN / DISPATCH WITHIN 24 HOURS"
    action_urgency = "URGENT / CRITICAL"
    action_recommendation = "IMMEDIATE INTERVENTION REQUIRED. High likelihood of bearing seizure, motor winding insulation breakdown, or mechanical lockup."
    component_color_bearing = "#ef4444"
    component_color_thermal = "#ef4444"
    component_color_pressure = "#ef4444"
    rotor_animation_class = "rotating-rotor-erratic"
    chassis_shake_class = "motor-shake"
    thermal_glow_class = "thermal-glow"


# Web Audio Beeper for Critical State
if enable_audio and risk_pct >= 68.0:
    st.markdown("""
    <script>
    (function() {
        try {
            var ctx = new (window.AudioContext || window.webkitAudioContext)();
            var osc = ctx.createOscillator();
            var gain = ctx.createGain();
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(880, ctx.currentTime);
            osc.frequency.setValueAtTime(440, ctx.currentTime + 0.15);
            gain.gain.setValueAtTime(0.08, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.35);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start();
            osc.stop(ctx.currentTime + 0.35);
        } catch(e) {}
    })();
    </script>
    """, unsafe_allow_html=True)


# ==========================================
# TOP HERO BAR WITH RADAR SWEEP & HABIN DAS
# ==========================================
st.markdown(f"""
<div class="scada-header-card">
    <div style="display: flex; align-items: center; gap: 16px;">
        <div class="brand-logo-badge">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
            </svg>
        </div>
        <div>
            <div class="radar-wrapper" style="margin-bottom: 4px;">
                <div class="radar-dish"></div>
                <span style="font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.14em; color: #38bdf8; font-weight: 700; font-family: 'JetBrains Mono', monospace;">
                    AUTONOMOUS SCADA TELEMETRY • LIVE STREAM
                </span>
            </div>
            <h1 class="scada-title">CAMPUS PREDICTIVE MAINTENANCE MONITOR</h1>
            <div style="font-size: 0.86rem; color: #94a3b8; margin-top: 4px;">
                Monitored Asset: <strong style="color: #38bdf8;">{profile['name']}</strong> [{selected_key}] • {profile['location']}
            </div>
        </div>
    </div>
    <div style="text-align: right; display: flex; flex-direction: column; align-items: flex-end; gap: 8px;">
        <span class="status-badge {badge_class}">{status_label}</span>
        <div class="architect-badge">
            <span style="font-size: 0.65rem; color: #f59e0b; letter-spacing: 0.16em; font-weight: 800; font-family: 'Orbitron', sans-serif;">LEAD SYSTEM ARCHITECT</span><br>
            <span style="font-size: 1.05rem; font-weight: 900; color: #ffffff; letter-spacing: 0.04em;">HABIN DAS H</span><br>
            <span style="font-size: 0.72rem; color: #38bdf8; font-family: 'JetBrains Mono', monospace;">BCA 2ND YEAR • ARTIFICIAL INTELLIGENCE</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# TABS ARCHITECTURE (CLEAN ENTERPRISE STRUCTURE)
tabs = st.tabs([
    "⚡ Active SCADA Diagnostics",
    "🌀 Animated Machine Physics Blueprint",
    "📈 Degradation Strip-Charts & 14D Forecast",
    "🌐 3D Machine State Space",
    "🔍 Feature Importance & SHAP",
    "📁 Batch Telemetry CSV Inspector",
    "🏆 Model Benchmark Arena & ROC Curves"
])


# ---------------------------------------------------------------------
# TAB 1: ACTIVE SCADA DIAGNOSTICS
# ---------------------------------------------------------------------
with tabs[0]:
    row1_c1, row1_c2, row1_c3 = st.columns([1.1, 1.1, 1.2])

    with row1_c1:
        # Speedometer Gauge Card
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_pct,
            domain={'x': [0.06, 0.94], 'y': [0.06, 0.94]},
            title={'text': "Breakdown Risk Score", 'font': {'size': 16, 'color': '#f8fafc', 'family': 'Outfit'}},
            number={'suffix': "%", 'font': {'size': 44, 'color': badge_color, 'family': 'JetBrains Mono'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1.5, 'tickcolor': "#64748b"},
                'bar': {'color': badge_color, 'thickness': 0.28},
                'bgcolor': "#0f172a",
                'borderwidth': 1,
                'bordercolor': "#334155",
                'steps': [
                    {'range': [0, 28], 'color': 'rgba(34, 197, 94, 0.22)'},
                    {'range': [28, 68], 'color': 'rgba(234, 179, 8, 0.22)'},
                    {'range': [68, 100], 'color': 'rgba(239, 68, 68, 0.32)'}
                ],
                'threshold': {
                    'line': {'color': "#ef4444", 'width': 3},
                    'thickness': 0.8,
                    'value': 68.0
                }
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=235,
            margin=dict(l=35, r=35, t=25, b=25)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

        st.markdown(f"""
        <div class="scada-card" style="padding: 16px 20px; margin-top: 10px;">
            <div class="metric-title">Dispatch Urgency</div>
            <div style="font-size: 1.15rem; font-weight: 700; color: {badge_color};">
                {action_urgency}
            </div>
            <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">
                ⏱️ Target Action Window: <strong>{action_window}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with row1_c2:
        health_reserve_pct = min(100.0, max(0.0, (pred_rul_hours / 1200.0) * 100.0))
        st.markdown(f"""
        <div class="scada-card">
            <div class="metric-title">Remaining Useful Life (RUL Regression Proxy)</div>
            <div class="metric-value-huge" style="color: #38bdf8;">
                {pred_rul_hours:.0f} <span style="font-size: 1rem; color: #94a3b8;">HRS</span>
            </div>
            <div style="font-size: 0.9rem; color: #94a3b8; margin-top: 2px;">
                ≈ <strong>{pred_rul_days}</strong> operational runtime days remaining
            </div>
            <div style="margin-top: 18px;">
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #94a3b8; margin-bottom: 6px;">
                    <span>Health Reserve Index</span>
                    <span style="font-weight: 700; color: {badge_color};">{health_reserve_pct:.1f}%</span>
                </div>
                <div style="background-color: #1e293b; border-radius: 8px; height: 12px; width: 100%; overflow: hidden; border: 1px solid #334155;">
                    <div style="background: linear-gradient(90deg, {badge_color}, #38bdf8); width: {health_reserve_pct}%; height: 100%; border-radius: 8px;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Cost & Campus Risk Calculator
        downtime_exposure = profile["downtime_cost_per_hr"] * (8 if risk_pct > 68 else 2)
        st.markdown(f"""
        <div class="scada-card" style="padding: 14px 18px;">
            <div class="metric-title">Financial & Campus Impact</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #f43f5e; font-family: 'JetBrains Mono', monospace;">
                ${downtime_exposure:,} <span style="font-size: 0.8rem; color: #94a3b8; font-weight: normal;">Unscheduled Outage Exposure</span>
            </div>
            <div style="font-size: 0.82rem; color: #cbd5e1; margin-top: 6px; line-height: 1.4;">
                🏫 <strong>Campus Scope:</strong> {profile['campus_impact']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with row1_c3:
        st.markdown("##### 📡 Live Telemetry Stream vs Rated Baseline")
        m_a, m_b = st.columns(2)
        with m_a:
            st.metric("Core Temp", f"{inp_temp:.1f} °C", delta=f"{temp_delta:+.1f} °C", delta_color="inverse")
            st.metric("Vibration RMS", f"{inp_vib:.2f} mm/s", delta=f"{vib_delta:+.2f} mm/s", delta_color="inverse")
            st.metric("Loop Pressure", f"{inp_press:.1f} psi", delta=f"{(inp_press - press_base):+.1f} psi")
        with m_b:
            st.metric("Power Load", f"{inp_kw:.1f} kW", delta=f"{(inp_kw - profile['power_base']):+.1f} kW", delta_color="inverse")
            st.metric("Sound Level", f"{inp_sound:.1f} dB", delta=f"{(inp_sound - profile['sound_base']):+.1f} dB", delta_color="inverse")
            st.metric("Run Hours", f"{inp_hours:,.0f} hrs")

    st.divider()

    # Maintenance Recommendation Directive
    st.markdown("#### 🛠️ AI Maintenance Action Directive")
    st.info(f"**Operator Directive:** {action_recommendation}")

    # Formal Printable Work Order Dispatch
    col_btn, col_empty = st.columns([1.5, 2.5])
    with col_btn:
        generate_ticket = st.button("🚨 Generate Official Campus Dispatch Work Order", width="stretch")

    if generate_ticket or risk_pct >= 68.0:
        ticket_id = f"WO-CMP-{selected_key[:4].upper()}-{np.random.randint(10000, 99999)}"
        st.markdown(f"""
        <div class="work-order-ticket">
            <div style="display: flex; justify-content: space-between; border-bottom: 1px dashed #475569; padding-bottom: 10px; margin-bottom: 12px;">
                <div>
                    <span style="font-size: 1.1rem; font-weight: 700; color: #38bdf8;">FACILITIES MAINTENANCE DIVISION • DISPATCH WORK ORDER</span><br>
                    <span style="font-size: 0.8rem; color: #94a3b8;">CAMPUS CENTRAL UTILITIES AUTOMATION DISPATCH SYSTEM</span>
                </div>
                <div style="text-align: right;">
                    <span style="color: {badge_color}; font-weight: 700; font-size: 1.1rem;">[{action_urgency}]</span><br>
                    <span style="font-size: 0.85rem; color: #cbd5e1;">TICKET ID: {ticket_id}</span>
                </div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.88rem;">
                <div><strong>ASSET IDENTIFIER:</strong> {profile['name']}</div>
                <div><strong>TIMESTAMP:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                <div><strong>PHYSICAL LOCATION:</strong> {profile['location']}</div>
                <div><strong>CURRENT RUNTIME:</strong> {inp_hours:,.0f} Operational Hours</div>
                <div><strong>AI FAILURE RISK:</strong> <span style="color: {badge_color}; font-weight: bold;">{risk_pct}% ({status_label})</span></div>
                <div><strong>ESTIMATED RUL:</strong> {pred_rul_hours:.0f} Hours (≈ {pred_rul_days} Days)</div>
                <div><strong>TARGET DISPATCH WINDOW:</strong> {action_window}</div>
                <div><strong>PREVENTATIVE SAVINGS:</strong> Approx ${downtime_exposure:,}</div>
            </div>
            <div style="margin-top: 14px; padding-top: 10px; border-top: 1px dashed #475569;">
                <div style="color: #f59e0b; font-weight: bold; margin-bottom: 4px;">REQUIRED REPLACEMENT INVENTORY & ACTION:</div>
                <div style="font-size: 0.85rem; color: #cbd5e1;">
                    • <strong>Primary Directives:</strong> {action_recommendation}<br>
                    • <strong>Requisition Critical Parts:</strong> {', '.join(profile['critical_parts'])}<br>
                    • <strong>Telemetry Snapshot:</strong> Temp: {inp_temp:.1f}°C (Δ{temp_delta:+.1f}) | Vib: {inp_vib:.2f} mm/s (Δ{vib_delta:+.2f}) | Press: {inp_press:.1f} psi
                </div>
            </div>
            <div style="margin-top: 16px; display: flex; justify-content: space-between; font-size: 0.8rem; color: #64748b;">
                <div>AUTHORIZED DISPATCH SIGNATURE: ____________________________________</div>
                <div class="barcode-line">||| | ||||| || |||||| | |||</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------------------
# TAB 2: ANIMATED MACHINE PHYSICS BLUEPRINT
# ---------------------------------------------------------------------
with tabs[1]:
    st.markdown(f"### 🌀 Physics-Driven Machinery Blueprint & Dynamic Animation • `{selected_key}`")
    st.caption("Live animated mechanical subcomponents: rotating impeller, vibrating stator, and hydraulic fluid streamlines.")

    bp_c1, bp_c2 = st.columns([1.6, 1.0])

    with bp_c1:
        svg_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=JetBrains+Mono:wght@600&display=swap');
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ background: transparent; overflow: hidden; }}
            .blueprint-svg {{
                background: #090e17;
                border: 1px solid #1e293b;
                border-radius: 14px;
                padding: 10px;
                width: 100%;
                height: 100%;
            }}
            .fluid-flow {{
                stroke-dasharray: 8 6;
                animation: fluidFlow 0.75s linear infinite;
            }}
            @keyframes fluidFlow {{
                from {{ stroke-dashoffset: 28; }}
                to {{ stroke-dashoffset: 0; }}
            }}
            .motor-shake {{
                animation: mechanicalShake 0.1s linear infinite;
                transform-origin: center;
            }}
            @keyframes mechanicalShake {{
                0% {{ transform: translate(0, 0); }}
                25% {{ transform: translate(-2px, 2px); }}
                50% {{ transform: translate(2px, -2px); }}
                75% {{ transform: translate(-1.5px, -1.5px); }}
                100% {{ transform: translate(0, 0); }}
            }}
            .rotating-rotor {{
                transform-origin: 370px 140px;
                animation: rotorSpin 1s linear infinite;
            }}
            .rotating-rotor-fast {{
                transform-origin: 370px 140px;
                animation: rotorSpin 0.35s linear infinite;
            }}
            .rotating-rotor-erratic {{
                transform-origin: 370px 140px;
                animation: rotorWobble 0.25s cubic-bezier(.36,.07,.19,.97) infinite;
            }}
            @keyframes rotorSpin {{
                from {{ transform: rotate(0deg); }}
                to {{ transform: rotate(360deg); }}
            }}
            @keyframes rotorWobble {{
                0% {{ transform: rotate(0deg) scale(0.97); }}
                50% {{ transform: rotate(180deg) scale(1.03) skewX(3deg); }}
                100% {{ transform: rotate(360deg) scale(0.97); }}
            }}
            .thermal-glow {{
                animation: heatGlow 1.5s ease-in-out infinite alternate;
            }}
            @keyframes heatGlow {{
                0% {{ filter: drop-shadow(0 0 5px rgba(239, 68, 68, 0.4)); opacity: 0.65; }}
                100% {{ filter: drop-shadow(0 0 22px rgba(239, 68, 68, 1)); opacity: 1; }}
            }}
        </style>
        </head>
        <body>
        <div class="blueprint-svg">
            <svg viewBox="0 0 700 280" style="width: 100%; height: auto;">
                <g class="{chassis_shake_class}">
                    <rect x="50" y="40" width="600" height="200" rx="14" fill="#0f172a" stroke="#334155" stroke-width="2"/>
                    <line x1="200" y1="40" x2="200" y2="240" stroke="#1e293b" stroke-dasharray="4"/>
                    <line x1="450" y1="40" x2="450" y2="240" stroke="#1e293b" stroke-dasharray="4"/>

                    <!-- Electric Motor Stator Housing -->
                    <rect x="80" y="70" width="100" height="140" rx="8" fill="#1e293b" stroke="#475569" stroke-width="2"/>
                    <text x="130" y="145" fill="#94a3b8" font-size="12" font-family="Outfit, sans-serif" text-anchor="middle">ELECTRIC MOTOR</text>

                    <!-- Bearing Assembly -->
                    <rect x="220" y="110" width="60" height="60" rx="4" fill="#1e293b" stroke="#475569" stroke-width="2"/>
                    <circle cx="250" cy="140" r="18" fill="none" stroke="{component_color_bearing}" stroke-width="3.5" class="{thermal_glow_class}"/>
                    <text x="250" y="190" fill="#94a3b8" font-size="11" font-family="Outfit, sans-serif" text-anchor="middle">BEARING TRAIN</text>

                    <!-- Rotating Core Rotor / Impeller -->
                    <circle cx="370" cy="140" r="55" fill="#1e293b" stroke="#475569" stroke-width="2"/>
                    
                    <!-- SVG Animated Impeller Turbine Blades -->
                    <g class="{rotor_animation_class}">
                        <path d="M 370 140 L 370 90 A 25 25 0 0 1 390 100 Z" fill="{component_color_pressure}" opacity="0.85"/>
                        <path d="M 370 140 L 420 140 A 25 25 0 0 1 410 160 Z" fill="{component_color_pressure}" opacity="0.85"/>
                        <path d="M 370 140 L 370 190 A 25 25 0 0 1 350 180 Z" fill="{component_color_pressure}" opacity="0.85"/>
                        <path d="M 370 140 L 320 140 A 25 25 0 0 1 330 120 Z" fill="{component_color_pressure}" opacity="0.85"/>
                        <circle cx="370" cy="140" r="12" fill="#334155" stroke="#94a3b8" stroke-width="2"/>
                    </g>
                    <text x="370" y="215" fill="#cbd5e1" font-size="12" font-family="Outfit, sans-serif" text-anchor="middle">TURBINE IMPELLER</text>

                    <!-- Animated Coolant / Hydraulic Flow Pipes -->
                    <path d="M 450 90 L 590 90 L 590 190 L 450 190" fill="none" stroke="#1e293b" stroke-width="8"/>
                    <path d="M 450 90 L 590 90 L 590 190 L 450 190" fill="none" stroke="{component_color_thermal}" stroke-width="4" class="fluid-flow {thermal_glow_class}"/>
                    <text x="520" y="145" fill="#94a3b8" font-size="11" font-family="Outfit, sans-serif" text-anchor="middle">HEAT EXCHANGER</text>

                    <!-- Interactive Sensor Node Callouts -->
                    <circle cx="250" cy="85" r="8" fill="{component_color_bearing}" stroke="#fff" stroke-width="2"/>
                    <text x="250" y="70" fill="{component_color_bearing}" font-size="11" font-family="JetBrains Mono, monospace" font-weight="bold" text-anchor="middle">
                        VIB: {inp_vib:.2f} mm/s
                    </text>

                    <circle cx="520" cy="85" r="8" fill="{component_color_thermal}" stroke="#fff" stroke-width="2"/>
                    <text x="520" y="70" fill="{component_color_thermal}" font-size="11" font-family="JetBrains Mono, monospace" font-weight="bold" text-anchor="middle">
                        TEMP: {inp_temp:.1f}°C
                    </text>

                    <circle cx="450" cy="190" r="8" fill="{component_color_pressure}" stroke="#fff" stroke-width="2"/>
                    <text x="450" y="215" fill="{component_color_pressure}" font-size="11" font-family="JetBrains Mono, monospace" font-weight="bold" text-anchor="middle">
                        PRESS: {inp_press:.1f} psi
                    </text>
                </g>
            </svg>
        </div>
        </body>
        </html>
        """
        components.html(svg_html, height=310)

    with bp_c2:
        st.markdown("#### Real-Time Physical Anomaly Diagnostics")
        
        # 1. Bearing
        if component_color_bearing == "#ef4444":
            st.error(f"""**1. Mechanical Bearing Train • CRITICAL**  
Current RMS: `{inp_vib:.2f} mm/s` (Nominal: `{vib_base:.2f}`)  

*Diagnosis:* Severe rotor-shaft imbalance causing chassis shudder.""")
        elif component_color_bearing == "#eab308":
            st.warning(f"""**1. Mechanical Bearing Train • ELEVATED WEAR**  
Current RMS: `{inp_vib:.2f} mm/s` (Nominal: `{vib_base:.2f}`)  

*Diagnosis:* Bearing race pitting or high harmonic imbalance.""")
        else:
            st.success(f"""**1. Mechanical Bearing Train • NOMINAL**  
Current RMS: `{inp_vib:.2f} mm/s` (Nominal: `{vib_base:.2f}`)  

*Diagnosis:* Smooth hydrodynamic oil wedge film.""")

        # 2. Impeller
        if risk_pct > 68:
            st.error(f"""**2. Core Turbine Rotor • ERRATIC OSCILLATION**  
Impeller State: `WOBBLE`  

*Diagnosis:* Severe rotational imbalance.""")
        elif risk_pct > 28:
            st.warning(f"""**2. Core Turbine Rotor • ELEVATED LOAD**  
Impeller State: `HIGH LOAD`  

*Diagnosis:* Minor cavitation resistance.""")
        else:
            st.success(f"""**2. Core Turbine Rotor • STABLE SPIN**  
Impeller State: `LAMINAR`  

*Diagnosis:* Stable laminar velocity profile.""")

        # 3. Cooling Loop
        if component_color_thermal == "#ef4444":
            st.error(f"""**3. Coolant / Hydraulic Pipe Loop • THERMAL RUNAWAY**  
Core Temp: `{inp_temp:.1f} °C` (Nominal: `{temp_base:.1f}`)  

*Diagnosis:* Thermal runaway glow active. Liquid vapor cavitation.""")
        elif component_color_thermal == "#f59e0b":
            st.warning(f"""**3. Coolant / Hydraulic Pipe Loop • ELEVATED HEAT**  
Core Temp: `{inp_temp:.1f} °C` (Nominal: `{temp_base:.1f}`)  

*Diagnosis:* Coolant heat absorption rate degraded.""")
        else:
            st.success(f"""**3. Coolant / Hydraulic Pipe Loop • NOMINAL**  
Core Temp: `{inp_temp:.1f} °C` (Nominal: `{temp_base:.1f}`)  

*Diagnosis:* Convective heat transfer within steady state.""")



# ---------------------------------------------------------------------
# TAB 3: DEGRADATION STRIP-CHARTS & 14-DAY FORECAST
# ---------------------------------------------------------------------
with tabs[2]:
    st.markdown("### 📈 Time-Series Waveforms & 14-Day Degradation Trajectory Forecast")
    st.caption("Historical rolling telemetry with Upper Control Limits (UCL) and forward-looking failure threshold trajectory.")

    # Rolling window
    np.random.seed(42)
    n_pts = 60
    t_stamps = [datetime.now() - timedelta(minutes=15 * (n_pts - i)) for i in range(n_pts)]
    hist_vib = np.linspace(vib_base, inp_vib, n_pts) + np.random.normal(0, 0.08, n_pts)
    hist_temp = np.linspace(temp_base, inp_temp, n_pts) + np.random.normal(0, 0.9, n_pts)
    
    col_w1, col_w2 = st.columns(2)

    with col_w1:
        fig_vib = go.Figure()
        fig_vib.add_trace(go.Scatter(x=t_stamps, y=hist_vib, mode='lines', name='Vibration RMS (mm/s)', line=dict(color='#38bdf8', width=2.5)))
        ucl_vib = vib_base + 1.5
        fig_vib.add_hline(y=ucl_vib, line_dash="dash", line_color="#ef4444", annotation_text="Upper Control Limit (UCL = Bearing Danger)", annotation_position="top right")
        fig_vib.update_layout(
            title="Vibration Trajectory vs Upper Control Limit (UCL)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8',
            height=300,
            margin=dict(l=45, r=25, t=40, b=35),
            xaxis=dict(showgrid=True, gridcolor='#1e293b'),
            yaxis=dict(showgrid=True, gridcolor='#1e293b')
        )
        st.plotly_chart(fig_vib, use_container_width=True)

    with col_w2:
        fig_tmp = go.Figure()
        fig_tmp.add_trace(go.Scatter(x=t_stamps, y=hist_temp, mode='lines', name='Core Temp (°C)', line=dict(color='#f59e0b', width=2.5)))
        ucl_temp = temp_base + 20.0
        fig_tmp.add_hline(y=ucl_temp, line_dash="dash", line_color="#ef4444", annotation_text="Thermal Runaway Limit (UCL)", annotation_position="top right")
        fig_tmp.update_layout(
            title="Thermal Drift Trajectory vs Upper Control Limit (UCL)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8',
            height=300,
            margin=dict(l=45, r=25, t=40, b=35),
            xaxis=dict(showgrid=True, gridcolor='#1e293b'),
            yaxis=dict(showgrid=True, gridcolor='#1e293b')
        )
        st.plotly_chart(fig_tmp, use_container_width=True)

    st.markdown("#### 🔮 14-Day Remaining Useful Life & Degradation Forecast")
    forecast_days = [datetime.now() + timedelta(days=i) for i in range(15)]
    wear_rate = (100.0 - health_reserve_pct) / max(1.0, pred_rul_days)
    forecast_health = [max(0.0, health_reserve_pct - (i * wear_rate)) for i in range(15)]
    
    fig_forecast = go.Figure()
    fig_forecast.add_trace(go.Scatter(
        x=forecast_days, y=forecast_health, mode='lines+markers', name='Predicted Health Reserve %',
        line=dict(color='#818cf8', width=3),
        fill='tozeroy', fillcolor='rgba(129, 140, 248, 0.15)'
    ))
    fig_forecast.add_hline(y=20.0, line_dash="dash", line_color="#ef4444", annotation_text="Critical Breakdown Floor (20%)", annotation_position="top left")
    fig_forecast.update_layout(
        title="Projected Equipment Health Reserve over Next 14 Days",
        xaxis_title="Date",
        yaxis_title="Health Reserve (%)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#cbd5e1',
        height=320,
        margin=dict(l=50, r=25, t=45, b=40),
        xaxis=dict(showgrid=True, gridcolor='#1e293b'),
        yaxis=dict(showgrid=True, gridcolor='#1e293b')
    )
    st.plotly_chart(fig_forecast, use_container_width=True)


# ---------------------------------------------------------------------
# TAB 4: 3D MACHINE STATE SPACE
# ---------------------------------------------------------------------
with tabs[3]:
    st.markdown("### 🌐 3D Equipment State Space Visualizer")
    st.caption("Interactive 3D manifold showing Operating Hours vs Vibration RMS vs Temperature, with current machine position highlighted.")

    # Load telemetry sample
    if os.path.exists("campus_sensor_telemetry.csv"):
        df_3d = pd.read_csv("campus_sensor_telemetry.csv").sample(n=600, random_state=42)
    else:
        df_3d = pd.DataFrame({
            "operating_hours": np.random.uniform(500, 8000, 600),
            "temperature_c": np.random.uniform(40, 110, 600),
            "vibration_rms": np.random.uniform(0.5, 6.0, 600),
            "maintenance_required": np.random.choice([0, 1], 600, p=[0.85, 0.15])
        })

    fig_3d = go.Figure()

    # Normal Points
    normal_pts = df_3d[df_3d["maintenance_required"] == 0]
    fig_3d.add_trace(go.Scatter3d(
        x=normal_pts["operating_hours"],
        y=normal_pts["vibration_rms"],
        z=normal_pts["temperature_c"],
        mode='markers',
        name='Healthy Historical State',
        marker=dict(size=3, color='#22c55e', opacity=0.4)
    ))

    # Anomaly Points
    fail_pts = df_3d[df_3d["maintenance_required"] == 1]
    fig_3d.add_trace(go.Scatter3d(
        x=fail_pts["operating_hours"],
        y=fail_pts["vibration_rms"],
        z=fail_pts["temperature_c"],
        mode='markers',
        name='Historical Failures',
        marker=dict(size=4, color='#ef4444', opacity=0.7)
    ))

    # Current Machine Point
    fig_3d.add_trace(go.Scatter3d(
        x=[inp_hours],
        y=[inp_vib],
        z=[inp_temp],
        mode='markers+text',
        name=f'CURRENT: {selected_key}',
        text=['⚡ ACTIVE ASSET'],
        textposition="top center",
        marker=dict(size=14, color=badge_color, symbol='diamond', line=dict(color='#ffffff', width=2))
    ))

    fig_3d.update_layout(
        scene=dict(
            xaxis=dict(title='Operating Hours', backgroundcolor='#090e17', gridcolor='#1e293b'),
            yaxis=dict(title='Vibration RMS (mm/s)', backgroundcolor='#090e17', gridcolor='#1e293b'),
            zaxis=dict(title='Temperature (°C)', backgroundcolor='#090e17', gridcolor='#1e293b'),
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#cbd5e1',
        height=520,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_3d, use_container_width=True)


# ---------------------------------------------------------------------
# TAB 5: FEATURE IMPORTANCE & SHAP
# ---------------------------------------------------------------------
with tabs[4]:
    st.markdown("### 🔍 Model Feature Importance & Telemetry Attribution")
    st.caption("Gini feature importances showing which parameters drive the Random Forest breakdown probability.")

    col_exp1, col_exp2 = st.columns([1.3, 1.0])

    with col_exp1:
        df_imp = pd.DataFrame(feat_imp)
        fig_imp = px.bar(
            df_imp.head(8),
            x="importance",
            y="feature",
            orientation="h",
            title="Top 8 Predictive Feature Importances",
            color="importance",
            color_continuous_scale="Teal"
        )
        fig_imp.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#cbd5e1',
            height=370,
            margin=dict(l=150, r=25, t=40, b=35)
        )
        st.plotly_chart(fig_imp, use_container_width=True)

    with col_exp2:
        st.markdown("#### 🔬 Root Cause Telemetry Drivers")
        st.markdown(f"""
        1. **`vib_delta` ({feat_imp[0]['importance']*100:.1f}% Model Weight):**  
           Current value: `{vib_delta:+.2f} mm/s`. Mechanical vibration is the earliest empirical indicator of shaft misalignment and raceway spalling.
        
        2. **`mech_thermal_synergy` ({feat_imp[1]['importance']*100:.1f}% Model Weight):**  
           Current value: `{mech_thermal_synergy:.2f}`. Multiplies excess temperature by excess vibration to capture exponential friction runaway.
        
        3. **`temp_delta` ({feat_imp[2]['importance']*100:.1f}% Model Weight):**  
           Current value: `{temp_delta:+.1f}°C`. Direct indicator of cooling loop obstruction or motor winding overload.

        4. **`pressure_drop_pct` ({feat_imp[5]['importance']*100:.1f}% Model Weight):**  
           Current value: `{pressure_drop_pct*100.0:+.1f}%`. Detects cavitation and pump mechanical seal failure.
        """)


# ---------------------------------------------------------------------
# TAB 6: BATCH CSV TELEMETRY INSPECTOR
# ---------------------------------------------------------------------
with tabs[5]:
    st.markdown("### 📁 Batch Telemetry CSV Inspector & Anomaly Scorer")
    st.caption("Upload any sensor CSV file to score an entire campus machine fleet simultaneously.")

    uploaded_file = st.file_uploader("Upload Telemetry CSV (or test with default dataset)", type=["csv"])

    if uploaded_file is not None:
        batch_df = pd.read_csv(uploaded_file)
    else:
        st.info("💡 No file uploaded yet. Showing live test evaluation on `campus_sensor_telemetry.csv`.")
        batch_df = pd.read_csv("campus_sensor_telemetry.csv")

    if st.button("🚀 Run Batch Model Inference & Flag High-Risk Assets"):
        from train_model import engineer_features, FEATURE_COLUMNS
        
        with st.spinner("Scoring batch telemetry across Random Forest ensemble..."):
            engineered_batch = engineer_features(batch_df)
            X_batch = engineered_batch[FEATURE_COLUMNS]
            
            probas = clf.predict_proba(X_batch)[:, 1]
            ruls = reg.predict(X_batch)
            
            batch_df["failure_risk_pct"] = (probas * 100.0).round(1)
            batch_df["predicted_rul_hrs"] = ruls.round(0)
            batch_df["predicted_status"] = np.where(
                batch_df["failure_risk_pct"] > 68, "CRITICAL",
                np.where(batch_df["failure_risk_pct"] > 28, "WARNING", "HEALTHY")
            )
            
            flagged = batch_df[batch_df["failure_risk_pct"] > 68]

            c_b1, c_b2, c_b3 = st.columns(3)
            with c_b1:
                st.metric("Total Rows Evaluated", len(batch_df))
            with c_b2:
                st.metric("Healthy Units", len(batch_df[batch_df["predicted_status"] == "HEALTHY"]))
            with c_b3:
                st.metric("Critical Alerts Flagged", len(flagged), delta=f"{len(flagged)} critical", delta_color="inverse")

            st.markdown("#### 🚨 Flagged High-Risk Anomalies")
            st.dataframe(flagged.head(25), use_container_width=True)

            # Downloadable Scored CSV
            csv_export = batch_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download Scored Diagnostic Report (CSV)",
                data=csv_export,
                file_name="scored_campus_telemetry_report.csv",
                mime="text/csv",
                use_container_width=True
            )


# ---------------------------------------------------------------------
# TAB 7: MODEL BENCHMARK ARENA & ROC CURVES (NO SCHOOL RUBRIC MATRIX)
# ---------------------------------------------------------------------
with tabs[6]:
    st.markdown("### 🏆 Algorithm Benchmark Arena & Performance Metrics")
    st.caption("Demonstrating empirical performance of Random Forest vs classical ML baselines.")

    col_bench1, col_bench2 = st.columns([1.2, 1.2])

    with col_bench1:
        st.markdown("#### 📊 Multi-Algorithm Benchmark Comparison")
        df_bench = pd.DataFrame(benchmark_data)
        st.dataframe(
            df_bench.style.format({
                "Accuracy": "{:.3%}",
                "Precision": "{:.3%}",
                "Recall": "{:.3%}",
                "F1-Score": "{:.3%}",
                "ROC-AUC": "{:.4f}"
            }),
            use_container_width=True
        )

        st.markdown("#### 🧮 Confusion Matrix (Test Split = 1,500 samples)")
        cm_fig = go.Figure(data=go.Heatmap(
            z=cm_data,
            x=['Predicted Healthy', 'Predicted Failure'],
            y=['Actual Healthy', 'Actual Failure'],
            colorscale='Blues',
            text=cm_data,
            texttemplate="%{text}",
            textfont={"size": 18}
        ))
        cm_fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#cbd5e1',
            height=280,
            margin=dict(l=45, r=25, t=35, b=25)
        )
        st.plotly_chart(cm_fig, use_container_width=True)

    with col_bench2:
        st.markdown("#### 📈 Multi-Model ROC Curves")
        fig_roc = go.Figure()
        colors = {"Random Forest (Champion)": "#38bdf8", "Gradient Boosting": "#22c55e", "Decision Tree": "#f59e0b", "Logistic Regression": "#ec4899"}

        for m_name, r_info in roc_data.items():
            fig_roc.add_trace(go.Scatter(
                x=r_info["fpr"],
                y=r_info["tpr"],
                mode='lines',
                name=f"{m_name} (AUC={r_info['auc']:.4f})",
                line=dict(color=colors.get(m_name, "#ffffff"), width=2)
            ))
        fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', line=dict(dash='dash', color='#64748b'), name='Random Guess (0.50)'))
        fig_roc.update_layout(
            title="ROC-AUC Comparison (Test Set)",
            xaxis_title="False Positive Rate",
            yaxis_title="True Positive Rate",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#cbd5e1',
            height=340,
            margin=dict(l=50, r=25, t=45, b=40),
            legend=dict(font=dict(size=10))
        )
        st.plotly_chart(fig_roc, use_container_width=True)
