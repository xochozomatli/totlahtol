import React, { useState } from 'react'
import axios from 'axios'
import { Redirect } from 'react-router-dom'
import { Header, Card, CardTitle, Form, Input, TextBox, Button, Error } from "../components/FeedComponents"
import { useAuth } from '../context/auth'
import { useUser } from '../context/user'


function Feed() {
    const [title, setTitle] = useState("")
    const [lessonText, setLessonText] = useState("")

    return (
        <div>
            <Header></Header>
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