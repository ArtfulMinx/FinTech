import streamlit as st

def initialize_session_state():
    """Initialize session state variables."""
    defaults = {
        'user_points': 0,
        'completed_lessons': [],
        'active_page': 'Home',
        'language': 'en'
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def get_badges():
    """Define available badges for learning."""
    return [
        {'id': 'budgeting', 'name': 'Budgeting Master', 'points_required': 50},
        {'id': 'credit', 'name': 'Credit Guru', 'points_required': 100},
        {'id': 'investing', 'name': 'Investment Wizard', 'points_required': 150}
    ]

def get_learn_content():
    """Define learning content with points and locking mechanism."""
    return [
        {
            'id': 'budgeting',
            'title': 'Budgeting Basics',
            'duration': '5:30',
            'level': 'Beginner',
            'description': 'Learn how to create and stick to a budget',
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
        ],
        'lending_opportunities': [
            {
                'title': 'Small Business Microloan',
                'max_amount': '$5,000',
                'interest_rate': '4.5%',
                'available_slots': 12
            },
            {
                'title': 'Community Education Grant',
                'max_amount': '$2,500',
                'interest_rate': '3.8%',
                'available_slots': 8
            }
        ]
    }

def start_lesson(lesson):
    """Handle lesson start logic with points and unlocking."""
    points_map = {'Beginner': 20, 'Intermediate': 40, 'Advanced': 60}
    points_earned = points_map.get(lesson['level'], 20)

    if (lesson['points_required'] > st.session_state.user_points and 
        lesson['is_locked']):
        st.warning(f"You need {lesson['points_required']} points to unlock this lesson!")
        return

    st.session_state.user_points += points_earned
    st.session_state.completed_lessons.append(lesson['id'])
    st.success(f"Congratulations! You earned {points_earned} points!")

def home_page():
    """Render home page with quick stats and community information."""
    st.title("FinBright: Riverwood Community Financial Empowerment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Financial Health", "72%")
    with col2:
        st.metric("Savings Goal", "$10,000", "$3,500 saved")
    with col3:
        st.metric("Learning Streak", "14 Days")

    st.subheader("Community Impact")
    community_data = get_community_data()
    
    cols = st.columns(3)
    with cols[0]:
        st.metric("Referrals", community_data['referrals'])
    with cols[1]:
        st.metric("Total Savings", f"${community_data['total_savings']}")
    with cols[2]:
        st.metric("Interest Earned", f"${community_data['interest_earned']}")

    st.subheader("Upcoming Events")
    for event in community_data['upcoming_events']:
        with st.expander(event['title']):
            st.write(f"**Date:** {event['date']}")
            st.write(f"**Location:** {event['location']}")
            st.write(f"**Description:** {event['description']}")

def learn_page():
    """Render learning content page with gamification."""
    st.subheader(f"Your Points: {st.session_state.user_points}")
    
    st.write("Earn points to unlock advanced lessons!")

    learn_content = get_learn_content()
    badges = get_badges()

    for lesson in learn_content:
        with st.expander(lesson['title']):
            st.write(f"**Level:** {lesson['level']}")
            st.write(f"**Duration:** {lesson['duration']}")
            st.write(lesson['description'])

            if lesson['points_required'] > st.session_state.user_points:
                st.warning(f"Locked! Requires {lesson['points_required']} points")
            else:
                if st.button(f"Start {lesson['title']} Lesson", key=lesson['id']):
                    start_lesson(lesson)

    st.subheader("Available Badges")
    badge_cols = st.columns(len(badges))
    for i, badge in enumerate(badges):
        with badge_cols[i]:
            earned = st.session_state.user_points >= badge['points_required']
            st.metric(
                badge['name'], 
                "Earned" if earned else f"{badge['points_required']} pts", 
                "✅" if earned else "🔒"
            )

def community_help_page():
    """Render community help and support page."""
    st.subheader("Help & Support")
    
    help_options = [
        ("FAQ", "Answers to common questions"),
        ("Contact Support", "Get help from our team"),
        ("Community Resources", "Local financial support")
    ]

    for title, description in help_options:
        with st.expander(title):
            st.write(description)
            st.button(f"Learn More about {title}")

def settings_page():
    """Render app settings page."""
    st.subheader("App Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Language**")
        st.write(f"Current: {'English' if st.session_state.language == 'en' else 'Spanish'}")
    
    with col2:
        if st.button("Switch Language"):
            st.session_state.language = 'es' if st.session_state.language == 'en' else 'en'

    st.write("**Notifications**")
    notify = st.checkbox("Receive updates and alerts")
    
    st.write("**Privacy**")
    st.button("Review Privacy Settings")

def main():
    """Main Streamlit app function."""
    initialize_session_state()
    
    page = st.sidebar.radio(
        "Navigation", 
        ["Home", "Learn", "Community Help", "Settings"]
    )

    if page == "Home":
        home_page()
    elif page == "Learn":
        learn_page()
    elif page == "Community Help":
        community_help_page()
    elif page == "Settings":
        settings_page()

if __name__ == "__main__":
    main()