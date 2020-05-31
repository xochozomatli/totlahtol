import React, { useState } from 'react'
import axios from 'axios'
import { Redirect } from 'react-router-dom'
import { Card, Form, Input, Button, Error } from "../components/AuthForms"
import { useAuth } from '../context/auth'
import { useUser } from '../context/user'

function Landing(props) {
    const [isLoggedIn, setLoggedIn] = useState(false);
    const [isError, setIsError] = useState(false);
    const [email, setEmail] = useState("")
    const [signupUsername, setSignupUsername] = useState("");
    const [signupPassword, setSignupPassword] = useState("");
    const [loginUsername, setLoginUsername] = useState("");
    const [loginPassword, setLoginPassword] = useState("");
    const { setAuthTokens } = useAuth();
    const { setUserData } = useUser();
    //const referer = props.location.state.referer || '/';

    function postLogin() {
        axios.post("http://localhost:5000/api/tokens", {}, {
            auth: {
                username: loginUsername,
                password: loginPassword
            }
        }).then(result => {
            if (result.status === 200) {
                console.log(result.data.token)
                setAuthTokens(result.data);
                return result.data
            } else {
                setIsError(true)
                Promise.reject()
            }
        }).then(data => { 
            const bearer = "Bearer ".concat(data.token)
            return axios.get("http://localhost:5000/api/users/current/"+data.token, { headers: { Authorization: bearer } })
        }).then(result => {
            if (result.status === 200) {
                setUserData(result.data)
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
        axios.post("http://localhost:5000/api/users", {
        username: signupUsername,
        email: email,
        password: signupPassword
        }).then(result => {
        if (result.status === 201) {
            setAuthTokens({ 'token': result.data.token })
            delete result.data.token
            setUserData(result.data)
            setLoggedIn(true)
        } else {
            console.log('This is the first error catch')
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
        <div>
        <Card>
        <h1 style={{textAlign: 'center', color: 'white'}}>Totlahtol</h1>
            <Form>
                <Input
                type="username"
                value={loginUsername}
                onChange={e => {
                    setLoginUsername(e.target.value);
                }}
                placeholder="username"
                />
                <Input
                type="password"
                value={loginPassword}
                onChange={e => {
                    setLoginPassword(e.target.value);
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
                placeholder="email"
                />
                <Input
                type="username"
                value={signupUsername}
                onChange={e => {
                    setSignupUsername(e.target.value);
                }}
                placeholder="username"
                />
                <Input
                type="password"
                value={signupPassword}
                onChange={e => {
                    setSignupPassword(e.target.value);
                }}
                placeholder="password"
                />
                <Button onClick={postSignup}>Sign Up</Button>
            </Form>
                { isError &&<Error></Error> }
        </Card>
    </div>
    )
}

export default Landing