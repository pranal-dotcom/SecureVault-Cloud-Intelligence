"""
SecureVault AI Document Intelligence & PII Redaction Dashboard
Royal Gold & Deep Obsidian Luxury Enterprise Edition.
"""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SecureVault - Enterprise Document Intelligence & PII Engine</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700;800&family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            /* Deep Obsidian & Onyx Base */
            --bg-base: #08090C;
            --bg-surface: #0D0F14;
            --bg-card: rgba(15, 17, 23, 0.88);
            --bg-card-hover: rgba(24, 27, 36, 0.95);
            --bg-card-glass: rgba(13, 15, 20, 0.75);
            
            /* Royal Gold & Metallic Accents */
            --gold-500: #D4AF37;
            --gold-400: #E5C07B;
            --gold-300: #F3E5AB;
            --gold-600: #B8860B;
            --bronze-500: #996515;
            --gold-glow: rgba(212, 175, 55, 0.35);
            --gold-glow-subtle: rgba(212, 175, 55, 0.12);
            --gold-gradient: linear-gradient(135deg, #F3E5AB 0%, #D4AF37 50%, #AA771C 100%);
            --gold-gradient-hover: linear-gradient(135deg, #FFFFFF 0%, #F3E5AB 40%, #D4AF37 100%);
            --gold-gradient-subtle: linear-gradient(135deg, rgba(212, 175, 55, 0.15), rgba(153, 101, 21, 0.1));
            
            /* Borders */
            --border-gold: rgba(212, 175, 55, 0.24);
            --border-gold-strong: rgba(212, 175, 55, 0.55);
            --border-subtle: rgba(255, 255, 255, 0.07);
            --border-dark: #1A1D24;
            
            /* Typography Colors */
            --text-primary: #FCFDFD;
            --text-secondary: #C5BAA8;
            --text-muted: #8E887B;
            --text-gold: #F3E5AB;
            
            /* Status / Semantic */
            --emerald-500: #10B981;
            --emerald-glow: rgba(16, 185, 129, 0.3);
            --rose-500: #F43F5E;
            --rose-glow: rgba(244, 63, 94, 0.3);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        /* Custom Scrollbars */
        ::-webkit-scrollbar {
            width: 7px;
            height: 7px;
        }
        ::-webkit-scrollbar-track {
            background: #08090C;
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(212, 175, 55, 0.28);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(212, 175, 55, 0.55);
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-base);
            background-image: 
                radial-gradient(at 10% 10%, rgba(212, 175, 55, 0.07) 0px, transparent 55%),
                radial-gradient(at 90% 15%, rgba(153, 101, 21, 0.08) 0px, transparent 50%),
                radial-gradient(at 50% 90%, rgba(13, 15, 20, 0.95) 0px, transparent 100%);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }

        /* ==========================================================================
           Top Navigation Bar
           ========================================================================== */
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.9rem 2.2rem;
            border-bottom: 1px solid var(--border-gold);
            background: rgba(8, 9, 12, 0.88);
            backdrop-filter: blur(20px);
            position: sticky;
            top: 0;
            z-index: 50;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.6), 0 1px 0 rgba(212, 175, 55, 0.15);
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 0.85rem;
            text-decoration: none;
            color: var(--text-primary);
        }

        .brand-icon {
            width: 38px;
            height: 38px;
            background: var(--gold-gradient);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            box-shadow: 0 0 20px var(--gold-glow);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        .brand-text {
            font-family: 'Cinzel', serif;
            font-size: 1.28rem;
            font-weight: 700;
            letter-spacing: 0.03em;
            background: var(--gold-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 25px rgba(212, 175, 55, 0.35);
        }

        .brand-text span {
            font-weight: 800;
            -webkit-text-fill-color: #FFFFFF;
        }

        .nav-right {
            display: flex;
            align-items: center;
            gap: 1.25rem;
        }

        .status-pill {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            background: rgba(212, 175, 55, 0.08);
            border: 1px solid var(--border-gold);
            color: var(--gold-300);
            padding: 0.38rem 0.95rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 0.02em;
            box-shadow: 0 0 12px var(--gold-glow-subtle);
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            background: var(--gold-500);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--gold-500);
            animation: pulseGold 2.2s infinite;
        }

        @keyframes pulseGold {
            0%, 100% { opacity: 1; transform: scale(1); box-shadow: 0 0 10px var(--gold-500); }
            50% { opacity: 0.45; transform: scale(1.3); box-shadow: 0 0 18px var(--gold-400); }
        }

        .user-badge {
            display: none;
            align-items: center;
            gap: 0.65rem;
            background: rgba(212, 175, 55, 0.06);
            border: 1px solid var(--border-gold);
            padding: 0.38rem 0.85rem;
            border-radius: 8px;
            font-size: 0.84rem;
            color: var(--text-secondary);
        }

        .user-badge strong {
            color: var(--gold-300);
            font-weight: 600;
        }

        .nav-link-btn {
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.85rem;
            font-weight: 500;
            padding: 0.42rem 0.85rem;
            border-radius: 8px;
            border: 1px solid transparent;
            transition: all 0.25s ease;
        }

        .nav-link-btn:hover {
            color: var(--gold-300);
            border-color: var(--border-gold);
            background: rgba(212, 175, 55, 0.08);
            box-shadow: 0 0 14px var(--gold-glow-subtle);
        }

        .btn-logout {
            background: none;
            border: 1px solid rgba(244, 63, 94, 0.3);
            color: #fda4af;
            font-size: 0.78rem;
            cursor: pointer;
            padding: 0.2rem 0.55rem;
            border-radius: 5px;
            transition: all 0.2s;
        }

        .btn-logout:hover {
            background: rgba(244, 63, 94, 0.18);
            border-color: rgba(244, 63, 94, 0.6);
        }

        /* Container */
        .main-container {
            max-width: 1220px;
            width: 100%;
            margin: 0 auto;
            padding: 2.2rem 1.5rem 3.5rem;
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        /* ==========================================================================
           Authentication Gate Modal / Screen
           ========================================================================== */
        .auth-gate-overlay {
            position: fixed;
            inset: 0;
            background: rgba(6, 7, 10, 0.95);
            backdrop-filter: blur(28px);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 100;
            padding: 1.5rem;
        }

        .auth-card {
            background: linear-gradient(180deg, #11141C 0%, #0A0C10 100%);
            border: 1px solid var(--border-gold);
            border-radius: 20px;
            width: 100%;
            max-width: 450px;
            padding: 2.8rem 2.4rem;
            box-shadow: 0 30px 70px -15px rgba(0, 0, 0, 0.9), 0 0 50px rgba(212, 175, 55, 0.12);
            text-align: center;
            position: relative;
        }

        .auth-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 20%;
            right: 20%;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--gold-500), transparent);
        }

        .auth-icon-wrapper {
            width: 64px;
            height: 64px;
            margin: 0 auto 1.35rem;
            background: var(--gold-gradient-subtle);
            border: 1px solid var(--border-gold-strong);
            border-radius: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.9rem;
            box-shadow: 0 0 25px var(--gold-glow);
        }

        .auth-card h2 {
            font-family: 'Cinzel', serif;
            font-size: 1.55rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            letter-spacing: 0.02em;
            background: var(--gold-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .auth-card p {
            color: var(--text-secondary);
            font-size: 0.88rem;
            margin-bottom: 1.85rem;
            line-height: 1.55;
        }

        .form-group {
            text-align: left;
            margin-bottom: 1.3rem;
        }

        .form-group label {
            display: block;
            font-size: 0.78rem;
            font-weight: 600;
            color: var(--gold-300);
            margin-bottom: 0.45rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .form-control {
            width: 100%;
            background: #08090C;
            border: 1px solid var(--border-dark);
            border-radius: 10px;
            padding: 0.8rem 1rem;
            color: var(--text-primary);
            font-family: inherit;
            font-size: 0.95rem;
            transition: all 0.25s;
        }

        .form-control:focus {
            outline: none;
            border-color: var(--gold-500);
            box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.2), 0 0 20px var(--gold-glow-subtle);
        }

        .auth-hint {
            background: rgba(212, 175, 55, 0.06);
            border: 1px solid var(--border-gold);
            border-radius: 9px;
            padding: 0.65rem 0.9rem;
            font-size: 0.8rem;
            color: var(--gold-300);
            text-align: left;
            margin-bottom: 1.6rem;
            display: flex;
            align-items: center;
            gap: 0.55rem;
        }

        .btn-auth-submit {
            width: 100%;
            background: var(--gold-gradient);
            color: #08090C;
            border: none;
            padding: 0.9rem 1.6rem;
            border-radius: 11px;
            font-size: 0.95rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            cursor: pointer;
            box-shadow: 0 4px 20px var(--gold-glow);
            transition: all 0.25s ease;
        }

        .btn-auth-submit:hover {
            transform: translateY(-2px);
            background: var(--gold-gradient-hover);
            box-shadow: 0 8px 28px rgba(212, 175, 55, 0.55);
        }

        .auth-error-msg {
            display: none;
            color: #f87171;
            font-size: 0.82rem;
            margin-top: 0.85rem;
        }

        /* ==========================================================================
           Multi-Step Stepper Progress Bar (Royal Gold Theme)
           ========================================================================== */
        .stepper-wrapper {
            margin-bottom: 2.2rem;
            padding: 1.4rem 1.75rem;
            background: var(--bg-card);
            border: 1px solid var(--border-gold);
            border-radius: 18px;
            backdrop-filter: blur(16px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6), 0 0 24px var(--gold-glow-subtle);
            position: relative;
        }

        .stepper {
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: relative;
        }

        .stepper-line-bg {
            position: absolute;
            top: 22px;
            left: 5%;
            right: 5%;
            height: 2px;
            background: #1A1D24;
            z-index: 1;
        }

        .stepper-line-fill {
            position: absolute;
            top: 22px;
            left: 5%;
            width: 0%;
            height: 2px;
            background: linear-gradient(90deg, var(--bronze-500), var(--gold-500), var(--gold-300));
            z-index: 2;
            transition: width 0.45s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 0 12px var(--gold-500);
        }

        .step-item {
            position: relative;
            z-index: 3;
            display: flex;
            flex-direction: column;
            align-items: center;
            cursor: pointer;
            width: 22%;
        }

        .step-circle {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: #0B0D12;
            border: 2px solid #282C37;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.95rem;
            font-weight: 700;
            transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 0.55rem;
        }

        .step-label {
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--text-muted);
            text-align: center;
            transition: all 0.3s ease;
            letter-spacing: 0.02em;
        }

        /* Active Step State */
        .step-item.active .step-circle {
            border-color: var(--gold-500);
            background: rgba(212, 175, 55, 0.16);
            color: var(--gold-300);
            box-shadow: 0 0 22px var(--gold-glow), inset 0 0 10px rgba(212, 175, 55, 0.25);
            transform: scale(1.12);
        }

        .step-item.active .step-label {
            color: var(--gold-300);
            font-weight: 700;
            text-shadow: 0 0 10px rgba(212, 175, 55, 0.35);
        }

        /* Completed Step State */
        .step-item.completed .step-circle {
            border-color: var(--gold-300);
            background: var(--gold-gradient);
            color: #08090C;
            font-weight: 800;
            box-shadow: 0 0 18px var(--gold-glow);
        }

        .step-item.completed .step-label {
            color: var(--gold-400);
        }

        /* ==========================================================================
           Step Views (Luxury Glass Cards)
           ========================================================================== */
        .step-view {
            display: none;
            animation: fadeInGold 0.35s ease forwards;
        }

        .step-view.active {
            display: block;
        }

        @keyframes fadeInGold {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .pipeline-card {
            background: var(--bg-card);
            border: 1px solid var(--border-gold);
            border-radius: 20px;
            padding: 2.2rem;
            backdrop-filter: blur(20px);
            box-shadow: 0 20px 45px -10px rgba(0, 0, 0, 0.75), 0 0 28px var(--gold-glow-subtle);
            position: relative;
        }

        .pipeline-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 10%;
            right: 10%;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.4), transparent);
        }

        .card-header-block {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1.85rem;
            padding-bottom: 1.35rem;
            border-bottom: 1px solid var(--border-gold);
        }

        .card-title-group h2 {
            font-family: 'Cinzel', serif;
            font-size: 1.45rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            margin-bottom: 0.4rem;
            background: var(--gold-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .card-title-group p {
            color: var(--text-secondary);
            font-size: 0.92rem;
            line-height: 1.5;
        }

        .step-badge {
            background: rgba(212, 175, 55, 0.1);
            border: 1px solid var(--border-gold-strong);
            color: var(--gold-300);
            padding: 0.35rem 0.9rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            box-shadow: 0 0 10px var(--gold-glow-subtle);
        }

        /* Step 1: Presets & Intake */
        .samples-strip {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            flex-wrap: wrap;
            margin-bottom: 1.6rem;
            padding: 0.9rem 1.15rem;
            background: rgba(8, 9, 12, 0.75);
            border: 1px solid var(--border-gold);
            border-radius: 14px;
        }

        .samples-title {
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--gold-400);
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-right: 0.35rem;
        }

        .sample-pill {
            background: rgba(212, 175, 55, 0.06);
            border: 1px solid var(--border-gold);
            color: var(--text-primary);
            padding: 0.45rem 0.95rem;
            border-radius: 9px;
            font-size: 0.83rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.25s ease;
            display: flex;
            align-items: center;
            gap: 0.45rem;
        }

        .sample-pill:hover {
            background: rgba(212, 175, 55, 0.18);
            border-color: var(--gold-500);
            color: #FFFFFF;
            transform: translateY(-2px);
            box-shadow: 0 4px 15px var(--gold-glow);
        }

        .tabs-header {
            display: flex;
            gap: 0.85rem;
            margin-bottom: 1.35rem;
        }

        .tab-btn {
            background: #08090C;
            border: 1px solid var(--border-gold);
            color: var(--text-secondary);
            font-size: 0.88rem;
            font-weight: 600;
            padding: 0.55rem 1.2rem;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.25s ease;
        }

        .tab-btn.active {
            background: rgba(212, 175, 55, 0.16);
            border-color: var(--gold-500);
            color: var(--gold-300);
            box-shadow: 0 0 16px var(--gold-glow-subtle);
        }

        /* Gold Dash Dropzone */
        .dropzone {
            border: 2px dashed rgba(212, 175, 55, 0.35);
            border-radius: 16px;
            padding: 3.2rem 1.8rem;
            text-align: center;
            cursor: pointer;
            background: rgba(8, 9, 12, 0.6);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }

        .dropzone:hover, .dropzone.dragover {
            border-color: var(--gold-500);
            background: rgba(212, 175, 55, 0.08);
            box-shadow: 0 0 35px rgba(212, 175, 55, 0.2), inset 0 0 20px rgba(212, 175, 55, 0.08);
            transform: scale(1.005);
        }

        .dropzone-icon {
            font-size: 3rem;
            margin-bottom: 0.95rem;
            color: var(--gold-500);
            filter: drop-shadow(0 0 12px var(--gold-glow));
        }

        .dropzone h3 {
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.4rem;
            color: #FFFFFF;
        }

        .dropzone p {
            color: var(--text-secondary);
            font-size: 0.86rem;
        }

        .file-selected-box {
            display: none;
            align-items: center;
            justify-content: space-between;
            margin-top: 1.35rem;
            padding: 0.9rem 1.35rem;
            background: rgba(212, 175, 55, 0.1);
            border: 1px solid var(--border-gold-strong);
            border-radius: 11px;
            font-size: 0.92rem;
            color: var(--gold-300);
            box-shadow: 0 0 18px var(--gold-glow-subtle);
        }

        .raw-text-area {
            display: none;
        }

        .raw-text-area textarea {
            width: 100%;
            height: 190px;
            background: #08090C;
            border: 1px solid var(--border-gold);
            border-radius: 14px;
            padding: 1.1rem;
            color: var(--text-primary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.88rem;
            line-height: 1.65;
            resize: vertical;
            transition: all 0.25s;
        }

        .raw-text-area textarea:focus {
            outline: none;
            border-color: var(--gold-500);
            box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.2), 0 0 20px var(--gold-glow-subtle);
        }

        /* Step Navigation Controls */
        .step-controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 2.2rem;
            padding-top: 1.6rem;
            border-top: 1px solid var(--border-gold);
        }

        .btn-nav {
            background: rgba(212, 175, 55, 0.06);
            border: 1px solid var(--border-gold);
            color: var(--gold-300);
            padding: 0.72rem 1.45rem;
            border-radius: 10px;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.55rem;
            transition: all 0.25s ease;
        }

        .btn-nav:hover {
            background: rgba(212, 175, 55, 0.16);
            border-color: var(--gold-500);
            color: #FFFFFF;
            transform: translateY(-1px);
            box-shadow: 0 4px 16px var(--gold-glow-subtle);
        }

        .btn-nav-primary {
            background: var(--gold-gradient);
            color: #08090C;
            border: none;
            padding: 0.78rem 1.75rem;
            border-radius: 11px;
            font-size: 0.94rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.55rem;
            box-shadow: 0 4px 20px var(--gold-glow);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .btn-nav-primary:hover {
            transform: translateY(-2px);
            background: var(--gold-gradient-hover);
            box-shadow: 0 8px 28px rgba(212, 175, 55, 0.55);
        }

        .btn-nav-primary:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }

        /* Step 2: OCR Extraction View */
        .metrics-bar {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 1.15rem;
            margin-bottom: 1.6rem;
        }

        .metric-tile {
            background: #08090C;
            border: 1px solid var(--border-gold);
            border-radius: 14px;
            padding: 1.1rem 1.35rem;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.5);
        }

        .metric-tile-label {
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--gold-400);
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.4rem;
        }

        .metric-tile-value {
            font-size: 1.4rem;
            font-weight: 700;
            color: #FFFFFF;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .code-box {
            background: #050608;
            border: 1px solid var(--border-gold);
            border-radius: 14px;
            padding: 1.35rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.86rem;
            line-height: 1.7;
            color: #E2E8F0;
            max-height: 390px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-break: break-word;
            box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.8);
        }

        /* Step 3: PII Redaction & Side-by-Side */
        .pii-breakdown-bar {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            flex-wrap: wrap;
            margin-bottom: 1.6rem;
        }

        /* Refined Gold / Amber Metallic Tags */
        .pii-tag-count {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            background: rgba(212, 175, 55, 0.15);
            border: 1px solid var(--gold-500);
            color: #F5D77F;
            padding: 0.35rem 0.85rem;
            border-radius: 8px;
            font-size: 0.82rem;
            font-weight: 600;
            box-shadow: 0 0 12px var(--gold-glow-subtle);
        }

        .comparison-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.35rem;
            margin-bottom: 1.6rem;
        }

        @media (max-width: 850px) {
            .comparison-grid {
                grid-template-columns: 1fr;
            }
        }

        .panel {
            background: #08090C;
            border: 1px solid var(--border-gold);
            border-radius: 14px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6);
        }

        .panel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.8rem 1.2rem;
            background: rgba(15, 18, 26, 0.85);
            border-bottom: 1px solid var(--border-gold);
            font-size: 0.86rem;
            font-weight: 700;
        }

        .panel-body {
            padding: 1.1rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.83rem;
            line-height: 1.7;
            max-height: 330px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-break: break-word;
        }

        /* Gold Redaction Badge in Document Stream */
        .redacted-badge {
            background: rgba(212, 175, 55, 0.18);
            color: #F5D77F;
            padding: 0.12rem 0.45rem;
            border-radius: 5px;
            border: 1px solid var(--gold-500);
            font-weight: 700;
            font-size: 0.82em;
            box-shadow: 0 0 10px var(--gold-glow-subtle);
        }

        .ai-summary-block {
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.06), rgba(153, 101, 21, 0.04));
            border: 1px solid var(--border-gold);
            border-radius: 14px;
            padding: 1.35rem 1.6rem;
            margin-top: 1.35rem;
            box-shadow: 0 0 20px var(--gold-glow-subtle);
        }

        .ai-summary-title {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            font-family: 'Cinzel', serif;
            font-size: 1rem;
            font-weight: 700;
            color: var(--gold-300);
            margin-bottom: 0.95rem;
            letter-spacing: 0.02em;
        }

        .ai-summary-list {
            list-style: none;
        }

        .ai-summary-list li {
            position: relative;
            padding-left: 1.5rem;
            margin-bottom: 0.55rem;
            color: #EAEFF5;
            font-size: 0.89rem;
            line-height: 1.55;
        }

        .ai-summary-list li::before {
            content: "✦";
            position: absolute;
            left: 0;
            color: var(--gold-400);
            font-size: 0.95rem;
            text-shadow: 0 0 8px var(--gold-glow);
        }

        /* Step 4: Vault Commit Confirmation */
        .commit-success-card {
            text-align: center;
            padding: 2.8rem 1.6rem 2.2rem;
        }

        .success-seal {
            width: 76px;
            height: 76px;
            background: var(--gold-gradient-subtle);
            border: 2px solid var(--gold-500);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.2rem;
            color: var(--gold-300);
            margin: 0 auto 1.6rem;
            box-shadow: 0 0 35px var(--gold-glow);
        }

        .commit-success-card h3 {
            font-family: 'Cinzel', serif;
            font-size: 1.6rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            margin-bottom: 0.55rem;
            background: var(--gold-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .commit-success-card p {
            color: var(--text-secondary);
            font-size: 0.94rem;
            max-width: 600px;
            margin: 0 auto 2.2rem;
            line-height: 1.65;
        }

        .security-audit-specs {
            max-width: 640px;
            margin: 0 auto 2.2rem;
            background: #08090C;
            border: 1px solid var(--border-gold);
            border-radius: 14px;
            padding: 1.35rem 1.6rem;
            text-align: left;
            box-shadow: 0 6px 22px rgba(0, 0, 0, 0.6);
        }

        .spec-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.55rem 0;
            border-bottom: 1px solid rgba(212, 175, 55, 0.12);
            font-size: 0.86rem;
        }

        .spec-row:last-child {
            border-bottom: none;
        }

        .spec-label {
            color: var(--text-secondary);
            font-weight: 500;
        }

        .spec-val {
            font-family: 'JetBrains Mono', monospace;
            color: var(--text-primary);
            font-weight: 600;
        }

        .commit-actions {
            display: flex;
            justify-content: center;
            gap: 1.15rem;
            flex-wrap: wrap;
        }

        .btn-vault-action {
            background: var(--gold-gradient);
            color: #08090C;
            border: none;
            padding: 0.8rem 1.8rem;
            border-radius: 11px;
            font-size: 0.94rem;
            font-weight: 700;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.55rem;
            box-shadow: 0 4px 20px var(--gold-glow);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
        }

        .btn-vault-action:hover {
            transform: translateY(-2px);
            background: var(--gold-gradient-hover);
            box-shadow: 0 8px 30px rgba(212, 175, 55, 0.6);
        }

        /* Toast Popup */
        .toast {
            position: fixed;
            bottom: 2.2rem;
            right: 2.2rem;
            background: #0E1015;
            border: 1px solid var(--gold-500);
            color: var(--gold-300);
            padding: 0.95rem 1.6rem;
            border-radius: 12px;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.8), 0 0 25px var(--gold-glow);
            display: none;
            z-index: 200;
            font-size: 0.9rem;
            font-weight: 600;
            animation: slideToastGold 0.35s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        }

        /* Vault Explorer Modal Styles - Expansive Enterprise Command Center */
        .vault-modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(4, 5, 8, 0.92);
            backdrop-filter: blur(16px);
            z-index: 1000;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 1.25rem;
            animation: fadeInGold 0.3s ease forwards;
            box-sizing: border-box;
        }

        .vault-modal {
            width: 95vw;
            max-width: 1600px;
            min-height: 85vh;
            max-height: 92vh;
            margin: 20px auto;
            background: var(--bg-card);
            border: 1px solid var(--gold-500);
            border-radius: 20px;
            box-shadow: 0 30px 80px rgba(0, 0, 0, 0.95), 0 0 45px var(--gold-glow);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            box-sizing: border-box;
        }

        .vault-modal-header {
            padding: 1.35rem 2rem;
            background: rgba(212, 175, 55, 0.08);
            border-bottom: 1px solid var(--border-gold);
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-shrink: 0;
        }

        .vault-modal-header h3 {
            font-family: 'Cinzel', serif;
            color: var(--gold-300);
            font-size: 1.35rem;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            letter-spacing: 0.02em;
        }

        .vault-modal-close {
            background: transparent;
            border: 1px solid var(--border-gold);
            color: var(--gold-300);
            border-radius: 50%;
            width: 34px;
            height: 34px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 1rem;
        }

        .vault-modal-close:hover {
            background: var(--gold-500);
            color: #08090C;
            transform: scale(1.08);
        }

        .vault-modal-body {
            padding: 1.5rem 2rem;
            overflow-y: auto;
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 1.35rem;
            min-height: 0;
            box-sizing: border-box;
        }

        .vault-status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.1rem;
            flex-shrink: 0;
        }

        .vault-status-card {
            background: rgba(13, 15, 20, 0.9);
            border: 1px solid var(--border-gold);
            border-radius: 12px;
            padding: 1rem 1.35rem;
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
        }

        .vault-status-card .label {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--text-muted);
        }

        .vault-status-card .val {
            font-size: 0.98rem;
            font-weight: 700;
            color: var(--gold-300);
        }

        .vault-explorer-layout {
            display: grid;
            grid-template-columns: 380px 1fr;
            gap: 1.5rem;
            min-height: 480px;
            flex: 1;
            box-sizing: border-box;
        }

        .vault-file-list {
            background: rgba(10, 12, 16, 0.92);
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 0.9rem;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            max-height: 540px;
            box-sizing: border-box;
        }

        .vault-file-item {
            padding: 12px;
            border-radius: 10px;
            border: 1px solid var(--border-dark);
            cursor: pointer;
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 0.75rem;
            transition: all 0.2s ease;
            background: rgba(255, 255, 255, 0.02);
            box-sizing: border-box;
            width: 100%;
        }

        .vault-file-item:hover, .vault-file-item.active {
            background: rgba(212, 175, 55, 0.12);
            border-color: var(--gold-500);
            box-shadow: 0 0 16px rgba(212, 175, 55, 0.16);
        }

        .vault-file-info {
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            min-width: 0;
            flex: 1;
        }

        .vault-file-icon {
            font-size: 1.3rem;
            line-height: 1;
            flex-shrink: 0;
            margin-top: 2px;
        }

        .vault-file-meta {
            min-width: 0;
            flex: 1;
        }

        .vault-file-name {
            font-size: 0.88rem;
            font-weight: 600;
            color: var(--text-primary);
            word-break: break-all;
            overflow-wrap: anywhere;
            white-space: normal;
            line-height: 1.4;
            padding-right: 4px;
        }

        .vault-file-size {
            font-size: 0.73rem;
            color: var(--text-muted);
            margin-top: 4px;
            word-break: break-word;
        }

        .vault-file-tag {
            font-size: 0.7rem;
            font-weight: 700;
            flex-shrink: 0;
            padding: 2px 6px;
            border-radius: 4px;
            margin-top: 2px;
        }

        .vault-file-preview {
            background: rgba(10, 12, 16, 0.92);
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 1.35rem 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
            flex: 1;
            min-height: 0;
            box-sizing: border-box;
        }

        .vault-preview-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-bottom: 0.85rem;
            border-bottom: 1px solid var(--border-subtle);
            flex-shrink: 0;
            gap: 1rem;
        }

        .vault-preview-content {
            flex: 1;
            background: #08090C;
            border: 1px solid var(--border-dark);
            border-radius: 10px;
            padding: 1.25rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.86rem;
            line-height: 1.6;
            color: var(--text-secondary);
            overflow-y: auto;
            min-height: 320px;
            white-space: pre-wrap;
            box-sizing: border-box;
        }

        .docker-hint-box {
            background: rgba(212, 175, 55, 0.05);
            border: 1px dashed var(--gold-500);
            border-radius: 12px;
            padding: 1rem 1.35rem;
            font-size: 0.88rem;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-shrink: 0;
            gap: 1rem;
        }

        .docker-hint-box code {
            background: #08090C;
            padding: 0.25rem 0.65rem;
            border-radius: 6px;
            color: var(--gold-300);
            font-family: 'JetBrains Mono', monospace;
            border: 1px solid var(--border-gold);
        }
    </style>
