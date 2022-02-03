import React from "react";
import { Container } from "react-bootstrap";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory from "react-bootstrap-table2-paginator";

const UrlContainer = (props) => {
  const columns = [
    { dataField: "long_url", text: "Long url" },
    {
      dataField: "short_url",
      text: "Short url",
      formatter: (cell, row, rowIndex, extraData) => <a href={row.short_url}>{row.short_url}</a>,
    },
  ];
  return (
    <Container>
      <BootstrapTable keyField="short_url" data={props.urls} columns={columns} pagination={paginationFactory()} />
    </Container>
  );
};

export default UrlContainer;
