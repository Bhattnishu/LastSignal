import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import ReportLost from "./pages/ReportLost";
import Login from "./pages/Login";
import Register from "./pages/Register";
import LostResults from "./pages/LostResults";
import ReportFound from "./pages/ReportFound";
import MyActivity from "./pages/MyActivity";
import Profile from "./pages/Profile";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/report/lost" element={<ReportLost />} />
      <Route path="/report/lost/:id/results" element={<LostResults />} />
      <Route path="/report/found" element={<ReportFound />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/my-activity" element={<MyActivity />} />
      <Route path="/profile" element={<Profile />} />
    </Routes>
  );
}

export default App;