import React from "react";
import "../resources/index.css";
import Warning from "../resources/warning.gif";
import Success from "../resources/database.gif";
import Dialog from "@mui/material/Dialog";

import {
  Button,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from "@mui/material";

const Alert = (props) => {
  return (
    <Dialog open={props.open}>
      <DialogTitle>{props.success ? "Success" : "Error"}</DialogTitle>
      <DialogContent className="Loading-content">
        <img
          src={props.success ? Success : Warning}
          alt="Warning"
          className="Loading-warning"
        />
        <DialogContentText>{props.text}</DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={props.close} autoFocus>
          Ok
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default Alert;
