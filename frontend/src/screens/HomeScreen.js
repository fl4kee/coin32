import React, { useState, useEffect } from "react";
import CustomForm from "../components/CustomForm";
import UrlContainer from "../components/UrlContainer";
import axios from "axios";

const HomeScreen = () => {
  const [urls, setUrls] = useState([]);
  //  получение списка всех ссылок
  const getUrlsData = async () => {
    try {
      const urls_list = await axios.get("http://127.0.0.1:8000/api/urls/", { withCredentials: true });
      setUrls(urls_list.data);
      console.log(urls_list.data);
    } catch (e) {
      console.log(e);
    }
  };
  // получение ссылок при первой загрузке
  useEffect(() => {
    getUrlsData();
  }, []);

  return (
    <div>
      <h1>Shorten your url</h1>
      <CustomForm onSubmitForm={getUrlsData} />
      <UrlContainer urls={urls} />
    </div>
  );
};

export default HomeScreen;
