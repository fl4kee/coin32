import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import axios from "axios";
import qs from "qs";

const CustomForm = (props) => {
  const [enteredLongUrl, setEnteredLongUrl] = useState("");
  const [enteredSubpart, setEnteredSubpart] = useState("");
  const handleSubmit = (e) => {
    e.preventDefault();
    let long_url = e.target.elements[0].value;
    let subpart = e.target.elements[1].value;

    // запрос на преобразование и запись ссылки в базу данных
    const setUrls = async () => {
      try {
        const data = await axios.post(
          "http://127.0.0.1:8000/api/urls/",
          qs.stringify({
            long: long_url,
            subpart: subpart,
          }),
          { withCredentials: true }
        );
        // обновление стейта
        if (data.data.err) {
          alert(data.data.err);
          throw data.data.err;
        }
        props.onSubmitForm();
      } catch (e) {
        console.log(e);
      }
    };

    setUrls();
    setEnteredSubpart("");
    setEnteredLongUrl("");
  };

  const longUrlChangeHandler = (e) => {
    setEnteredLongUrl(e.target.value);
  };
  const subpartChangeHandler = (e) => {
    setEnteredSubpart(e.target.value);
  };

  return (
    <Form className="mb-5" onSubmit={handleSubmit}>
      <Form.Group className="mb-3" controlId="formBasicEmail">
        <Form.Label>Enter your url here</Form.Label>
        <Form.Control
          type="text"
          value={enteredLongUrl}
          placeholder="Enter url"
          name="long"
          required
          onChange={longUrlChangeHandler}
        />
      </Form.Group>
      <Form.Group className="mb-3" controlId="formBasicEmail">
        <Form.Label>Enter desired subpart</Form.Label>
        <Form.Control
          type="text"
          value={enteredSubpart}
          placeholder="Enter subpart"
          name="subpart"
          onChange={subpartChangeHandler}
        />
      </Form.Group>
      <Button className="button1" variant="primary" type="submit">
        Submit
      </Button>
    </Form>
  );
};

export default CustomForm;
