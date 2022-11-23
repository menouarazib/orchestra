// Importing modules
import React, { useState, useEffect } from "react";
import rocket from "../resources/rocket.gif";
import Button from "@mui/material/Button";
import "../resources/index.css";
import { InputAdornment, Stack, TextField } from "@mui/material";
import GitHubIcon from "@mui/icons-material/GitHub";
import ImportExportIcon from "@mui/icons-material/ImportExport";
import { Container } from "@mui/system";
import Loading from "../component/Loading";
import Alert from "../component/Alert";
import { isGitRepo } from "../utils/Utils";
import {
  __json_data_key__,
  __json_info__,
  __json_type_key__,
  __docker_message__,
} from "../component/Constants";

const __import_build__ = "build";
const __import_build_url__ = "url";

function Home(props) {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [showAlert, setShowAlert] = useState(false);
  const [error, setError] = useState("");
  const [messages, setMessages] = useState([]);
  const [success, setSuccess] = useState(false);

  const handleChange = (event) => {
    setUrl(event.target.value);
  };

  const handleError = (error) => {
    console.log(error);
  };

  const handleResponse = (response) => {
    setLoading(false);
    if (response[__json_type_key__] !== __json_info__) {
      setSuccess(false);
    } else {
      setSuccess(true);
    }
    setError(response[__json_data_key__]);
    setShowAlert(true);
    setMessages([]);
  };

  const handleImport = () => {
    if (!isGitRepo(url)) {
      setError("This url " + url + " it is not a Git Repo !");
      setShowAlert(true);
    } else {
      props.socket.emit(__docker_message__, "Start Building");
      setLoading(true);
      fetch(
        "http://localhost:5000/" +
          __import_build__ +
          "?" +
          __import_build_url__ +
          "=" +
          url,
        {
          method: "GET",
        }
      )
        .then((response) => response.json())
        .then((data) => {
          handleResponse(data);
        })
        .catch((error) => handleError(error));
    }
  };

  useEffect(() => {
    props.socket.on(__docker_message__, (msg) => {
      setMessages((old) => [...old, msg]);
    });
  }, [props.socket]);

  return (
    <div className="Home">
      <img src={rocket} className="Home-rocket" alt="import your project" />
      <h1>Import your Project</h1>
      <Container>
        <Stack spacing={10}>
          <TextField
            required
            id="standard-basic"
            label="Git Repository Url"
            variant="standard"
            helperText="Please enter the url of the Git Repository of your Machine Learning Module"
            value={url}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <GitHubIcon />
                </InputAdornment>
              ),
            }}
            onChange={handleChange}
          />
          <Button
            variant="text"
            fullWidth={false}
            size="large"
            endIcon={<ImportExportIcon />}
            onClick={handleImport}
          >
            Import
          </Button>
        </Stack>
        {loading ? (
          <Loading
            messages={messages}
            img={require("../resources/docker.png")}
            title={"Docker: bulding image"}
          />
        ) : null}
        {showAlert ? (
          <Alert
            text={error}
            open={showAlert}
            success={success}
            close={() => setShowAlert(false)}
          />
        ) : null}
      </Container>
    </div>
  );
}

export default Home;
