import React from 'react'
import { useHistory } from 'react-router-dom'
import { Background, Body, Content, Exit, Field, Header, Title } from './ModalStyles'
function ModalField(props){
    return(
        <Field id={props.id}>
            <span>{props.label}</span>
            <input value={props.fieldValue} onChange={e=>{props.setFieldValue(e.target.value)}}></input>
        </Field>
    )
}

function Modal(props){
    const history = useHistory()
    const closeModal = e => {
        e.stopPropagation()
        history.push('/')
    }

    return(<Background>
                <Body>
                    <Exit id="modal-exit" onClick={closeModal}>
                        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" style={{height:'1.5rem',width:'1.5rem'}}>
                            <line x1="1" y1="22" x2="22" y2="1" stroke="black" strokeWidth="2"/>
                            <line x1="1" y1="1" x2="22" y2="22" stroke="black" strokeWidth="2"/>
                        </svg>
                    </Exit>
                    <Header>
                        <Title id="modal-title">{props.title}</Title>
                        { props.headerButton && props.headerButton() }
                    </Header>
                    <Content id="modal-content" user={props.user}>{props.children}</Content>
                </Body>
            </Background>
    )
}

export { ModalField, Modal }
