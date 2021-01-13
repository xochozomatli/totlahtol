import React from 'react'
import { Route, Redirect } from 'react-router-dom'
import { useUser } from './context/user'

function PrivateRoute({ component: Component, ...rest }) {
    const { userData } = useUser()

    return (
        <Route
            {...rest}
            render={props =>
                userData ? (
                    <Component {...props} />
                ):(
                    <Redirect
                        to={{ pathname: "/login", state: {referer: props.location } }}
                    />
                )
            }
        />
    )
}

export default PrivateRoute