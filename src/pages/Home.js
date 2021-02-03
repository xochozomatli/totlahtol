import React from 'react'
import { Route, Switch } from 'react-router-dom'
import Header from './Header'
import LessonForm from './LessonForm'
import LessonFeed from './LessonFeed'
import LessonModal from './LessonModal'

function Home(props) {
    console.log(props.match)
    return (
        <div>
        <Header />
        <LessonForm />
        <LessonFeed match={props.match} />
        <Switch>
            { console.log('HELLO THERE!!!')}
            <Route path='/lessons/:id/edit' render={ ()=><LessonModal editing={true} {...props} />} />
            <Route path='/lessons/:id' component={LessonModal} />
        </Switch>
        
        </div>
    )
}

export default Home