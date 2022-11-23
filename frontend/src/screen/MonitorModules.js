import React, { useState, useEffect } from "react";
import Box from "@mui/material/Box";
import List from "@mui/material/List";
import ModuleView from "../component/ModuleView";
import { CircularProgress, ListSubheader, Stack } from "@mui/material";

const url_fetch = "http://localhost:5000/modules";

const MonitorModules = (props) => {
  const [modules, setModules] = useState([]);
  const [loading, setLoading] = useState(true);

  const handleError = (error) => {
    console.log(JSON.stringify(error));
  };

  const handleResponse = (data) => {
    setModules(data);
    setLoading(false);
  };

  useEffect(() => {
    fetch(url_fetch, {
      method: "GET",
    })
      .then((response) => response.json())
      .then((data) => {
        handleResponse(data);
      })
      .catch((error) => handleError(error));
  }, []);

  return (
    <Box
      sx={{
        width: "100%",
        bgcolor: "background.paper",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <nav aria-label="all modules">
        <List
          subheader={
            <ListSubheader component="div" id="nested-list-subheader">
              Orchestra Modules
            </ListSubheader>
          }
        >
          {loading ? (
            <Stack alignItems="center">
              <CircularProgress />
            </Stack>
          ) : null}
          {modules.map((item, index) => (
            <ModuleView item={item} key={item.name} socket={props.socket} />
          ))}
        </List>
      </nav>
    </Box>
  );
};

export default MonitorModules;
