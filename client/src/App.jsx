import { useState, useEffect } from 'react';
import './App.css';
import WelcomeScreen from './components/WelcomeScreen';
import AuthChoice from './components/AuthChoice';
import SignupForm from './components/SignupForm';
import LoginForm from './components/LoginForm';
import PsychologyQuestions from './components/PsychologyQuestions';
import RelationshipType from './components/RelationshipType';
import SexualOrientation from './components/SexualOrientation';
import DetailedPreferences from './components/DetailedPreferences';
import BeardPreference from './components/BeardPreference';
import PrivacyZone from './components/PrivacyZone';
import ProfileSetup from './components/ProfileSetup';
import MainApp from './components/MainApp';

function App() {
  const [currentScreen, setCurrentScreen] = useState('welcome');
  const [user, setUser] = useState(null);

  useEffect(() => {
    const savedUser = localStorage.getItem('onetwo_user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
      setCurrentScreen('main');
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('onetwo_user');
    setUser(null);
    setCurrentScreen('welcome');
  };

  const renderScreen = () => {
    switch (currentScreen) {
      case 'welcome':
        return <WelcomeScreen onContinue={() => setCurrentScreen('auth-choice')} />;
      case 'auth-choice':
        return <AuthChoice 
          onSignup={() => setCurrentScreen('signup')} 
          onLogin={() => setCurrentScreen('login')} 
        />;
      case 'signup':
        return <SignupForm onNext={(userData) => {
          setUser(userData);
          setCurrentScreen('psychology');
        }} />;
      case 'login':
        return <LoginForm onLogin={(userData) => {
          setUser(userData);
          setCurrentScreen('main');
        }} onBack={() => setCurrentScreen('auth-choice')} />;
      case 'psychology':
        return <PsychologyQuestions 
          user={user}
          onNext={(data) => {
            setUser({...user, ...data});
            setCurrentScreen('relationship-type');
          }} 
        />;
      case 'relationship-type':
        return <RelationshipType 
          user={user}
          onNext={(data) => {
            setUser({...user, ...data});
            setCurrentScreen('sexual-orientation');
          }} 
        />;
      case 'sexual-orientation':
        return <SexualOrientation 
          user={user}
          onNext={(data) => {
            setUser({...user, ...data});
            setCurrentScreen('detailed-preferences');
          }} 
        />;
      case 'detailed-preferences':
        return <DetailedPreferences 
          user={user}
          onNext={(data) => {
            setUser({...user, ...data});
            if (user?.gender === 'woman') {
              setCurrentScreen('beard-preference');
            } else {
              setCurrentScreen('privacy-zone');
            }
          }} 
        />;
      case 'beard-preference':
        return <BeardPreference 
          user={user}
          onNext={(data) => {
            setUser({...user, ...data});
            setCurrentScreen('privacy-zone');
          }} 
        />;
      case 'privacy-zone':
        return <PrivacyZone 
          user={user}
          onNext={(data) => {
            setUser({...user, ...data});
            setCurrentScreen('profile-setup');
          }} 
        />;
      case 'profile-setup':
        return <ProfileSetup 
          user={user}
          onComplete={(data) => {
            const completeUser = {...user, ...data};
            setUser(completeUser);
            localStorage.setItem('onetwo_user', JSON.stringify(completeUser));
            setCurrentScreen('main');
          }} 
        />;
      case 'main':
        return <MainApp user={user} onLogout={handleLogout} />;
      default:
        return <WelcomeScreen onContinue={() => setCurrentScreen('auth-choice')} />;
    }
  };

  return (
    <div className="App">
      {renderScreen()}
    </div>
  );
}

export default App;
