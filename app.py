import streamlit as st
import random

# ============================================================================
# PAGE CONFIGURATION & STYLING
# ============================================================================

st.set_page_config(
    page_title="Number Guessing Game",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium styling
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 100%);
        }
        
        .main {
            background: transparent;
        }
        
        h1 {
            text-align: center;
            background: linear-gradient(90deg, #00d4ff, #0099ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 0.5em;
            letter-spacing: 2px;
        }
        
        .subtitle {
            text-align: center;
            color: #a0aec0;
            font-size: 1.1em;
            margin-bottom: 1.5em;
            font-weight: 300;
        }
        
        .game-container {
            max-width: 600px;
            margin: 0 auto;
            padding: 30px;
            border-radius: 15px;
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid rgba(0, 212, 255, 0.3);
            backdrop-filter: blur(10px);
        }
        
        .stats-box {
            background: rgba(0, 212, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #00d4ff;
            margin: 15px 0;
            text-align: center;
        }
        
        .feedback {
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            text-align: center;
            font-weight: 600;
            font-size: 1.1em;
        }
        
        .too-low {
            background: rgba(255, 193, 7, 0.2);
            color: #ffc107;
            border-left: 4px solid #ffc107;
        }
        
        .too-high {
            background: rgba(244, 67, 54, 0.2);
            color: #f44336;
            border-left: 4px solid #f44336;
        }
        
        .correct {
            background: rgba(76, 175, 80, 0.2);
            color: #4caf50;
            border-left: 4px solid #4caf50;
        }
        
        .button-container {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin: 20px 0;
        }
        
        .range-info {
            text-align: center;
            color: #64748b;
            font-size: 0.95em;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'secret_number' not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.feedback = ""
    st.session_state.guess_history = []
    st.session_state.lower_bound = 1
    st.session_state.upper_bound = 100

# ============================================================================
# MAIN GAME INTERFACE
# ============================================================================

st.markdown("<h1>🎯 Number Guessing Game</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Test your luck and guess the secret number!</p>", unsafe_allow_html=True)

# Create game container
with st.container():
    st.markdown("<div class='game-container'>", unsafe_allow_html=True)
    
    # Range information
    st.markdown(f"""
        <div class='range-info'>
        <p>📊 The secret number is between <strong>{st.session_state.lower_bound}</strong> and <strong>{st.session_state.upper_bound}</strong></p>
        </div>
    """, unsafe_allow_html=True)
    
    # Game status
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class='stats-box'>
            <p>🔢 Attempts Made</p>
            <p style='font-size: 2em; color: #00d4ff; margin: 10px 0;'>{st.session_state.attempts}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='stats-box'>
            <p>📝 Status</p>
            <p style='font-size: 1.2em; color: #00d4ff; margin: 10px 0;'>{'🎉 WON' if st.session_state.game_over else '🎮 PLAYING'}</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Guess history
    if st.session_state.guess_history:
        st.markdown("<p style='color: #a0aec0; text-align: center; margin-top: 20px;'><strong>Your guesses:</strong></p>", unsafe_allow_html=True)
        
        # Display guesses in a nice format
        guess_text = " | ".join([f"<span style='color: #00d4ff; font-weight: bold;'>{g}</span>" for g in st.session_state.guess_history])
        st.markdown(f"<p style='text-align: center; font-size: 1.1em;'>{guess_text}</p>", unsafe_allow_html=True)
    
    # Feedback message
    if st.session_state.feedback:
        if "Too Low" in st.session_state.feedback:
            st.markdown(f"<div class='feedback too-low'>{st.session_state.feedback}</div>", unsafe_allow_html=True)
        elif "Too High" in st.session_state.feedback:
            st.markdown(f"<div class='feedback too-high'>{st.session_state.feedback}</div>", unsafe_allow_html=True)
        elif "Congratulations" in st.session_state.feedback:
            st.markdown(f"<div class='feedback correct'>{st.session_state.feedback}</div>", unsafe_allow_html=True)
    
    # Game controls
    st.markdown("<hr style='margin: 30px 0; border-color: rgba(0, 212, 255, 0.2);'>", unsafe_allow_html=True)
    
    if not st.session_state.game_over:
        # Input for guess
        guess = st.number_input(
            "Enter your guess:",
            min_value=st.session_state.lower_bound,
            max_value=st.session_state.upper_bound,
            value=50,
            step=1,
            key="guess_input"
        )
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            if st.button("🎲 Submit Guess", use_container_width=True):
                st.session_state.attempts += 1
                st.session_state.guess_history.append(guess)
                
                if guess < st.session_state.secret_number:
                    st.session_state.feedback = "📉 Too Low! Try a higher number."
                    st.session_state.lower_bound = max(st.session_state.lower_bound, guess + 1)
                elif guess > st.session_state.secret_number:
                    st.session_state.feedback = "📈 Too High! Try a lower number."
                    st.session_state.upper_bound = min(st.session_state.upper_bound, guess - 1)
                else:
                    st.session_state.feedback = f"🎉 Congratulations! You guessed the number {st.session_state.secret_number} in {st.session_state.attempts} attempts!"
                    st.session_state.game_over = True
                
                st.rerun()
    else:
        # Game over message
        st.markdown(f"""
            <div class='feedback correct'>
            🎉 <strong>You Won!</strong><br>
            The secret number was <strong>{st.session_state.secret_number}</strong><br>
            You took <strong>{st.session_state.attempts}</strong> attempts
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Play Again", use_container_width=True):
            st.session_state.secret_number = random.randint(1, 100)
            st.session_state.attempts = 0
            st.session_state.game_over = False
            st.session_state.feedback = ""
            st.session_state.guess_history = []
            st.session_state.lower_bound = 1
            st.session_state.upper_bound = 100
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR INFO
# ============================================================================

with st.sidebar:
    st.markdown("### 📋 How to Play")
    st.info("""
    1. **Guess a Number**: Enter a number between 1 and 100
    2. **Get Feedback**: Receive hints if your guess is too high or too low
    3. **Win the Game**: Guess the correct number in as few attempts as possible
    4. **Try Again**: Play multiple rounds and beat your high score!
    """)
    
    st.markdown("### 🏆 Tips & Tricks")
    st.success("""
    - **Binary Search**: Try 50 first, then adjust based on feedback
    - **Narrow Down**: Each guess helps eliminate half the range
    - **Stay Focused**: Keep track of previous guesses
    """)
    
    st.markdown("### 📊 Statistics")
    if st.session_state.guess_history:
        best_possible = len(bin(st.session_state.upper_bound - st.session_state.lower_bound + 1)) - 2
        st.metric("Current Attempts", st.session_state.attempts)
        st.metric("Optimal Attempts", best_possible)
    else:
        st.text("Play a game to see statistics!")
