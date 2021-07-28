import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import PrivateRoute from './PrivateRoute'
import { AuthContext } from './context/auth'
import { UserContext } from './context/user'
import Landing from './components/landing/Landing'
import Home from './components/home/Home'

function App() {
  const [authToken, setAuthToken] = useState(null)
  const [userData, setUserData] = useState(JSON.parse(localStorage.getItem('totlahtoluser')))
  const [loadingState, setLoadingState] = useState(null)

  const setUser = data => {
    if (data !== null){
	console.log('Data is NOT null')
        if (localStorage.getItem("totlahtoluser") !== null){
	    console.log('totlahtoluser is NOT null')
	    let oldData = JSON.parse(localStorage.getItem("totlahtoluser"))
	    if (oldData.id === data.id){
	        console.log('User ID is the same')
	        let newData = oldData
	        for (const key in data){
	            newData[key] = data[key]
	        }
	        localStorage.setItem("totlahtoluser", JSON.stringify(newData))
	        setUserData(newData)
            } else {
	        console.log('User ID is the NOT same')
                localStorage.setItem("totlahtoluser", JSON.stringify(data))
	        setUserData(data)
	    }
	} else {
	    console.log("totlahtoluser is null")
	    localStorage.setItem("totlahtoluser", JSON.stringify(data))
	    setUserData(data)
	}
    } else {
	console.log("Data is null")
        localStorage.removeItem("totlahtoluser")
	setUserData(null)
    }
  }

  useEffect(()=>{
    setLoadingState(true)
    axios.get('http://dev.localhost:5000/api/refresh', {withCredentials: true})
      .then(res=>{setAuthToken(res.data);setLoadingState(false)})
      .catch(err=>{console.log("valio verga");
    setLoadingState(false)
  })
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
          <Router>
            <Switch>
              <Route path='/login' component={Landing} />
              <PrivateRoute path='/' component={Home} />
            </Switch>
          </Router>
      </UserContext.Provider>
    </AuthContext.Provider>
  );
}

export default App;
