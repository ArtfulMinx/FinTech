import streamlit as st
import pandas as pd

def set_custom_style():
    """Set custom CSS for improved styling."""
    st.markdown("""
    <style>
    /* Custom Background */
    .stApp {
        background-color: #f0f4f8;
    }
    
    /* Card-like containers */
    .card {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Metrics styling */
    .metric-container {
        display: flex;
        justify-content: space-between;
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Sidebar enhancements */
    .css-1aumxhk {
        background-color: #2c3e50;
        color: white;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 5px;
    }
    
    .stButton>button:hover {
        background-color: #2980b9;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #ecf0f1;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    defaults = {
        'user_points': 0,
        'completed_lessons': [],
        'financial_health': 72,
        'savings_goal': 10000,
        'current_savings': 3500,
        'learning_streak': 14
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def get_badges():
    """Define available badges for learning."""
    return [
        {'id': 'budgeting', 'name': 'Budgeting Master', 'points_required': 50, 'icon': '💰'},
        {'id': 'credit', 'name': 'Credit Guru', 'points_required': 100, 'icon': '📈'},
        {'id': 'investing', 'name': 'Investment Wizard', 'points_required': 150, 'icon': '🏦'}
    ]

def get_learn_content():
    """Define learning content with points and locking mechanism."""
    return [
        {
            'id': 'budgeting',
            'title': 'Budgeting Basics',
            'duration': '5:30',
            'level': 'Beginner',
            'description': 'Create and maintain an effective personal budget',
            'points_required': 0,
            'is_locked': False
        },
        {
            'id': 'credit',
            'title': 'Understanding Credit',
            'duration': '7:15',
            'level': 'Intermediate',
            'description': 'Improve your credit score and financial health',
            'points_required': 50,
            'is_locked': True
        },
        {
            'id': 'investing',
            'title': 'Investing 101',
            'duration': '6:45',
            'level': 'Advanced',
            'description': 'Introduction to investment strategies',
            'points_required': 100,
            'is_locked': True
        }
    ]

def get_community_data():
    """Simulate community data."""
    return {
        'referrals': 42,
        'total_savings': 487500,
        'interest_earned': 3420,
        'upcoming_events': [
            {
                'title': 'Entrepreneurship Workshop',
                'date': 'April 15, 2025',
                'location': 'Community Center',
                'description': 'Learn startup strategies for local businesses'
            },
            {
                'title': 'Financial Literacy Fest',
                'date': 'May 22, 2025',
                'location': 'River Elara Park',
                'description': 'Free workshops and community networking'
            }
        ]
    }

def start_lesson(lesson):
    """Handle lesson start logic with points and unlocking."""
    points_map = {'Beginner': 20, 'Intermediate': 40, 'Advanced': 60}
    points_earned = points_map.get(lesson['level'], 20)

    if lesson['is_locked']:
        st.warning(f"You need {lesson['points_required']} points to unlock this lesson!")
        return

    st.session_state.user_points += points_earned
    st.success(f"Congratulations! You earned {points_earned} points!")

def home_page():
    """Render home page with financial overview and community impact."""
    st.markdown("## 📊 Financial Dashboard")
    
    # Financial Health Overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h4>Financial Health</h4>
            <h2>72%</h2>
            <small>Keep improving!</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="card">
            <h4>Savings Progress</h4>
            <h2>${st.session_state.current_savings}</h2>
            <small>Goal: ${st.session_state.savings_goal}</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h4>Learning Streak</h4>
            <h2>14 Days</h2>
            <small>Keep learning!</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Community Impact
    st.markdown("## 🌟 Community Impact")
    community_data = get_community_data()
    
    impact_df = pd.DataFrame([
        {'Metric': 'Community Referrals', 'Value': community_data['referrals']},
        {'Metric': 'Total Community Savings', 'Value': f'${community_data["total_savings"]:,}'},
        {'Metric': 'Total Interest Earned', 'Value': f'${community_data["interest_earned"]:,}'}
    ])
    
    st.dataframe(impact_df, use_container_width=True)
    
    # Upcoming Events
    st.markdown("## 📅 Upcoming Events")
    for event in community_data['upcoming_events']:
        with st.expander(event['title']):
            st.write(f"**Date:** {event['date']}")
            st.write(f"**Location:** {event['location']}")
            st.write(f"**Description:** {event['description']}")

def learn_page():
    """Render learning content page with gamification."""
    st.markdown("## 🎓 Learning Center")
    
    # Points and Progress
    st.markdown(f"""
    <div class="card">
        <h3>Your Learning Points: {st.session_state.user_points} 🏆</h3>
        <p>Earn points by completing lessons and unlock new content!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Learn Content
    learn_content = get_learn_content()
    
    for lesson in learn_content:
        with st.expander(lesson['title']):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Level:** {lesson['level']}")
                st.write(f"**Duration:** {lesson['duration']}")
                st.write(lesson['description'])
            
            with col2:
                if lesson['points_required'] > st.session_state.user_points:
                    st.warning(f"🔒 {lesson['points_required']} pts")
                else:
                    if st.button(f"Start Lesson", key=lesson['id']):
                        start_lesson(lesson)
    
    # Badges
    st.markdown("## 🏅 Available Badges")
    badges = get_badges()
    
    badge_cols = st.columns(len(badges))
    for i, badge in enumerate(badges):
        with badge_cols[i]:
            earned = st.session_state.user_points >= badge['points_required']
            st.metric(
                badge['icon'] + " " + badge['name'], 
                "Earned" if earned else f"{badge['points_required']} pts", 
                "✅" if earned else "🔒"
            )

def main():
    """Main Streamlit app function."""
    set_custom_style()
    initialize_session_state()
    
    st.sidebar.title("🌈 FinBright")
    st.sidebar.write("Riverwood Community Financial Empowerment")
    
    menu_options = ["Home", "Learn", "Community"]
    choice = st.sidebar.radio("Navigation", menu_options)

    if choice == "Home":
        home_page()
    elif choice == "Learn":
        learn_page()
    else:
        st.write("Community features coming soon!")

if __name__ == "__main__":
    main()