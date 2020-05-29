import React, { useState } from 'react'
import axios from 'axios'
import { Link, Redirect } from 'react-router-dom'
import { Card, Logo, Form, Input, Button, Error } from "../components/AuthForms"
import { useAuth } from './context/auth'
import { useUser } from './context/user'

function Landing(props) {
    const [isLoggedIn, setLoggedIn] = useState(false);
    const [isError, setIsError] = useState(false);
    const [email, setEmail] = useState("")
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
        // The response to posting a new user is the user object itself as per REST guidlines
        // The backend now sends the user object with an added "token" attribute to avoid having to make two requests
        axios.post("https://localhost:5000/api/users", {
        username,
        email,
        password
        }).then(result => {
        if (result.status === 201) {
            setAuthTokens({ 'token': result.data.token })
            delete result.data.token
            setCurrentUser(result.data)
            setLoggedIn(true)
        } else {
            setIsError(true)
        }
        }).catch(e => {
        setIsError(true);
        });
    }

    if (isLoggedIn) {
        return <Redirect to='/' />; // Hardcoded redirect to home, was "to={referer}"
    }

    return (
        <Card>
            <Form>
                <Input
                type="username"
                value={username}
                onChange={e => {
                    setUserName(e.target.value);
                }}
                placeholder="username"
                />
                <Input
                type="password"
                value={password}
                onChange={e => {
                    setPassword(e.target.value);
                }}
                placeholder="password"
                />
                <Button onClick={postLogin}>Sign In</Button>
            </Form>
                { isError &&<Error>The username or password provided were incorrect!</Error> }
        </Card>
        <Card>
            <Form>
                <Input
                type="email"
                value={email}
                onChange={e => {
                    setEmail(e.target.value);
                }}
                placeholder="username"
                />
                <Input
                type="username"
                value={username}
                onChange={e => {
                    setUsername(e.target.value);
                }}
                placeholder="username"
                />
                <Input
                type="password"
                value={password}
                onChange={e => {
                    setPassword(e.target.value);
                }}
                placeholder="password"
                />
                <Button onClick={postSignup}>Sign Up</Button>
            </Form>
                { isError &&<Error></Error> }
        </Card>

    )
}