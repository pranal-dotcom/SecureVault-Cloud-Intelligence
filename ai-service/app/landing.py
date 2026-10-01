LANDING_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    <title>SecureVault - Enterprise Document Intelligence</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #0B0F17;
            --text-primary: #FFFFFF;
            --text-secondary: #94A3B8;
            --accent-amber: #F59E0B;
            --accent-amber-hover: #D97706;
            --glass-bg: rgba(17, 24, 39, 0.7);
            --glass-border: rgba(255, 255, 255, 0.08);
            --font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body, .app-root-container {
            font-family: var(--font-family);
            background: 
                radial-gradient(circle at 75% 20%, rgba(245, 158, 11, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 15% 85%, rgba(30, 58, 138, 0.12) 0%, transparent 50%),
                linear-gradient(180deg, rgba(11, 15, 23, 0.88) 0%, rgba(11, 15, 23, 0.95) 100%),
                url('https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=2400&q=85') center/cover no-repeat fixed !important;
            background-color: #0B0F17 !important;
            color: #F8FAFC !important;
            min-height: 100vh;
            line-height: 1.6;
            overflow-x: hidden;
            -webkit-font-smoothing: antialiased;
        }

        /* Navbar */
        .top-nav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem 3rem;
            border-bottom: 1px solid var(--glass-border);
            background: rgba(11, 15, 23, 0.85);
            backdrop-filter: blur(12px);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .nav-logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--text-primary);
            text-decoration: none;
            letter-spacing: -0.02em;
        }

        .nav-logo svg {
            width: 24px;
            height: 24px;
            color: var(--accent-amber);
        }

        .nav-logo .brand-highlight {
            color: var(--accent-amber);
            font-weight: 600;
        }

        .nav-links {
            display: flex;
            gap: 2rem;
            align-items: center;
        }

        .nav-links a {
            text-decoration: none;
            color: var(--text-secondary);
            font-size: 0.95rem;
            font-weight: 500;
            transition: color 0.2s;
        }

        .nav-links a:hover {
            color: var(--text-primary);
        }

        .nav-actions {
            display: flex;
            gap: 1rem;
            align-items: center;
        }

        .btn-nav-outline {
            text-decoration: none;
            color: var(--text-secondary);
            font-size: 0.95rem;
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            transition: all 0.2s;
        }

        .btn-nav-outline:hover {
            color: var(--text-primary);
            background: rgba(255,255,255,0.05);
        }

        .btn-nav-primary {
            text-decoration: none;
            background: rgba(245, 158, 11, 0.1);
            color: var(--accent-amber);
            border: 1px solid rgba(245, 158, 11, 0.3);
            padding: 0.5rem 1.25rem;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.2s;
        }

        .btn-nav-primary:hover {
            background: rgba(245, 158, 11, 0.2);
        }

        /* Split Hero Layout */
        .hero {
            display: flex;
            max-width: 1400px;
            margin: 5rem auto;
            padding: 0 3rem;
            align-items: center;
            justify-content: space-between;
            gap: 4rem;
        }

        .hero-content {
            flex: 1;
            max-width: 600px;
        }

        .eyebrow-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            border-radius: 100px;
            background: rgba(245, 158, 11, 0.1);
            border: 1px solid rgba(245, 158, 11, 0.2);
            color: var(--accent-amber);
            font-size: 0.85rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            margin-bottom: 1.5rem;
        }

        .hero-title {
            font-size: 3.5rem;
            font-weight: 800;
            line-height: 1.15;
            color: #FFFFFF;
            margin-bottom: 1.5rem;
            letter-spacing: -0.03em;
        }

        .hero-title .highlight {
            color: var(--accent-amber);
        }

        .hero-subtitle {
            color: var(--text-secondary);
            font-size: 1.125rem;
            line-height: 1.6;
            margin-bottom: 2.5rem;
        }

        .hero-actions {
            display: flex;
            gap: 1rem;
            align-items: center;
        }

        .btn-primary {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: var(--accent-amber);
            color: var(--bg-base);
            font-weight: 600;
            font-size: 1rem;
            padding: 14px 28px;
            border-radius: 8px;
            text-decoration: none;
            transition: all 0.2s ease;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 14px rgba(245, 158, 11, 0.25);
        }

        .btn-primary:hover {
            background: var(--accent-amber-hover);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(245, 158, 11, 0.4);
        }

        .btn-secondary {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            background: rgba(255, 255, 255, 0.03);
            color: #F8FAFC;
            padding: 14px 28px;
            border-radius: 8px;
            font-weight: 500;
            font-size: 1rem;
            text-decoration: none;
            transition: all 0.2s ease;
        }

        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.3);
        }

        /* Right Column: Active Security Pipeline Card */
        .hero-visual {
            flex: 1;
            display: flex;
            justify-content: flex-end;
            max-width: 600px;
        }

        .pipeline-card {
            width: 100%;
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(16px);
        }

        .card-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--glass-border);
        }

        .mac-dot { width: 12px; height: 12px; border-radius: 50%; }
        .mac-dot.r { background: #EF4444; }
        .mac-dot.y { background: #F59E0B; }
        .mac-dot.g { background: #22C55E; }

        .card-title {
            margin-left: auto;
            margin-right: auto;
            color: var(--text-secondary);
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }

        .pipeline-step {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px;
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.03);
            border-radius: 8px;
            margin-bottom: 12px;
            transition: transform 0.2s;
        }
        
        .pipeline-step:hover {
            transform: translateX(4px);
            background: rgba(255, 255, 255, 0.02);
        }

        .step-info {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .step-name {
            font-weight: 600;
            font-size: 0.95rem;
            color: var(--text-primary);
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 100px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .badge-green {
            background: rgba(34, 197, 94, 0.1);
            color: #4ADE80;
            border: 1px solid rgba(34, 197, 94, 0.2);
        }

        .badge-amber {
            background: rgba(245, 158, 11, 0.1);
            color: #F59E0B;
            border: 1px solid rgba(245, 158, 11, 0.2);
            animation: pulse-amber 2s infinite;
        }

        @keyframes pulse-amber {
            0% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.4); }
            70% { box-shadow: 0 0 0 6px rgba(245, 158, 11, 0); }
            100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
        }

        .badge-blue {
            background: rgba(59, 130, 246, 0.1);
            color: #60A5FA;
            border: 1px solid rgba(59, 130, 246, 0.2);
        }

        .badge-icon {
            width: 8px; height: 8px; border-radius: 50%;
        }

        .bg-green { background: #4ADE80; }
        .bg-amber { background: #F59E0B; }
        .bg-blue { background: #60A5FA; }

        /* Floating Feedback Button - Bottom Right */
        .feedback-trigger {
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: var(--glass-bg);
            backdrop-filter: blur(8px);
            border: 1px solid var(--glass-border);
            color: var(--text-secondary);
            padding: 10px 20px;
            border-radius: 100px;
            font-weight: 600;
            font-size: 0.9rem;
            cursor: pointer;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            transition: all 0.2s;
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .feedback-trigger:hover {
            color: var(--text-primary);
            border-color: rgba(255, 255, 255, 0.2);
            background: rgba(255, 255, 255, 0.05);
        }

        /* Modal Overlay & Content */
        .modal-overlay {
            position: fixed; top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(4px);
            display: none; align-items: center; justify-content: center;
            z-index: 2000; opacity: 0; transition: opacity 0.2s;
        }
        .modal-overlay.active { display: flex; opacity: 1; }

        .modal-content {
            background: var(--bg-base);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            width: 100%; max-width: 420px;
            padding: 24px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.5);
        }

        .modal-header {
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;
        }
        .modal-header h3 { font-size: 1.25rem; font-weight: 600; color: #fff; }
        
        .close-btn { background: none; border: none; color: var(--text-secondary); font-size: 1.5rem; cursor: pointer; }
        .close-btn:hover { color: #fff; }

        .feedback-textarea {
            width: 100%; height: 120px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--glass-border);
            border-radius: 8px; padding: 12px;
            color: #fff; font-family: inherit; resize: none; margin-bottom: 20px;
        }
        .feedback-textarea:focus { outline: none; border-color: var(--accent-amber); }

        .modal-actions { display: flex; justify-content: flex-end; gap: 12px; }
        
        .btn-modal-cancel {
            background: transparent; border: 1px solid var(--glass-border);
            color: var(--text-secondary); padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: 500;
        }
        .btn-modal-cancel:hover { color: #fff; background: rgba(255,255,255,0.05); }

        .btn-modal-submit {
            background: var(--accent-amber); border: none; color: var(--bg-base);
            padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: 600;
        }
        .btn-modal-submit:hover { background: var(--accent-amber-hover); }

        .toast {
            position: fixed; bottom: -100px; left: 50%; transform: translateX(-50%);
            background: #10B981; color: #fff; padding: 12px 24px;
            border-radius: 8px; font-weight: 600; font-size: 0.95rem;
            transition: bottom 0.3s; z-index: 3000; box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }
        .toast.show { bottom: 32px; }
        @media (max-width: 768px) {
            .hero { flex-direction: column; padding: 2rem 1.5rem; gap: 2rem; margin: 2rem auto; }
            .hero-title { font-size: 2.2rem; }
            .top-nav { flex-direction: column; gap: 1rem; padding: 1rem; }
            .nav-actions { width: 100%; justify-content: center; }
            .btn-primary, .btn-secondary, .btn-nav-primary, .btn-nav-outline {
                width: 100%; text-align: center; justify-content: center; min-height: 44px;
            }
            .nav-links { flex-wrap: wrap; justify-content: center; gap: 1rem; }
            .features-grid { grid-template-columns: 1fr; padding: 1.5rem; }
            .feature-card { padding: 1.5rem; }
            .pipeline-card { padding: 1.5rem; }
            .modal-content { width: 90%; margin: 2rem auto; }
        }
    </style>
</head>
<body>
    
    <!-- Navbar -->
    <nav class="top-nav">
        <a href="/" class="nav-logo" style="text-decoration: none;">
            <div style="display: flex; align-items: center; gap: 12px; cursor: pointer;">
                <!-- Realistic 3D Cyber Vault Shield -->
                <svg width="36" height="40" viewBox="0 0 36 40" fill="none" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 2px 8px rgba(245, 158, 11, 0.35));">
                    <defs>
                        <!-- Metallic Outer Shield Gradient -->
                        <linearGradient id="shieldMetal" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#FDE68A" />
                            <stop offset="35%" stop-color="#F59E0B" />
                            <stop offset="70%" stop-color="#D97706" />
                            <stop offset="100%" stop-color="#78350F" />
                        </linearGradient>
                        <!-- Bevel Inner Shadow Gradient -->
                        <linearGradient id="innerBevel" x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" stop-color="#1E293B" />
                            <stop offset="100%" stop-color="#0F172A" />
                        </linearGradient>
                        <!-- Core Vault Glow -->
                        <radialGradient id="coreVaultGlow" cx="50%" cy="45%" r="60%">
                            <stop offset="0%" stop-color="#FBBF24" />
                            <stop offset="70%" stop-color="#D97706" />
                            <stop offset="100%" stop-color="#92400E" />
                        </radialGradient>
                    </defs>
                    
                    <!-- Outer Shield Crest -->
                    <path d="M18 1.5 L33 6.5 V18 C33 28.5 26.5 35.8 18 38.5 C9.5 35.8 3 28.5 3 18 V6.5 L18 1.5 Z" 
                          fill="url(#shieldMetal)" stroke="#FDE68A" stroke-width="0.75" />
                    
                    <!-- Inner Dark Bevel Recess -->
                    <path d="M18 4.2 L30.2 8.2 V17.8 C30.2 26.5 24.8 32.8 18 35.2 C11.2 32.8 5.8 26.5 5.8 17.8 V8.2 L18 4.2 Z" 
                          fill="url(#innerBevel)" stroke="rgba(245, 158, 11, 0.3)" stroke-width="0.8" />
                    
                    <!-- Center Vault Core Ring -->
                    <circle cx="18" cy="18" r="7.5" fill="#0B0F17" stroke="url(#shieldMetal)" stroke-width="1.5" />
                    
                    <!-- Heavy Solid Vault Lock / Keyhole Core -->
                    <path d="M18 13.5 C16.2 13.5 14.8 14.9 14.8 16.7 C14.8 17.8 15.4 18.8 16.3 19.3 L15.8 22.8 H20.2 L19.7 19.3 C20.6 18.8 21.2 17.8 21.2 16.7 C21.2 14.9 19.8 13.5 18 13.5 Z" 
                          fill="url(#coreVaultGlow)" />
                </svg>

                <span style="font-size: 1.35rem; font-weight: 700; color: #FFFFFF; letter-spacing: -0.02em;">
                    SecureVault <span style="font-weight: 400; color: #F59E0B; margin-left: 6px;">| Enterprise AI</span>
                </span>
            </div>
        </a>

        <div class="nav-actions">
            <a href="#" onclick="openLoginModal(); return false;" class="btn-nav-primary">Launch Engine</a>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero">
        <div class="hero-content">
            <div class="eyebrow-badge">
                <svg width="20" height="22" viewBox="0 0 36 40" fill="none" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 0 8px rgba(245, 158, 11, 0.45)); vertical-align: middle; margin-right: 6px;">
                  <defs>
                    <linearGradient id="badgeShieldMetal" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stop-color="#FDE68A" />
                      <stop offset="35%" stop-color="#F59E0B" />
                      <stop offset="70%" stop-color="#D97706" />
                      <stop offset="100%" stop-color="#78350F" />
                    </linearGradient>
                    <linearGradient id="badgeInnerBevel" x1="0%" y1="0%" x2="0%" y2="100%">
                      <stop offset="0%" stop-color="#1E293B" />
                      <stop offset="100%" stop-color="#0F172A" />
                    </linearGradient>
                    <radialGradient id="badgeCoreVaultGlow" cx="50%" cy="45%" r="60%">
                      <stop offset="0%" stop-color="#FBBF24" />
                      <stop offset="70%" stop-color="#D97706" />
                      <stop offset="100%" stop-color="#92400E" />
                    </radialGradient>
                  </defs>
                  <path d="M18 1.5 L33 6.5 V18 C33 28.5 26.5 35.8 18 38.5 C9.5 35.8 3 28.5 3 18 V6.5 L18 1.5 Z" fill="url(#badgeShieldMetal)" stroke="#FDE68A" stroke-width="0.75" />
                  <path d="M18 4.2 L30.2 8.2 V17.8 C30.2 26.5 24.8 32.8 18 35.2 C11.2 32.8 5.8 26.5 5.8 17.8 V8.2 L18 4.2 Z" fill="url(#badgeInnerBevel)" stroke="rgba(245, 158, 11, 0.3)" stroke-width="0.8" />
                  <circle cx="18" cy="18" r="7.5" fill="#0B0F17" stroke="url(#badgeShieldMetal)" stroke-width="1.5" />
                  <path d="M18 13.5 C16.2 13.5 14.8 14.9 14.8 16.7 C14.8 17.8 15.4 18.8 16.3 19.3 L15.8 22.8 H20.2 L19.7 19.3 C20.6 18.8 21.2 17.8 21.2 16.7 C21.2 14.9 19.8 13.5 18 13.5 Z" fill="url(#badgeCoreVaultGlow)" />
                </svg> Zero-Trust Document Intelligence
            </div>
            <h1 class="hero-title">
                Your Documents, Sanitized.<br>
                <span class="highlight">Your Enterprise, Secured.</span>
            </h1>
            <p class="hero-subtitle">
                Deploy autonomous PII detection, automated redaction pipelines, and isolated Nextcloud Vault storage—built for strict compliance and enterprise security.
            </p>
            <div class="hero-actions">
                <a href="#" onclick="openLoginModal(); return false;" class="btn-primary">
                    🚀 Launch AI Dashboard
                </a>
            </div>
        </div>


    </section>

    <!-- Fixed Feedback Button -->
    <button class="feedback-trigger" id="feedbackTrigger">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg>
        Feedback
    </button>

    <!-- Feedback Modal -->
    <div class="modal-overlay" id="feedbackModal">
        <div class="modal-content" style="max-width: 450px;">
            <div class="modal-header" style="border-bottom: none; padding-bottom: 0;">
                <div>
                    <h3 style="margin-bottom: 4px;">Submit feedback</h3>
                    <p style="font-size: 0.9rem; color: var(--text-secondary); margin: 0;">Classify your feedback</p>
                </div>
                <button class="close-btn" id="closeModal" style="align-self: flex-start;">&times;</button>
            </div>
            
            <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 20px;" id="feedbackOptions">
                <button type="button" class="feedback-option-btn" style="display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: rgba(255, 255, 255, 0.03); border: 1px solid var(--border-subtle); border-radius: 8px; color: var(--text-primary); cursor: pointer; text-align: left; transition: all 0.2s;" onclick="selectFeedbackCategory(this, 'Compliment')">
                    <span style="font-size: 1.2rem;">💙</span> Give a compliment
                </button>
                <button type="button" class="feedback-option-btn" style="display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: rgba(255, 255, 255, 0.03); border: 1px solid var(--border-subtle); border-radius: 8px; color: var(--text-primary); cursor: pointer; text-align: left; transition: all 0.2s;" onclick="selectFeedbackCategory(this, 'Problem')">
                    <span style="font-size: 1.2rem;">⚠️</span> Report a problem
                </button>
                <button type="button" class="feedback-option-btn" style="display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: rgba(255, 255, 255, 0.03); border: 1px solid var(--border-subtle); border-radius: 8px; color: var(--text-primary); cursor: pointer; text-align: left; transition: all 0.2s;" onclick="selectFeedbackCategory(this, 'Suggestion')">
                    <span style="font-size: 1.2rem;">💡</span> Make a suggestion
                </button>
            </div>

            <div id="feedbackDetailArea" style="display: none; margin-top: 20px;">
                <textarea class="feedback-textarea" id="feedbackText" placeholder="Please provide details..."></textarea>
                <div class="modal-actions" style="margin-top: 16px;">
                    <button class="btn-modal-cancel" id="cancelFeedback">Cancel</button>
                    <button class="btn-modal-submit" id="submitFeedback">Submit</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Auth / Login Modal -->
    <div class="modal-overlay" id="loginModal">
        <div class="modal-content" style="max-width: 400px; text-align: center;">
            <div class="modal-header" style="justify-content: center; margin-bottom: 10px;">
                <h3 style="font-size: 1.5rem;">Operator Login</h3>
            </div>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 24px;">SecureVault Zero-Trust Authentication</p>
            
            <div style="text-align: left; margin-bottom: 16px;">
                <label style="display: block; font-size: 0.8rem; font-weight: 600; color: var(--accent-amber); margin-bottom: 8px; text-transform: uppercase;">Username</label>
                <input type="text" id="authUsername" class="feedback-textarea" style="height: 48px; margin-bottom: 0;" placeholder="Operator ID" />
            </div>
            
            <div style="text-align: left; margin-bottom: 24px;">
                <label style="display: block; font-size: 0.8rem; font-weight: 600; color: var(--accent-amber); margin-bottom: 8px; text-transform: uppercase;">Access Token / Password</label>
                <div style="position: relative; display: flex; align-items: center; width: 100%;">
                    <input type="password" id="authPassword" class="feedback-textarea" style="height: 48px; margin-bottom: 0; width: 100%; padding-right: 42px;" placeholder="••••••••" />
                    <button type="button" id="togglePasswordBtn" onclick="togglePasswordVisibility()" style="position: absolute; right: 12px; background: none; border: none; cursor: pointer; color: #64748B; font-size: 18px; display: flex; align-items: center; justify-content: center; padding: 4px;" aria-label="Toggle password visibility">
                        <svg id="eyeIcon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                            <circle cx="12" cy="12" r="3"></circle>
                        </svg>
                    </button>
                </div>
            </div>
            
            <div id="loginError" style="color: #EF4444; font-size: 0.85rem; margin-bottom: 16px; display: none;">Invalid credentials</div>

            <div class="modal-actions" style="justify-content: space-between;">
                <button class="btn-modal-cancel" id="cancelLogin" style="flex: 1;">Cancel</button>
                <button class="btn-modal-submit" id="submitLogin" style="flex: 1;">Authenticate</button>
            </div>
        </div>
    </div>

    <!-- Toast Notification -->
    <div class="toast" id="toast">Thank you for helping us improve SecureVault!</div>

    <script>
        const trigger = document.getElementById('feedbackTrigger');
        const modal = document.getElementById('feedbackModal');
        const closeBtn = document.getElementById('closeModal');
        const cancelBtn = document.getElementById('cancelFeedback');
        const submitBtn = document.getElementById('submitFeedback');
        const textarea = document.getElementById('feedbackText');
        const toast = document.getElementById('toast');

        const loginModal = document.getElementById('loginModal');
        const cancelLoginBtn = document.getElementById('cancelLogin');
        const submitLoginBtn = document.getElementById('submitLogin');
        const authUsernameInput = document.getElementById('authUsername');
        const authPasswordInput = document.getElementById('authPassword');
        const loginError = document.getElementById('loginError');

        function togglePasswordVisibility() {
            const passInput = document.getElementById('authPassword');
            const eyeIcon = document.getElementById('eyeIcon');
            
            if (passInput.type === 'password') {
                passInput.type = 'text';
                eyeIcon.innerHTML = `
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                    <line x1="1" y1="1" x2="23" y2="23"></line>
                `;
            } else {
                passInput.type = 'password';
                eyeIcon.innerHTML = `
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                `;
            }
        }

        let selectedCategory = '';

        function selectFeedbackCategory(btn, category) {
            document.querySelectorAll('.feedback-option-btn').forEach(b => {
                b.style.borderColor = 'var(--border-subtle)';
                b.style.background = 'rgba(255, 255, 255, 0.03)';
            });
            btn.style.borderColor = 'var(--accent-amber)';
            btn.style.background = 'rgba(245, 158, 11, 0.1)';
            selectedCategory = category;
            
            document.getElementById('feedbackDetailArea').style.display = 'block';
            document.getElementById('feedbackText').focus();
        }

        function openModal() {
            modal.style.display = 'flex';
            setTimeout(() => modal.classList.add('active'), 10);
        }

        function closeModal() {
            modal.classList.remove('active');
            setTimeout(() => { 
                modal.style.display = 'none'; 
                textarea.value = ''; 
                document.querySelectorAll('.feedback-option-btn').forEach(b => {
                    b.style.borderColor = 'var(--border-subtle)';
                    b.style.background = 'rgba(255, 255, 255, 0.03)';
                });
                document.getElementById('feedbackDetailArea').style.display = 'none';
                selectedCategory = '';
            }, 200);
        }

        function openLoginModal() {
            loginModal.style.display = 'flex';
            setTimeout(() => loginModal.classList.add('active'), 10);
            authUsernameInput.focus();
        }

        function closeLoginModal() {
            loginModal.classList.remove('active');
            setTimeout(() => { 
                loginModal.style.display = 'none'; 
                authUsernameInput.value = ''; 
                authPasswordInput.value = ''; 
                loginError.style.display = 'none';
            }, 200);
        }

        window.addEventListener('DOMContentLoaded', () => {
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('login') === 'true') {
                openLoginModal();
            }
        });

        trigger.addEventListener('click', openModal);
        closeBtn.addEventListener('click', closeModal);
        cancelBtn.addEventListener('click', closeModal);
        modal.addEventListener('click', (e) => { if (e.target === modal) closeModal(); });

        cancelLoginBtn.addEventListener('click', closeLoginModal);
        loginModal.addEventListener('click', (e) => { if (e.target === loginModal) closeLoginModal(); });

        submitLoginBtn.addEventListener('click', async () => {
            const u = authUsernameInput.value.trim();
            const p = authPasswordInput.value.trim();
            if (!u || !p) {
                loginError.innerText = "Please provide both username and password.";
                loginError.style.display = 'block';
                return;
            }

            submitLoginBtn.innerText = "Authenticating...";
            loginError.style.display = 'none';

            try {
                const res = await fetch('/ai-api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username: u, password: p })
                });

                if (res.ok) {
                    sessionStorage.setItem('securevault_auth_user', u);
                    sessionStorage.setItem('securevault_auth_pass', p);
                    window.location.href = '/dashboard';
                } else {
                    const errorData = await res.json();
                    loginError.innerText = errorData.detail || "Invalid credentials.";
                    loginError.style.display = 'block';
                }
            } catch (err) {
                loginError.innerText = "Authentication error. Please try again.";
                loginError.style.display = 'block';
            } finally {
                submitLoginBtn.innerText = "Authenticate";
            }
        });

        submitBtn.addEventListener('click', async () => {
            if (!textarea.value.trim()) return;
            submitBtn.textContent = 'Submitting...';
            try {
                await fetch('/ai-api/api/feedback', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ category: selectedCategory || 'General', comment: textarea.value.trim() })
                });
                closeModal();
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 3000);
            } catch (err) {}
            submitBtn.textContent = 'Submit';
        });
    </script>
</body>
</html>
"""
