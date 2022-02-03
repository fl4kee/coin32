import { Container } from "react-bootstrap";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import React from "react";
import HomeScreen from "./screens/HomeScreen";

const App = () => {
  return (
    <Router>
      <main className="py-3">
        <Container>
          <Routes>
            <Route path="/" element={<HomeScreen />} exact />
          </Routes>
        </Container>
      </main>
    </Router>
  );
};

export default App;
