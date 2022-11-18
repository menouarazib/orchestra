import React, { useEffect, useState } from "react";
import List from "@mui/material/List";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Collapse from "@mui/material/Collapse";
import ViewModuleIcon from "@mui/icons-material/ViewModule";
import ExpandLess from "@mui/icons-material/ExpandLess";
import ExpandMore from "@mui/icons-material/ExpandMore";
import InfoIcon from "@mui/icons-material/Info";
import BuildCircleIcon from "@mui/icons-material/BuildCircle";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import Link from "@mui/material/Link";
import { __docker_message__, __json_data_key__ } from "./Constants";
import Loading from "./Loading";

const ModuleView = ({ item, socket }) => {
  const [open, setOpen] = useState(true);
  const [show, setShow] = useState(false);
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);

  const url_fetch = "http://localhost:5000/rebuild/" + item.id;

  const handleClick = () => {
    setOpen(!open);
  };

  const handleRebuild = () => {
    setShow(true);
  };

  const handleRebuildOk = () => {
    socket.emit(__docker_message__, "I'm Connected");
    setLoading(true);
    setShow(false);
    fetch(url_fetch)
      .then((response) => response.json())
      .then((data) => {
        setMessages([]);
        setLoading(false);

        alert(data[__json_data_key__]);
      })
      .catch((error) => console.log(error));
  };

  useEffect(() => {
    socket.on(__docker_message__, (msg) => {
      setMessages((old) => [...old, msg]);
    });
  }, [socket]);

  const close = () => {
    setShow(false);
  };

  const showDetails = () => {
    alert(JSON.stringify(item));
  };

  return (
    <div>
      <ListItemButton onClick={handleClick}>
        <ListItemIcon>
          <ViewModuleIcon />
        </ListItemIcon>
        <ListItemText primary={item.name + " - " + item.version} />
        {open ? <ExpandLess /> : <ExpandMore />}
      </ListItemButton>
      <Collapse in={open} timeout="auto" unmountOnExit>
        <List component="div" disablePadding>
          <ListItemButton sx={{ pl: 4 }} onClick={showDetails}>
            <ListItemIcon>
              <InfoIcon />
            </ListItemIcon>
            <ListItemText primary="Details" />
          </ListItemButton>
          <ListItemButton sx={{ pl: 4 }} onClick={handleRebuild}>
            <ListItemIcon>
              <BuildCircleIcon />
            </ListItemIcon>
            <ListItemText primary="Re-Builds from Git Repo" />
          </ListItemButton>
        </List>
      </Collapse>

      <Dialog
        open={show}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          {"Rebuild the current module from its Git Repository"}
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            If you confirm the rebuild, the previous module will be removed and
            replaced by the new version. The new version will be build from
            <Link href={item.git_url} underline="hover">
              {" "}
              its Git Repo
            </Link>
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={close}>Cancel</Button>
          <Button onClick={handleRebuildOk} autoFocus>
            Rebuild
          </Button>
        </DialogActions>
      </Dialog>
      {loading ? (
        <Loading
          messages={messages}
          img={require("../resources/docker.png")}
          title={"Rebuilding"}
        />
      ) : null}
    </div>
  );
};
export default ModuleView;
