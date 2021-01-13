import React, { useState } from 'react'
import { secureRequest } from '../requestWrapper'
import { useAuth } from '../context/auth'
import { useUser } from '../context/user'
import { TlahtolliBody, TlahtolliWord, TlahtolliHint } from "../style/ModalComponents"

function Tlahtolli(props) {
    const { userData } = useUser()
    const { authToken, setAuthToken } = useAuth()
    const [hintText, setHintText] = useState(props.definition || "")

    function submitNewDefinition(){
        const bearer = "Bearer ".concat(authToken.token)
        const requestConfig = {
            method: props.definition ? 'put' : 'post',
            url: "http://localhost:5000/api/tlahtolli"+(props.definition ? '/'+props.word : ''),
            data: {
                word: props.word,
                user_id: userData.id,
                definition: hintText,
                state: "tlahtolli"
            },
            headers: { Authorization: bearer }
        }
        const succ = res => { props.setReloadLessonData(true) }
        const err = res => {console.log(res)}
        const setter = setAuthToken
        secureRequest(requestConfig, succ, err, setter)
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

export default Tlahtolli