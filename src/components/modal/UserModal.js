import React, { useState } from 'react'
import { secureRequest } from '../../requestWrapper'
import { useAuth } from '../../context/auth'
import { useUser } from '../../context/user'
import { ModalField, Modal } from './Modal'
import { Button, Success, Error } from './ModalStyles'

function UserModal(){
    const { authToken, setAuthToken } = useAuth()
    const { userData, setUserData } = useUser()
    const [usernameFieldValue, setUsernameFieldValue] = useState(userData.username)
    const [emailFieldValue, setEmailFieldValue] = useState(userData.email)
    const [confirmedDelete, setConfirmedDelete] = useState(false)
    const [changingPassword, setChangingPassword] = useState(false)
    const [oldPassword, setOldPassword] = useState("")
    const [firstNewPassword, setFirstNewPassword] = useState("")
    const [secondNewPassword, setSecondNewPassword] = useState("")
    const [isSuccess, setIsSuccess] = useState(false)
    const [isEmail, setIsEmail] = useState(false)
    const [isError, setIsError] = useState(false)
    const [errorMessage, setErrorMessage] = useState('')

    if (!userData){
        if (isError){
            return <Modal title="Ooops :l">x_x looks like we had a problem fetching your lesson :(</Modal>
        }
        return null
    }



    function updateUser(){
        const bearer = "Bearer ".concat(authToken.token)
        const requestConfig = {
            method: 'put',
            url: "http://dev.localhost:5000/api/users/"+userData.id,
            data: {
                username: usernameFieldValue,
                email: emailFieldValue
            },
            headers: { Authorization: bearer }
        }
        const succ = res => {
	    setIsError(false)
            setIsSuccess(true)
            setIsEmail(emailFieldValue!==userData.email)
            setUserData(res.data)
        }
        const err = res => {
	    setIsSuccess(false)
            let code = res.response!==undefined ? res.response.status : "no error code to see here, folks"
            setIsError(true)
	    setUsernameFieldValue(userData.username)
	    setEmailFieldValue(userData.email)
        }
        const setter = setAuthToken
        secureRequest(requestConfig, succ, err, setter)

    }
    function updatePassword(){
        const bearer = "Bearer ".concat(authToken.token)
        const requestConfig = {
            method: 'put',
            url: "http://dev.localhost:5000/api/users/"+userData.id,
            data: {
                old_password: oldPassword,
                password: firstNewPassword
            },
            headers: { Authorization: bearer }
        }
        const succ = res => {
	    setIsError(false)
            setIsSuccess(true)
        }
        const err = res => {
	    setIsSuccess(false)
            let code = res.response!==undefined ? res.response.status : "no error code to see here, folks"

            setIsError(true)
            setErrorMessage(res.response.data.message)
        }
        const setter = setAuthToken
        secureRequest(requestConfig, succ, err, setter)
    }

    function deleteUser(){
        setConfirmedDelete(confirmedDelete ? false : true)
        if (!confirmedDelete){return null}
        const bearer = "Bearer ".concat(authToken.token)
        const requestConfig = {
            method: 'delete',
            url: "http://dev.localhost:5000/api/users/"+userData.id,
            headers: { Authorization: bearer }
        }
        const succ = res => {setAuthToken(null);setUserData(null)}
        const err = res => {console.log(res)}
        const setter = setAuthToken
        secureRequest(requestConfig, succ, err, setter)
    }

    const DeleteButton = () => <button id="profile-delete-button" onClick={deleteUser}>{confirmedDelete ? "Are You Sure?" : "Delete Account"}</button>
    return(
        <Modal title={userData.username} user={true} headerButton={DeleteButton}>
            { isSuccess &&<Success className="success">Profile Updated! { isEmail && "Check your email" }</Success> }
            {/* { isEmail &&<Success>Check your email</Success> } */}
            { isError &&<Error className="error">There was a problem updating your profile: {errorMessage}</Error> }
            <ModalField id="profile-username" label="username" fieldValue={usernameFieldValue} setFieldValue={setUsernameFieldValue} />
            <ModalField id="profile-email" label="email" fieldValue={emailFieldValue} setFieldValue={setEmailFieldValue} />
            { changingPassword ? <>
            <ModalField type="password" label="old password" fieldValue={oldPassword} setFieldValue={setOldPassword} />
            <ModalField type="password" label="new password" fieldValue={firstNewPassword} setFieldValue={setFirstNewPassword} />
            <ModalField type="password" label="new password again" fieldValue={secondNewPassword} setFieldValue={setSecondNewPassword} />
            <Button id='password-save' onClick={()=>{updatePassword(); setChangingPassword(!changingPassword)}}>Save New Password</Button>
            </>
            : ""
            }
            <Button id='change-password-toggle' onClick={()=>{setChangingPassword(!changingPassword)}}>{changingPassword ? "Cancel" : "Change Password"}</Button>
            <br/>
            <Button id='profile-save' onClick={updateUser}>Save</Button>
        </Modal>
    )
}

export default UserModal
