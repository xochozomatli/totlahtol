import React, { useEffect, useState, useRef } from 'react'
import { Link, Redirect, useHistory, useRouteMatch } from 'react-router-dom'
import { secureRequest } from '../../requestWrapper'
import { useAuth } from '../../context/auth'
import { useUser } from '../../context/user'
import Tlahtolli from './Tlahtolli'
import { Modal } from './Modal'
import { TextBox, Button } from "./ModalStyles"

function LessonModal(props){
    const { authToken, setAuthToken } = useAuth()
    const { userData } = useUser()
    const [ lessonData, setLessonData ] = useState()
    const textBoxRef = useRef()
    const [ editing, setEditing] = useState(false)
    const [isLoading, setIsLoading] = useState(false)
    const [isError, setIsError] = useState(false)
    const [reloadLessonData, setReloadLessonData] = useState(false)
    const history = useHistory()
    const match = useRouteMatch()
    const [confirmedDelete, setConfirmedDelete] = useState(false)
    
    useEffect(() => {
        let didCancel=false;
        setIsLoading(true)
        const bearer = "Bearer ".concat(authToken.token)
        const requestConfig = {
            method: 'get',
            url: "http://dev.localhost:5000/api/lessons/"+props.match.params.id,
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
    if (isLoading){
        return(
            <Modal title="loading">
                Loading...
            </Modal>
        )
    }

    function updateLesson(){
        const bearer = "Bearer ".concat(authToken.token)
        const requestConfig = {
            method: 'put',
            url: "http://dev.localhost:5000/api/lessons/"+match.params.id,
            data: {
                content: textBoxRef.current.value
            },
            headers: { Authorization: bearer }
        }
        const succ = res => {
            setLessonData(res.data)
	    setEditing(false)
        }
        const err = res => {
            let code = res.response!==undefined ? res.response.status : "no error code to see here, folks"
            setIsError(true)
        }
        const setter = setAuthToken
        secureRequest(requestConfig, succ, err, setter)

    }

    function deleteLesson(){
        setConfirmedDelete(confirmedDelete ? false : true)
        if (!confirmedDelete){return null}
        const bearer = " Bearer ".concat(authToken.token)
        const requestConfig = {
            method: 'delete',
            url: "http://dev.localhost:5000/api/lessons/"+match.params.id,
            headers: { Authorization: bearer }
        }
        const succ = res => {
            history.replace('/')
        }
        const err = res => {
        }
        const setter = setAuthToken
        secureRequest(requestConfig, succ, err, setter)
    }

    if (editing){
        const DeleteButton = () => <button id="delete-lesson-button" onClick={deleteLesson}>{confirmedDelete ? "Are you sure?" : "Delete"}</button>
	console.log(textBoxRef.current)
        return(
            <Modal id="lesson-modal" title={lessonData.title} editing={editing} headerButton={DeleteButton} >
                <TextBox id="edit-lesson-textarea" ref={textBoxRef} defaultValue={lessonData.content}/>
                <Button id="edit-lesson-save" onClick={updateLesson}>Save</Button>
                <Button id="edit-lesson-cancel" onClick={()=>{setEditing(false)}}>Cancel</Button>
            </Modal>
        )
    }

    const EditButton = () => <button id="edit-lesson-button" onClick={()=>{setEditing(true)}}>Edit</button>
    
    return(
        <Modal id="lesson-modal" title={lessonData.title} headerButton={userData.id===lessonData.author_id ? EditButton : false} >
            {lessonData.content.split(/([^\w'-])/).map((word,index) =>
            <Tlahtolli word={word} //TODO maybe expand these using object spread? Needs organization
                        definition={
				lessonData.user_tlahtolli.find(obj=>
				obj.word===word.toLowerCase())
				? lessonData.user_tlahtolli.find(obj=>
					obj.word===word.toLowerCase()).definition
				: undefined
			}
                        seen={lessonData.user_tlahtolli.map(entry=>entry.word).includes(word.toLowerCase()) ? true : false}
                        setReloadLessonData={setReloadLessonData}
                        key={index}
                        index={index} />
            )}
        </Modal>
    )
}

export default LessonModal
