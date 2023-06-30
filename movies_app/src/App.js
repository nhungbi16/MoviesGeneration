import React from 'react';
import { useState } from 'react';
import './App.css';

import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import MovieCard from './Card';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

function App() {
  const [link, setLink] = useState('')
  const [movies, setMovies] = useState([])
  const [genres, setGenres] = useState([])

  function changeLink(event){
    setLink(event.target.value)
  }
 
  async function getMovies(event) {
    event.preventDefault();
    const imageUrl = event.target.link.value
    const requestOptions = {
      method: 'POST',
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({inputURL: imageUrl}),
    };

    try {
      const response = await fetch('/get_movies_recommendations', requestOptions)
      const data = await response.json();
      setGenres(data.genres)
      setMovies(data.movies)
    } catch (e) {
      console.log(e) }
    }


  return (
    <div className="App">
      <Container>
        <br/>
        <img src={link} alt="Link Not Valid" width="400"/>
        <br/>
      <Row>
        <Form onSubmit={getMovies}>
          <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label>ImageUrls: </Form.Label>
            <Form.Control onChange={changeLink} type="text" name = "link" placeholder="Enter link" />
            <Form.Text className="text-muted">
              PNG or JPEG
            </Form.Text>
          </Form.Group>
          <Button variant="primary" type="submit">
            Submit
          </Button>
        </Form>
      </Row>
      <br/>
      <Row> {genres && <h3> {genres.join(", ")} </h3>}  </Row>
      <Row>
      {movies && movies.map((movie,i)=> {
        return <Col><MovieCard key = {"card"+i} movie = {movie}/></Col>
      })}
      </Row>

    </Container>
      
    </div>
  );
}

export default App;
