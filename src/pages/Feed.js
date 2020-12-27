import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { secureRequest } from '../requestWrapper'
import { Redirect } from 'react-router-dom'
import { HeaderBar, HeaderContentStart, HeaderContentEnd, HeaderTitle, HeaderButton, Form, Input, TextBox, Button, Logo, Card, LessonCard, CardTitle, Error } from "../components/FeedComponents"
import {ModalBackground, ModalBody, ModalTitle, ModalContent, ModalExit, TlahtolliBody, TlahtolliWord, TlahtolliHint} from "../components/ModalComponents"
import { useAuth, AuthContext } from '../context/auth'
import { useUser, UserContext } from '../context/user'
import { useLesson, LessonContext } from '../context/lesson'

function Header(){
    const { authToken, setAuthToken } = useAuth()
    const { userData, setUserData } = useUser()

    function deauthUser(){
        const bearer = "Bearer ".concat(authToken.token)
        const requestConfig = {
            method: 'put',
            url: "http://localhost:5000/api/users/"+userData.id,
            data: { action: 'deauth' },
            headers: { Authorization: bearer }
        }
        const succ = res => {setAuthToken('');setUserData('');console.log(authToken)}
        const err = res => {console.log(res)}
        const setter = setAuthToken
        secureRequest(requestConfig, succ, err, setter)

    }

    function deleteUser(){
        const bearer = "Bearer ".concat(authToken.token)
        axios.delete('http://localhost:5000/api/users/'+userData.id, { headers: { Authorization: bearer } })
        const requestConfig = {
            method: 'delete',
            url: "http://localhost:5000/api/users/"+userData.id,
            headers: { Authorization: bearer }
        }
        const succ = res => {setAuthToken(null);setUserData(null)}
        const err = res => {console.log(res)}
        const setter = setAuthToken
        secureRequest(requestConfig, succ, err, setter)
    }

   return(
        <>
        <HeaderBar>
            <HeaderContentStart>
                <HeaderTitle>Totlahtol</HeaderTitle>
            </HeaderContentStart>
            <HeaderContentEnd>
                <HeaderButton onClick={deauthUser}>
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
    const { userData } = useUser(null)

    function createLesson(){
        const bearer = "Bearer ".concat(authToken.token)
        const requestConfig = {
            method: 'post',
            url: "http://localhost:5000/api/lessons",
            data: {
                title: lessonTitle,
                content: lessonText,
                author_id: userData.id
            },
            headers: { Authorization: bearer }
        }
        const succ = res => { setLessonTitle(""); setLessonText("") }
        const err = res => {console.log(res)}
        const setter = setAuthToken
        secureRequest(requestConfig, succ, err, setter)
        // const bearer = "Bearer ".concat(authToken.token)
        // axios.post("http://localhost:5000/api/lessons", {
        //     title: lessonTitle,
        //     content: lessonText,
        //     author_id: userData.id
        // },
        // {
        //     headers: { Authorization: bearer }
        // }).then( e => {
        //     setLessonTitle("")
        //     setLessonText("")
        // })
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
    const { authToken, setAuthToken } = useAuth()
    const { lessonData, setLessonData } = useLesson()
    const [currentTlahtolli, setCurrentTlahtolli] = useState()
    const [isLoading, setIsLoading] = useState(false)
    const [isError, setIsError] = useState(false)
    const [reloadLessonData, setReloadLessonData] = useState(false)
    
    useEffect(() => {
        let didCancel=false;
        setIsLoading(true)
        const bearer = "Bearer ".concat(authToken.token)
        axios.get('http://localhost:5000/api/lessons/'+props.lesson,
                { headers: { Authorization: bearer },
                validateStatus: (status) => (status >= 200 && status<300) || status===401}
        ).then( result => {
            if (result.status==200){
                return result.data
            } else {
                console.log('i guess it was 401...')
            }
        }).then( data => {
            if (!didCancel) {
                setLessonData(data)
                setIsLoading(false)
                console.log(data)
                setReloadLessonData(false)
            }
        }).catch( e => {
            let code = e.response!==undefined ? e.response.status : "nothing to see here, folks"
            setIsError(true)
        })

        return () => { console.log("modal unmounted during request; canceling; show lesson: "+props.lesson); didCancel=true }

    }, [props.lesson, reloadLessonData])
    if (!props.lesson){
        return null
    }
    console.log("isLoading: "+isLoading)
    if (isLoading){
        return(
            <>
            <ModalBackground>
                <ModalBody>
                    <ModalExit onClick={e=>{props.setLesson(null);setLessonData(null)}}>
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
                    <ModalTitle>Loading...</ModalTitle>
                    <ModalContent>
                        Loading...
                    </ModalContent>
                </ModalBody>
            </ModalBackground> 
            </>
        )
    }
    return(
        <>
            <ModalBackground>
                <ModalBody>
                    <ModalExit onClick={e=>{props.setLesson(null);setLessonData(null)}}>
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
                        <Tlahtolli word={word.toLowerCase()} //TODO maybe expand these using object spread? Needs organization
                                    definition={lessonData.user_tlahtolli.find(obj=>obj.word===word.toLowerCase()) ? lessonData.user_tlahtolli.find(obj=>obj.word===word.toLowerCase()).definition : undefined}
                                    seen={lessonData.user_tlahtolli.map(entry=>entry.word).includes(word.toLowerCase()) ? true : false}
                                    active={currentTlahtolli===index}
                                    activate={setCurrentTlahtolli}
                                    setReloadLessonData={setReloadLessonData}
                                    key={index}
                                    index={index} />
                        )}
                    </ModalContent>
                </ModalBody>
            </ModalBackground> 
        </>
    )
}

