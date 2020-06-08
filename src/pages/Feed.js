import React, { useState } from 'react'
import axios from 'axios'
import { Redirect } from 'react-router-dom'
import { Header, HeaderContentStart, HeaderContentEnd, HeaderTitle, HeaderButton, Form, Input, TextBox, Button, Logo, Card, CardTitle, Error } from "../components/FeedComponents"
import { useAuth, AuthContext } from '../context/auth'
import { useUser, UserContext } from '../context/user'


function Feed() {
    const [title, setTitle] = useState("")
    const [lessonText, setLessonText] = useState("")
    const { authToken, setAuthToken } = useAuth()
    const { userData, setUserData } = useUser()

    console.log(authToken)
    console.log(useUser())

    function deleteUser(){
        const bearer = "Bearer ".concat(authToken)
        console.log(bearer)

        axios.delete('http://localhost:5000/api/users/'+userData.id, { headers: { Authorization: bearer } })
    }

    return (
        <div>
            <Header>
                <HeaderContentStart>
                    <HeaderTitle>Totlahtol</HeaderTitle>
                </HeaderContentStart>
                <HeaderContentEnd>
                    <HeaderButton onClick={e => {setAuthToken(null);setUserData(null)}}>Sign Out</HeaderButton>
                    <HeaderButton onClick={deleteUser}>
                        Delete Account
                    </HeaderButton>
                </HeaderContentEnd>
            </Header>
            <CardTitle>Create Lesson</CardTitle>

            <Card>
                <Form>
                    <Input
                    type="title"
                    value={title}
                    onChange={e => {
                        setTitle(e.target.value)
                    }}
                    placeholder="What do you want to call your lesson?"
                    />
                    <TextBox
                    type="lessontext"
                    value={lessonText}
                    onChange={e => {
                        setLessonText(e.target.value)
                    }}
                    placeholder="Enter your lesson's text here"
                    />
                    <Button onClick={e => {console.log('lesson shared!')}}>Share</Button>
                </Form>
            </Card>
        </div>
    )
}

export default Feed