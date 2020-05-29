import React, { useState } from 'react'
import { BrowserRouter as Router, Link, Route } from 'react-router-dom'
import PrivateRoute from 'PrivateRoute'
import { AuthContext } from './context/auth'

function App() {
  const [authTokens, setAuthTokens] = useState()

  const setTokens = data => {
    localStorage.setItem("totlahtoltoken", JSON.stringify(data));
    setAuthTokens(data)
  }

  return (
    <AuthContext.Provider value={{ authTokens, setAuthTokens: setTokens }}>
      <Router>
        <div>
          <PrivateRoute exact path='/' component={Feed} />
          <Route path='/login' component={Landing} />
        </div>
      </Router>
    </AuthContext.Provider>
  );
}

export default App;
