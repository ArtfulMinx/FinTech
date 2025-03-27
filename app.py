import streamlit as st
import random
from PIL import Image
import io

# Mock icons using emoji (since we can't directly use Lucide icons)
ICONS = {
    'home': '🏠',
    'learn': '📚',
    'help': '❓',
    'settings': '⚙️',
    'trending_up': '📈',
    'target': '🎯',
    'book': '📖',
    'users': '👥',
    'calendar': '📅',
    'gift': '🎁',
    'dollar': '💵',
    'award': '🏆',
    'help_circle': '❓',
    'map_pin': '📍',
    'star': '⭐'
}

class FinBrightApp:
    def __init__(self):
        # Initialize session state variables
        if 'active_tab' not in st.session_state:
            st.session_state.active_tab = 'Home'
        if 'language' not in st.session_state:
            st.session_state.language = 'en'
        if 'user_points' not in st.session_state:
            st.session_state.user_points = 0
        if 'completed_lessons' not in st.session_state:
            st.session_state.completed_lessons = []
        if 'show_settings' not in st.session_state:
            st.session_state.show_settings = False

        # Initialize data similar to React version
        self.user_profile = {
            'name': 'Maria Rodriguez',
            'financialHealthScore': 72,
            'savingsGoal': 10000,
            'currentSavings': 3500,
            'learningStreak': 14
        }

        self.community_data = {
            'referrals': 42,
            'totalSavings': 487500,
            'interestEarned': 3420,
            'upcomingEvents': [
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
            'lendingOpportunities': [
                {
                    'title': 'Small Business Microloan',
                    'maxAmount': '$5,000',
                    'interestRate': '4.5%',
                    'availableSlots': 12
                },
                {
                    'title': 'Community Education Grant',
                    'maxAmount': '$2,500',
                    'interestRate': '3.8%',
                    'availableSlots': 8
                }
            ]
        }

        self.available_badges = [
            {'id': 'budgeting', 'name': 'Budgeting Master', 'points_required': 50},
            {'id': 'credit', 'name': 'Credit Guru', 'points_required': 100},
            {'id': 'investing', 'name': 'Investment Wizard', 'points_required': 150}
        ]

        self.learn_content = [
            {
                'id': 'budgeting',
                'title': 'Budgeting Basics',
                'duration': '5:30',
                'level': 'Beginner',
                'description': 'Learn how to create and stick to a budget',
                'is_locked': False,
                'points_required': 0
            },
            {
                'id': 'credit',
                'title': 'Understanding Credit',
                'duration': '7:15',
                'level': 'Intermediate',
                'description': 'Improve your credit score and financial health',
                'is_locked': True,
                'points_required': 50
            },
            {
                'id': 'investing',
                'title': 'Investing 101',
                'duration': '6:45',
                'level': 'Advanced',
                'description': 'Introduction to investment strategies',
                'is_locked': True,
                'points_required': 100
            }
        ]

    def start_lesson(self, lesson):
        # Check if lesson is locked
        if lesson['is_locked'] and st.session_state.user_points < lesson['points_required']:
            st.warning(f"Unlock this lesson by earning {lesson['points_required']} points!")
            return

        # Calculate points based on lesson difficulty
        points_earned = 20 if lesson['level'] == 'Beginner' else (40 if lesson['level'] == 'Intermediate' else 60)
        
        # Update user points
        st.session_state.user_points += points_earned
        
        # Mark lesson as completed
        st.session_state.completed_lessons.append(lesson['id'])

        # Update learn content
        for content in self.learn_content:
            if content['id'] == lesson['id']:
                content['is_locked'] = False
            
            # Unlock next lesson
            if content['points_required'] <= st.session_state.user_points:
                content['is_locked'] = False

        # Check for badge unlocks
        unlocked_badges = [
            badge for badge in self.available_badges 
            if st.session_state.user_points >= badge['points_required'] 
            and badge['id'] not in st.session_state.completed_lessons
        ]

        if unlocked_badges:
            st.success(f"Congratulations! You've unlocked: {', '.join(badge['name'] for badge in unlocked_badges)}")

    def render_home_content(self):
        # Quick Stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Health Score", value=self.user_profile['financialHealthScore'], delta=None)
        with col2:
            st.metric(
                label="Savings Goal", 
                value=f"${self.user_profile['savingsGoal']}", 
                delta="+$1,000",
                delta_color="normal"  # or "green" if you want the delta in green
            )        
        with col3:
            st.metric(label="Learning Streak", value=f"{self.user_profile['learningStreak']} Days", delta=None)

        # Community Impact
        st.subheader(f"{ICONS['users']} Community Impact")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Referrals", value=self.community_data['referrals'], delta=None)
        with col2:
            st.metric(label="Total Savings", value=f"${self.community_data['totalSavings']}", delta=None)
        with col3:
            st.metric(label="Interest Earned", value=f"${self.community_data['interestEarned']}", delta=None)

        # Upcoming Events
        st.subheader(f"{ICONS['calendar']} Upcoming Events")
        for event in self.community_data['upcomingEvents']:
            with st.expander(event['title']):
                st.write(f"Date: {event['date']}")
                st.write(f"Location: {event['location']}")
                st.write(f"Description: {event['description']}")

        # Lending Opportunities
        st.subheader(f"{ICONS['gift']} Community Lending")
        for opportunity in self.community_data['lendingOpportunities']:
            with st.expander(opportunity['title']):
                st.write(f"Max Amount: {opportunity['maxAmount']}")
                st.write(f"Interest Rate: {opportunity['interestRate']}")
                st.write(f"Available Slots: {opportunity['availableSlots']}")

    def render_learn_content(self):
        st.subheader(f"{ICONS['star']} Your Points: {st.session_state.user_points}")
        st.caption("Earn points to unlock advanced lessons!")

        st.subheader(f"{ICONS['book']} Learn & Grow")
        for lesson in self.learn_content:
            with st.expander(lesson['title']):
                st.write(f"Description: {lesson['description']}")
                st.write(f"Duration: {lesson['duration']}")
                st.write(f"Level: {lesson['level']}")

                if lesson['is_locked'] and st.session_state.user_points < lesson['points_required']:
                    st.warning(f"Requires {lesson['points_required']} points to unlock")
                else:
                    if st.button(f"Start {lesson['title']}", key=lesson['id']):
                        self.start_lesson(lesson)

        # Badges
        st.subheader(f"{ICONS['award']} Available Badges")
        cols = st.columns(len(self.available_badges))
        for i, badge in enumerate(self.available_badges):
            with cols[i]:
                badge_status = "🟢" if st.session_state.user_points >= badge['points_required'] else "🔒"
                st.metric(
                    label=f"{badge_status} {badge['name']}", 
                    value=f"{badge['points_required']} pts"
                )

    def render_help_content(self):
        st.subheader(f"{ICONS['help_circle']} Help & Support")
        
        help_items = [
            {
                'title': 'Local Consultants', 
                'description': 'Connect with financial experts in Riverwood',
                'options': [
                    'Schedule a Free Consultation',
                    'Book a One-on-One Session',
                    'Join Community Financial Workshops'
                ]
            },
            {
                'title': 'FAQ', 
                'description': 'Answers to common financial questions',
                'options': [
                    'Budgeting Tips',
                    'Credit Score Management',
                    'Investment Basics'
                ]
            },
            {
                'title': 'Community Resources', 
                'description': 'Local financial support and programs',
                'options': [
                    'Government Assistance Programs',
                    'Community Grants',
                    'Financial Education Centers'
                ]
            }
        ]

        for item in help_items:
            with st.expander(item['title']):
                st.write(item['description'])
                
                # Create interactive buttons for each option
                for option in item['options']:
                    if st.button(option, key=f"{item['title']}_{option}"):
                        st.info(f"You selected: {option}")
                        if item['title'] == 'Local Consultants':
                            st.write("Our team will contact you shortly to arrange your consultation.")

    def render_settings_content(self):
        st.subheader(f"{ICONS['settings']} App Settings")

        # Language Settings
        st.selectbox(
            "Language", 
            ["English", "Spanish"], 
            index=0 if st.session_state.language == 'en' else 1,
            key='language_select'
        )

        # Notifications
        st.checkbox("Enable Notifications")

        # Privacy
        st.button("Review Privacy Settings")

    def run(self):
        # App Title
        # App Title
        st.markdown("""
        <h1 style='text-align: center; color: black; background-color: #E6F2FF; padding: 15px; border-radius: 10px;'>
        FinBright Solutions
        </h1>
        """, unsafe_allow_html=True)

        # Sidebar for navigation
        navigation_options = ["Home", "Learn", "Help", "Settings"]
        # Use a default index of 0 if the current active tab is not in the list
        current_index = navigation_options.index(st.session_state.active_tab) if st.session_state.active_tab in navigation_options else 0
        
        st.session_state.active_tab = st.sidebar.radio(
            "Navigation", 
            navigation_options,
            index=current_index
        )

        # Render content based on active tab
        if st.session_state.active_tab == "Home":
            self.render_home_content()
        elif st.session_state.active_tab == "Learn":
            self.render_learn_content()
        elif st.session_state.active_tab == "Help":
            self.render_help_content()
        elif st.session_state.active_tab == "Settings":
            self.render_settings_content()

def main():
    app = FinBrightApp()
    app.run()

if __name__ == "__main__":
    main()