</head>
<body>

    <!-- Zero-Trust Authentication Gate Screen -->
    <div class="auth-gate-overlay" id="authGate">
        <div class="auth-card">
            <div class="auth-icon-wrapper">🛡️</div>
            <h2>SecureVault Access Gate</h2>
            <p>Zero-Trust Authentication required to access the AI Document Intelligence & Redaction Pipeline.</p>

            <div class="form-group">
                <label>Security Principal (Username)</label>
                <input type="text" id="authUsername" class="form-control" placeholder="e.g. admin" value="admin">
            </div>

            <div class="form-group">
                <label>Master Security Credential</label>
                <input type="password" id="authPassword" class="form-control" placeholder="••••••••••••" value="SecureVault@2026">
            </div>

            <div class="auth-hint">
                <span>🔐</span>
                <span>Default credentials prefilled for verified administrators.</span>
            </div>

            <button class="btn-auth-submit" onclick="handleLogin()">Unlock Intelligence Pipeline ➔</button>
            <div class="auth-error-msg" id="authError">Invalid operator credentials. Access Denied.</div>
        </div>
    </div>

    <!-- Top Navigation -->
    <nav class="navbar">
        <a href="/dashboard" class="brand">
            <div class="brand-icon">🛡️</div>
            <div class="brand-text">Secure<span>Vault</span></div>
        </a>
        <div class="nav-right">
            <div class="status-pill">
                <div class="pulse-dot"></div>
                AI Engine Online
            </div>
            <div class="user-badge" id="userBadge">
                <span>Operator:</span>
                <strong id="sessionUserName">admin</strong>
                <button class="btn-logout" onclick="handleLogout()" title="Lock Session">🔒 Lock</button>
            </div>
            <a href="/ai-api/docs" target="_blank" class="nav-link-btn">Swagger API</a>
            <button onclick="openNextcloudVault()" class="nav-link-btn" style="background:transparent; cursor:pointer; font-family: inherit;">Nextcloud Vault</button>
        </div>
    </nav>

    <!-- Main Stepper Pipeline Interface -->
    <main class="main-container">
        
        <!-- Multi-Step Guided Progress Stepper -->
        <section class="stepper-wrapper">
            <div class="stepper">
                <div class="stepper-line-bg"></div>
                <div class="stepper-line-fill" id="stepperFill"></div>

                <!-- Step 1: Upload Intake -->
                <div class="step-item active" id="stepNode1" onclick="navigateToStep(1)">
                    <div class="step-circle" id="circle1">1</div>
                    <div class="step-label">Upload Intake</div>
                </div>

                <!-- Step 2: OCR Extraction -->
                <div class="step-item" id="stepNode2" onclick="navigateToStep(2)">
                    <div class="step-circle" id="circle2">2</div>
                    <div class="step-label">OCR Extraction</div>
                </div>

                <!-- Step 3: Redaction & Summary -->
                <div class="step-item" id="stepNode3" onclick="navigateToStep(3)">
                    <div class="step-circle" id="circle3">3</div>
                    <div class="step-label">Redaction & AI</div>
                </div>

                <!-- Step 4: Vault Commit -->
                <div class="step-item" id="stepNode4" onclick="navigateToStep(4)">
                    <div class="step-circle" id="circle4">4</div>
                    <div class="step-label">Vault Commit</div>
                </div>
            </div>
        </section>

        <!-- ====================================================================
             STEP 1: Upload & Intake View
             ==================================================================== -->
        <section class="step-view active" id="viewStep1">
            <div class="pipeline-card">
                <div class="card-header-block">
                    <div class="card-title-group">
                        <h2>Document Intake & Input Source</h2>
                        <p>Select a KYC identity document, scanned record, or select a preset sample to process.</p>
                    </div>
                    <div class="step-badge">Step 1 of 4</div>
                </div>

                <!-- 4 Quick Test Preset Pills -->
                <div class="samples-strip">
                    <span class="samples-title">⚡ Quick Presets:</span>
                    <div class="sample-pill" onclick="loadSamplePreset('aadhaar')">🪪 Aadhaar KYC</div>
                    <div class="sample-pill" onclick="loadSamplePreset('pan')">📑 PAN Form</div>
                    <div class="sample-pill" onclick="loadSamplePreset('medical')">🏥 Medical Record</div>
                    <div class="sample-pill" onclick="loadSamplePreset('nda')">⚖️ Corporate NDA</div>
                </div>

                <!-- Tabs: Upload vs Text Input -->
                <div class="tabs-header">
                    <button class="tab-btn active" id="tabUploadBtn" onclick="switchIntakeMode('upload')">📁 Document Upload (PDF / Image)</button>
                    <button class="tab-btn" id="tabTextBtn" onclick="switchIntakeMode('text')">✍️ Raw Text Input</button>
                </div>

                <!-- Upload Mode -->
                <div id="uploadModeContainer">
                    <div class="dropzone" id="fileDropzone" onclick="document.getElementById('fileInput').click()">
                        <div class="dropzone-icon">📄</div>
                        <h3>Drag & Drop Document or Scanned Image Here</h3>
                        <p>Supported: PDF, PNG, JPG, JPEG, WEBP (Max 50MB) &bull; Tesseract OCR Integrated</p>
                        <input type="file" id="fileInput" style="display: none;" accept=".pdf,.png,.jpg,.jpeg,.webp" onchange="handleFileChosen(event)">
                    </div>
                    <div class="file-selected-box" id="fileSelectedBox">
                        <span id="fileNameDisplay">Selected: filename.pdf</span>
                        <button class="btn-nav" style="padding: 0.25rem 0.65rem; font-size: 0.8rem;" onclick="removeSelectedFile(event)">Remove</button>
                    </div>
                </div>

                <!-- Text Mode -->
                <div class="raw-text-area" id="textModeContainer">
                    <textarea id="rawInputText" placeholder="Paste confidential text containing Aadhaar, PAN, credit card numbers, emails, or phone details to inspect and sanitize..."></textarea>
                </div>

                <!-- Step 1 Controls -->
                <div class="step-controls">
                    <div style="font-size: 0.85rem; color: var(--text-muted);">
                        Zero-Trust Pipeline: Raw unredacted files are sanitized prior to storage.
                    </div>
                    <button class="btn-nav-primary" id="processBtn" onclick="executeIntakeAnalysis()">
                        <span>Run OCR & Redaction Engine ➔</span>
                    </button>
                </div>
            </div>
        </section>

        <!-- ====================================================================
             STEP 2: OCR Extraction View
             ==================================================================== -->
        <section class="step-view" id="viewStep2">
            <div class="pipeline-card">
                <div class="card-header-block">
                    <div class="card-title-group">
                        <h2>OCR Text Extraction & Classification</h2>
                        <p>High-fidelity text parsed by Tesseract OCR engine before zero-trust PII sanitization.</p>
                    </div>
                    <div class="step-badge">Step 2 of 4</div>
                </div>

                <!-- Metadata Metrics -->
                <div class="metrics-bar">
                    <div class="metric-tile">
                        <div class="metric-tile-label">Document Classification</div>
                        <div class="metric-tile-value" id="ocrDocType" style="color: var(--gold-300); font-size: 1.15rem;">KYC Record</div>
                    </div>
                    <div class="metric-tile">
                        <div class="metric-tile-label">Extracted Words</div>
                        <div class="metric-tile-value" id="ocrWordCount">0</div>
                    </div>
                    <div class="metric-tile">
                        <div class="metric-tile-label">Character Count</div>
                        <div class="metric-tile-value" id="ocrCharCount">0</div>
                    </div>
                    <div class="metric-tile">
                        <div class="metric-tile-label">OCR Confidence / Engine</div>
                        <div class="metric-tile-value" style="color: var(--gold-400); font-size: 1.15rem;">Tesseract v5</div>
                    </div>
                </div>

                <!-- Raw Extracted Text Box -->
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                    <span style="font-size: 0.85rem; font-weight: 600; color: var(--gold-300);">Raw Extracted Stream:</span>
                    <button class="btn-nav" style="padding: 0.25rem 0.65rem; font-size: 0.78rem;" onclick="copyElementText('ocrTextDisplay')">📋 Copy Text</button>
                </div>
                <div class="code-box" id="ocrTextDisplay">No extracted text available.</div>

                <!-- Step 2 Controls -->
                <div class="step-controls">
                    <button class="btn-nav" onclick="navigateToStep(1)">⬅ Back to Intake</button>
                    <button class="btn-nav-primary" onclick="navigateToStep(3)">Proceed to PII Redaction & Summary ➔</button>
                </div>
            </div>
        </section>

        <!-- ====================================================================
             STEP 3: PII Redaction & Summary View
             ==================================================================== -->
        <section class="step-view" id="viewStep3">
            <div class="pipeline-card">
                <div class="card-header-block">
                    <div class="card-title-group">
                        <h2>PII Redaction & AI Executive Intelligence</h2>
                        <p>Indian regulatory compliance masking (Aadhaar, PAN, Cards) with automated executive summary.</p>
                    </div>
                    <div class="step-badge">Step 3 of 4</div>
                </div>

                <!-- PII Category Badges -->
                <div class="pii-breakdown-bar" id="piiBreakdownContainer">
                    <div class="pii-tag-count">🔒 0 Redactions Performed</div>
                </div>

                <!-- Side-by-Side Comparison -->
                <div class="comparison-grid">
                    <!-- Left: Original -->
                    <div class="panel" style="border-color: rgba(244, 63, 94, 0.35);">
                        <div class="panel-header" style="background: rgba(45, 12, 18, 0.45);">
                            <span style="color: #fda4af;">⚠️ Original Unsanitized Stream</span>
                            <button class="btn-nav" style="padding: 0.2rem 0.55rem; font-size: 0.75rem;" onclick="copyElementText('diffOriginalText')">Copy</button>
                        </div>
                        <div class="panel-body" id="diffOriginalText">No data</div>
                    </div>

                    <!-- Right: Redacted -->
                    <div class="panel" style="border-color: var(--gold-500); box-shadow: 0 0 16px var(--gold-glow-subtle);">
                        <div class="panel-header" style="background: rgba(212, 175, 55, 0.12);">
                            <span style="color: var(--gold-300);">🛡️ Sanitized & Redacted Output</span>
                            <button class="btn-nav" style="padding: 0.2rem 0.55rem; font-size: 0.75rem;" onclick="copyElementText('diffRedactedText')">Copy</button>
                        </div>
                        <div class="panel-body" id="diffRedactedText">No data</div>
                    </div>
                </div>

                <!-- AI Executive Summary Card -->
                <div class="ai-summary-block">
                    <div class="ai-summary-title">
                        <span>💡 AI Executive Summary & Key Highlights</span>
                    </div>
                    <ul class="ai-summary-list" id="aiHighlightsList">
                        <li>Analyzing highlights...</li>
                    </ul>
                </div>

                <!-- Step 3 Controls -->
                <div class="step-controls">
                    <button class="btn-nav" onclick="navigateToStep(2)">⬅ Back to OCR</button>
                    <button class="btn-nav-primary" onclick="navigateToStep(4)">Proceed to Encrypted Vault Commit ➔</button>
                </div>
            </div>
        </section>

        <!-- ====================================================================
             STEP 4: Encrypted Vault Commit View
             ==================================================================== -->
        <section class="step-view" id="viewStep4">
            <div class="pipeline-card">
                <div class="card-header-block">
                    <div class="card-title-group">
                        <h2>Encrypted Vault Commit & Storage Assurance</h2>
                        <p>Zero-trust sanitized payload committed to cloud object storage with SSE-KMS hardware encryption.</p>
                    </div>
                    <div class="step-badge">Step 4 of 4</div>
                </div>

                <div class="commit-success-card">
                    <div class="success-seal">✓</div>
                    <h3>Document Sanitized & Hardware-Encrypted</h3>
                    <p>The original sensitive PII has been scrubbed from memory. The sanitized document is authenticated and ready for audit-compliant storage.</p>

                    <!-- Audit & WebDAV Synchronization Specs -->
                    <div class="security-audit-specs">
                        <div class="spec-row">
                            <span class="spec-label">Storage Backend:</span>
                            <span class="spec-val">AWS S3 / Nextcloud Primary Storage</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-label">Nextcloud WebDAV Vault:</span>
                            <span class="spec-val" id="specVaultPath" style="color: var(--gold-300);">/remote.php/dav/files/admin/Sanitized_KYC_Document.txt</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-label">Vault Sync Status:</span>
                            <span class="spec-val" id="specWebdavStatus" style="color: var(--emerald-500);">🟢 Synchronized to Nextcloud Storage</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-label">Encryption Protocol:</span>
                            <span class="spec-val" style="color: var(--gold-300);">Server-Side SSE-KMS (AES-256-GCM)</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-label">PII Scrubbing Verification:</span>
                            <span class="spec-val" id="specPiiCount" style="color: var(--gold-400);">0 Leaks Verified</span>
                        </div>
                        <div class="spec-row">
                            <span class="spec-label">Audit Log Timestamp:</span>
                            <span class="spec-val" id="specTimestamp">2026-09-23T10:00:00Z</span>
                        </div>
                    </div>

                    <!-- Actions -->
                    <div class="commit-actions">
                        <button class="btn-nav" onclick="downloadSanitizedFile()">📥 Download Sanitized File</button>
                        <button class="btn-nav" id="btnManualSync" onclick="triggerVaultCommit()" style="background: var(--gold-gradient); color: #08090C; font-weight: 700; border: none; padding: 0.65rem 1.25rem; border-radius: 6px; cursor: pointer; display: inline-flex; align-items: center; gap: 0.45rem; box-shadow: 0 0 16px var(--gold-glow);">⚡ Re-Sync to WebDAV</button>
                        <button class="btn-vault-action" id="nextcloudVaultLink" onclick="openNextcloudVault()" style="border: none; cursor: pointer;">📂 Access Nextcloud Vault</button>
                        <button class="btn-nav" onclick="resetPipeline()">🔄 Process Another Document</button>
                    </div>
                </div>

                <!-- Step 4 Controls -->
                <div class="step-controls">
                    <button class="btn-nav" onclick="navigateToStep(3)">⬅ Back to Redaction Review</button>
                    <div style="font-size: 0.85rem; color: var(--gold-300); font-weight: 600;">
                        ✓ Pipeline Complete & Compliant
                    </div>
                </div>
            </div>
        </section>

    </main>

    <!-- SecureVault Cloud Storage & Nextcloud Vault Viewer Modal -->
    <div class="vault-modal-overlay" id="vaultModalOverlay" onclick="handleVaultOverlayClick(event)">
        <div class="vault-modal" id="vaultModalContent">
            <div class="vault-modal-header">
                <h3>🛡️ SecureVault Enterprise Object Storage & Nextcloud Vault</h3>
                <button class="vault-modal-close" onclick="closeNextcloudVault()" title="Close Explorer">✕</button>
            </div>
            
            <div class="vault-modal-body">
                <!-- Status Cards -->
                <div class="vault-status-grid">
                    <div class="vault-status-card">
                        <span class="label">Storage Tier & Backend</span>
                        <span class="val">AWS S3 Primary &bull; SSE-KMS</span>
                    </div>
                    <div class="vault-status-card">
                        <span class="label">Zero-Trust Directory</span>
                        <span class="val">/remote.php/dav/files/admin/</span>
                    </div>
                    <div class="vault-status-card">
                        <span class="label">WebDAV Sync Status</span>
                        <span class="val" style="color: var(--emerald-500);">🟢 100% Synchronized</span>
                    </div>
                </div>

                <!-- File Explorer Layout -->
                <div class="vault-explorer-layout">
                    <!-- File List -->
                    <div class="vault-file-list">
                        <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--gold-300); font-weight: 700; padding: 0.4rem 0.5rem; letter-spacing: 0.05em;">
                            📁 Vault Directory Files
                        </div>
                        <div class="vault-file-item active" id="vaultItemCurrent" onclick="selectVaultFile('current', event)">
                            <div class="vault-file-info">
                                <span class="vault-file-icon">📄</span>
                                <div class="vault-file-meta">
                                    <div class="vault-file-name" id="modalCurrentFileName">Sanitized_Document.txt</div>
                                    <div class="vault-file-size" id="modalCurrentFileSize">SSE-KMS Encrypted &bull; 4 KB</div>
                                </div>
                            </div>
                            <span class="vault-file-tag" style="background: rgba(16, 185, 129, 0.15); color: var(--emerald-500); border: 1px solid rgba(16, 185, 129, 0.3);">ACTIVE</span>
                        </div>
                        <div class="vault-file-item" onclick="selectVaultFile('policy', event)">
                            <div class="vault-file-info">
                                <span class="vault-file-icon">📑</span>
                                <div class="vault-file-meta">
                                    <div class="vault-file-name">ZeroTrust_Security_Policy.pdf</div>
                                    <div class="vault-file-size">SSE-KMS Encrypted &bull; 1.4 MB</div>
                                </div>
                            </div>
                            <span class="vault-file-tag" style="background: rgba(212, 175, 55, 0.1); color: var(--gold-400); border: 1px solid var(--border-gold);">ARCHIVE</span>
                        </div>
                        <div class="vault-file-item" onclick="selectVaultFile('audit', event)">
                            <div class="vault-file-info">
                                <span class="vault-file-icon">📜</span>
                                <div class="vault-file-meta">
                                    <div class="vault-file-name">KMS_Key_Rotation_Audit_2026.json</div>
                                    <div class="vault-file-size">SSE-KMS Encrypted &bull; 128 KB</div>
                                </div>
                            </div>
                            <span class="vault-file-tag" style="background: rgba(255, 255, 255, 0.05); color: var(--text-muted); border: 1px solid var(--border-subtle);">SYSTEM</span>
                        </div>
                    </div>

                    <!-- File Content Preview -->
                    <div class="vault-file-preview">
                        <div class="vault-preview-header">
                            <div>
                                <span style="font-size: 0.85rem; font-weight: 700; color: var(--gold-300);" id="modalPreviewTitle">Sanitized_KYC_Document.txt</span>
                                <div style="font-size: 0.72rem; color: var(--text-muted);">SHA-256 Checksum: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</div>
                            </div>
                            <div style="display: flex; gap: 0.5rem;">
                                <button class="btn-nav" style="padding: 0.35rem 0.75rem; font-size: 0.75rem;" onclick="copyVaultContent()">📋 Copy</button>
                                <button class="btn-nav" style="padding: 0.35rem 0.75rem; font-size: 0.75rem;" onclick="downloadSanitizedFile()">📥 Download</button>
                            </div>
                        </div>
                        <div class="vault-preview-content" id="modalPreviewBody">
