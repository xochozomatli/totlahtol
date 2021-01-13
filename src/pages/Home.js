import React from 'react'
import { Route } from 'react-router-dom'
import Header from './Header'
import LessonForm from './LessonForm'
import LessonFeed from './LessonFeed'
import LessonModal from './LessonModal'

function Home(props) {
    return (
        <div>
        <Header />
        <LessonForm />
        <LessonFeed match={props.match}/>
        <Route path='/lessons/:id' component={LessonModal}/>
        </div>
    )
}

export default Home