function Tlahtolli(props) {
    const { userData } = useUser()
    const { authToken } = useAuth()
    const [hintText, setHintText] = useState(props.definition || "")

     function submitNewDefinition(){
        const bearer = "Bearer ".concat(authToken.token)
        if (props.definition) {
            axios.put("http://localhost:5000/api/tlahtolli/"+props.word, {
                word: props.word,
                user_id: userData.id,
                definition: hintText,
                state: "tlahtolli"
            },
            {
                headers: { Authorization: bearer }
            }).then( e => { props.setReloadLessonData(true) })
        } else {
            axios.post("http://localhost:5000/api/tlahtolli", {
                word: props.word,
                user_id: userData.id,
                definition: hintText,
                state: "tlahtolli"
            },
            {
                headers: { Authorization: bearer }
            }).then( e => { props.setReloadLessonData(true) })
        }
    }   

    return(
        <TlahtolliBody onMouseEnter={() => {props.activate(props.index)}}
                    onMouseLeave={() => {props.activate()}}
                    showHint={props.active}
                    seen={props.seen}>
            <TlahtolliWord>{props.word}</TlahtolliWord>
            <TlahtolliHint onSubmit={e=>{e.preventDefault(); submitNewDefinition(hintText)}}>
              <input value={hintText} onChange={e=>setHintText(e.target.value)}/>
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
    const { authToken, setAuthToken } = useAuth(null)
    const { userData, setUserData } = useUser(null)
    const [ currentTlahtolli, setCurrentTlahtolli ] = useState(null)
    const [ currentLesson, setCurrentLesson ] = useState(null)

    function handleLessonClick(e){
        // axios.get('http://localhost:5000/api/refresh',{withCredentials: true}).then(res=>{console.log('Success!')}).catch(e=>{console.log(e.response)})
        setCurrentLesson(e.target.id.slice(6))
        console.log("current lesson set: "+currentLesson)
    }

    function getLessonsPage(){//TODO call this from within useEffect()
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
            {/* TODO remove this button and call getLessonsPage from useEffect() */}
                <Button onClick={getLessonsPage}>Load Lessons</Button>
            </Card>
            <Modal lesson={currentLesson} setLesson={setCurrentLesson}/>
        </div>
    )
}

export default Feed