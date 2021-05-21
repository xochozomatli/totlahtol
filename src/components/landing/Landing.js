import React, { useState } from 'react'
import axios from 'axios'
import { Redirect } from 'react-router-dom'
import { Card, Form, Input, Button, Success, Error } from "./LandingStyles"
import { useAuth } from '../../context/auth'
import { useUser } from '../../context/user'

function Landing() {
    const { setAuthToken } = useAuth();
    const { userData, setUserData } = useUser();
    const [isError, setIsError] = useState(false);
    const [isSuccess, setIsSuccess] = useState(false);
    const [email, setEmail] = useState("")
    const [signupUsername, setSignupUsername] = useState("");
    const [signupPassword, setSignupPassword] = useState("");
    const [loginUsername, setLoginUsername] = useState("");
    const [loginPassword, setLoginPassword] = useState("");
    function postLogin() {
        axios.post("http://localhost:5000/api/tokens", {}, {
            auth: {
                username: loginUsername,
                password: loginPassword
            }, withCredentials: true
        }).then(result => {
            if (result.status === 200) {
                console.log(result.data)
                setAuthToken(result.data);
                return result.data
            } else {
                setIsError(true)
                Promise.reject()
            }
        }).then(data => { 
            const bearer = "Bearer ".concat(data.token)
            return axios.get("http://localhost:5000/api/users/current", { headers: { Authorization: bearer } })
        }).then(result => {
            if (result.status === 200) {
                setUserData(result.data)
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
            setIsSuccess(true)
        } else {
            console.log('This is the first error catch')
            setIsError(true)
        }
        }).catch(e => {
        setIsError(true);
        });
    }

    if (userData) { 
        return <Redirect to='/' /> 
    }

    return (
        <div>
        <Card>
        <h1 style={{textAlign: 'center', color: 'white'}}>Totlahtol</h1>
            <Form>
                <Input
                type="username"
	        id="login-username"
                value={loginUsername}
                onChange={e => { setLoginUsername(e.target.value) }}
                onKeyDown={e => { if(e.key==='Enter'){postLogin()} }}
                placeholder="username"
                />
                <Input
                type="password"
	        id="login-password"
                value={loginPassword}
                onChange={e => { setLoginPassword(e.target.value) }}
                onKeyDown={e => { if(e.key==='Enter'){postLogin()} }}
                placeholder="password"
                />
                <Button onClick={postLogin}>Sign In</Button>
            </Form>
                { isError &&<Error className='error'>The username or password provided were incorrect!</Error> }
            <Form>
                <Input
                type="email"
	        id="register-email"
                value={email}
                onChange={e => { setEmail(e.target.value) }}
                onKeyDown={e => { if(e.key==='Enter'){postSignup()} }}
                placeholder="email"
                />
                <Input
                type="username"
	        id="register-username"
                value={signupUsername}
                onChange={e => { setSignupUsername(e.target.value) }}
                onKeyDown={e => { if(e.key==='Enter'){postSignup()} }}
                placeholder="username"
                />
                <Input
                type="password"
	        id="register-password"
                value={signupPassword}
                onChange={e => { setSignupPassword(e.target.value) }}
                onKeyDown={e => { if(e.key==='Enter'){postSignup()} }}
                placeholder="password"
                />
                <Button onClick={postSignup}>Sign Up</Button>
            </Form>
                { isSuccess &&<Success className='success'>Thanks for signing up! Check your email to verify your account.</Success> }
                { isError &&<Error ></Error> }
        </Card>
    </div>
    )
}

export default Landing
