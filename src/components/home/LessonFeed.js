import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Button, Card, LessonCard, Error } from "./HomeStyles"

function LessonFeed(props){
    const { lessonsOnPage, setLessonsOnPage, isError, getLessonsPage } = props
    return(
    <>
        <div id="lessons">{ lessonsOnPage.map( lesson =>
            <LessonCard key={lesson.id} id={'lesson'+lesson.id}>
                <Link to={`${props.match.url}lessons/${lesson.id}`}>{lesson.title} by {lesson.author_name}</Link>
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
