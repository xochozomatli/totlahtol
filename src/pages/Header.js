import React from 'react'
import { secureRequest } from '../requestWrapper'
import { useAuth} from '../context/auth'
import { useUser } from '../context/user'
import { HeaderBar, HeaderContentStart, HeaderContentEnd, HeaderTitle, HeaderButton } from "../style/FeedComponents"

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
        const succ = res => {setAuthToken(null);setUserData(null);console.log(authToken)}
        const err = res => {console.log(res)}
        const setter = setAuthToken
        secureRequest(requestConfig, succ, err, setter)
    }

    function deleteUser(){
        const bearer = "Bearer ".concat(authToken.token)
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

export default Header