import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import PrivateRoute from './PrivateRoute'
import { AuthContext } from './context/auth'
import { UserContext } from './context/user'
import { LessonContext } from './context/lesson'
import Landing from './pages/Landing'
import Feed from './pages/Feed'

function App() {
  const [authToken, setAuthToken] = useState(null)
  const [userData, setUserData] = useState(JSON.parse(localStorage.getItem('totlahtoluser')))
  const [lessonData, setLesson] = useState(null)
  const [loadingState, setLoadingState] = useState(null)

  const setUser = data => {
    if (data !== null){
      localStorage.setItem("totlahtoluser", JSON.stringify(data))
    } else {
      localStorage.removeItem("totlahtoluser")
    }
    setUserData(data)
  }
  console.log(authToken)

  useEffect(()=>{
    setLoadingState(true)
    axios.get('http://localhost:5000/api/refresh', {withCredentials: true}).then(res=>{setAuthToken(res.data);setLoadingState(false)}).catch(err=>{console.log("valio verga");setLoadingState(false)})
  },[])

  if (loadingState===null){
    return "Initializing..."
  }

  if (loadingState===true){
    return "Loading..."
  }


  return (
    <AuthContext.Provider value={{ authToken, setAuthToken}}>
      <UserContext.Provider value={{ userData, setUserData: setUser }}>
        <LessonContext.Provider value={{ lessonData, setLessonData: setLesson }}>
          <Router>
            <Switch>
              <PrivateRoute exact path='/' component={Feed} />
              <Route path='/login' component={Landing} />
            </Switch>
          </Router>
        </LessonContext.Provider>
      </UserContext.Provider>
    </AuthContext.Provider>
  );
}

export default App;
