// Importing modules
import React, { useState, useEffect } from "react";
import running from "../resources/diagram.gif";
import "../resources/index.css";
import { Stack } from "@mui/material";

import { Container } from "@mui/system";

import Printer from "../component/Printer";

const __running_message__ = "running";

function ModuleRuning(props) {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    props.socket.emit(__running_message__, "I'm Connected");
    props.socket.on(__running_message__, (msg) => {
      setMessages((old) => [...old, msg]);
    });
  }, [props]);

  return (
    <div className="Home">
      <img
        src={running}
        className="Home-rocket"
        alt="Truck the Runing Module"
      />
      <h1>Truck the Runing Module</h1>
      <Container>
        <Stack spacing={10}>
          <Printer messages={messages} />
        </Stack>
      </Container>
    </div>
  );
}

export default ModuleRuning;
