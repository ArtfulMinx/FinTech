import React, { useState } from 'react';
import { 
  Home, TrendingUp, Users, Award, Gift, Book, 
  Calendar, DollarSign, Target, MapPin, Globe, 
  Settings, Play, HelpCircle, Percent, Star, Lock, Unlock 
} from 'lucide-react';

const FinBrightCommunityApp = () => {
  const [activeTab, setActiveTab] = useState('home');
  const [language, setLanguage] = useState('en');
  const [showSettings, setShowSettings] = useState(false);
  
  // New state for gamification
  const [userPoints, setUserPoints] = useState(0);
  const [completedLessons, setCompletedLessons] = useState([]);
  const [availableBadges, setAvailableBadges] = useState([
    { id: 'budgeting', name: 'Budgeting Master', icon: <DollarSign />, pointsRequired: 50 },
    { id: 'credit', name: 'Credit Guru', icon: <TrendingUp />, pointsRequired: 100 },
    { id: 'investing', name: 'Investment Wizard', icon: <Percent />, pointsRequired: 150 }
  ]);

  // Simulated community data reflecting Riverwoods demographics
  const communityData = {
    referrals: 42,
    totalSavings: 487500,
    interestEarned: 3420,
    upcomingEvents: [
      {
        title: 'Entrepreneurship Workshop',
        date: 'April 15, 2025',
        location: 'Community Center',
        description: 'Learn startup strategies for local businesses'
      },
      {
        title: 'Financial Literacy Fest',
        date: 'May 22, 2025',
        location: 'River Elara Park',
        description: 'Free workshops and community networking'
      }
    ],
    lendingOpportunities: [
      {
        title: 'Small Business Microloan',
        maxAmount: '$5,000',
        interestRate: '4.5%',
        availableSlots: 12
      },
      {
        title: 'Community Education Grant',
        maxAmount: '$2,500',
        interestRate: '3.8%',
        availableSlots: 8
      }
    ]
  };

  // Personalized user profile
  const userProfile = {
    name: 'Maria Rodriguez',
    financialHealthScore: 72,
    savingsGoal: 10000,
    currentSavings: 3500,
    learningStreak: 14
  };

  // Learn content with gamification
  const [learnContent, setLearnContent] = useState([
    {
      id: 'budgeting',
      title: 'Budgeting Basics',
      duration: '5:30',
      level: 'Beginner',
      icon: <DollarSign />,
      description: 'Learn how to create and stick to a budget',
      isLocked: false,
      pointsEarned: 0,
      pointsRequired: 0
    },
    {
      id: 'credit',
      title: 'Understanding Credit',
      duration: '7:15',
      level: 'Intermediate',
      icon: <TrendingUp />,
      description: 'Improve your credit score and financial health',
      isLocked: true,
      pointsRequired: 50,
      pointsEarned: 0
    },
    {
      id: 'investing',
      title: 'Investing 101',
      duration: '6:45',
      level: 'Advanced',
      icon: <Percent />,
      description: 'Introduction to investment strategies',
      isLocked: true,
      pointsRequired: 100,
      pointsEarned: 0
    }
  ]);

  const handleStartLesson = (lesson) => {
    // Check if lesson is locked
    if (lesson.isLocked && userPoints < lesson.pointsRequired) {
      alert(`Unlock this lesson by earning ${lesson.pointsRequired} points!`);
      return;
    }

    // Calculate points based on lesson difficulty
    const pointsEarned = lesson.level === 'Beginner' ? 20 : 
                         lesson.level === 'Intermediate' ? 40 : 60;
    
    // Update user points
    setUserPoints(prevPoints => prevPoints + pointsEarned);
    
    // Mark lesson as completed
    setCompletedLessons(prev => [...prev, lesson.id]);

    // Update learn content to unlock next lessons
    setLearnContent(prevContent => prevContent.map(content => {
      if (content.id === lesson.id) {
        return { ...content, isLocked: false };
      }
      // Unlock next lesson if current lesson is completed
      if (content.pointsRequired <= userPoints + pointsEarned) {
        return { ...content, isLocked: false };
      }
      return content;
    }));

    // Check for badge unlocks
    const unlockedBadges = availableBadges.filter(badge => 
      userPoints + pointsEarned >= badge.pointsRequired && 
      !completedLessons.includes(badge.id)
    );

    if (unlockedBadges.length > 0) {
      alert(`Congratulations! You've unlocked: ${unlockedBadges.map(b => b.name).join(', ')}`);
    }
  };

  const renderLearnContent = () => (
    <div>
      <div className="bg-white rounded-lg shadow-md p-4 mb-4 flex items-center">
        <Star className="mr-2 text-yellow-500" />
        <div>
          <h3 className="font-bold">Your Points: {userPoints}</h3>
          <p className="text-xs text-gray-600">Earn points to unlock advanced lessons!</p>
        </div>
      </div>

      <h2 className="text-xl font-bold mb-4 flex items-center">
        <Book className="mr-2 text-blue-600" /> Learn & Grow
      </h2>
      {learnContent.map((item, index) => (
        <div 
          key={index} 
          className={`bg-white rounded-lg shadow-md p-4 mb-3 flex items-center ${
            item.isLocked && userPoints < item.pointsRequired ? 'opacity-50' : ''
          }`}
        >
          <div className={`bg-blue-100 p-3 rounded-full mr-4 ${
            item.isLocked ? 'bg-gray-200' : 'bg-blue-100'
          }`}>
            {item.isLocked ? <Lock size={24} className="text-gray-500" /> : item.icon}
          </div>
          <div className="flex-grow">
            <h3 className="font-semibold">{item.title}</h3>
            <p className="text-xs text-gray-600 mb-2">{item.description}</p>
            <div className="flex justify-between text-xs text-gray-600">
              <span>Duration: {item.duration}</span>
              <span>Level: {item.level}</span>
            </div>
            {item.isLocked ? (
              <p className="text-xs text-red-600 mt-2">
                Requires {item.pointsRequired} points to unlock
              </p>
            ) : (
              <button 
                onClick={() => handleStartLesson(item)}
                className="mt-2 flex items-center text-blue-600 hover:bg-blue-50 p-1 rounded"
              >
                <Play size={16} className="mr-1" /> Start Lesson
              </button>
            )}
          </div>
        </div>
      ))}

      <div className="bg-white rounded-lg shadow-md p-4 mt-4">
        <h3 className="font-bold mb-2 flex items-center">
          <Award className="mr-2 text-yellow-600" /> Available Badges
        </h3>
        <div className="grid grid-cols-3 gap-2">
          {availableBadges.map((badge, index) => (
            <div 
              key={index} 
              className={`flex flex-col items-center p-2 rounded ${
                userPoints >= badge.pointsRequired 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-gray-100 text-gray-500'
              }`}
            >
              {badge.icon}
              <span className="text-xs mt-1">{badge.name}</span>
              <span className="text-xs">{badge.pointsRequired} pts</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderHomeContent = () => (
    <>
      {/* Quick Stats */}
      <div className="bg-white rounded-lg shadow-md p-4 grid grid-cols-3 gap-2">
        <div className="text-center">
          <TrendingUp className="mx-auto text-green-600" />
          <p className="text-xs">Health Score</p>
          <p className="font-bold">{userProfile.financialHealthScore}</p>
        </div>
        <div className="text-center">
          <Target className="mx-auto text-blue-600" />
          <p className="text-xs">Savings Goal</p>
          <p className="font-bold">${userProfile.savingsGoal}</p>
        </div>
        <div className="text-center">
          <Book className="mx-auto text-purple-600" />
          <p className="text-xs">Learning Streak</p>
          <p className="font-bold">{userProfile.learningStreak} Days</p>
        </div>
      </div>

      {/* Community Impact */}
      <div className="bg-white rounded-lg shadow-md p-4">
        <h2 className="font-bold mb-2 flex items-center">
          <Users className="mr-2 text-blue-600" /> Community Impact
        </h2>
        <div className="grid grid-cols-3 gap-2 text-center">
          <div>
            <p className="text-sm">Referrals</p>
            <p className="font-bold">{communityData.referrals}</p>
          </div>
          <div>
            <p className="text-sm">Total Savings</p>
            <p className="font-bold">${communityData.totalSavings}</p>
          </div>
          <div>
            <p className="text-sm">Interest Earned</p>
            <p className="font-bold">${communityData.interestEarned}</p>
          </div>
        </div>
      </div>

      {/* Upcoming Events */}
      <div className="bg-white rounded-lg shadow-md p-4">
        <h2 className="font-bold mb-2 flex items-center">
          <Calendar className="mr-2 text-green-600" /> Upcoming Events
        </h2>
        {communityData.upcomingEvents.map((event, index) => (
          <div key={index} className="bg-gray-50 p-2 rounded mb-2">
            <div className="flex justify-between">
              <h3 className="font-semibold">{event.title}</h3>
              <MapPin size={16} className="text-red-500" />
            </div>
            <p className="text-xs text-gray-600">{event.date}</p>
            <p className="text-xs">{event.description}</p>
          </div>
        ))}
      </div>

      {/* Lending Opportunities */}
      <div className="bg-white rounded-lg shadow-md p-4">
        <h2 className="font-bold mb-2 flex items-center">
          <Gift className="mr-2 text-yellow-600" /> Community Lending
        </h2>
        {communityData.lendingOpportunities.map((opportunity, index) => (
          <div key={index} className="bg-green-50 p-2 rounded mb-2">
            <div className="flex justify-between">
              <h3 className="font-semibold">{opportunity.title}</h3>
              <DollarSign size={16} className="text-green-600" />
            </div>
            <div className="flex justify-between text-xs">
              <span>Max Amount: {opportunity.maxAmount}</span>
              <span>Interest: {opportunity.interestRate}</span>
            </div>
            <p className="text-xs text-gray-600">
              Available Slots: {opportunity.availableSlots}
            </p>
          </div>
        ))}
      </div>
    </>
  );

  const renderHelpContent = () => (
    <div>
      <h2 className="text-xl font-bold mb-4 flex items-center">
        <HelpCircle className="mr-2 text-green-600" /> Help & Support
      </h2>
      {[
        {
          title: 'FAQ',
          description: 'Answers to common questions',
          icon: <HelpCircle />
        },
        {
          title: 'Contact Support',
          description: 'Get help from our team',
          icon: <Users />
        },
        {
          title: 'Community Resources',
          description: 'Local financial support',
          icon: <MapPin />
        }
      ].map((item, index) => (
        <div key={index} className="bg-white rounded-lg shadow-md p-4 mb-3 flex items-center">
          <div className="bg-green-100 p-3 rounded-full mr-4">
            {item.icon}
          </div>
          <div className="flex-grow">
            <h3 className="font-semibold">{item.title}</h3>
            <p className="text-xs text-gray-600">{item.description}</p>
            <button className="mt-2 text-green-600">Learn More</button>
          </div>
        </div>
      ))}
    </div>
  );

  const renderSettingsContent = () => (
    <div>
      <h2 className="text-xl font-bold mb-4 flex items-center">
        <Settings className="mr-2 text-gray-600" /> App Settings
      </h2>
      <div className="bg-white rounded-lg shadow-md p-4 space-y-4">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="font-semibold">Language</h3>
            <p className="text-xs text-gray-600">Current: {language === 'en' ? 'English' : 'Spanish'}</p>
          </div>
          <button 
            onClick={() => setLanguage(language === 'en' ? 'es' : 'en')}
            className="bg-blue-100 px-3 py-1 rounded"
          >
            Switch
          </button>
        </div>
        <div className="flex justify-between items-center">
          <div>
            <h3 className="font-semibold">Notifications</h3>
            <p className="text-xs text-gray-600">Receive updates and alerts</p>
          </div>
          <button className="bg-green-100 px-3 py-1 rounded">
            Manage
          </button>
        </div>
        <div className="flex justify-between items-center">
          <div>
            <h3 className="font-semibold">Privacy</h3>
            <p className="text-xs text-gray-600">Manage your data and privacy</p>
          </div>
          <button className="bg-red-100 px-3 py-1 rounded">
            Review
          </button>
        </div>
      </div>
    </div>
  );

  return (
    <div className="bg-blue-50 h-screen flex flex-col">
      {/* Header */}
      <header className="bg-blue-600 text-white p-4 flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold flex items-center">
            <DollarSign className="mr-2" /> FinBright
          </h1>
          <p className="text-sm">Riverwood Community Financial Empowerment</p>
        </div>
        <div className="flex items-center">
          <button 
            onClick={() => setShowSettings(!showSettings)}
            className="mr-3"
          >
            <Settings size={24} />
          </button>
          <Award size={24} />
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-grow overflow-y-auto p-4 space-y-4">
        {!showSettings && activeTab === 'home' && renderHomeContent()}
        {!showSettings && activeTab === 'learn' && renderLearnContent()}
        {!showSettings && activeTab === 'community' && renderHelpContent()}
        {showSettings && renderSettingsContent()}
      </main>

      {/* Bottom Navigation */}
      {!showSettings && (
        <nav className="bg-white border-t flex justify-around p-3">
          <button 
            onClick={() => setActiveTab('home')} 
            className={`flex flex-col items-center ${activeTab === 'home' ? 'text-blue-600' : 'text-gray-500'}`}
          >
            <Home size={24} />
            <span className="text-xs">Home</span>
          </button>
          <button 
            onClick={() => setActiveTab('learn')} 
            className={`flex flex-col items-center ${activeTab === 'learn' ? 'text-blue-600' : 'text-gray-500'}`}
          >
            <Book size={24} />
            <span className="text-xs">Learn</span>
          </button>
          <button 
            onClick={() => setActiveTab('community')} 
            className={`flex flex-col items-center ${activeTab === 'community' ? 'text-blue-600' : 'text-gray-500'}`}
          >
            <Users size={24} />
            <span className="text-xs">Help</span>
          </button>
        </nav>
      )}
    </div>
  );
};

export default FinBrightCommunityApp;
