import React, { useState } from 'react'
import { useHistory } from 'react-router-dom'
import { secureRequest } from '../../requestWrapper'
import { useAuth} from '../../context/auth'
import { useUser } from '../../context/user'
import { Bar, ContentStart, ContentEnd, Title, MenuToggle, AccountPopover, PopoverItem, PopoverLink } from "./HomeStyles"

function Header(){
    const { authToken, setAuthToken } = useAuth()
    const { userData, setUserData } = useUser()
    const [ showMenu, setShowMenu ] = useState()
    const history = useHistory()

    function deauthUser(){
        const bearer = "Bearer ".concat(authToken.token)
        const requestConfig = {
            method: 'put',
            url: "http://localhost:5000/api/users/"+userData.id,
            data: { action: 'deauth' },
            headers: { Authorization: bearer }
        }
        const succ = res => {setAuthToken(null);setUserData(null);console.log(authToken)}
        const err = res => {}
        const setter = setAuthToken
        secureRequest(requestConfig, succ, err, setter)
    }

   return(
        <>
        <Bar>
            <ContentStart>
                <Title>Totlahtol</Title>
            </ContentStart>
            <ContentEnd onClick={()=>{console.log('Toggle Clicked!!!');setShowMenu(!showMenu)}} id="content-end">
                <MenuToggle id="menu-toggle">{userData.username.charAt(0).toUpperCase()+userData.username.slice(1)}</MenuToggle>
                
            </ContentEnd>
            { showMenu ?
                <AccountPopover id="menu">
                    <PopoverItem className="menu-item" onClick={()=>{history.push('/users/'+userData.username)}}>
                        <PopoverLink>Profile</PopoverLink>
                    </PopoverItem>
                    <PopoverItem className="menu-item" onClick={deauthUser}>
                        <PopoverLink>Log Out</PopoverLink>
                    </PopoverItem>
                </AccountPopover>
                : ""
            }
        </Bar>
        </>
    )
}

export default Header
