import React from "react";
import "../resources/index.css";

import Dialog from "@mui/material/Dialog";

import { CircularProgress, DialogContent, DialogTitle } from "@mui/material";
import Printer from "./Printer";

const Loading = (props) => {
  return (
    <Dialog open={true}>
      <DialogTitle>Building</DialogTitle>
      <DialogContent className="Loading-content">
        <CircularProgress />
        <Printer
          messages={props.messages}
          img={props.img}
          title={props.title}
        />
      </DialogContent>
    </Dialog>
  );
};

export default Loading;
