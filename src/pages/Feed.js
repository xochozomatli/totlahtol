import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Redirect } from 'react-router-dom'
import { HeaderBar, HeaderContentStart, HeaderContentEnd, HeaderTitle, HeaderButton, Form, Input, TextBox, Button, Logo, Card, LessonCard, CardTitle, Error } from "../components/FeedComponents"
import {ModalBackground, ModalBody, ModalTitle, ModalContent, ModalExit, TlahtolliBody, TlahtolliWord, TlahtolliHint} from "../components/ModalComponents"
import { useAuth, AuthContext } from '../context/auth'
import { useUser, UserContext } from '../context/user'
import { useLesson, LessonContext } from '../context/lesson'

function Header(){
    const { authToken, setAuthToken } = useAuth(null)
    const { userData, setUserData } = useUser(null)

    function deleteUser(){
        const bearer = "Bearer ".concat(authToken)
        axios.delete('http://localhost:5000/api/users/'+userData.id, { headers: { Authorization: bearer } })
    }

   return(
        <>
        <HeaderBar>
            <HeaderContentStart>
                <HeaderTitle>Totlahtol</HeaderTitle>
            </HeaderContentStart>
            <HeaderContentEnd>
                <HeaderButton onClick={e => {setAuthToken(null);setUserData(null)}}>
                    Sign Out
                </HeaderButton>
                <HeaderButton onClick={deleteUser}>
                    Delete Account
                </HeaderButton>
            </HeaderContentEnd>
        </HeaderBar>
        </>
    )
}

function LessonForm(){
    const [lessonTitle, setLessonTitle] = useState("")
    const [lessonText, setLessonText] = useState("")
    const { authToken, setAuthToken } = useAuth(null)
    const { userData, setUserData } = useUser(null)

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

    return(
        <>
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
        </>
    )
}

function Modal(props){
    const { lessonData, setLessonData } = useLesson()
    const [currentTlahtolli, setCurrentTlahtolli] = useState()
    const toggleShow = props.toggleShow
    console.log("Attempting modal rerender...")
    function activateTlahtolli(e){
        const word = e.target.innerText.toLowerCase().replace(/[^0-9a-z]/,'')
        const tlahtolli = lessonData.user_tlahtolli.find(obj => obj.word==word)
        setCurrentTlahtolli(tlahtolli)
        console.log(tlahtolli)
    }
    useEffect(()=>console.log("Modal Mounted----"))
    if (props.show){
        console.log("Rerender successful!")
        return(
            <>
                <ModalBackground>
                    <ModalBody>
                        <ModalExit onClick={e=>{toggleShow(false);setLessonData(null)}}>
                            <svg version="1.1" xmlns="http://www.w3.org/2000/svg" style={{height:'1.5rem',width:'1.5rem'}}>
                                <line x1="1" y1="22" 
                                    x2="22" y2="1" 
                                    stroke="black" 
                                    strokeWidth="2"/>
                                <line x1="1" y1="1" 
                                    x2="22" y2="22" 
                                    stroke="black" 
                                    strokeWidth="2"/>
                            </svg>
                        </ModalExit>
                        <ModalTitle>{lessonData.title}</ModalTitle>
                        <ModalContent>
                            {lessonData.content.split(/[\s\n]+/).map((word,index) =>
                            <Tlahtolli word={word.toLowerCase()}
                                       definition={lessonData.user_tlahtolli.find(obj=>obj.word===word.toLowerCase()) ? lessonData.user_tlahtolli.find(obj=>obj.word===word.toLowerCase()).definition : undefined}
                                       seen={lessonData.user_tlahtolli.map(entry=>entry.word).includes(word.toLowerCase()) ? true : false}
                                       active={currentTlahtolli===index}
                                       activate={setCurrentTlahtolli}
                                       key={index}
                                       index={index} />
                            )}
                        </ModalContent>
                    </ModalBody>
                </ModalBackground> 
            </>
        )
    } else {
        return ""
    }
}

function Tlahtolli(props) {
    const { lessonData } = useLesson()
    const { userData } = useUser()
    const { authToken } = useAuth()
    const [hintText, setHintText] = useState(props.definition)

     function submitNewDefinition(){
        const bearer = "Bearer ".concat(authToken)
        if (props.definition) {
            axios.put("http://localhost:5000/api/tlahtolli/"+props.word, {
                word: props.word,
                user_id: userData.id,
                definition: hintText,
                state: "tlahtolli"
            },
            {
                headers: { Authorization: bearer }
            }).then( e => { })
        } else {
            axios.post("http://localhost:5000/api/tlahtolli", {
                word: props.word,
                user_id: userData.id,
                definition: hintText,
                state: "tlahtolli"
            },
            {
                headers: { Authorization: bearer }
            }).then( e => { })
        }
    }   

    useEffect(()=>{
        // setHintText(props.definition)
    })
    return(
        <TlahtolliBody onMouseEnter={() => {props.activate(props.index)}}
                    onMouseLeave={() => {props.activate()}}
                    showHint={props.active}
                    seen={props.seen}>
            <TlahtolliWord>{props.word}</TlahtolliWord>
            <TlahtolliHint onSubmit={e=>{e.preventDefault(); submitNewDefinition(hintText)}}>
              <input value={hintText || ""} onChange={e=>setHintText(e.target.value)}/>
            </TlahtolliHint>
        </TlahtolliBody>
    )
}

// TODO: Change the name of Feed() to Home();
//       extract actual lesson feed fragment 
function Feed() {
    const [isError, setIsError] = useState(false);
    const [lessonsOnPage, setLessonsOnPage] = useState([])
    const perPage = 2
    const [lessonsLinks, setLessonsLinks] = useState(
        {
            "next": "/api/lessons?page=1&per_page="+perPage,
            "prev": null,
            "self": null
        })
    const [showModal, toggleShowModal] = useState(false)
    const { authToken, setAuthToken } = useAuth(null)
    const { userData, setUserData } = useUser(null)
    const { lessonData, setLessonData } = useLesson(null)
    const [ currentTlahtolli, setCurrentTlahtolli ] = useState(null)

    function handleLessonClick(e){
        const bearer = "Bearer ".concat(authToken)
        axios.get('http://localhost:5000/api/lessons/'+e.target.id.slice(6), {
            headers: { Authorization: bearer }
        }).then( result => {
            if (result.status==200){
                return result.data
            } else {
                setIsError(true)
                Promise.reject()
            }
        }).then( data => {
            setLessonData(data)
            console.log(data)
            toggleShowModal(true)
        }).catch( e => {
            setIsError(true)
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
            setLessonsLinks(data._links)
            let newLessons = data.items
            setLessonsOnPage([...lessonsOnPage, ...newLessons])
        }).catch( e => {
            setIsError(true)
        })
    }

    return (
        <div>
        <Header />
        <LessonForm />
            <div id="lessons">{ lessonsOnPage.map( lesson =>
                <LessonCard key={lesson.id} id={'lesson'+lesson.id} onClick={handleLessonClick}>
                    {lesson.title} by {lesson.author}
                </LessonCard>) }
            </div>
            <Card>
                <Button onClick={getLessonsPage}>Load Lessons</Button>
            </Card>
            <Modal show={showModal} toggleShow={toggleShowModal}/>
        </div>
    )
}

export default Feed