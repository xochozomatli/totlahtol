import React from 'react'
import axios from 'axios'
import { Link, Redirect } from 'react-router-dom'
import { Card, Logo, Form, Input, Button, Error } from "../components/AuthForms"
import { useAuth } from './context/auth'
import { useUser } from './context/user'

function Landing(props) {
    const [isLoggedIn, setLoggedIn] = useState(false);
    const [isError, setIsError] = useState(false);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const { setAuthTokens } = useAuth();
    const { setCurrentUser } = useUser();
    //const referer = props.location.state.referer || '/';

    function postLogin() {
        axios.post("https://localhost:5000/api/tokens", {
        username,
        password
        }).then(result => {
            if (result.status === 200) {
                setAuthTokens(result.data);
                return result.data
            } else {
                setIsError(true)
                Promise.reject()
            }
        }).then(token => { 
            axios.get("https://localhost:5000/api/users/current/"+token)
        }).then(result => {
            if (result.status === 200) {
                setCurrentUser(result.data)
                setLoggedIn(true);
            } else {
                setIsError(true)
            }
        }).catch(e => {
        setIsError(true);
        });
    }

    function postSignup() {
        axios.post("https://localhost:5000/api/users", {
        username,
        email,
        password
        }).then(result => {
        if (result.status === 201) {
            // response data is the user object itself
            // we should do something with it
            setLoggedIn(true);
        } else {
            setIsError(true);
        }
        }).catch(e => {
        setIsError(true);
        });
    }

    if (isLoggedIn) {
        return <Redirect to='/' />; // Hardcoded redirect to home, was "to={referer}"
    }

  return ()
}