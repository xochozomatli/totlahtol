import React, { useState } from 'react'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import Header from './Header'
import LessonForm from './LessonForm'
import LessonFeed from './LessonFeed'
import LessonModal from './LessonModal'

function Home(props) {
    const [isError, setIsError] = useState(false);

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