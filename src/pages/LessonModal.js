import React, { useEffect, useState } from 'react'
import { secureRequest } from '../requestWrapper'
import { useHistory } from 'react-router-dom'
import { ModalBackground, ModalBody, ModalTitle, ModalContent, ModalExit } from "../style/ModalComponents"
import Tlahtolli from './Tlahtolli'
import { useAuth } from '../context/auth'

function Modal(props){
    const history = useHistory()
    const closeModal = e => {
        e.stopPropagation()
        history.goBack()
    }

    return(<ModalBackground>
                <ModalBody>
                    <ModalExit onClick={closeModal}>
                        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" style={{height:'1.5rem',width:'1.5rem'}}>
                            <line x1="1" y1="22" x2="22" y2="1" stroke="black" strokeWidth="2"/>
                            <line x1="1" y1="1" x2="22" y2="22" stroke="black" strokeWidth="2"/>
                        </svg>
                    </ModalExit>
                    <ModalTitle>{props.title}</ModalTitle>
                    <ModalContent>{props.children}</ModalContent>
                </ModalBody>
            </ModalBackground>
    )
}

function LessonModal(props){
    const { authToken, setAuthToken } = useAuth()
    const [ lessonData, setLessonData ] = useState()
    const [currentTlahtolli, setCurrentTlahtolli] = useState()
    const [isLoading, setIsLoading] = useState(false)
    const [isError, setIsError] = useState(false)
    const [reloadLessonData, setReloadLessonData] = useState(false)
    console.log(props.match.params)
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
    return(
        <Modal title={lessonData.title}>
            {lessonData.content.match(/\w+|[^\w\s]+/g).map((word,index) =>
            <Tlahtolli word={word} //TODO maybe expand these using object spread? Needs organization
                        definition={lessonData.user_tlahtolli.find(obj=>obj.word===word.toLowerCase()) ? lessonData.user_tlahtolli.find(obj=>obj.word===word.toLowerCase()).definition : undefined}
                        seen={lessonData.user_tlahtolli.map(entry=>entry.word).includes(word.toLowerCase()) ? true : false}
                        active={currentTlahtolli===index}
                        activate={setCurrentTlahtolli}
                        setReloadLessonData={setReloadLessonData}
                        key={index}
                        index={index} />
            )}
        </Modal>
    )
}

export default LessonModal