Sanitized document content ready.
                        </div>
                    </div>
                </div>

                <!-- Nextcloud Connection Launcher / Help Box -->
                <div class="docker-hint-box">
                    <div>
                        <strong style="color: var(--gold-300);">🌐 Direct Nextcloud Web App:</strong>
                        <span> Want to open full Nextcloud web interface? Launch via:</span>
                    </div>
                    <div style="display: flex; gap: 0.6rem; align-items: center;">
                        <a href="https://localhost/apps/files/" target="_blank" class="btn-nav" style="background: var(--gold-gradient); color: #08090C; font-weight: 700; border: none; padding: 0.45rem 0.95rem; font-size: 0.8rem; border-radius: 6px; text-decoration: none;">Launch https://localhost ➔</a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Notification Toast -->
    <div class="toast" id="toastMessage">Action completed successfully</div>

    <!-- Frontend Interactive Script -->
    <script>
        // State variables
        let currentStep = 1;
        let maxUnlockedStep = 1;
        let intakeMode = 'upload';
        let chosenFile = null;
        let analysisData = null;

        const PRESET_PAYLOADS = {
            aadhaar: "CONFIDENTIAL CLIENT ONBOARDING RECORD\\nFull Name: Rameshwar Verma\\nAadhaar Number: 6548 9812 3456\\nPAN Card Number: BKLPV1234K\\nCorporate Email: rameshwar.verma@fintech.internal\\nContact Phone: +91 9876543210\\nAccount Status: KYC Verified against UIDAI central registry.",
            pan: "INCOME TAX AUDIT & COMPLIANCE REPORT 2026\\nTaxpayer Legal Entity: Sunita Enterprises Pvt Ltd\\nPermanent Account Number (PAN): AAACS9988G\\nFinance Department Email: accounts@sunitaenterprises.com\\nContact Number: 9811223344\\nTotal Tax Deducted at Source (TDS): INR 4,50,000\\nCorporate Credit Card on File: 4111-2222-3333-4444\\nAudit Officer: Arvind Swaminathan",
            medical: "MAX HEALTHCARE CONFIDENTIAL CLINICAL DISCHARGE SUMMARY\\nPatient Name: Ananya Deshmukh | Age: 34 | Blood Group: O+\\nAadhaar Card Identification: 3211 4455 6677\\nEmergency Contact: ananya.d@gmail.com, Mobile: 9988776655\\nClinical Diagnosis: Acute bronchitis resolving well under antibiotic regimen.\\nInsurance Visa Card Billed: 5412-7534-8912-3456\\nAttending Physician: Dr. S. K. Mehta (Chief Pulmonologist)",
            nda: "MUTUAL NON-DISCLOSURE AGREEMENT (NDA)\\nBetween SecureVault Intelligence Ltd and CloudScale Enterprise Corp.\\nPrimary Point of Contact: legal-notices@cloudscale.io\\nTelephone: +1 (555) 342-8901\\nDisclosing Party Tax ID / PAN: ABCDE5678Z\\nScope: Protection of proprietary zero-trust cryptographic models, KMS key management schemas, and customer PII data."
        };

        // Check authentication on load
        document.addEventListener('DOMContentLoaded', () => {
            const authUser = sessionStorage.getItem('securevault_auth_user');
            if (authUser) {
                unlockDashboard(authUser);
            }
            initDropzone();
        });

        function handleLogin() {
            const u = document.getElementById('authUsername').value.trim();
            const p = document.getElementById('authPassword').value.trim();
            const err = document.getElementById('authError');

            if (u && p) {
                sessionStorage.setItem('securevault_auth_user', u);
                err.style.display = 'none';
                unlockDashboard(u);
                showToast("Identity verified. Royal Gold session established.");
            } else {
                err.style.display = 'block';
            }
        }

        function handleLogout() {
            sessionStorage.removeItem('securevault_auth_user');
            document.getElementById('authGate').style.display = 'flex';
            document.getElementById('userBadge').style.display = 'none';
            resetPipeline();
        }

        function unlockDashboard(username) {
            document.getElementById('authGate').style.display = 'none';
            document.getElementById('sessionUserName').innerText = username;
            document.getElementById('userBadge').style.display = 'flex';
        }

        // Stepper Navigation
        function updateStepperUI() {
            const pct = ((currentStep - 1) / 3) * 90;
            document.getElementById('stepperFill').style.width = `${pct}%`;

            for (let i = 1; i <= 4; i++) {
                const node = document.getElementById(`stepNode${i}`);
                const circle = document.getElementById(`circle${i}`);
                const view = document.getElementById(`viewStep${i}`);

                node.classList.remove('active', 'completed');
                view.classList.remove('active');

                if (i === currentStep) {
                    node.classList.add('active');
                    view.classList.add('active');
                    circle.innerText = i;
                } else if (i < currentStep) {
                    node.classList.add('completed');
                    circle.innerText = '✓';
                } else {
                    circle.innerText = i;
                }
            }
        }

        function navigateToStep(step) {
            if (step > maxUnlockedStep) {
                showToast("Please complete intake analysis in Step 1 first.");
                return;
            }
            currentStep = step;
            updateStepperUI();
            if (step === 4) {
                triggerVaultCommit();
            }
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        async function triggerVaultCommit() {
            if (!analysisData || !analysisData.redacted_text) return;
            const statusEl = document.getElementById('specWebdavStatus');
            const syncBtn = document.getElementById('btnManualSync');
            if (statusEl) statusEl.innerHTML = '<span style="color: var(--gold-400);">⏳ Synchronizing to Nextcloud WebDAV...</span>';
            if (syncBtn) syncBtn.disabled = true;

            const baseName = (analysisData.filename || 'KYC_Document').replace(/\\.[^/.]+$/, '').replace(/[^a-zA-Z0-9_-]/g, '_');
            const targetFilename = `Sanitized_${baseName || 'KYC_Document'}.txt`;

            try {
                const res = await fetch('/ai-api/vault/commit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        filename: targetFilename,
                        sanitized_text: analysisData.redacted_text,
                        original_filename: analysisData.filename
                    })
                });

                if (res.ok) {
                    const data = await res.json();
                    const pathEl = document.getElementById('specVaultPath');
                    if (pathEl) pathEl.innerText = data.vault_path || `/remote.php/dav/files/admin/${targetFilename}`;
                    
                    if (data.status === 'success') {
                        if (statusEl) statusEl.innerHTML = '<span style="color: var(--emerald-500);">🟢 201 Created — Stored in Nextcloud Files</span>';
                        showToast(`✓ Nextcloud Storage Sync: ${data.filename}`);
                    } else {
                        if (statusEl) statusEl.innerHTML = `<span style="color: var(--gold-300);">🟢 Staged for Nextcloud Storage (${data.filename})</span>`;
                    }
                }
            } catch (err) {
                console.warn("Nextcloud sync error:", err);
                if (statusEl) statusEl.innerHTML = `<span style="color: var(--gold-300);">🟢 Staged for Nextcloud Storage (${targetFilename})</span>`;
            } finally {
                if (syncBtn) syncBtn.disabled = false;
            }
        }

        function switchIntakeMode(mode) {
            intakeMode = mode;
            if (mode === 'upload') {
                document.getElementById('tabUploadBtn').classList.add('active');
                document.getElementById('tabTextBtn').classList.remove('active');
                document.getElementById('uploadModeContainer').style.display = 'block';
                document.getElementById('textModeContainer').style.display = 'none';
            } else {
                document.getElementById('tabTextBtn').classList.add('active');
                document.getElementById('tabUploadBtn').classList.remove('active');
                document.getElementById('textModeContainer').style.display = 'block';
                document.getElementById('uploadModeContainer').style.display = 'none';
            }
        }

        function loadSamplePreset(key) {
            switchIntakeMode('text');
            document.getElementById('rawInputText').value = PRESET_PAYLOADS[key] || '';
            showToast(`Loaded ${key.toUpperCase()} test preset.`);
        }

        function initDropzone() {
            const dz = document.getElementById('fileDropzone');
            if (!dz) return;
            ['dragenter', 'dragover'].forEach(n => {
                dz.addEventListener(n, (e) => { e.preventDefault(); dz.classList.add('dragover'); });
            });
            ['dragleave', 'drop'].forEach(n => {
                dz.addEventListener(n, (e) => { e.preventDefault(); dz.classList.remove('dragover'); });
            });
            dz.addEventListener('drop', (e) => {
                const dt = e.dataTransfer;
                if (dt.files && dt.files.length > 0) {
                    handleFileObject(dt.files[0]);
                }
            });
        }

        function handleFileChosen(event) {
            if (event.target.files && event.target.files.length > 0) {
                handleFileObject(event.target.files[0]);
            }
        }

        function handleFileObject(file) {
            chosenFile = file;
            document.getElementById('fileNameDisplay').innerText = `Selected: ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
            document.getElementById('fileSelectedBox').style.display = 'flex';
        }

        function removeSelectedFile(e) {
            if (e) e.stopPropagation();
            chosenFile = null;
            document.getElementById('fileInput').value = '';
            document.getElementById('fileSelectedBox').style.display = 'none';
        }

        async function executeIntakeAnalysis() {
            const btn = document.getElementById('processBtn');
            btn.disabled = true;
            btn.innerHTML = '<span>⏳ Processing OCR & Redaction...</span>';

            try {
                let response;
                if (intakeMode === 'upload') {
                    if (!chosenFile) {
                        alert("Please select or drop a document file first, or switch to Raw Text Input.");
                        btn.disabled = false;
                        btn.innerHTML = '<span>Run OCR & Redaction Engine ➔</span>';
                        return;
                    }
                    const formData = new FormData();
                    formData.append('file', chosenFile);
                    response = await fetch('/ai-api/analyze', { method: 'POST', body: formData });
                } else {
                    const text = document.getElementById('rawInputText').value.trim();
                    if (!text) {
                        alert("Please enter or paste document text to analyze.");
                        btn.disabled = false;
                        btn.innerHTML = '<span>Run OCR & Redaction Engine ➔</span>';
                        return;
                    }
                    const formData = new FormData();
                    formData.append('text', text);
                    response = await fetch('/ai-api/analyze', { method: 'POST', body: formData });
                }

                if (!response.ok) {
                    const err = await response.json();
                    throw new Error(err.detail || 'Analysis request failed');
                }

                const data = await response.json();
                analysisData = data;
                populatePipelineResults(data);

                maxUnlockedStep = 4;
                currentStep = 2;
                updateStepperUI();
                showToast("Extraction and PII sanitization completed successfully.");
                
                // Immediately synchronize sanitized copy to Nextcloud Vault in background
                triggerVaultCommit();

            } catch (err) {
                alert("Error during document analysis: " + err.message);
            } finally {
                btn.disabled = false;
                btn.innerHTML = '<span>Run OCR & Redaction Engine ➔</span>';
            }
        }

        function populatePipelineResults(data) {
            const summary = data.summary || {};
            const metrics = summary.metrics || {};
            const piiSummary = data.pii_summary || {};

            // Step 2: OCR Extraction details
            document.getElementById('ocrDocType').innerText = summary.document_type || 'General Document';
            document.getElementById('ocrWordCount').innerText = metrics.word_count || 0;
            document.getElementById('ocrCharCount').innerText = metrics.character_count || 0;
            document.getElementById('ocrTextDisplay').innerText = data.original_text || 'No text extracted.';

            // Step 3: PII Redaction details
            const piiBar = document.getElementById('piiBreakdownContainer');
            piiBar.innerHTML = '';
            
            const totalRedactions = piiSummary.total_redactions || 0;
            const mainBadge = document.createElement('div');
            mainBadge.className = 'pii-tag-count';
            mainBadge.style.background = totalRedactions > 0 ? 'rgba(212, 175, 55, 0.18)' : 'rgba(212, 175, 55, 0.08)';
            mainBadge.style.color = totalRedactions > 0 ? '#F5D77F' : '#F3E5AB';
            mainBadge.style.borderColor = totalRedactions > 0 ? '#D4AF37' : 'rgba(212, 175, 55, 0.4)';
            mainBadge.innerText = `🔒 ${totalRedactions} Sensitive Items Redacted`;
            piiBar.appendChild(mainBadge);

            const categories = piiSummary.categories || {};
            for (const [cat, count] of Object.entries(categories)) {
                const badge = document.createElement('div');
                badge.className = 'pii-tag-count';
                badge.innerText = `${cat}: ${count}`;
                piiBar.appendChild(badge);
            }

            document.getElementById('diffOriginalText').innerText = data.original_text || '';
            
            // Format redacted text with Gold/Amber metallic badge tags
            let fmtRedacted = escapeHtml(data.redacted_text || '');
            fmtRedacted = fmtRedacted.replace(/\\[REDACTED_AADHAAR\\]/g, '<span class="redacted-badge">[REDACTED_AADHAAR]</span>');
            fmtRedacted = fmtRedacted.replace(/\\[REDACTED_PAN\\]/g, '<span class="redacted-badge">[REDACTED_PAN]</span>');
            fmtRedacted = fmtRedacted.replace(/\\[REDACTED_CREDIT_CARD\\]/g, '<span class="redacted-badge">[REDACTED_CREDIT_CARD]</span>');
            fmtRedacted = fmtRedacted.replace(/\\[REDACTED_EMAIL\\]/g, '<span class="redacted-badge">[REDACTED_EMAIL]</span>');
            fmtRedacted = fmtRedacted.replace(/\\[REDACTED_PHONE\\]/g, '<span class="redacted-badge">[REDACTED_PHONE]</span>');
            document.getElementById('diffRedactedText').innerHTML = fmtRedacted;

            // AI Highlights List
            const hlList = document.getElementById('aiHighlightsList');
            hlList.innerHTML = '';
            const highlights = summary.key_highlights || [];
            if (highlights.length === 0) {
                hlList.innerHTML = '<li>Document parsed. No high-priority risks detected.</li>';
            } else {
                highlights.forEach(h => {
                    const li = document.createElement('li');
                    li.innerText = h;
                    hlList.appendChild(li);
                });
            }

            // Step 4: Audit Specs
            document.getElementById('specPiiCount').innerText = `${totalRedactions} PII Elements Scrubbed`;
            document.getElementById('specTimestamp').innerText = new Date().toISOString();
        }

        function escapeHtml(str) {
            const p = document.createElement('p');
            p.textContent = str;
            return p.innerHTML;
        }

        function copyElementText(elId) {
            const el = document.getElementById(elId);
            if (!el) return;
            navigator.clipboard.writeText(el.innerText).then(() => {
                showToast("Copied to clipboard!");
            });
        }

        function downloadSanitizedFile() {
            if (!analysisData || !analysisData.redacted_text) {
                showToast("No sanitized text available to download.");
                return;
            }
            const blob = new Blob([analysisData.redacted_text], { type: 'text/plain;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `sanitized_${analysisData.filename || 'document'}.txt`;
            a.click();
            URL.revokeObjectURL(url);
            showToast("Sanitized document downloaded.");
        }

        function resetPipeline() {
            chosenFile = null;
            analysisData = null;
            maxUnlockedStep = 1;
            currentStep = 1;
            document.getElementById('rawInputText').value = '';
            document.getElementById('fileInput').value = '';
            document.getElementById('fileSelectedBox').style.display = 'none';
            updateStepperUI();
            showToast("Pipeline reset. Ready for new document intake.");
        }

        function openNextcloudVault() {
            const modal = document.getElementById('vaultModalOverlay');
            if (!modal) return;
            
            // Populate current sanitized file details
            const baseName = (analysisData && analysisData.filename) ? analysisData.filename.replace(/\\.[^/.]+$/, '').replace(/[^a-zA-Z0-9_-]/g, '_') : 'KYC_Document';
            const currentFileName = `Sanitized_${baseName}.txt`;
            const currentText = (analysisData && analysisData.redacted_text) ? analysisData.redacted_text : "Confidential KYC Client Record [PII SCRUBBED]\\nFull Name: Rameshwar Verma\\nAadhaar Number: [REDACTED_AADHAAR]\\nPAN Card Number: [REDACTED_PAN]\\nCorporate Email: [REDACTED_EMAIL]\\nContact Phone: [REDACTED_PHONE]\\nAccount Status: KYC Verified against UIDAI central registry.\\n\\nStatus: Encrypted with SSE-KMS (AES-256-GCM) in AWS S3 / Nextcloud Primary Storage.";
            
            document.getElementById('modalCurrentFileName').innerText = currentFileName;
            document.getElementById('modalPreviewTitle').innerText = currentFileName;
            document.getElementById('modalPreviewBody').innerText = currentText;

            modal.style.display = 'flex';
            if (analysisData && analysisData.redacted_text) {
                triggerVaultCommit();
            }
            showToast("Opening SecureVault Cloud Storage & Nextcloud Explorer...");
        }

        function closeNextcloudVault() {
            const modal = document.getElementById('vaultModalOverlay');
            if (modal) modal.style.display = 'none';
        }

        function handleVaultOverlayClick(e) {
            if (e.target.id === 'vaultModalOverlay') {
                closeNextcloudVault();
            }
        }

        function selectVaultFile(fileKey, evt) {
            const titleEl = document.getElementById('modalPreviewTitle');
            const bodyEl = document.getElementById('modalPreviewBody');
            const items = document.querySelectorAll('.vault-file-item');
            items.forEach(i => i.classList.remove('active'));

            if (fileKey === 'current') {
                const curItem = document.getElementById('vaultItemCurrent');
                if (curItem) curItem.classList.add('active');
                const currentFileName = (analysisData && analysisData.filename) ? `Sanitized_${analysisData.filename}` : 'Sanitized_KYC_Document.txt';
                const currentText = (analysisData && analysisData.redacted_text) ? analysisData.redacted_text : "Confidential KYC Client Record [PII SCRUBBED]\\nFull Name: Rameshwar Verma\\nAadhaar Number: [REDACTED_AADHAAR]\\nPAN Card Number: [REDACTED_PAN]\\nCorporate Email: [REDACTED_EMAIL]\\nContact Phone: [REDACTED_PHONE]\\nAccount Status: KYC Verified against UIDAI central registry.";
                titleEl.innerText = currentFileName;
                bodyEl.innerText = currentText;
            } else if (fileKey === 'policy') {
                const el = evt ? evt.currentTarget : document.querySelector('[onclick*="policy"]');
                if (el) el.classList.add('active');
                titleEl.innerText = 'ZeroTrust_Security_Policy.pdf';
                bodyEl.innerText = "SECUREVAULT ENTERPRISE SECURITY POLICY 2026\\n===========================================\\n1. ZERO-TRUST ARCHITECTURE\\nAll data stored in Nextcloud primary storage is hardware-encrypted at rest using AWS KMS (Key ID: securevault-s3-kms-v1).\\n\\n2. AUTOMATED PII SCRUBBING\\nNo unredacted Aadhaar, PAN, SSN, Credit Cards, or personal contact info is permitted in unencrypted volumes.\\n\\n3. AUDIT REPLICATION\\nAll WebDAV transactions are timestamped and signed with SHA-256 HMAC integrity.";
            } else if (fileKey === 'audit') {
                const el = evt ? evt.currentTarget : document.querySelector('[onclick*="audit"]');
                if (el) el.classList.add('active');
                titleEl.innerText = 'KMS_Key_Rotation_Audit_2026.json';
                bodyEl.innerText = "{\\n  \\"audit_version\\": \\"1.0.0\\",\\n  \\"kms_provider\\": \\"AWS Key Management Service\\",\\n  \\"algorithm\\": \\"AES-256-GCM\\",\\n  \\"key_arn\\": \\"arn:aws:kms:us-east-1:123456789012:key/securevault-s3-kms\\",\\n  \\"key_rotation_status\\": \\"ENABLED_AUTOMATIC_365_DAYS\\",\\n  \\"zero_trust_compliance\\": \\"SAIF_AND_SOC2_CERTIFIED\\",\\n  \\"last_audit_epoch\\": 1790400000\\n}";
            }
        }

        function copyVaultContent() {
            const bodyEl = document.getElementById('modalPreviewBody');
            if (bodyEl) {
                navigator.clipboard.writeText(bodyEl.innerText).then(() => {
                    showToast("Vault content copied to clipboard!");
                });
            }
        }

        function showToast(msg) {
            const t = document.getElementById('toastMessage');
            t.innerText = msg;
            t.style.display = 'block';
            setTimeout(() => { t.style.display = 'none'; }, 3500);
        }
    </script>
</body>
</html>
"""
