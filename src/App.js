import React, { useState } from 'react'
import { BrowserRouter as Router, Link, Route } from 'react-router-dom'
import PrivateRoute from './PrivateRoute'
import { AuthContext } from './context/auth'
import { UserContext } from './context/user'
import Landing from './pages/Landing'
import Feed from './pages/Feed'

function App() {
  const [authTokens, setAuthTokens] = useState()
  const [userData, setUserData] = useState()

  const setTokens = data => {
    localStorage.setItem("totlahtoltoken", JSON.stringify(data));
    setAuthTokens(data)
  }

  return (
    <AuthContext.Provider value={{ authTokens, setAuthTokens: setTokens }}>
      <UserContext.Provider value={{ userData, setUserdata: setUserData }}>
      <Router>
        <div>
          <PrivateRoute exact path='/' component={Feed} />
          <Route path='/login' component={Landing} />
        </div>
      </Router>
      </UserContext.Provider>
    </AuthContext.Provider>
  );
}

export default App;
