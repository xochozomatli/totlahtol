import React, { useEffect, useState } from 'react'
import { Link, Redirect, useHistory, useRouteMatch } from 'react-router-dom'
import { secureRequest } from '../requestWrapper'
import { ModalBackground, ModalBody, ModalHeader, ModalTitle, TextBox, EditButton, DeleteButton, ModalContent, ModalExit } from "../style/ModalComponents"
import Tlahtolli from './Tlahtolli'
import { useAuth } from '../context/auth'
import { useUser } from '../context/user'

function Modal(props){
    console.log(props)
    const history = useHistory()
    const closeModal = e => {
        e.stopPropagation()
        history.push('/')
    }

    return(<ModalBackground>
                <ModalBody>
                    <ModalExit onClick={closeModal}>
                        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" style={{height:'1.5rem',width:'1.5rem'}}>
                            <line x1="1" y1="22" x2="22" y2="1" stroke="black" strokeWidth="2"/>
                            <line x1="1" y1="1" x2="22" y2="22" stroke="black" strokeWidth="2"/>
                        </svg>
                    </ModalExit>
                    <ModalHeader>
                        <ModalTitle>{props.title}</ModalTitle>
                        { props.headerButton && props.headerButton() }
                    </ModalHeader>
                    <ModalContent>{props.children}</ModalContent>
                </ModalBody>
            </ModalBackground>
    )
}

function LessonModal(props){
    const { authToken, setAuthToken } = useAuth()
    const { userData } = useUser()
    const [ lessonData, setLessonData ] = useState()
    const [ lessonText, setLessonText] = useState()
    const [isLoading, setIsLoading] = useState(false)
    const [isError, setIsError] = useState(false)
    const [reloadLessonData, setReloadLessonData] = useState(false)
    const history = useHistory()
    const match = useRouteMatch()
    const [confirmedDelete, setConfirmedDelete] = useState(false)
    console.log(match.params)
    console.log(lessonData)
    
    useEffect(() => {
        console.log("Entered useEffect in LessonModal")
        let didCancel=false;
        setIsLoading(true)
        const bearer = "Bearer ".concat(authToken.token)
        const requestConfig = {
            method: 'get',
            url: "http://localhost:5000/api/lessons/"+props.match.params.id,
            headers: { Authorization: bearer }
        }
        const succ = res => {
            if (!didCancel){
                setLessonData(res.data)
                setLessonText(res.data.content)
            }
            setIsLoading(false)
            setReloadLessonData(false)
        }
        const err = res => {
            let code = res.response!==undefined ? res.response.status : "no error code to see here, folks"
            console.log(code)
            setIsError(true)
        }
        const setter = setAuthToken
        secureRequest(requestConfig, succ, err, setter)

        return () => { console.log("modal unmounted during request; canceling; show lesson: "+props.match.params.id); didCancel=true }
    }, [reloadLessonData])

    if (!lessonData){
        if (isError){
            return <Modal title="Ooops :l">x_x looks like we had a problem fetching your lesson :(</Modal>
        }
        return null
    }
    console.log("isLoading: "+isLoading)
    if (isLoading){
        return(
            <Modal title="loading">
                Loading...
            </Modal>
        )
    }

    function updateLesson(){
        console.log(props)
        const bearer = "Bearer ".concat(authToken.token)
        const requestConfig = {
            method: 'put',
            url: "http://localhost:5000/api/lessons/"+match.params.id,
            data: {
                content: lessonText
            },
            headers: { Authorization: bearer }
        }
        const succ = res => {
            console.log("lessonData before: ", lessonData)
            setLessonData(res.data)
            setLessonText(res.data.content)
            console.log("lessonData after: ", res.data)
            history.goBack()
        }
        const err = res => {
            let code = res.response!==undefined ? res.response.status : "no error code to see here, folks"
            console.log(code)
            setIsError(true)
        }
        const setter = setAuthToken
        secureRequest(requestConfig, succ, err, setter)

    }

    function deleteLesson(){
        setConfirmedDelete(confirmedDelete ? false : true)
        if (!confirmedDelete){return null}
        console.log("this shouldn't run")
        const bearer = " Bearer ".concat(authToken.token)
        const requestConfig = {
            method: 'delete',
            url: "http://localhost:5000/api/lessons/"+match.params.id,
            headers: { Authorization: bearer }
        }
        const succ = res => {
            console.log(res)
            history.replace('/')
        }
        const err = res => {
            console.log(res)
        }
        const setter = setAuthToken
        secureRequest(requestConfig, succ, err, setter)
    }

    if (props.editing){
        const DeleteButton = () => <button onClick={deleteLesson}>{confirmedDelete ? "Are you sure?" : "Delete"}</button>
        return(
            <Modal title={lessonData.title} editing={props.editing} headerButton={DeleteButton} >
                <TextBox value={lessonText} onChange={e => { setLessonText(e.target.value) }}/>
                <button onClick={updateLesson}>Save</button>
                <button onClick={()=>{history.goBack()}}>Cancel</button>
            </Modal>
        )
    }

    const EditButton = () => <button><Link to={`${match.url}/edit`}>Edit</Link></button>
    return(
        <Modal title={lessonData.title} headerButton={userData.id===lessonData.author_id ? EditButton : false} >
            {lessonData.content.match(/\w+|[^\w\s]+/g).map((word,index) =>
            <Tlahtolli word={word} //TODO maybe expand these using object spread? Needs organization
                        definition={lessonData.user_tlahtolli.find(obj=>obj.word===word.toLowerCase()) ? lessonData.user_tlahtolli.find(obj=>obj.word===word.toLowerCase()).definition : undefined}
                        seen={lessonData.user_tlahtolli.map(entry=>entry.word).includes(word.toLowerCase()) ? true : false}
                        setReloadLessonData={setReloadLessonData}
                        key={index}
                        index={index} />
            )}
        </Modal>
    )
}

export default LessonModal