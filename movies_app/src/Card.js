
import Card from 'react-bootstrap/Card';

function MovieCard({movie}) {
  return (
    <Card style={{ width: '18rem' }}>
      <Card.Img variant="top" style={{ width: '6rem', margin:'auto' }} src={movie.Poster_Link} />
      <Card.Body>
        <Card.Title>{movie.Series_Title}</Card.Title>
        <Card.Text>
          {movie.Overview}
        </Card.Text>
        <Card.Footer>
            <p> Rated: {movie.Certificate ? movie.Certificate : "N/A" } </p>
            <p>Genre: {movie.Genre} </p>
        </Card.Footer>
      </Card.Body>
    </Card>
  );
}

export default MovieCard;