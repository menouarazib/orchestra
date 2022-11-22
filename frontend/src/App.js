import * as React from "react";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import "react-tabs/style/react-tabs.css";
import { io } from "socket.io-client";
import Home from "./screen/Home";
import ModuleRunning from "./screen/ModuleRunning";
import MonitorModules from "./screen/MonitorModules";

export default function App() {
  const endPoint = "http://localhost:5000";
  const socket = io.connect(`${endPoint}`);

  return (
    <Tabs>
      <TabList>
        <Tab>Home</Tab>
        <Tab>Monitor Modules</Tab>
        <Tab>Module Running</Tab>
      </TabList>

      <TabPanel>
        <Home socket={socket} />
      </TabPanel>

      <TabPanel>
        <MonitorModules socket={socket} />
      </TabPanel>

      <TabPanel>
        <ModuleRunning socket={socket} />
      </TabPanel>
    </Tabs>
  );
}
