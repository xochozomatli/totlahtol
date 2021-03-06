import React, { useState } from 'react'
import { secureRequest } from '../../requestWrapper'
import { useAuth } from '../../context/auth'
import { useUser } from '../../context/user'
import { Body, Word, Punct, Hint } from "./TlahtolliStyles"

function Tlahtolli(props) {
    const { userData } = useUser()
    const { authToken, setAuthToken } = useAuth()
    const [hintText, setHintText] = useState(props.definition || "")
    const [active, setActive] = useState(false)

    function submitNewDefinition(){
        const bearer = "Bearer ".concat(authToken.token)
        const requestConfig = {
            method: props.definition ? 'put' : 'post',
            url: "http://localhost:5000/api/tlahtolli"+(props.definition ? '/'+props.word.toLowerCase() : ''),
            data: {
                word: props.word.toLowerCase(),
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
    if (props.word.match(/[^\w]+/)){
        return <Body><Punct>{props.word}</Punct></Body>
    }

    return(
        <Body onMouseEnter={() => {setActive(true)}}
                    onMouseLeave={() => {setActive(false)}}
                    showHint={active}
                    seen={props.seen}>
            <Word>{props.word}</Word>
            <Hint onSubmit={e=>{e.preventDefault(); submitNewDefinition(hintText)}}>
              <input value={hintText} onChange={e=>setHintText(e.target.value)}/>
            </Hint>
        </Body>
    )
}

export default Tlahtolli