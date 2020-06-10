import React, { useState } from 'react'
import axios from 'axios'
import { Redirect } from 'react-router-dom'
import { Header, HeaderContentStart, HeaderContentEnd, HeaderTitle, HeaderButton, Form, Input, TextBox, Button, Logo, Card, CardTitle, Error } from "../components/FeedComponents"
import { useAuth, AuthContext } from '../context/auth'
import { useUser, UserContext } from '../context/user'


function Feed() {
    const [isError, setIsError] = useState(false);
    const [lessonTitle, setLessonTitle] = useState("")
    const [lessonText, setLessonText] = useState("")
    const [lessonsOnPage, setLessonsOnPage] = useState([])
    const perPage = 2
    const [lessonsLinks, setLessonsLinks] = useState(
        {
            "next": "/api/lessons?page=1&per_page="+perPage,
            "prev": null,
            "self": null
        })
    const { authToken, setAuthToken } = useAuth()
    const { userData, setUserData } = useUser()

    console.log(lessonTitle)

    function deleteUser(){
        const bearer = "Bearer ".concat(authToken)
        console.log(bearer)

        axios.delete('http://localhost:5000/api/users/'+userData.id, { headers: { Authorization: bearer } })
    }

    function createLesson(){
        const bearer = "Bearer ".concat(authToken)

        axios.post("http://localhost:5000/api/lessons", {
            title: lessonTitle,
            content: lessonText,
            author_id: userData.id
        },
        {
            headers: { Authorization: bearer }
        }).then( e => {
            setLessonTitle("")
            setLessonText("")
        })
    }

    function getLessonsPage(){
        axios.get('http://localhost:5000'+lessonsLinks.next
        ).then(result => {
            if (result.status===200){
                return result.data
            } else {
                setIsError(true)
                Promise.reject()
            }
        }).then( data => {
            console.log(data)
            setLessonsLinks(data._links)
            let newLessons = data.items
            console.log(newLessons)
            setLessonsOnPage([...lessonsOnPage, ...newLessons])
        }).catch( e => {
            setIsError(true)
        })
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
                    value={lessonTitle}
                    onChange={e => {
                        setLessonTitle(e.target.value)
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
                    <Button onClick={createLesson}>Share</Button>
                </Form>
            </Card>
            <div id="lessons">{ lessonsOnPage.map( lesson =>
                <Card>
                    <span>{lesson.title} by {lesson.author}</span>
                </Card>) }
            </div>
            <Card>
                <Button onClick={getLessonsPage}>Load Lessons</Button>
            </Card>
        </div>
    )
}

export default Feed