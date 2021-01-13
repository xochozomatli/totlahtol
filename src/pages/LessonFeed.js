import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import { Button, Card, LessonCard } from "../style/FeedComponents"
import { Error } from "../style/AuthForms"

function LessonFeed(props){
    console.log(props.match)
    const [isError, setIsError] = useState(false)
    const [lessonsOnPage, setLessonsOnPage] = useState([])
    const perPage = 2
    const [lessonsLinks, setLessonsLinks] = useState(
        {
            "next": "/api/lessons?page=1&per_page="+perPage,
            "prev": null,
            "self": null
        })

    function getLessonsPage(){//TODO call this from within useEffect()
        axios.get('http://localhost:5000'+lessonsLinks.next
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

    return(
    <>
        <div id="lessons">{ lessonsOnPage.map( lesson =>
            <LessonCard key={lesson.id} id={'lesson'+lesson.id}>
                <Link to={`${props.match.url}lessons/${lesson.id}`}>{lesson.title} by {lesson.author}</Link>
            </LessonCard>) }
        </div>
        <Card>
        {/* TODO remove this button and call getLessonsPage from useEffect() */}
            <Button onClick={getLessonsPage}>Load Lessons</Button>
            { isError &&<Error>Sorry! We weren't able to load your lessons UnU</Error> }
        </Card>
    </>
    )
}

export default LessonFeed