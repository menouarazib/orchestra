import React from "react";
import "../resources/index.css";

import Card from "@mui/material/Card";

import CardContent from "@mui/material/CardContent";

import Typography from "@mui/material/Typography";
import {
  __font_size__,
  __json_data_key__,
  __json_info__,
  __json_type_key__,
  __json_error__,
  __json_warning__,
} from "./Constants";

const paragraph = (item, index) => {
  let color_ = null;
  const data = item[__json_data_key__];
  const key = index + "";
  switch (item[__json_type_key__]) {
    case __json_info__:
      color_ = "black";
      break;
    case __json_warning__:
      color_ = "orange";
      break;
    case __json_error__:
      color_ = "red";
      break;

    default:
      color_ = "blue";
      break;
  }

  return (
    <p key={key} style={{ color: color_, fontSize: __font_size__ }}>
      {data}
    </p>
  );
};

const Printer = (props) => {
  return (
    <Card sx={{ maxWidth: "100%" }} className="Loading-content">
      <img src={props.img} alt={props.title} />
      <Typography gutterBottom variant="h5" component="div">
        {props.title}
      </Typography>
      <CardContent sx={{ overflowY: "scroll", maxHeight: 400 }}>
        {props.messages.map((item, index) => paragraph(item, index))}
      </CardContent>
    </Card>
  );
};

export default Printer;
