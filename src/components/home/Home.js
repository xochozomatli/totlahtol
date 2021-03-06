import React, {useState } from 'react'
import { Route, Switch } from 'react-router-dom'
import Header from './Header'
import LessonForm from './LessonForm'
import LessonFeed from './LessonFeed'
import LessonModal from '../modal/LessonModal'
import UserModal from '../modal/UserModal'

function Home(props) {
    const [ userModal, setUserModal ] = useState(false)
    return (
        <div>
        <Header setUserModal={setUserModal}/>
        <LessonForm />
        <LessonFeed match={props.match} />
        <Route path='/lessons/:id' component={LessonModal} />
        <Route path='/users/:username' component={UserModal} />
        </div>
    )
}

export default Home