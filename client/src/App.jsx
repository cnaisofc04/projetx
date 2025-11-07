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
    // Nettoyer le localStorage des anciennes données
    try {
      const savedUser = localStorage.getItem('onetwo_user');
      if (savedUser) {
        const parsedUser = JSON.parse(savedUser);
        setUser(parsedUser);
        setCurrentScreen('main');
      }

      // Nettoyer les clés inutiles
      const keysToRemove = [];
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key && key !== 'onetwo_user' && key.includes('temp')) {
          keysToRemove.push(key);
        }
      }
      keysToRemove.forEach(key => localStorage.removeItem(key));
    } catch (error) {
      console.error('Erreur de chargement:', error);
      // Vider complètement le localStorage en cas d'erreur
      localStorage.clear();
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

            // Nettoyer le localStorage avant de sauvegarder
            try {
              // Supprimer les anciennes données inutiles
              localStorage.removeItem('tempUserData');
              localStorage.removeItem('tempProfileData');

              // Sauvegarder uniquement les données essentielles
              const essentialUser = {
                ...completeUser,
                profile: {
                  ...data, // Utiliser 'data' car il contient les nouvelles informations du profil
                  // Réduire la taille des photos en ne gardant que les URLs
                  photos: data.photos?.slice(0, 6) || []
                }
              };

              localStorage.setItem('onetwo_user', JSON.stringify(essentialUser));
              setCurrentScreen('main');
            } catch (error) {
              console.error('Erreur de sauvegarde:', error);
              // En cas d'erreur, continuer quand même sans localStorage
              alert('⚠️ Impossible de sauvegarder toutes les données. Vous pourrez continuer mais vos données seront perdues au rechargement.');
              setCurrentScreen('main');
            }
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