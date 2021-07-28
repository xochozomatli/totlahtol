import axios from 'axios'
import React, {useState, useEffect } from 'react'
import { Route, Switch } from 'react-router-dom'
import Header from './Header'
import LessonForm from './LessonForm'
import LessonFeed from './LessonFeed'
import LessonModal from '../modal/LessonModal'
import UserModal from '../modal/UserModal'

function Home(props) {
    const [ userModal, setUserModal ] = useState(false)
    const [lessonsOnPage, setLessonsOnPage] = useState([])

    const [isError, setIsError] = useState(false)
    const perPage = 5 //--default on backend is 5, but explicit is better than implicit--
    const [lessonsLinks, setLessonsLinks] = useState(
        {
            "next": "/api/lessons?page=1&per_page="+perPage,
            "prev": null,
            "self": null
        })

    function getLessonsPage(){
        axios.get('http://dev.localhost:5000'+lessonsLinks.next
        ).then(result => {
            if (result.status===200){
                return result.data
            } else {
                setIsError(true)
                Promise.reject()
            }
        }).then( data => {
            setLessonsLinks(data._links)
            let newLessons = data.items
            setLessonsOnPage([...lessonsOnPage, ...newLessons])
        }).catch( e => {
            setIsError(true)
            
        })
    }
    
    useEffect(()=>{
        getLessonsPage()
    }, [lessonsOnPage])

    return (
        <div>
        <Header setUserModal={setUserModal}/>
        <LessonForm lessonsOnPage={lessonsOnPage} setLessonsOnPage={setLessonsOnPage}/>
        <LessonFeed match={props.match} lessonsOnPage={lessonsOnPage} setLessonsOnPage={setLessonsOnPage} isError={isError} getLessonsPage={getLessonsPage}/>
        <Route path='/lessons/:id' component={LessonModal} />
        <Route path='/users/:username' component={UserModal} />
        </div>
    )
}

export default Home
