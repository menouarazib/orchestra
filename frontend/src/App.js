import { BrowserRouter, Routes, Route } from "react-router-dom";
import { io } from "socket.io-client";
import Home from "./screen/Home";
import ModuleRunning from "./screen/ModuleRunning";
import MonitorModules from "./screen/MonitorModules";

export default function App() {
  const endPoint = "http://localhost:5000";
  const socket = io.connect(`${endPoint}`);
  return (
    <BrowserRouter>
      <Routes>
        <Route index element={<Home socket={socket} />} />
        <Route
          path="/module-running"
          element={<ModuleRunning socket={socket} />}
        />
        <Route
          path="/monitoring-modules"
          element={<MonitorModules socket={socket} />}
        />
      </Routes>
    </BrowserRouter>
  );
}
