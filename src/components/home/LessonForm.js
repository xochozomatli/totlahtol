import React, { useState } from 'react'
import { secureRequest } from '../../requestWrapper'
import { useAuth} from '../../context/auth'
import { useUser } from '../../context/user'
import { Input, TextBox, Button, Card, CardTitle, Form } from "./HomeStyles"

function LessonForm(props){
    const [lessonTitle, setLessonTitle] = useState("")
    const [lessonText, setLessonText] = useState("")
    const { authToken, setAuthToken } = useAuth(null)
    const { userData } = useUser(null)
    const { lessonsOnPage, setLessonsOnPage } = props

    function createLesson(){
        const bearer = "Bearer ".concat(authToken.token)
        const requestConfig = {
            method: 'post',
            url: "http://dev.localhost:5000/api/lessons",
            data: {
                title: lessonTitle,
                content: lessonText,
                author_id: userData.id
            },
            headers: { Authorization: bearer }
        }
        const succ = res => { setLessonTitle(""); setLessonText(""); setLessonsOnPage([res.data,...lessonsOnPage]).then(console.log(lessonsOnPage)) }
        const err = res => {console.log(res)}
        const setter = setAuthToken
        secureRequest(requestConfig, succ, err, setter)
    }

    return(
        <>
            <CardTitle>Create Lesson</CardTitle>
            <Card>
                <Form>
                    <Input
	            id="new-lesson-title"
                    type="title"
                    value={lessonTitle}
                    onChange={e => {
                        setLessonTitle(e.target.value)
                    }}
                    placeholder="What do you want to call your lesson?"
                    />
                    <TextBox
	            id="new-lesson-textarea"
                    type="lessontext"
                    value={lessonText}
                    onChange={e => {
                        setLessonText(e.target.value)
                    }}
                    placeholder="Enter your lesson's text here"
                    />
                    <Button id="new-lesson-share-button" onClick={createLesson}>Share</Button>
                </Form>
            </Card>
        </>
    )
}

export default LessonForm
