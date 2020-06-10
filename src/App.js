import React, { useState } from 'react'
import { BrowserRouter as Router, Route } from 'react-router-dom'
import PrivateRoute from './PrivateRoute'
import { AuthContext } from './context/auth'
import { UserContext } from './context/user'
import Landing from './pages/Landing'
import Feed from './pages/Feed'

function App() {
  const [authToken, setAuthToken] = useState(localStorage.getItem('totlahtoltoken'))
  const [userData, setUserData] = useState(JSON.parse(localStorage.getItem('totlahtoluser')))

  const setToken = data => {
    if (data !== null){
      localStorage.setItem("totlahtoltoken", data)
    } else {
      localStorage.removeItem("totlahtoltoken")
    }
    setAuthToken(data)
  }

  const setUser = data => {
    if (data !== null){
      localStorage.setItem("totlahtoluser", JSON.stringify(data))
    } else {
      localStorage.removeItem("totlahtoluser")
    }
    setUserData(data)
  }

  return (
    <AuthContext.Provider value={{ authToken, setAuthToken: setToken }}>
      <UserContext.Provider value={{ userData, setUserData: setUser }}>
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
